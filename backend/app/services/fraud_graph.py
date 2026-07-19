"""Fraud Graph: entity neighbourhood queries, community detection, money flow tracing.

Yashi's logic layer — Srinivas's routers call these functions and return their JSON-ready
dicts/lists directly; no ORM models, raw SQL via SQLAlchemy Core (matches correlation.py).
"""

from __future__ import annotations

import json
from decimal import Decimal
from collections import defaultdict
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.phone import normalize_phone


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


# ---------------------------------------------------------------------------
# Entity neighbourhood (recursive CTE) + money flow
# ---------------------------------------------------------------------------

_NEIGHBOURHOOD_QUERY = text(
    """
    WITH RECURSIVE hops AS (
        SELECT e.id, e.entity_type, e.entity_value, e.risk_score,
               e.display_label, e.properties, e.cluster_id, 0 AS depth
        FROM fraud_graph.entities e
        WHERE e.entity_type = :entity_type AND e.entity_value = :entity_value

        UNION ALL

        SELECT e2.id, e2.entity_type, e2.entity_value, e2.risk_score,
               e2.display_label, e2.properties, e2.cluster_id, h.depth + 1
        FROM hops h
        JOIN fraud_graph.edges eg ON (eg.source_id = h.id OR eg.target_id = h.id)
        JOIN fraud_graph.entities e2 ON (
            e2.id = CASE WHEN eg.source_id = h.id THEN eg.target_id ELSE eg.source_id END
        )
        WHERE h.depth < :depth
    )
    -- ORDER BY id, depth keeps the *shallowest* depth seen for a node reached via
    -- multiple paths, rather than an arbitrary one (DISTINCT ON with no explicit
    -- ordering would pick whichever row Postgres happens to visit last).
    SELECT DISTINCT ON (id) * FROM hops ORDER BY id, depth;
    """
)

_EDGES_BETWEEN_QUERY = text(
    """
    SELECT e.id, e.source_id, e.target_id, e.relationship, e.weight, e.properties,
           e.first_seen, e.last_seen,
           s.entity_value AS source_label, t.entity_value AS target_label
    FROM fraud_graph.edges e
    JOIN fraud_graph.entities s ON e.source_id = s.id
    JOIN fraud_graph.entities t ON e.target_id = t.id
    WHERE e.source_id = ANY((:ids)::uuid[]) AND e.target_id = ANY((:ids)::uuid[])
    """
)


async def get_entity_neighbourhood(db: AsyncSession, entity_type: str, entity_value: str, depth: int = 2) -> dict:
    """Get the N-hop neighbourhood of an entity, ready for frontend graph visualisation."""
    if entity_type == "phone_number":
        # Stored as +91XXXXXXXXXX; callers pass whatever was typed or detected.
        entity_value = normalize_phone(entity_value)
    nodes = (
        await db.execute(_NEIGHBOURHOOD_QUERY, {"entity_type": entity_type, "entity_value": entity_value, "depth": depth})
    ).mappings().all()
    if not nodes:
        return {"nodes": [], "edges": []}

    node_ids = [n["id"] for n in nodes]
    edges = (await db.execute(_EDGES_BETWEEN_QUERY, {"ids": node_ids})).mappings().all()

    return _to_jsonable({"nodes": [dict(n) for n in nodes], "edges": [dict(e) for e in edges]})


async def get_money_flow(db: AsyncSession, entity_id: UUID) -> list[dict]:
    """Trace money flow (transferred_to edges) through the entity's fraud cluster."""
    rows = (
        await db.execute(
            text(
                """
                SELECT e.id, e.source_id, e.target_id, e.weight AS amount, e.first_seen,
                       s.entity_value AS from_entity, s.entity_type AS from_type,
                       t.entity_value AS to_entity, t.entity_type AS to_type
                FROM fraud_graph.edges e
                JOIN fraud_graph.entities s ON e.source_id = s.id
                JOIN fraud_graph.entities t ON e.target_id = t.id
                WHERE e.relationship = 'transferred_to'
                AND e.source_id IN (
                    SELECT id FROM fraud_graph.entities WHERE cluster_id = (
                        SELECT cluster_id FROM fraud_graph.entities WHERE id = :entity_id
                    )
                )
                ORDER BY e.first_seen
                """
            ),
            {"entity_id": entity_id},
        )
    ).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


