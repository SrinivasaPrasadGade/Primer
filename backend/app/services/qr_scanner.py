"""QR Scanner: QR content parsing, UPI/URL risk assessment.

Yashi's logic layer — Srinivas's routers call scan_qr_code() and never touch
persistence or the risk heuristics directly.
"""

from __future__ import annotations

import ipaddress
import json
from decimal import Decimal
import re
from urllib.parse import urlparse
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

DANGEROUS_RISK_SCORE = 70
CAUTION_RISK_SCORE = 30

# The MVP schema has no dedicated URL/domain fraud table (fraud_graph.entities has no
# 'url'/'domain' entity_type), so URL risk is a heuristic check rather than a live
# threat-intel lookup — consistent with the hackathon's data-model scope.
URL_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rebrand.ly"}
SUSPICIOUS_KEYWORDS = ["verify", "kyc", "suspended", "urgent", "block", "reward", "cashback", "prize"]
SUSPICIOUS_TLDS = {"tk", "ml", "ga", "cf", "gq", "xyz", "top", "work", "click"}
TRUSTED_DOMAINS = {
    "paytm.com", "phonepe.com", "google.com", "npci.org.in",
    "sbi.co.in", "hdfcbank.com", "icicibank.com",
}


def _to_jsonable(value):
    """Round-trip UUID/datetime/Decimal through JSON so they're plain str/float.

    Decimal must become a JSON number, not a string -- json.dumps(default=str) on its
    own stringifies Decimal, which silently breaks downstream numeric use (e.g. a
    Jinja "{:,.2f}".format(...) on a value that's now a str, or a risk_score/weight
    field that renders as "85" instead of 85 in an API response).
    """
    def _default(v):
        if isinstance(v, Decimal):
            return float(v)
        return str(v)

    return json.loads(json.dumps(value, default=_default))


def _is_ip_address(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _risk_level_for(risk_score: int) -> str:
    if risk_score >= DANGEROUS_RISK_SCORE:
        return "dangerous"
    if risk_score >= CAUTION_RISK_SCORE:
        return "caution"
    return "safe"


def _upi_flags(params: dict) -> list[str]:
    flags = []
    if not params.get("pn"):
        flags.append("missing_payee_name")
    amount = params.get("am")
    if amount:
        try:
            if float(amount) >= 50000:
                flags.append("large_amount")
        except ValueError:
            flags.append("malformed_amount")
    return flags


async def assess_upi_qr(db: AsyncSession, upi_string: str) -> dict:
    """Parse a UPI payment QR (upi://pay?pa=xyz@bank&pn=Name&am=1000) and check the
    payee UPI ID against the fraud graph."""
    query = upi_string.split("?", 1)[-1]
    params = dict(re.findall(r"(\w+)=([^&]+)", query))
    upi_id = params.get("pa", "")

    row = (
        await db.execute(
            text(
                """
                SELECT e.risk_score, COUNT(eg.id) AS connection_count
                FROM fraud_graph.entities e
                LEFT JOIN fraud_graph.edges eg ON eg.source_id = e.id OR eg.target_id = e.id
                WHERE e.entity_type = 'upi_id' AND e.entity_value = :upi
                GROUP BY e.id, e.risk_score
                """
            ),
            {"upi": upi_id},
        )
    ).mappings().first()

    risk_score = row["risk_score"] if row else 0
    complaint_count = row["connection_count"] if row else 0
    risk_level = _risk_level_for(risk_score)

    if risk_level == "dangerous":
        explanation = f"Known fraud account with {complaint_count} linked complaints"
    elif risk_level == "caution":
        explanation = "Some suspicious activity linked to this account"
    elif row:
        explanation = "No known issues with this account"
    else:
        explanation = "UPI ID not seen in the fraud graph"

    return {
        "content_type": "upi_payment",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "destination_account": upi_id,
        "destination_url": None,
        "complaint_count": complaint_count,
        "explanation": explanation,
        "flags": _upi_flags(params),
    }


def assess_url_qr(url: str) -> dict:
    """Heuristic domain-reputation check for a URL QR code."""
    parsed = urlparse(url)
    domain = (parsed.hostname or "").lower()

    if domain in TRUSTED_DOMAINS or any(domain.endswith(f".{trusted}") for trusted in TRUSTED_DOMAINS):
        return {
            "content_type": "url",
            "risk_level": "safe",
            "risk_score": 0,
            "destination_account": None,
            "destination_url": url,
            "complaint_count": 0,
            "explanation": f"{domain} is a recognised, trusted domain",
            "flags": [],
        }

    flags = []
    if _is_ip_address(domain):
        flags.append("ip_address_host")
    if domain in URL_SHORTENERS:
        flags.append("url_shortener")
    if parsed.scheme != "https":
        flags.append("no_https")
    tld = domain.rsplit(".", 1)[-1] if "." in domain else ""
    if tld in SUSPICIOUS_TLDS:
        flags.append("suspicious_tld")
    if any(keyword in url.lower() for keyword in SUSPICIOUS_KEYWORDS):
        flags.append("suspicious_keywords")

    risk_score = min(100, len(flags) * 25)
    explanation = f"Flagged: {', '.join(flags)}" if flags else f"No known risk indicators for {domain}"

    return {
        "content_type": "url",
        "risk_level": _risk_level_for(risk_score),
        "risk_score": risk_score,
        "destination_account": None,
        "destination_url": url,
        "complaint_count": 0,
        "explanation": explanation,
        "flags": flags,
    }


async def assess_qr_risk(db: AsyncSession, qr_content: str) -> dict:
    """Parse QR content, identify its type, and assess fraud risk."""
    content = (qr_content or "").strip()
    if content.startswith("upi://"):
        return await assess_upi_qr(db, content)
    if content.startswith("http://") or content.startswith("https://"):
        return assess_url_qr(content)
    return {
        "content_type": "text",
        "risk_level": "safe",
        "risk_score": 0,
        "destination_account": None,
        "destination_url": None,
        "complaint_count": 0,
        "explanation": "Plain text QR code — no payment or link destination",
        "flags": [],
    }


async def scan_qr_code(db: AsyncSession, qr_content: str, user_id: UUID | None = None) -> dict:
    """Assess a scanned QR code's risk and persist the result. Entry point for Srinivas's router."""
    assessment = await assess_qr_risk(db, qr_content)

    row = (
        await db.execute(
            text(
                """
                INSERT INTO qr_scans.scan_results
                    (user_id, qr_content, content_type, destination_account, destination_url,
                     risk_level, risk_score, complaint_count, explanation, flags)
                VALUES
                    (:user_id, :qr_content, :content_type, :destination_account, :destination_url,
                     :risk_level, :risk_score, :complaint_count, :explanation, CAST(:flags AS JSONB))
                RETURNING id, user_id, qr_content, content_type, destination_account, destination_url,
                          risk_level, risk_score, complaint_count, explanation, flags, scanned_at
                """
            ),
            {
                "user_id": user_id,
                "qr_content": qr_content,
                "content_type": assessment["content_type"],
                "destination_account": assessment["destination_account"],
                "destination_url": assessment["destination_url"],
                "risk_level": assessment["risk_level"],
                "risk_score": assessment["risk_score"],
                "complaint_count": assessment["complaint_count"],
                "explanation": assessment["explanation"],
                "flags": json.dumps(assessment["flags"]),
            },
        )
    ).mappings().first()
    await db.commit()
    return _to_jsonable(dict(row))
