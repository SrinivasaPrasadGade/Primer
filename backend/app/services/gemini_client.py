import asyncio
import logging
from typing import Any, Awaitable, Callable

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, ResourceExhausted

from app.config import settings

logger = logging.getLogger(__name__)

# gemini-2.5-flash was retired for new API keys and returns 404 "no longer available
# to new users" — which surfaced only as the generic fallback reply, never as a
# visible error. Verified against this project's key: gemini-flash-latest and
# gemini-3.5-flash both answer 503 "experiencing high demand", so this is the
# fastest model that actually completes. `python -m scripts.check_gemini` re-checks.
DEFAULT_MODEL = "gemini-3.1-flash-lite"
DEFAULT_TEMPERATURE = 0.3
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 1.5

# Per-attempt deadline. The SDK call runs in a worker thread and does not reliably
# time out on its own, so without this a stalled HTTPS connection blocks the awaiting
# request forever and the caller's spinner never resolves.
ATTEMPT_TIMEOUT_SECONDS = 20.0
# Ceiling across all attempts + backoff. Kept under the dashboard's 90s client-side
# abort so the API returns a real error rather than having the browser give up first.
TOTAL_TIMEOUT_SECONDS = 75.0

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
    """Run `call` in a worker thread, retrying transient API errors under a deadline.

    Every attempt is bounded by ATTEMPT_TIMEOUT_SECONDS and the whole loop by
    TOTAL_TIMEOUT_SECONDS. A timed-out attempt is treated as a retryable failure.

    Caveat: asyncio cannot cancel a thread, so a hung SDK call keeps occupying its
    worker until the process exits — but the request stops waiting on it, which is
    what turns an infinite spinner into an error the UI can show.
    """
    loop = asyncio.get_running_loop()
    deadline = loop.time() + TOTAL_TIMEOUT_SECONDS
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        remaining = deadline - loop.time()
        if remaining <= 0:
            break
        try:
            return await asyncio.wait_for(
                asyncio.to_thread(call), timeout=min(ATTEMPT_TIMEOUT_SECONDS, remaining)
            )
        except asyncio.TimeoutError as exc:
            last_error = exc
            logger.warning(
                "Gemini call timed out after %ss (attempt %s/%s)", ATTEMPT_TIMEOUT_SECONDS, attempt, MAX_RETRIES
            )
        except (ResourceExhausted, GoogleAPICallError) as exc:
            last_error = exc
            logger.warning("Gemini call failed (attempt %s/%s): %s", attempt, MAX_RETRIES, exc)

        backoff = RETRY_BACKOFF_SECONDS * attempt
        if attempt < MAX_RETRIES and loop.time() + backoff < deadline:
            await asyncio.sleep(backoff)

    raise GeminiError(f"Gemini API call failed or timed out after {MAX_RETRIES} attempts") from last_error


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


async def run_with_tools(
    prompt: str,
    tools: list[dict],
    execute_tool: Callable[[str, dict], Awaitable[Any]],
    *,
    system_instruction: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
    model_name: str = DEFAULT_MODEL,
    max_rounds: int = 4,
) -> dict:
    """Drive a Gemini function-calling loop to completion.

    Sends `prompt` to a chat session; whenever Gemini requests a function call,
    awaits `execute_tool(name, args)` and feeds the result back as a function
    response, repeating until Gemini returns a plain text answer or `max_rounds`
    is exhausted.

    Returns {"answer": str, "tool_calls": [{"name", "args", "result"}, ...]}.
    """
    model = _build_model(system_instruction, tools, model_name)
    generation_config = genai.types.GenerationConfig(temperature=temperature)
    chat = model.start_chat()
    tool_calls: list[dict] = []

    message: Any = prompt
    for _ in range(max_rounds):
        response = await _call_with_retries(
            lambda message=message: chat.send_message(message, generation_config=generation_config)
        )
        calls = extract_function_calls(response)
        if not calls:
            return {"answer": response.text, "tool_calls": tool_calls}

        response_parts = []
        for call in calls:
            result = await execute_tool(call["name"], call["args"])
            tool_calls.append({"name": call["name"], "args": call["args"], "result": result})
            response_parts.append(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=call["name"],
                        response={"result": result},
                    )
                )
            )
        message = response_parts

    return {
        "answer": "I gathered some data but couldn't finish forming an answer in time.",
        "tool_calls": tool_calls,
    }
