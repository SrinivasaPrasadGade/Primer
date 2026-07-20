"""Check that the Gemini key works and that DEFAULT_MODEL is still served.

Every Gemini failure in this codebase degrades to a canned fallback reply, which is
the right behaviour for users but means an expired key or a retired model looks
identical to a working one from the UI. `gemini-2.5-flash` was retired for new API
keys and nothing surfaced it except a chat that quietly stopped being useful.

    python -m scripts.check_gemini            # key + configured model
    python -m scripts.check_gemini --list     # also list every usable model

Exit code is 0 only if the configured model actually returned text.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

from app.config import settings
from app.services.gemini_client import DEFAULT_MODEL

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
TIMEOUT = 60


def _get(path: str) -> dict:
    with urllib.request.urlopen(f"{API_ROOT}/{path}&key={settings.gemini_api_key}", timeout=TIMEOUT) as r:
        return json.loads(r.read())


def _error_detail(exc: urllib.error.HTTPError) -> str:
    try:
        return json.loads(exc.read()).get("error", {}).get("message", "")[:200]
    except Exception:
        return ""


def list_models() -> list[str]:
    data = _get("models?pageSize=200")
    return [
        m["name"].removeprefix("models/")
        for m in data.get("models", [])
        if "generateContent" in m.get("supportedGenerationMethods", [])
    ]


def try_model(model: str) -> tuple[bool, str]:
    url = f"{API_ROOT}/models/{model}:generateContent?key={settings.gemini_api_key}"
    body = json.dumps({"contents": [{"parts": [{"text": "Reply with exactly: OK"}]}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read())
        return True, data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code} {_error_detail(exc)}"
    except Exception as exc:
        return False, str(exc)


def main(show_list: bool) -> int:
    if not settings.gemini_api_key:
        print("GEMINI_API_KEY is empty.")
        print("  .env is read relative to app/config.py, so the repo-root .env is picked up")
        print("  from any working directory. Check the key is actually set there.")
        return 1
    print(f"key loaded ({len(settings.gemini_api_key)} chars)")

    try:
        usable = list_models()
    except urllib.error.HTTPError as exc:
        print(f"could not list models: HTTP {exc.code} {_error_detail(exc)}")
        print("  a 400/403 here usually means the key is invalid or restricted.")
        return 1
    print(f"{len(usable)} model(s) support generateContent")

    if show_list:
        for name in usable:
            print(f"    {name}")

    if DEFAULT_MODEL not in usable:
        print(f"\nDEFAULT_MODEL {DEFAULT_MODEL!r} is NOT in the usable list — it has been retired.")
        print("  Pick one from the list above and update DEFAULT_MODEL in app/services/gemini_client.py.")
        return 1

    ok, detail = try_model(DEFAULT_MODEL)
    if ok:
        print(f"\nDEFAULT_MODEL {DEFAULT_MODEL!r} responded: {detail!r}")
        return 0

    print(f"\nDEFAULT_MODEL {DEFAULT_MODEL!r} is listed but did not answer: {detail}")
    print("  503 = temporary capacity, retry later. 429 = quota. 404 = retired for this key.")
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print every usable model")
    args = parser.parse_args()
    sys.exit(main(args.list))
