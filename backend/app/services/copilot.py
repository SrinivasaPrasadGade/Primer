import json
import logging
from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import correlation as correlation_service
from app.services.gemini_client import GeminiError, run_with_tools

logger = logging.getLogger(__name__)

COPILOT_SYSTEM = """You are an AI investigation assistant for the Primer fraud intelligence
platform. Law enforcement officers ask you natural-language questions about fraud
complaints, phone numbers, bank accounts, UPI IDs, and fraud clusters.

Call the most relevant tool to look up real data before answering — never guess at
facts or invent figures. You may call more than one tool if the question requires it.
Once you have enough data, answer concisely and cite which entity or record it came
from. If no tool applies to the question, say so plainly instead of speculating."""

_ENTITY_TYPES = ["phone_number", "bank_account", "upi_id", "person", "device", "ip_address"]

COPILOT_TOOLS = [
    {
        "name": "search_entity",
        "description": (
            "Look up a single entity (phone number, bank account, UPI ID, person, device, "
            "or IP address) in the fraud graph and return its risk score and cluster."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": _ENTITY_TYPES},
                "entity_value": {
                    "type": "string",
                    "description": "The raw value, e.g. a phone number or UPI handle",
                },
            },
            "required": ["entity_type", "entity_value"],
        },
    },
    {
        "name": "get_entity_connections",
        "description": (
            "Get every entity directly connected to a given entity in the fraud graph "
            "(calls, transfers, shared devices, ownership, etc)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": _ENTITY_TYPES},
                "entity_value": {"type": "string"},
            },
            "required": ["entity_type", "entity_value"],
        },
    },
    {
        "name": "search_complaints_for_entity",
        "description": "Find fraud complaints linked to a given phone number, bank account, or UPI ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": ["phone_number", "bank_account", "upi_id"]},
                "entity_value": {"type": "string"},
            },
            "required": ["entity_type", "entity_value"],
        },
    },
    {
        "name": "get_cluster_loss",
        "description": (
            "Get the estimated total financial loss and victim count for the fraud cluster "
            "that a given entity belongs to."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": _ENTITY_TYPES},
                "entity_value": {"type": "string"},
            },
            "required": ["entity_type", "entity_value"],
        },
    },
    {
        "name": "check_number_reputation",
        "description": "Check a phone number's scam-sentinel reputation score, blacklist status, and flag count.",
        "parameters": {
            "type": "object",
            "properties": {
                "phone_number": {"type": "string"},
            },
            "required": ["phone_number"],
        },
    },
    {
        "name": "correlate_scam_session",
        "description": (
            "Given a scam session ID, correlate it across modules: the fraud-graph "
            "entities/cluster for its caller and callee numbers, and any geo-intel map "
            "incidents reported from that session."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "UUID of the scam_sentinel session"},
            },
            "required": ["session_id"],
        },
    },
]


def _jsonable(value: Any) -> Any:
    """Round-trip through JSON so UUID/datetime/Decimal become plain str/float.

    Needed because tool results are sent back to Gemini as a function-response
    payload, which only accepts JSON-scalar types.
    """
    return json.loads(json.dumps(value, default=str))


async def _find_entity(db: AsyncSession, entity_type: str, entity_value: str) -> dict | None:
    row = (
        await db.execute(
            text(
                """
                SELECT id, entity_type, entity_value, display_label, risk_score,
                       cluster_id, first_seen, last_seen
                FROM fraud_graph.entities
                WHERE entity_type = :entity_type AND entity_value = :entity_value
                """
            ),
            {"entity_type": entity_type, "entity_value": entity_value},
        )
    ).mappings().first()
    return dict(row) if row else None


async def search_entity(db: AsyncSession, entity_type: str, entity_value: str) -> dict:
    entity = await _find_entity(db, entity_type, entity_value)
    if not entity:
        return {"found": False, "entity_type": entity_type, "entity_value": entity_value}
    return {"found": True, **entity}


async def get_entity_connections(db: AsyncSession, entity_type: str, entity_value: str) -> dict:
    entity = await _find_entity(db, entity_type, entity_value)
    if not entity:
        return {"found": False, "entity_type": entity_type, "entity_value": entity_value, "connections": []}

    rows = (
        await db.execute(
            text(
                """
                SELECT e.relationship, e.weight, e.last_seen,
                       CASE WHEN e.source_id = :id THEN t.entity_type ELSE s.entity_type END AS entity_type,
                       CASE WHEN e.source_id = :id THEN t.entity_value ELSE s.entity_value END AS entity_value,
                       CASE WHEN e.source_id = :id THEN t.risk_score ELSE s.risk_score END AS risk_score
                FROM fraud_graph.edges e
                JOIN fraud_graph.entities s ON s.id = e.source_id
                JOIN fraud_graph.entities t ON t.id = e.target_id
                WHERE e.source_id = :id OR e.target_id = :id
                ORDER BY e.last_seen DESC
                LIMIT 25
                """
            ),
            {"id": entity["id"]},
        )
    ).mappings().all()
    return {
        "found": True,
        "entity": entity,
        "connection_count": len(rows),
        "connections": [dict(row) for row in rows],
    }


