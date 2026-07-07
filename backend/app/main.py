from fastapi import FastAPI

from app.routers.copilot import router as copilot_router

app = FastAPI(title="Primer API")

app.include_router(copilot_router, prefix="/api/v1/copilot", tags=["AI Copilot"])


@app.get("/health")
async def health():
    return {"status": "ok"}
