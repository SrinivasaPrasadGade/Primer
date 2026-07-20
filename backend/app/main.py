import asyncio
import contextlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.auth.router import router as auth_router
from app.routers.call_screen import router as call_screen_router
from app.routers.case_summary import router as case_summary_router
from app.routers.citizen_shield import router as citizen_shield_router
from app.routers.copilot import router as copilot_router
from app.routers.correlation import router as correlation_router
from app.routers.fraud_graph import router as fraud_graph_router
from app.routers.geo_intel import router as geo_intel_router
from app.routers.knowledge_base import router as knowledge_base_router
from app.routers.note_verify import router as note_verify_router
from app.routers.panic import router as panic_router
from app.routers.qr_scanner import router as qr_scanner_router
from app.routers import scam_sentinel as scam_sentinel_router_module
from app.routers.scam_sentinel import router as scam_sentinel_router
from app.services import live_feed

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run one live-feed subscriber per worker.

    Without it a worker only ever sees the classifications it handled itself, so
    officers connected to other workers miss those alerts entirely.
    """
    subscriber = await scam_sentinel_router_module.start_live_feed_subscriber()
    try:
        yield
    finally:
        subscriber.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await subscriber
        await live_feed.aclose()


app = FastAPI(
    title="Primer API",
    description="AI-Powered Digital Public Safety Intelligence Platform",
    version="1.0.0-mvp",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(scam_sentinel_router, prefix="/api/v1/scam", tags=["Scam Sentinel"])
app.include_router(note_verify_router, prefix="/api/v1/note", tags=["Note Verify"])
app.include_router(fraud_graph_router, prefix="/api/v1/graph", tags=["Fraud Graph"])
app.include_router(geo_intel_router, prefix="/api/v1/geo", tags=["Geo Intel"])
app.include_router(citizen_shield_router, prefix="/api/v1/citizen", tags=["Citizen Shield"])
app.include_router(copilot_router, prefix="/api/v1/copilot", tags=["AI Copilot"])
app.include_router(qr_scanner_router, prefix="/api/v1/qr", tags=["QR Scanner"])
app.include_router(case_summary_router, prefix="/api/v1/case", tags=["Case Summary"])
app.include_router(panic_router, prefix="/api/v1/panic", tags=["Panic Button"])
app.include_router(call_screen_router, prefix="/api/v1/screen", tags=["Call Screening"])
app.include_router(correlation_router, prefix="/api/v1/correlation", tags=["Cross-Module Correlation"])
app.include_router(knowledge_base_router, prefix="/api/v1/kb", tags=["Adaptive Fraud KB"])

logger = logging.getLogger("primer")


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Services raise ValueError for bad/missing resources (e.g. an unknown session or
    cluster id); surface those as a clean 400 rather than an unhandled 500."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Last-resort safety net: log the traceback server-side, never leak it to clients."""
    logger.exception("Unhandled error handling %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0-mvp"}
