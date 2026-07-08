"""Citizen Shield: AI chatbot for citizens — Gemini prompts, language detection, risk assessment.

Yashi's logic layer — Srinivas's routers call start_chat_session()/send_message() as
the entry points.
"""

from __future__ import annotations

import json
import re
from decimal import Decimal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.gemini_client import GeminiError, generate

# langdetect samples internally at random unless seeded, so the same input can
# classify differently across calls/processes without this.
from langdetect import DetectorFactory, LangDetectException, detect

DetectorFactory.seed = 0

# The corpus/product only distinguishes English vs Hindi (scam_script_corpus has no
# other languages). langdetect confuses short Devanagari-script text with related
# languages (Marathi, Nepali, Sanskrit) since they share the script — normalize all
# of those to "hi" rather than surfacing a language the rest of the app can't use.
DEVANAGARI_VARIANTS = {"hi", "mr", "ne", "sa"}
SUPPORTED_LANGUAGES = {"en", "hi"}
DEFAULT_LANGUAGE = "en"

CITIZEN_SHIELD_SYSTEM = """You are Citizen Shield, an AI safety advisor for the Primer
fraud-intelligence platform, helping ordinary citizens in India who suspect they are
being scammed or have already been scammed. Respond in the same language as the citizen
(English or Hindi). Be calm, clear, and practical:
- If they describe an ongoing call/scam, tell them to hang up and never share OTPs,
  passwords, or make payments under pressure — no real government agency (police, CBI,
  income tax, customs, courts) ever arrests someone or demands payment over a phone call.
- If they've already lost money, tell them to immediately call the National Cyber Crime
  Helpline 1930 or report at cybercrime.gov.in, and to contact their bank to freeze the
  account/reverse the transaction.
- Never ask for or store personal identifying information beyond what they volunteer.
- Keep responses concise and reassuring; this is a stressed, possibly elderly user."""

# Messages describing an already-completed compromise (money sent, OTP shared, etc.)
# need urgent escalation guidance, not general advice — checked before calling Gemini
# so escalation doesn't depend on the model noticing it.
#
# A "compromise verb" (gave/shared/sent/paid/transferred) near a "sensitive noun"
# (otp/pin/card/password/money) covers far more real phrasing than an enumerated list
# of exact phrases would (e.g. "shared my otp", "gave the otp", "sent them money" all
# match without each needing its own entry).
_COMPROMISE_VERBS_EN = r"gave|shared|sent|paid|transferred|lost"
_SENSITIVE_NOUNS_EN = r"otp|pin|password|card (?:number|details)|money|rupees|rs\.?\s?\d|amount"
URGENT_RISK_PATTERN_EN = re.compile(rf"\b({_COMPROMISE_VERBS_EN})\b[^.!?]{{0,20}}\b({_SENSITIVE_NOUNS_EN})\b")

URGENT_RISK_PHRASES_HI = ["पैसे भेज दिए", "ओटीपी दे दिया", "पैसे चले गए", "पैसा गंवा दिया"]


def _to_jsonable(value):
    """Round-trip UUID/datetime/Decimal through JSON so they're plain str/float."""
    def _default(v):
        if isinstance(v, Decimal):
            return float(v)
        return str(v)

    return json.loads(json.dumps(value, default=_default))


# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------

def detect_language(text_content: str) -> str:
    """Detect English vs Hindi for a citizen's message; defaults to English on failure
    or text too short/ambiguous for langdetect to call confidently."""
    if not text_content or len(text_content.strip()) < 3:
        return DEFAULT_LANGUAGE

    try:
        detected = detect(text_content)
    except LangDetectException:
        return DEFAULT_LANGUAGE

    if detected in DEVANAGARI_VARIANTS:
        return "hi"
    if detected in SUPPORTED_LANGUAGES:
        return detected
    return DEFAULT_LANGUAGE


# ---------------------------------------------------------------------------
# Risk assessment
# ---------------------------------------------------------------------------

