"""Fraud Graph API layer — wraps app.services.fraud_graph + app.services.dossier
(Yashi's neighbourhood/community-detection/money-flow logic). Srinivas's routers
handle request validation, auth, and response formatting.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.database import get_db
from app.services import dossier as dossier_service
from app.services import fraud_graph as graph_service

router = APIRouter()

VALID_ENTITY_TYPES = (
    "phone_number", "bank_account", "upi_id", "person", "device", "ip_address", "complaint",
)


class SearchRequest(BaseModel):
    query: str
    limit: int = 20


@router.get("/entity/{entity_type}/{entity_value}")
async def get_entity(
    entity_type: str,
    entity_value: str,
    depth: int = Query(2, ge=1, le=4),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if entity_type not in VALID_ENTITY_TYPES:
        raise HTTPException(400, f"entity_type must be one of {VALID_ENTITY_TYPES}")
    result = await graph_service.get_entity_neighbourhood(db, entity_type, entity_value, depth=depth)
    if not result["nodes"]:
        raise HTTPException(404, "Entity not found")
    return result


@router.get("/money-flow/{entity_id}")
async def get_money_flow(
    entity_id: UUID,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await graph_service.get_money_flow(db, entity_id)


@router.get("/cluster/{cluster_id}")
async def get_cluster(
    cluster_id: UUID,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cluster = await dossier_service.get_cluster_data(db, cluster_id)
    if not cluster:
        raise HTTPException(404, "Cluster not found")
    entities = await dossier_service.get_cluster_entities(db, cluster_id)
    edges = await dossier_service.get_cluster_edges(db, cluster_id)
    return {"cluster": cluster, "entities": entities, "edges": edges}


@router.post("/dossier/{cluster_id}")
async def generate_dossier(
    cluster_id: UUID,
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    try:
        pdf_path = await dossier_service.generate_dossier(db, cluster_id, officer_id=UUID(str(user["id"])))
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"cluster_id": str(cluster_id), "pdf_path": pdf_path}


@router.post("/communities/detect")
async def detect_communities(
    min_cluster_size: int = Query(3, ge=2),
    user: dict = Depends(require_role("lea_officer")),
    db: AsyncSession = Depends(get_db),
):
    communities = await graph_service.detect_communities(db, min_cluster_size=min_cluster_size)
    return await graph_service.persist_communities(db, communities)


@router.post("/search")
async def search_entities(
    req: SearchRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Simple entity-value search across the fraud graph (response formatting only,
    not a scoring/business-logic concern — kept here rather than in Yashi's service)."""
    rows = (
        await db.execute(
            text(
                """
                SELECT id, entity_type, entity_value, display_label, risk_score, cluster_id
                FROM fraud_graph.entities
                WHERE entity_value ILIKE :pattern
                ORDER BY risk_score DESC
                LIMIT :limit
                """
            ),
            {"pattern": f"%{req.query}%", "limit": req.limit},
        )
    ).mappings().all()
    return graph_service._to_jsonable([dict(row) for row in rows])
