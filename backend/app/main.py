from fastapi import FastAPI

from app.routers.copilot import router as copilot_router
from app.routers.correlation import router as correlation_router

app = FastAPI(title="Primer API")

app.include_router(copilot_router, prefix="/api/v1/copilot", tags=["AI Copilot"])
app.include_router(correlation_router, prefix="/api/v1/correlation", tags=["Cross-Module Correlation"])


@app.get("/health")
async def health():
    return {"status": "ok"}
