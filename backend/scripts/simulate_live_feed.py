"""Drive the Scam Sentinel live feed by generating and classifying sessions on a timer.

`scam_sentinel.scam_sessions` only gains rows from 01_seed.sql, and the /scam/ws/live
socket only emits when an officer manually clicks Classify - so the "Live Monitor"
sits motionless during a demo no matter how long you watch it. This inserts a fresh
call record every N seconds and classifies it, so the board visibly reacts.

It classifies over HTTP rather than by calling process_scam_session directly, and
that is not incidental: broadcast_new_session pushes to `_connected_clients`, a
module-level list living in the API process. A script in its own process has its own
empty copy, so a direct service call would score the session silently and the
dashboard would never move. Going through POST /scam/sessions/{id}/classify makes the
API process do both the scoring and the broadcast.

Like bootstrap_predictions, this never writes model output by hand. It inserts call
metadata - the kind of record a telecom feed would supply - and leaves alert_level,
overall_confidence and signal_scores entirely to the real pipeline.

The API must already be running:

    python -m scripts.simulate_live_feed                  # every 8s until Ctrl+C
    python -m scripts.simulate_live_feed --interval 3     # faster, for a live pitch
    python -m scripts.simulate_live_feed --count 5        # emit 5 then stop
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import random
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import text

from app.database import async_session, engine

logger = logging.getLogger("simulate_live_feed")

DEFAULT_API_URL = "http://localhost:8000"
# The lea_officer seeded by 0001_initial_schema.py; classify requires that role.
DEFAULT_EMAIL = "yashi@primer.demo"
DEFAULT_PASSWORD = "Primer@2026"

_HTTP_TIMEOUT_SEC = 30
_MAX_CONSECUTIVE_FAILURES = 5


def _post(url: str, payload: dict | None, token: str | None = None) -> dict:
    """Minimal JSON POST. Uses urllib so the script adds no runtime dependency -
    httpx is deliberately dev-only and absent from the API image."""
    data = json.dumps(payload).encode() if payload is not None else b""
    request = urllib.request.Request(url, data=data, method="POST")
    request.add_header("Content-Type", "application/json")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=_HTTP_TIMEOUT_SEC) as response:
        body = response.read().decode()
    return json.loads(body) if body else {}


def _login(api_url: str, email: str, password: str) -> str:
    result = _post(f"{api_url}/api/v1/auth/login", {"email": email, "password": password})
    token = result.get("access_token")
    if not token:
        raise RuntimeError("Login succeeded but returned no access_token")
    return token


async def _sample_caller_numbers(db) -> list[str]:
    """Prefer numbers that already carry a reputation.

    caller_risk_score and caller_complaint_count are real classifier inputs, so
    reusing flagged numbers produces a feed with genuinely varied alert levels
    instead of a wall of identical low-confidence rows.
    """
    rows = (
        await db.execute(
            text(
                """
                SELECT phone_number FROM scam_sentinel.number_reputation
                ORDER BY risk_score DESC
                LIMIT 40
                """
            )
        )
    ).all()
    return [row[0] for row in rows]


async def _sample_transcripts(db) -> list[str]:
    """Real scam scripts from the corpus, used as simulated call transcripts.

    script_similarity scores a transcript against this same corpus, so feeding
    genuine entries is what makes that signal (and urgency_phrases) produce
    non-zero scores instead of the "No transcript available" floor.
    """
    rows = (
        await db.execute(
            text("SELECT content FROM scam_sentinel.scam_script_corpus WHERE is_active LIMIT 50")
        )
    ).all()
    return [row[0] for row in rows]


# Ordinary calls, so the feed isn't uniformly hostile. Nothing here trips an
# urgency phrase or resembles the corpus, which is the point.
BENIGN_TRANSCRIPTS = [
    "Hi, this is the clinic calling to confirm your appointment on Thursday morning.",
    "Hello, your parcel is out for delivery today. No action needed from your side.",
    "This is a reminder that your electricity bill is due at the end of the month.",
    "Hi, just calling to check whether you are still interested in the flat viewing.",
]


def _random_callee() -> str:
    return "+919" + "".join(random.choice("0123456789") for _ in range(9))


async def _insert_session(db, caller_numbers: list[str], transcripts: list[str]) -> tuple[str, str]:
    """Insert one unclassified call record. Returns (session_id, caller_number)."""
    # Mostly known-bad callers, with a slice of unknown numbers so the feed isn't
    # uniformly red.
    scammy = random.random() < 0.7
    if caller_numbers and scammy:
        caller = random.choice(caller_numbers)
    else:
        caller = _random_callee()

    # Pair a flagged caller with a real scam script and an unknown caller with an
    # ordinary one, so alert levels spread across RED/AMBER/YELLOW instead of
    # clustering at one end.
    if scammy and transcripts:
        transcript = random.choice(transcripts)
    else:
        transcript = random.choice(BENIGN_TRANSCRIPTS)

    session_id = str(uuid4())
    duration = random.randint(45, 900)
    call_start = datetime.now(timezone.utc) - timedelta(seconds=duration)

    await db.execute(
        text(
            """
            INSERT INTO scam_sentinel.scam_sessions
                (id, caller_number, callee_number, call_start, call_end,
                 call_duration_sec, spoofing_detected, voice_synthetic_probability,
                 transcript_text, status)
            VALUES
                (:id, :caller, :callee, :call_start, :call_end,
                 :duration, :spoofing, :voice_prob, :transcript, 'active')
            """
        ),
        {
            "id": session_id,
            "caller": caller,
            "callee": _random_callee(),
            "call_start": call_start,
            "call_end": datetime.now(timezone.utc),
            "duration": duration,
            "transcript": transcript,
            "spoofing": random.random() < 0.35,
            # 0-1, matching the seed data and what generate_voice_explanation expects.
            # Writing 0-100 here makes the voice signal dwarf the other four (all 0-1),
            # so compute_overall_confidence saturates and every call comes out RED/100.
            "voice_prob": round(random.uniform(0, 0.95), 2),
        },
    )
    await db.commit()
    return session_id, caller


async def main(interval: float, count: int, api_url: str, email: str, password: str) -> int:
    api_url = api_url.rstrip("/")

    try:
        token = await asyncio.to_thread(_login, api_url, email, password)
    except urllib.error.URLError as exc:
        logger.error("Could not reach the API at %s - is it running? (%s)", api_url, exc)
        return 1
    except Exception:
        logger.exception("Login failed for %s", email)
        return 1

    logger.info("Signed in as %s. Emitting a session every %.1fs (Ctrl+C to stop).", email, interval)

    emitted = 0
    consecutive_failures = 0
    try:
        async with async_session() as db:
            caller_numbers = await _sample_caller_numbers(db)
            if not caller_numbers:
                logger.warning("No rows in scam_sentinel.number_reputation - load 01_seed.sql for a "
                               "more varied feed. Falling back to random numbers.")
            transcripts = await _sample_transcripts(db)
            if not transcripts:
                logger.warning("No rows in scam_sentinel.scam_script_corpus - every call will use a "
                               "benign transcript, so alert levels will stay low.")

            while count == 0 or emitted < count:
                session_id, caller = await _insert_session(db, caller_numbers, transcripts)
                try:
                    result = await asyncio.to_thread(
                        _post, f"{api_url}/api/v1/scam/sessions/{session_id}/classify", None, token
                    )
                except Exception:
                    # Leave the row in place: it's a real unclassified session an
                    # officer can still classify by hand.
                    logger.exception("Classify failed for session %s", session_id)
                    consecutive_failures += 1
                    # Without this, a persistently failing API (expired token, restart)
                    # would insert unclassified rows forever.
                    if consecutive_failures >= _MAX_CONSECUTIVE_FAILURES:
                        logger.error("Giving up after %d consecutive classify failures.", consecutive_failures)
                        return 1
                else:
                    consecutive_failures = 0
                    emitted += 1
                    logger.info(
                        "[%d] %s -> %s (confidence %s)",
                        emitted,
                        caller,
                        result.get("alert_level", "?"),
                        result.get("overall_confidence", "?"),
                    )

                if count == 0 or emitted < count:
                    await asyncio.sleep(interval)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Stopped after %d session(s).", emitted)
    finally:
        # Dispose inside this loop - the asyncpg pool is bound to it.
        await engine.dispose()

    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interval", type=float, default=8.0, help="seconds between sessions (default: 8)")
    parser.add_argument("--count", type=int, default=0, help="how many to emit; 0 runs until Ctrl+C (default: 0)")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help=f"API base URL (default: {DEFAULT_API_URL})")
    parser.add_argument("--email", default=DEFAULT_EMAIL, help=f"officer login (default: {DEFAULT_EMAIL})")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help="officer password")
    args = parser.parse_args()

    try:
        exit_code = asyncio.run(main(args.interval, args.count, args.api_url, args.email, args.password))
    except KeyboardInterrupt:
        exit_code = 0

    sys.exit(exit_code)