def assess_message_risk(text_content: str) -> str:
    """Classify a citizen message as 'low', 'medium', or 'high' urgency.

    'high' -> the citizen describes an already-completed compromise (money sent, OTP
    shared) and the session should be escalated for human follow-up, not just chat.
    """
    if not text_content:
        return "low"

    lowered = text_content.lower()
    if URGENT_RISK_PATTERN_EN.search(lowered) or any(phrase in text_content for phrase in URGENT_RISK_PHRASES_HI):
        return "high"
    if any(keyword in lowered for keyword in ("scam", "fraud", "threat", "arrest", "otp", "स्कैम", "धोखा")):
        return "medium"
    return "low"


# ---------------------------------------------------------------------------
# Chat session persistence
# ---------------------------------------------------------------------------

async def _get_session_messages(db: AsyncSession, session_id: UUID) -> list[dict]:
    rows = (
        await db.execute(
            text(
                """
                SELECT role, content FROM citizen_shield.chat_messages
                WHERE session_id = :session_id ORDER BY created_at
                """
            ),
            {"session_id": session_id},
        )
    ).mappings().all()
    return [dict(row) for row in rows]


async def _add_message(db: AsyncSession, session_id: UUID, role: str, content: str) -> None:
    await db.execute(
        text(
            "INSERT INTO citizen_shield.chat_messages (session_id, role, content) VALUES (:session_id, :role, :content)"
        ),
        {"session_id": session_id, "role": role, "content": content},
    )


def _build_prompt(history: list[dict], latest_message: str) -> str:
    """Gemini's plain generate() call is stateless, so prior turns are folded into
    the prompt text rather than tracked via a chat-session object."""
    lines = [f"{turn['role']}: {turn['content']}" for turn in history]
    lines.append(f"user: {latest_message}")
    return "\n".join(lines)


async def _generate_reply(history: list[dict], latest_message: str) -> str:
    prompt = _build_prompt(history, latest_message)
    try:
        return await generate(prompt, system_instruction=CITIZEN_SHIELD_SYSTEM)
    except GeminiError:
        return (
            "I'm having trouble responding right now. If you're in immediate danger of "
            "losing money, hang up on any suspicious caller and call the National Cyber "
            "Crime Helpline 1930 or report at cybercrime.gov.in."
        )


async def start_chat_session(db: AsyncSession, user_id: UUID | None, first_message: str) -> dict:
    """Start a new Citizen Shield session with the citizen's first message."""
    language = detect_language(first_message)
    risk = assess_message_risk(first_message)
    status = "escalated" if risk == "high" else "active"

    session_row = (
        await db.execute(
            text(
                """
                INSERT INTO citizen_shield.chat_sessions (user_id, language, status, risk_assessment)
                VALUES (:user_id, :language, :status, :risk)
                RETURNING id, user_id, language, status, risk_assessment, created_at
                """
            ),
            {"user_id": user_id, "language": language, "status": status, "risk": risk},
        )
    ).mappings().first()
    session_id = session_row["id"]

    await _add_message(db, session_id, "user", first_message)
    reply = await _generate_reply([], first_message)
    await _add_message(db, session_id, "assistant", reply)
    await db.commit()

    return _to_jsonable({**dict(session_row), "reply": reply})


async def send_message(db: AsyncSession, session_id: UUID, message: str) -> dict:
    """Continue an existing Citizen Shield session with a new citizen message."""
    history = await _get_session_messages(db, session_id)
    risk = assess_message_risk(message)

    await _add_message(db, session_id, "user", message)
    reply = await _generate_reply(history, message)
    await _add_message(db, session_id, "assistant", reply)

    if risk == "high":
        await db.execute(
            text("UPDATE citizen_shield.chat_sessions SET status = 'escalated', risk_assessment = :risk WHERE id = :id"),
            {"risk": risk, "id": session_id},
        )
    await db.commit()

    return _to_jsonable({"session_id": str(session_id), "reply": reply, "risk_assessment": risk})


async def get_chat_history(db: AsyncSession, session_id: UUID) -> list[dict]:
    rows = (
        await db.execute(
            text(
                """
                SELECT id, role, content, created_at FROM citizen_shield.chat_messages
                WHERE session_id = :session_id ORDER BY created_at
                """
            ),
            {"session_id": session_id},
        )
    ).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


async def close_chat_session(db: AsyncSession, session_id: UUID) -> None:
    await db.execute(
        text("UPDATE citizen_shield.chat_sessions SET status = 'closed', ended_at = NOW() WHERE id = :id"),
        {"id": session_id},
    )
    await db.commit()
