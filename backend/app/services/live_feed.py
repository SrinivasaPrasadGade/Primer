"""Cross-process fan-out for the Scam Sentinel live feed, over Redis pub/sub.

WebSocket clients are held in a per-process list. With more than one uvicorn worker
that list only ever contains the sockets that happened to land on *this* worker, so
a classify handled by worker A never reaches an officer connected to worker B — the
dashboard silently misses alerts, and which ones depends on load balancing.

Publishing to Redis and having every worker fan out to its own local sockets fixes
that: the publishing worker receives its own message back through the subscription,
so delivery happens exactly once per socket regardless of which worker scored the
session.

Redis being unreachable is not fatal. `publish()` reports failure and the caller
falls back to delivering locally, which is correct for the common single-worker
dev setup — you just lose cross-worker delivery, which a single worker doesn't need.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, Awaitable, Callable

from app.config import settings

logger = logging.getLogger("primer.live_feed")

CHANNEL = "primer:scam:live"

# How long to wait before retrying a connection after a failure, so a missing Redis
# doesn't turn every broadcast into a TCP connect attempt.
_RETRY_COOLDOWN_SEC = 30.0
_SUBSCRIBE_RETRY_SEC = 5.0

_client: Any = None
_next_retry_at: float = 0.0
_warned = False


async def _get_client():
    """Cached Redis client, or None while Redis looks unreachable."""
    global _client, _next_retry_at, _warned

    if _client is not None:
        return _client
    if time.monotonic() < _next_retry_at:
        return None

    try:
        import redis.asyncio as redis_asyncio

        client = redis_asyncio.from_url(settings.redis_url, decode_responses=True)
        await client.ping()
    except Exception as exc:
        _next_retry_at = time.monotonic() + _RETRY_COOLDOWN_SEC
        if not _warned:
            # Once, not per broadcast — this is an expected state in local dev.
            logger.warning(
                "Redis unreachable at %s (%s). Live feed falls back to in-process "
                "delivery; alerts will not cross uvicorn workers.",
                settings.redis_url,
                exc,
            )
            _warned = True
        return None

    logger.info("Live feed connected to Redis at %s", settings.redis_url)
    _client = client
    _warned = False
    return _client


async def publish(payload: dict) -> bool:
    """Publish one live-feed event. Returns False if it could not be published."""
    client = await _get_client()
    if client is None:
        return False
    try:
        await client.publish(CHANNEL, json.dumps(payload))
        return True
    except Exception:
        global _client, _next_retry_at
        logger.warning("Live feed publish failed; falling back to in-process delivery", exc_info=True)
        _client = None
        _next_retry_at = time.monotonic() + _RETRY_COOLDOWN_SEC
        return False


async def run_subscriber(handler: Callable[[dict], Awaitable[None]]) -> None:
    """Deliver every published event to `handler` until cancelled.

    Reconnects on failure rather than dying, so a Redis restart doesn't silently
    leave this worker deaf for the rest of its life.
    """
    while True:
        try:
            client = await _get_client()
            if client is None:
                await asyncio.sleep(_SUBSCRIBE_RETRY_SEC)
                continue

            pubsub = client.pubsub()
            await pubsub.subscribe(CHANNEL)
            logger.info("Live feed subscribed to %s", CHANNEL)
            try:
                async for message in pubsub.listen():
                    if message.get("type") != "message":
                        continue
                    try:
                        await handler(json.loads(message["data"]))
                    except Exception:
                        # One malformed or undeliverable event must not end the loop.
                        logger.exception("Live feed handler failed for one event")
            finally:
                await pubsub.aclose()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.warning("Live feed subscriber dropped; retrying", exc_info=True)
            global _client
            _client = None
            await asyncio.sleep(_SUBSCRIBE_RETRY_SEC)


async def aclose() -> None:
    """Drop the cached client (used on shutdown)."""
    global _client
    if _client is not None:
        try:
            await _client.aclose()
        except Exception:
            pass
        _client = None
