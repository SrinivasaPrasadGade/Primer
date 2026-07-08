"""Dossier: PDF evidence-dossier generation for a fraud cluster (Jinja2 + WeasyPrint).

Yashi's logic layer — Srinivas's routers call generate_dossier() as the entry point.
"""

from __future__ import annotations

import json
from decimal import Decimal
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from jinja2 import Environment, FileSystemLoader
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from weasyprint import HTML

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
DOSSIERS_DIR = Path("uploads/dossiers")

_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


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


async def get_cluster_data(db: AsyncSession, cluster_id: UUID) -> dict | None:
    row = (
        await db.execute(
            text(
                """
                SELECT id, name, node_count, edge_count, estimated_loss, victim_count, status, detected_at
                FROM fraud_graph.clusters WHERE id = :cluster_id
                """
            ),
            {"cluster_id": cluster_id},
        )
    ).mappings().first()
    return _to_jsonable(dict(row)) if row else None


async def get_cluster_entities(db: AsyncSession, cluster_id: UUID) -> list[dict]:
    rows = (
        await db.execute(
            text(
                """
                SELECT id, entity_type, entity_value, display_label, risk_score, first_seen, last_seen
                FROM fraud_graph.entities WHERE cluster_id = :cluster_id
                ORDER BY risk_score DESC
                """
            ),
            {"cluster_id": cluster_id},
        )
    ).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


async def get_cluster_edges(db: AsyncSession, cluster_id: UUID) -> list[dict]:
    rows = (
        await db.execute(
            text(
                """
                SELECT e.relationship, e.weight, e.first_seen,
                       s.entity_value AS source_label, t.entity_value AS target_label
                FROM fraud_graph.edges e
                JOIN fraud_graph.entities s ON s.id = e.source_id
                JOIN fraud_graph.entities t ON t.id = e.target_id
                WHERE s.cluster_id = :cluster_id AND t.cluster_id = :cluster_id
                ORDER BY e.first_seen
                """
            ),
            {"cluster_id": cluster_id},
        )
    ).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


async def get_cluster_timeline(db: AsyncSession, cluster_id: UUID) -> list[dict]:
    """Derive a chronological timeline from entity/edge first-seen timestamps
    (the schema has no dedicated timeline table for clusters)."""
    entities = await get_cluster_entities(db, cluster_id)
    edges = await get_cluster_edges(db, cluster_id)

    events = [
        {"date": e["first_seen"], "event": f"{e['entity_type']} {e['entity_value']} first observed"}
        for e in entities
    ]
    events += [
        {"date": e["first_seen"], "event": f"{e['source_label']} --[{e['relationship']}]--> {e['target_label']}"}
        for e in edges
    ]
    return sorted(events, key=lambda e: e["date"] or "")


async def generate_dossier(db: AsyncSession, cluster_id: UUID, officer_id: UUID) -> str:
    """Generate a PDF evidence dossier for a fraud cluster and persist a record of it."""
    cluster = await get_cluster_data(db, cluster_id)
    if not cluster:
        raise ValueError(f"Cluster {cluster_id} not found")

    nodes = await get_cluster_entities(db, cluster_id)
    edges = await get_cluster_edges(db, cluster_id)
    timeline = await get_cluster_timeline(db, cluster_id)

    template = _env.get_template("dossier.html")
    html_content = template.render(
        cluster=cluster,
        nodes=nodes,
        edges=edges,
        timeline=timeline,
        generated_at=datetime.now(timezone.utc).isoformat(),
        generated_by=str(officer_id),
    )

    DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    output_path = DOSSIERS_DIR / f"dossier_{cluster_id}_{timestamp}.pdf"
    HTML(string=html_content).write_pdf(str(output_path))

    await db.execute(
        text(
            """
            INSERT INTO fraud_graph.dossiers (cluster_id, title, content_json, pdf_path, generated_by)
            VALUES (:cluster_id, :title, CAST(:content AS JSONB), :pdf_path, :generated_by)
            """
        ),
        {
            "cluster_id": cluster_id,
            "title": f"Dossier - {cluster['name'] or cluster_id}",
            "content": json.dumps({"nodes": len(nodes), "edges": len(edges), "timeline_events": len(timeline)}),
            "pdf_path": str(output_path),
            "generated_by": officer_id,
        },
    )
    await db.commit()

    return str(output_path)
