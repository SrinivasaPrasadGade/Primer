"""Unit tests for app.services.citizen_shield — mocked Gemini/AsyncSession, no live Postgres/Gemini needed."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services import citizen_shield as svc
from app.services.gemini_client import GeminiError


class FakeResult:
    def __init__(self, row=None, rows=None):
        self._row = row
        self._rows = rows or []

    def mappings(self):
        return self

    def first(self):
        return self._row

    def all(self):
        return self._rows


# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------

def test_detect_language_english():
    assert svc.detect_language("Someone is threatening me over the phone") == "en"


def test_detect_language_hindi():
    assert svc.detect_language("यह कॉल स्कैम है, मुझे डर लग रहा है") == "hi"


def test_detect_language_devanagari_variant_normalizes_to_hindi():
    # langdetect classifies this specific short phrase as Marathi ("mr"), a
    # Devanagari-script cousin of Hindi -- must still normalize to "hi".
    assert svc.detect_language("मुझे मदद चाहिए") == "hi"


def test_detect_language_empty_defaults_to_english():
    assert svc.detect_language("") == "en"


def test_detect_language_too_short_defaults_to_english():
    assert svc.detect_language("ok") == "en"


# ---------------------------------------------------------------------------
# Risk assessment
# ---------------------------------------------------------------------------

def test_assess_message_risk_high_already_paid():
    assert svc.assess_message_risk("I already paid them 50000 rupees, what do I do") == "high"


def test_assess_message_risk_high_shared_otp():
    assert svc.assess_message_risk("I shared my OTP with the caller") == "high"


def test_assess_message_risk_medium_scam_mention():
    assert svc.assess_message_risk("I think this is a scam call") == "medium"


def test_assess_message_risk_low_generic():
    assert svc.assess_message_risk("How do I update my address?") == "low"


def test_assess_message_risk_empty():
    assert svc.assess_message_risk("") == "low"


# ---------------------------------------------------------------------------
# _generate_reply — degrade gracefully on Gemini failure
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_generate_reply_success(monkeypatch):
    async def fake_generate(prompt, system_instruction=None):
        return "Hang up immediately and don't share any OTP."

    monkeypatch.setattr(svc, "generate", fake_generate)
    reply = await svc._generate_reply([], "Someone is asking for my OTP")
    assert "OTP" in reply


@pytest.mark.asyncio
async def test_generate_reply_gemini_error_degrades(monkeypatch):
    async def fake_generate(prompt, system_instruction=None):
        raise GeminiError("no API key")

    monkeypatch.setattr(svc, "generate", fake_generate)
    reply = await svc._generate_reply([], "help")
    assert "1930" in reply


def test_build_prompt_includes_history():
    history = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
    prompt = svc._build_prompt(history, "new message")
    assert "user: hi" in prompt
    assert "assistant: hello" in prompt
    assert "user: new message" in prompt


# ---------------------------------------------------------------------------
# start_chat_session
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_start_chat_session_normal(monkeypatch):
    async def fake_reply(history, latest_message):
        return "I understand, let's figure this out together."

    monkeypatch.setattr(svc, "_generate_reply", fake_reply)

    session_id = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={"id": session_id, "user_id": None, "language": "en", "status": "active",
             "risk_assessment": "low", "created_at": None}
    )

    result = await svc.start_chat_session(db, None, "How do I check if a number is a scam?")

    assert result["status"] == "active"
    assert "reply" in result
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_chat_session_high_risk_escalates(monkeypatch):
    async def fake_reply(history, latest_message):
        return "Please call 1930 immediately."

    monkeypatch.setattr(svc, "_generate_reply", fake_reply)

    session_id = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={"id": session_id, "user_id": None, "language": "en", "status": "escalated",
             "risk_assessment": "high", "created_at": None}
    )

    result = await svc.start_chat_session(db, None, "I already sent money to the scammer")

    assert result["status"] == "escalated"


# ---------------------------------------------------------------------------
# send_message
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_send_message_low_risk_no_escalation(monkeypatch):
    async def fake_get_messages(db, session_id):
        return [{"role": "user", "content": "hi"}]

    async def fake_reply(history, latest_message):
        return "Sure, I can help with that."

    monkeypatch.setattr(svc, "_get_session_messages", fake_get_messages)
    monkeypatch.setattr(svc, "_generate_reply", fake_reply)

    session_id = uuid4()
    db = AsyncMock()

    result = await svc.send_message(db, session_id, "What's the cybercrime helpline number?")

    assert result["risk_assessment"] == "low"
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_message_high_risk_escalates_session(monkeypatch):
    async def fake_get_messages(db, session_id):
        return []

    async def fake_reply(history, latest_message):
        return "Call your bank immediately."

    monkeypatch.setattr(svc, "_get_session_messages", fake_get_messages)
    monkeypatch.setattr(svc, "_generate_reply", fake_reply)

    session_id = uuid4()
    db = AsyncMock()

    result = await svc.send_message(db, session_id, "I gave my OTP and lost money")

    assert result["risk_assessment"] == "high"
    # Should have issued the escalation UPDATE in addition to the two message inserts.
    # TextClause's repr doesn't expose its SQL, so inspect the compiled statement text directly.
    update_calls = [
        c for c in db.execute.call_args_list
        if "UPDATE citizen_shield.chat_sessions" in str(c.args[0])
    ]
    assert len(update_calls) == 1