async def search_complaints_for_entity(db: AsyncSession, entity_type: str, entity_value: str) -> dict:
    entity = await _find_entity(db, entity_type, entity_value)
    if not entity:
        return {"found": False, "entity_type": entity_type, "entity_value": entity_value, "complaints": []}

    rows = (
        await db.execute(
            text(
                """
                SELECT c.id, c.entity_value AS complaint_ref, c.display_label,
                       c.properties, c.first_seen
                FROM fraud_graph.edges e
                JOIN fraud_graph.entities c
                    ON c.id = CASE WHEN e.source_id = :id THEN e.target_id ELSE e.source_id END
                WHERE (e.source_id = :id OR e.target_id = :id)
                  AND c.entity_type = 'complaint'
                ORDER BY c.first_seen DESC
                LIMIT 25
                """
            ),
            {"id": entity["id"]},
        )
    ).mappings().all()
    return {
        "found": True,
        "entity": entity,
        "complaint_count": len(rows),
        "complaints": [dict(row) for row in rows],
    }


async def get_cluster_loss(db: AsyncSession, entity_type: str, entity_value: str) -> dict:
    entity = await _find_entity(db, entity_type, entity_value)
    if not entity or not entity.get("cluster_id"):
        return {"found": False, "entity_type": entity_type, "entity_value": entity_value}

    row = (
        await db.execute(
            text(
                """
                SELECT id, name, node_count, edge_count, estimated_loss, victim_count, status
                FROM fraud_graph.clusters
                WHERE id = :cluster_id
                """
            ),
            {"cluster_id": entity["cluster_id"]},
        )
    ).mappings().first()
    if not row:
        return {"found": False, "entity_type": entity_type, "entity_value": entity_value}
    return {"found": True, "cluster": dict(row)}


async def check_number_reputation(db: AsyncSession, phone_number: str) -> dict:
    row = (
        await db.execute(
            text(
                """
                SELECT phone_number, risk_score, total_flags, total_complaints,
                       is_blacklisted, primary_scam_type, last_flagged
                FROM scam_sentinel.number_reputation
                WHERE phone_number = :phone_number
                """
            ),
            {"phone_number": phone_number},
        )
    ).mappings().first()
    if not row:
        return {"found": False, "phone_number": phone_number}
    return {"found": True, **dict(row)}


async def correlate_scam_session(db: AsyncSession, session_id: str) -> dict:
    return await correlation_service.correlate_scam_session(db, UUID(session_id))


TOOL_HANDLERS = {
    "search_entity": search_entity,
    "get_entity_connections": get_entity_connections,
    "search_complaints_for_entity": search_complaints_for_entity,
    "get_cluster_loss": get_cluster_loss,
    "check_number_reputation": check_number_reputation,
    "correlate_scam_session": correlate_scam_session,
}


async def process_query(db: AsyncSession, question: str) -> dict:
    """Process a natural-language officer question via Gemini function calling.

    Returns {answer, data, sources, query_executed} per the AI Copilot API contract.
    """

    async def execute_tool(name: str, args: dict) -> dict:
        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            return {"error": f"Unknown tool '{name}'"}
        try:
            result = await handler(db, **args)
        except Exception:
            logger.exception("Copilot tool '%s' failed (args=%s)", name, args)
            return {"error": f"Tool '{name}' failed to execute"}
        return _jsonable(result)

    try:
        result = await run_with_tools(
            question,
            COPILOT_TOOLS,
            execute_tool,
            system_instruction=COPILOT_SYSTEM,
        )
    except GeminiError as exc:
        logger.warning("Copilot query failed: %s", exc)
        return {
            "answer": "The AI Copilot is temporarily unavailable. Please try again shortly.",
            "data": [],
            "sources": [],
            "query_executed": [],
        }

    tool_calls = result["tool_calls"]
    return {
        "answer": result["answer"],
        "data": [call["result"] for call in tool_calls],
        "sources": [call["name"] for call in tool_calls] or ["gemini"],
        "query_executed": [{"tool": call["name"], "args": call["args"]} for call in tool_calls],
    }
