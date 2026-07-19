from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services import copilot as copilot_service

router = APIRouter()


class CopilotQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class CopilotQueryResponse(BaseModel):
    # False when the model backend was unreachable — the answer is a status message,
    # not a finding, and the UI must not present it as one.
    available: bool = True
    answer: str
    data: list[dict]
    sources: list[str]
    query_executed: list[dict]


@router.post("/query", response_model=CopilotQueryResponse)
async def query(req: CopilotQueryRequest, db: AsyncSession = Depends(get_db)):
    return await copilot_service.process_query(db, req.question)