# ---------------------------------------------------------------------------
# Community detection — union-find over the whole graph
# ---------------------------------------------------------------------------

class _UnionFind:
    def __init__(self):
        self._parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self._parent.setdefault(x, x)
        while self._parent[x] != x:
            self._parent[x] = self._parent[self._parent[x]]  # path halving
            x = self._parent[x]
        return x

    def union(self, x: str, y: str) -> None:
        root_x, root_y = self.find(x), self.find(y)
        if root_x != root_y:
            self._parent[root_x] = root_y

    def nodes(self) -> list[str]:
        return list(self._parent)


async def detect_communities(db: AsyncSession, min_cluster_size: int = 3) -> dict[str, list[str]]:
    """Connected-component community detection via union-find.

    Not as sophisticated as a modularity-based algorithm, but O(edges) and good enough
    for the demo's scale. Returns {representative_entity_id: [member_entity_ids]},
    filtered to clusters with at least min_cluster_size members.
    """
    edges = (await db.execute(text("SELECT source_id, target_id FROM fraud_graph.edges"))).all()

    uf = _UnionFind()
    for row in edges:
        uf.union(str(row.source_id), str(row.target_id))

    members: dict[str, list[str]] = defaultdict(list)
    for node in uf.nodes():
        members[uf.find(node)].append(node)

    return {root: ids for root, ids in members.items() if len(ids) >= min_cluster_size}


async def persist_communities(db: AsyncSession, communities: dict[str, list[str]]) -> list[dict]:
    """Write detected communities back to fraud_graph.clusters + entities.cluster_id.

    Reuses an existing cluster row for a community if any of its members already carry
    a cluster_id (keeps cluster identity stable across re-runs); otherwise creates one.
    """
    results = []
    for member_ids in communities.values():
        existing = (
            await db.execute(
                text(
                    "SELECT cluster_id FROM fraud_graph.entities "
                    "WHERE id = ANY((:ids)::uuid[]) AND cluster_id IS NOT NULL LIMIT 1"
                ),
                {"ids": member_ids},
            )
        ).scalar()

        edge_count = (
            await db.execute(
                text(
                    "SELECT COUNT(*) FROM fraud_graph.edges "
                    "WHERE source_id = ANY((:ids)::uuid[]) AND target_id = ANY((:ids)::uuid[])"
                ),
                {"ids": member_ids},
            )
        ).scalar()

        if existing:
            cluster_id = existing
            await db.execute(
                text(
                    "UPDATE fraud_graph.clusters SET node_count = :nodes, edge_count = :edges "
                    "WHERE id = :cluster_id"
                ),
                {"nodes": len(member_ids), "edges": edge_count, "cluster_id": cluster_id},
            )
        else:
            cluster_id = (
                await db.execute(
                    text(
                        "INSERT INTO fraud_graph.clusters (name, node_count, edge_count) "
                        "VALUES (:name, :nodes, :edges) RETURNING id"
                    ),
                    {"name": f"Cluster ({len(member_ids)} entities)", "nodes": len(member_ids), "edges": edge_count},
                )
            ).scalar()

        await db.execute(
            text("UPDATE fraud_graph.entities SET cluster_id = :cluster_id WHERE id = ANY((:ids)::uuid[])"),
            {"cluster_id": cluster_id, "ids": member_ids},
        )
        results.append({"cluster_id": str(cluster_id), "node_count": len(member_ids), "edge_count": edge_count})

    await db.commit()
    return results
