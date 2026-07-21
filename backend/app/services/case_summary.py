"""Case Summarizer: evidence extraction + Gemini-powered structured case summaries.

Yashi's logic layer — Srinivas's routers call summarize_and_store() as the entry point.
"""

from __future__ import annotations

import json
from decimal import Decimal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import fraud_graph
from app.services.gemini_client import GeminiError, generate_json

SUMMARIZER_SYSTEM = """You are a forensic case analyst for the Primer fraud intelligence
platform. Given evidence gathered from fraud-graph entities, connections, and money-flow
records, produce a structured, evidence-grounded case summary. Never invent facts not
present in the evidence."""

SUMMARIZER_PROMPT_TEMPLATE = """Given the following evidence, generate a case summary with
exactly these JSON fields:
- summary: a 2-3 sentence executive summary
- timeline: array of {{"date": ISO-8601 string, "event": string}} objects, chronological
- suspects: array of {{"identifier": string, "type": string, "role": string, "risk_score": number}} objects
- related_complaints: array of complaint identifiers (strings)
- confidence_score: number 0-100 — how confident you are in this analysis given the evidence

Evidence:
{evidence}
"""


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


async def extract_evidence(db: AsyncSession, entity_type: str, entity_value: str) -> str:
    """Gather fraud-graph neighbourhood + money-flow evidence for an entity into text
    suitable for feeding to the summarizer prompt."""
    graph = await fraud_graph.get_entity_neighbourhood(db, entity_type, entity_value, depth=2)

    lines = [f"Entity: {entity_type} = {entity_value}", "", f"Connected entities ({len(graph['nodes'])}):"]
    for node in graph["nodes"]:
        lines.append(f"  - {node['entity_type']}: {node['entity_value']} (risk_score={node['risk_score']})")

    lines.append("")
    lines.append(f"Connections ({len(graph['edges'])}):")
    for edge in graph["edges"]:
        lines.append(
            f"  - {edge.get('source_label', edge['source_id'])} --[{edge['relationship']}]--> "
            f"{edge.get('target_label', edge['target_id'])} (weight={edge['weight']})"
        )

    if graph["nodes"]:
        # Money flow is scoped to the whole cluster, so any one member node's lookup covers it.
        money_flow = await fraud_graph.get_money_flow(db, UUID(graph["nodes"][0]["id"]))
        if money_flow:
            lines.append("")
            lines.append(f"Money flow ({len(money_flow)} transfers):")
            for flow in money_flow:
                lines.append(f"  - {flow['from_entity']} -> {flow['to_entity']}: {flow['amount']}")

    return "\n".join(lines)


async def generate_case_summary(evidence_text: str) -> dict:
    """Generate a structured case summary from evidence text using Gemini's JSON mode."""
    prompt = SUMMARIZER_PROMPT_TEMPLATE.format(evidence=evidence_text)
    try:
        return await generate_json(prompt, system_instruction=SUMMARIZER_SYSTEM)
    except (GeminiError, json.JSONDecodeError):
        # Degrade to a minimal, still-useful record rather than propagating an error
        # the router has no good way to handle mid-investigation.
        return {
            "summary": "Automatic summarization failed; evidence recorded for manual review.",
            "timeline": [],
            "suspects": [],
            "related_complaints": [],
            "confidence_score": 0,
        }


async def summarize_and_store(
    db: AsyncSession,
    entity_type: str,
    entity_value: str,
    generated_by: UUID,
    investigation_id: UUID | None = None,
) -> dict:
    """Entry point for Srinivas's routers: extract evidence, summarize via Gemini, persist."""
    evidence_text = await extract_evidence(db, entity_type, entity_value)
    summary = await generate_case_summary(evidence_text)

    row = (
        await db.execute(
            text(
                """
                INSERT INTO core.case_summaries
                    (investigation_id, summary_text, timeline_json, suspects_json,
                     related_complaints, confidence_score, source_evidence, generated_by)
                VALUES
                    (:investigation_id, :summary_text, CAST(:timeline AS JSONB), CAST(:suspects AS JSONB),
                     CAST(:related_complaints AS JSONB), :confidence_score, :source_evidence, :generated_by)
                RETURNING id, investigation_id, summary_text, timeline_json, suspects_json,
                          related_complaints, confidence_score, source_evidence, generated_by, created_at
                """
            ),
            {
                "investigation_id": investigation_id,
                "summary_text": summary.get("summary", ""),
                "timeline": json.dumps(summary.get("timeline", [])),
                "suspects": json.dumps(summary.get("suspects", [])),
                "related_complaints": json.dumps(summary.get("related_complaints", [])),
                "confidence_score": summary.get("confidence_score", 0),
                "source_evidence": [f"{entity_type}:{entity_value}"],
                "generated_by": str(generated_by),
            },
        )
    ).mappings().first()
    await db.commit()
    return _to_jsonable(dict(row))
