"""Knowledge Base: fraud-pattern similarity search (pgvector) + analyst pattern labeling.

Yashi's logic layer. Reuses scam_sentinel's multilingual sentence-transformer
(same 384-dim embedding space as scam_script_corpus) rather than loading a second
copy of the model into memory.
"""

from __future__ import annotations

import asyncio
import json
from decimal import Decimal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.scam_sentinel import _load_embedder


def _to_jsonable(value):
    """Round-trip UUID/datetime/Decimal through JSON so they're plain str/float.

    Decimal must become a JSON number, not a string -- json.dumps(default=str) on its
    own stringifies Decimal, which silently breaks downstream numeric use (e.g. a
    Jinja "{:,.2f}".format(...) on a value that's now a str, or a risk_score/weight
    field that renders as "85" instead of 85 in an API response).
    """
    def _default(v):
        if isinstance(v, Decimal):
            return float(v)
        return str(v)

    return json.loads(json.dumps(value, default=_default))


async def _embed(text_content: str) -> str:
    """Embed text and return it as a pgvector text literal, e.g. "[0.01,-0.02,...]".

    asyncpg has no native codec for the `vector` type — binding a Python list against
    a `(:param)::vector` cast raises "expected str, got list". pgvector's own text
    format (a bracketed, comma-separated literal) is what the `::vector` cast expects.
    """
    def _encode():
        embedder = _load_embedder()
        values = embedder.encode([text_content], normalize_embeddings=True)[0].tolist()
        return "[" + ",".join(repr(v) for v in values) + "]"

    # Embedding is CPU-bound; offload so it doesn't block the event loop.
    return await asyncio.to_thread(_encode)


async def find_similar_patterns(db: AsyncSession, description: str, top_k: int = 5) -> list[dict]:
    """Find verified fraud patterns most similar to a free-text description."""
    embedding = await _embed(description)

    rows = (
        await db.execute(
            text(
                """
                SELECT id, title, description, scam_type, key_indicators,
                       1 - (embedding <=> (:embedding)::vector) AS similarity
                FROM knowledge_base.patterns
                WHERE verified = true AND embedding IS NOT NULL
                ORDER BY embedding <=> (:embedding)::vector
                LIMIT :top_k
                """
            ),
            {"embedding": embedding, "top_k": top_k},
        )
    ).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


async def add_pattern(
    db: AsyncSession,
    title: str,
    description: str,
    scam_type: str,
    labeled_by: UUID,
    language: str = "en",
    key_indicators: list[str] | None = None,
) -> dict:
    """Analyst labels a new fraud pattern: embed the description and store it.

    New patterns start unverified (verified=false) — a second analyst/reviewer
    step (out of scope here) promotes them before find_similar_patterns surfaces them.
    """
    embedding = await _embed(description)

    row = (
        await db.execute(
            text(
                """
                INSERT INTO knowledge_base.patterns
                    (title, description, scam_type, language, key_indicators, embedding, labeled_by)
                VALUES
                    (:title, :description, :scam_type, :language, :key_indicators,
                     (:embedding)::vector, :labeled_by)
                RETURNING id, title, description, scam_type, language, key_indicators,
                          verified, labeled_by, created_at
                """
            ),
            {
                "title": title,
                "description": description,
                "scam_type": scam_type,
                "language": language,
                "key_indicators": key_indicators or [],
                "embedding": embedding,
                "labeled_by": labeled_by,
            },
        )
    ).mappings().first()
    await db.commit()
    return _to_jsonable(dict(row))


async def verify_pattern(db: AsyncSession, pattern_id: UUID) -> dict | None:
    """Promote an analyst-labeled pattern to verified, making it eligible for similarity search."""
    row = (
        await db.execute(
            text(
                """
                UPDATE knowledge_base.patterns
                SET verified = true, updated_at = NOW()
                WHERE id = :pattern_id
                RETURNING id, title, scam_type, verified
                """
            ),
            {"pattern_id": pattern_id},
        )
    ).mappings().first()
    await db.commit()
    return _to_jsonable(dict(row)) if row else None
