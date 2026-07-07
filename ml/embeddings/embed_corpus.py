"""
Embeds the scam script corpus and builds the FAISS index for the Adaptive
Knowledge Base (Sumanth task sheet, section 5).

Input:  scam_sentinel.scam_script_corpus rows from PostgreSQL
         (docker compose up postgres; seeded by backend/seed_data/01_seed.sql).
         If PostgreSQL is unreachable, falls back to parsing the corpus
         directly out of backend/seed_data/01_seed.sql.
Output: ml/embeddings/scam_corpus.faiss        FAISS IndexFlatIP (cosine, 384-dim)
        ml/embeddings/scam_corpus_meta.json    row metadata, position-aligned with the index
         (both copied to backend/app/ml/models/)
        scam_script_corpus.embedding           pgvector column updated in place, so the
         backend can also do similarity search in SQL (`embedding <=> $1`)

Model: paraphrase-multilingual-MiniLM-L12-v2 — multilingual (Hindi + English),
384-dim, normalized embeddings so inner product == cosine similarity.

Usage at inference time (backend): embed the new transcript/pattern with the
same model, index.search(embedding, k=5), then look up matches in the metadata
by position to suggest similar known scripts to the analyst.

Run:
    docker compose up -d postgres
    cd ml/embeddings
    python embed_corpus.py
    # or against a non-default DB:
    DATABASE_URL=postgresql://user:pass@host:5432/primer python embed_corpus.py
"""
import json
import os
import re
import shutil

import faiss
import numpy as np
import psycopg2
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM = 384

BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "scam_corpus.faiss")
META_PATH = os.path.join(BASE_DIR, "scam_corpus_meta.json")
BACKEND_MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "backend", "app", "ml", "models")
SEED_SQL_PATH = os.path.join(BASE_DIR, "..", "..", "backend", "seed_data", "01_seed.sql")

DEFAULT_DATABASE_URL = "postgresql://primer:primer_dev@localhost:5432/primer"


def database_url() -> str:
    url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
    # SQLAlchemy-style async URLs (from backend .env) also work if handed to us.
    return url.replace("postgresql+asyncpg://", "postgresql://")


def fetch_corpus() -> list[dict]:
    with psycopg2.connect(database_url()) as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, language, scam_type, title, content
            FROM scam_sentinel.scam_script_corpus
            WHERE is_active
            ORDER BY id
        """)
        return [
            {"id": str(row[0]), "language": row[1], "scam_type": row[2],
             "title": row[3], "content": row[4]}
            for row in cur.fetchall()
        ]


_SEED_ROW_RE = re.compile(
    r"INSERT INTO scam_sentinel\.scam_script_corpus\s*"
    r"\(id, language, scam_type, title, content, key_phrases, times_matched, is_active\)\s*"
    r"VALUES \(\s*"
    r"'((?:[^']|'')*)',\s*"    # id
    r"'((?:[^']|'')*)',\s*"    # language
    r"'((?:[^']|'')*)',\s*"    # scam_type
    r"'((?:[^']|'')*)',\s*"    # title
    r"'((?:[^']|'')*)',\s*"    # content
    r"'(?:[^']|'')*',\s*"      # key_phrases (unused)
    r"\d+,\s*(TRUE|FALSE)",    # times_matched (skipped), is_active
)


def fetch_corpus_from_seed() -> list[dict]:
    """Fallback when PostgreSQL is unreachable: parse the corpus INSERTs out of
    backend/seed_data/01_seed.sql (the canonical demo corpus)."""
    with open(SEED_SQL_PATH, encoding="utf-8") as f:
        sql = f.read()

    def unquote(s: str) -> str:
        return s.replace("''", "'")

    return [
        {"id": unquote(m.group(1)), "language": unquote(m.group(2)),
         "scam_type": unquote(m.group(3)), "title": unquote(m.group(4)),
         "content": unquote(m.group(5))}
        for m in _SEED_ROW_RE.finditer(sql)
        if m.group(6) == "TRUE"
    ]


def embed_texts(model: SentenceTransformer, texts: list[str]) -> np.ndarray:
    """Generate normalized 384-dim embeddings for a text list."""
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=True)


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Build FAISS index for cosine similarity search (inner product on
    normalized vectors)."""
    index = faiss.IndexFlatIP(EMBED_DIM)
    index.add(embeddings.astype(np.float32))
    return index


def store_embeddings_in_db(corpus: list[dict], embeddings: np.ndarray) -> None:
    """Write embeddings back to the pgvector column on scam_script_corpus."""
    with psycopg2.connect(database_url()) as conn, conn.cursor() as cur:
        for row, emb in zip(corpus, embeddings):
            vec = "[" + ",".join(f"{v:.8f}" for v in emb) + "]"
            cur.execute(
                "UPDATE scam_sentinel.scam_script_corpus SET embedding = %s::vector WHERE id = %s",
                (vec, row["id"]),
            )
        conn.commit()


def main():
    try:
        corpus = fetch_corpus()
        db_available = True
        source = "scam_sentinel.scam_script_corpus"
    except psycopg2.OperationalError as exc:
        print(f"WARNING: PostgreSQL unreachable ({exc}) — falling back to {SEED_SQL_PATH}")
        corpus = fetch_corpus_from_seed()
        db_available = False
        source = "backend/seed_data/01_seed.sql"
    if not corpus:
        raise RuntimeError("scam_script_corpus is empty — load backend/seed_data/01_seed.sql first")
    print(f"Fetched {len(corpus)} active scripts from {source}")

    model = SentenceTransformer(EMBED_MODEL)
    texts = [f"{row['title']}\n{row['content']}" for row in corpus]
    embeddings = embed_texts(model, texts)

    index = build_faiss_index(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump({"embed_model": EMBED_MODEL, "dim": EMBED_DIM, "rows": corpus},
                  f, ensure_ascii=False, indent=2)
    print(f"Wrote {INDEX_PATH} ({index.ntotal} vectors) and {META_PATH}")

    if db_available:
        store_embeddings_in_db(corpus, embeddings)
        print(f"Updated embedding column for {len(corpus)} rows in scam_script_corpus")
    else:
        print("Skipped pgvector write-back (DB unreachable) — rerun with postgres up to fill it")

    os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)
    shutil.copy(INDEX_PATH, os.path.join(BACKEND_MODELS_DIR, os.path.basename(INDEX_PATH)))
    shutil.copy(META_PATH, os.path.join(BACKEND_MODELS_DIR, os.path.basename(META_PATH)))
    print(f"Copied index + metadata -> {BACKEND_MODELS_DIR}")


if __name__ == "__main__":
    main()
