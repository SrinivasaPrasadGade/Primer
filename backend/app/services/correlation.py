"""Cross-module correlation: link a scam session to its fraud-graph footprint and map incidents."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def _get_session(db: AsyncSession, session_id: UUID) -> dict | None:
    row = (
        await db.execute(
            text(
                """
                SELECT id, caller_number, callee_number, call_start, call_end,
                       call_duration_sec, alert_level, overall_confidence, scam_type,
                       scam_phase, signal_scores, spoofing_detected,
                       real_originating_number, deepfake_detected,
                       voice_synthetic_probability, status, created_at, updated_at
                FROM scam_sentinel.scam_sessions
                WHERE id = :session_id
                """
            ),
            {"session_id": session_id},
        )
    ).mappings().first()
    return dict(row) if row else None


async def _matched_entities(db: AsyncSession, numbers: list[str]) -> list[dict]:
    if not numbers:
        return []
    rows = (
        await db.execute(
            text(
                """
                SELECT id, entity_type, entity_value, display_label, risk_score,
                       cluster_id, first_seen, last_seen
                FROM fraud_graph.entities
                WHERE entity_type = 'phone_number' AND entity_value = ANY(:numbers::varchar[])
                """
            ),
            {"numbers": numbers},
        )
    ).mappings().all()
    return [dict(row) for row in rows]


async def _clusters_for(db: AsyncSession, cluster_ids: list[UUID]) -> list[dict]:
    if not cluster_ids:
        return []
    rows = (
        await db.execute(
            text(
                """
                SELECT id, name, node_count, edge_count, estimated_loss,
                       victim_count, status, detected_at
                FROM fraud_graph.clusters
                WHERE id = ANY(:cluster_ids::uuid[])
                """
            ),
            {"cluster_ids": cluster_ids},
        )
    ).mappings().all()
    return [dict(row) for row in rows]


async def _connections_for(db: AsyncSession, entity_ids: list[UUID]) -> list[dict]:
    if not entity_ids:
        return []
    rows = (
        await db.execute(
            text(
                """
                SELECT e.relationship, e.weight, e.last_seen,
                       s.entity_type AS source_type, s.entity_value AS source_value,
                       t.entity_type AS target_type, t.entity_value AS target_value
                FROM fraud_graph.edges e
                JOIN fraud_graph.entities s ON s.id = e.source_id
                JOIN fraud_graph.entities t ON t.id = e.target_id
                WHERE e.source_id = ANY(:ids::uuid[]) OR e.target_id = ANY(:ids::uuid[])
                ORDER BY e.last_seen DESC
                LIMIT 50
                """
            ),
            {"ids": entity_ids},
        )
    ).mappings().all()
    return [dict(row) for row in rows]


async def _map_incidents(db: AsyncSession, session_id: UUID) -> list[dict]:
    rows = (
        await db.execute(
            text(
                """
                SELECT id, crime_type, title, description,
                       ST_X(location) AS lng, ST_Y(location) AS lat,
                       state, district, pin_code, severity, estimated_loss, reported_at
                FROM geo_intel.incidents
                WHERE source_module = 'scam_sentinel' AND source_ref_id = :session_id
                ORDER BY reported_at DESC
                """
            ),
            {"session_id": session_id},
        )
    ).mappings().all()
    return [dict(row) for row in rows]


async def correlate_scam_session(db: AsyncSession, session_id: UUID) -> dict:
    """Link a scam session to its fraud-graph entities/cluster and geo-intel map incidents.

    Correlation path: scam_sentinel.scam_sessions (session)
                    -> fraud_graph.entities/clusters (graph, matched on caller/callee number)
                    -> geo_intel.incidents (map, matched on source_module/source_ref_id)
    """
    session = await _get_session(db, session_id)
    if not session:
        return {"found": False, "session_id": str(session_id)}

    numbers = list({session["caller_number"], session["callee_number"]})
    entities = await _matched_entities(db, numbers)

    cluster_ids = list({e["cluster_id"] for e in entities if e.get("cluster_id")})
    clusters = await _clusters_for(db, cluster_ids)

    entity_ids = [e["id"] for e in entities]
    connections = await _connections_for(db, entity_ids)

    incidents = await _map_incidents(db, session_id)

    return {
        "found": True,
        "session": session,
        "graph": {
            "matched_entities": entities,
            "clusters": clusters,
            "connections": connections,
        },
        "map_incidents": incidents,
    }
