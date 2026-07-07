from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services import correlation as correlation_service

router = APIRouter()


class GraphCorrelation(BaseModel):
    matched_entities: list[dict] = Field(default_factory=list)
    clusters: list[dict] = Field(default_factory=list)
    connections: list[dict] = Field(default_factory=list)


class CorrelationResponse(BaseModel):
    found: bool
    session_id: str | None = None
    session: dict | None = None
    graph: GraphCorrelation = Field(default_factory=GraphCorrelation)
    map_incidents: list[dict] = Field(default_factory=list)


@router.get("/scam-session/{session_id}", response_model=CorrelationResponse)
async def get_scam_session_correlation(session_id: UUID, db: AsyncSession = Depends(get_db)):
    """Link a scam session to its fraud-graph cluster and geo-intel map incidents."""
    return await correlation_service.correlate_scam_session(db, session_id)
