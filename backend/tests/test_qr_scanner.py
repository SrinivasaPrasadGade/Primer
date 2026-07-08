"""Unit tests for app.services.qr_scanner — mocked AsyncSession, no live Postgres needed."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services import qr_scanner as svc


class FakeResult:
    def __init__(self, row=None):
        self._row = row

    def mappings(self):
        return self

    def first(self):
        return self._row


# ---------------------------------------------------------------------------
# assess_qr_risk — content-type dispatch
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_assess_qr_risk_plain_text():
    db = AsyncMock()
    result = await svc.assess_qr_risk(db, "just some plain text")
    assert result["content_type"] == "text"
    assert result["risk_level"] == "safe"
    db.execute.assert_not_called()


@pytest.mark.asyncio
async def test_assess_qr_risk_dispatches_upi(monkeypatch):
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    result = await svc.assess_qr_risk(db, "upi://pay?pa=scammer@ybl&pn=Test&am=100")
    assert result["content_type"] == "upi_payment"


@pytest.mark.asyncio
async def test_assess_qr_risk_dispatches_url():
    db = AsyncMock()
    result = await svc.assess_qr_risk(db, "https://paytm.com/pay")
    assert result["content_type"] == "url"


# ---------------------------------------------------------------------------
# UPI assessment
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_assess_upi_qr_dangerous():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"risk_score": 85, "connection_count": 12})
    result = await svc.assess_upi_qr(db, "upi://pay?pa=fraud@ybl&pn=Scammer&am=5000")
    assert result["risk_level"] == "dangerous"
    assert result["destination_account"] == "fraud@ybl"
    assert result["complaint_count"] == 12


@pytest.mark.asyncio
async def test_assess_upi_qr_caution():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"risk_score": 45, "connection_count": 2})
    result = await svc.assess_upi_qr(db, "upi://pay?pa=suspect@ybl&pn=Name&am=100")
    assert result["risk_level"] == "caution"


@pytest.mark.asyncio
async def test_assess_upi_qr_safe_known():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"risk_score": 0, "connection_count": 0})
    result = await svc.assess_upi_qr(db, "upi://pay?pa=merchant@ybl&pn=Shop&am=100")
    assert result["risk_level"] == "safe"
    assert result["explanation"] == "No known issues with this account"


@pytest.mark.asyncio
async def test_assess_upi_qr_unknown_not_in_graph():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    result = await svc.assess_upi_qr(db, "upi://pay?pa=random@ybl&pn=Someone&am=50")
    assert result["risk_level"] == "safe"
    assert result["explanation"] == "UPI ID not seen in the fraud graph"


@pytest.mark.asyncio
async def test_assess_upi_qr_flags_missing_payee_and_large_amount():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    result = await svc.assess_upi_qr(db, "upi://pay?pa=x@ybl&am=100000")
    assert "missing_payee_name" in result["flags"]
    assert "large_amount" in result["flags"]


# ---------------------------------------------------------------------------
# URL assessment
# ---------------------------------------------------------------------------

def test_assess_url_qr_trusted_domain():
    result = svc.assess_url_qr("https://paytm.com/pay?to=merchant")
    assert result["risk_level"] == "safe"
    assert result["flags"] == []


def test_assess_url_qr_trusted_subdomain():
    result = svc.assess_url_qr("https://pay.google.com/checkout")
    assert result["risk_level"] == "safe"


def test_assess_url_qr_suspicious_tld_and_keywords():
    result = svc.assess_url_qr("http://bank-kyc-verify.tk/urgent")
    assert "suspicious_tld" in result["flags"]
    assert "no_https" in result["flags"]
    assert "suspicious_keywords" in result["flags"]
    assert result["risk_level"] in ("caution", "dangerous")


def test_assess_url_qr_ip_address_host():
    result = svc.assess_url_qr("http://192.168.1.5/verify")
    assert "ip_address_host" in result["flags"]


def test_assess_url_qr_shortener():
    result = svc.assess_url_qr("https://bit.ly/abcd123")
    assert "url_shortener" in result["flags"]


def test_assess_url_qr_clean_unknown_domain():
    result = svc.assess_url_qr("https://example.com/page")
    assert result["risk_level"] == "safe"
    assert result["flags"] == []


# ---------------------------------------------------------------------------
# scan_qr_code — persistence
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_scan_qr_code_persists_and_returns_row():
    scan_id = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={
            "id": scan_id, "user_id": None, "qr_content": "https://example.com",
            "content_type": "url", "destination_account": None, "destination_url": "https://example.com",
            "risk_level": "safe", "risk_score": 0, "complaint_count": 0,
            "explanation": "No known risk indicators for example.com", "flags": [], "scanned_at": None,
        }
    )
    result = await svc.scan_qr_code(db, "https://example.com")
    assert result["id"] == str(scan_id)
    db.commit.assert_awaited_once()
