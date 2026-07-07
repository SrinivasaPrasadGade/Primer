import asyncio
import logging
from typing import Any

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, ResourceExhausted

from app.config import settings

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.3
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 1.5

_configured = False


class GeminiError(RuntimeError):
    """Raised when a Gemini call fails after retries or the API key is missing."""


def _ensure_configured() -> None:
    global _configured
    if _configured:
        return
    if not settings.gemini_api_key:
        raise GeminiError("GEMINI_API_KEY is not set")
    genai.configure(api_key=settings.gemini_api_key)
    _configured = True


def _normalize_schema_types(node: Any) -> Any:
    """Upper-case JSON-Schema "type" values (e.g. "object" -> "OBJECT").

    google-generativeai expects Gemini's Type enum names, not lowercase
    JSON-Schema types — passing a conventional lowercase schema (as one
    would write for OpenAPI/OpenAI tools) raises a proto ValueError at
    model-build time otherwise. Lets callers write tool schemas the usual
    way without hitting that trap.
    """
    if isinstance(node, dict):
        return {
            key: (value.upper() if key == "type" and isinstance(value, str) else _normalize_schema_types(value))
            for key, value in node.items()
        }
    if isinstance(node, list):
        return [_normalize_schema_types(item) for item in node]
    return node


def _build_model(
    system_instruction: str | None,
    tools: list[dict] | None,
    model_name: str,
) -> genai.GenerativeModel:
    _ensure_configured()
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        tools=_normalize_schema_types(tools) if tools else None,
    )


async def _call_with_retries(call):
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return await asyncio.to_thread(call)
        except (ResourceExhausted, GoogleAPICallError) as exc:
            last_error = exc
            logger.warning("Gemini call failed (attempt %s/%s): %s", attempt, MAX_RETRIES, exc)
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_BACKOFF_SECONDS * attempt)
    raise GeminiError(f"Gemini API call failed after {MAX_RETRIES} attempts") from last_error


async def generate(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
    model_name: str = DEFAULT_MODEL,
) -> str:
    """Generate plain text from a prompt."""
    model = _build_model(system_instruction, tools=None, model_name=model_name)
    generation_config = genai.types.GenerationConfig(temperature=temperature)
    response = await _call_with_retries(
        lambda: model.generate_content(prompt, generation_config=generation_config)
    )
    return response.text


async def generate_json(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
    model_name: str = DEFAULT_MODEL,
) -> Any:
    """Generate content constrained to JSON output and parse it.

    Useful for structured-output features (e.g. case summaries) that need
    a JSON object back rather than free text.
    """
    import json

    model = _build_model(system_instruction, tools=None, model_name=model_name)
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        response_mime_type="application/json",
    )
    response = await _call_with_retries(
        lambda: model.generate_content(prompt, generation_config=generation_config)
    )
    return json.loads(response.text)


async def generate_with_tools(
    prompt: str,
    tools: list[dict],
    *,
    system_instruction: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
    model_name: str = DEFAULT_MODEL,
):
    """Generate content with function-calling tools available to Gemini.

    `tools` is a list of function-declaration dicts (name/description/parameters),
    e.g. the COPILOT_TOOLS schema. Returns the raw SDK response — use
    `extract_function_calls` to read out any function calls Gemini requested.
    """
    model = _build_model(system_instruction, tools=tools, model_name=model_name)
    generation_config = genai.types.GenerationConfig(temperature=temperature)
    return await _call_with_retries(
        lambda: model.generate_content(prompt, generation_config=generation_config)
    )


def extract_function_calls(response) -> list[dict]:
    """Pull {"name": ..., "args": {...}} out of a Gemini response's function-call parts."""
    calls = []
    for candidate in getattr(response, "candidates", None) or []:
        for part in candidate.content.parts:
            function_call = getattr(part, "function_call", None)
            if function_call and function_call.name:
                calls.append({"name": function_call.name, "args": dict(function_call.args)})
    return calls
