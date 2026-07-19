"""Phone-number normalisation.

Every phone number in the database is stored E.164-style as ``+91XXXXXXXXXX`` (see
``seed_data/01_seed.sql``), but officers type numbers the way they appear in a
complaint: ``9876543210``, ``09876543210``, ``+91 98765 43210``, ``91-9876543210``.
An exact-match lookup on the raw input therefore misses a number that *is* in the
registry, and the caller reports it as having no records — a false clean verdict on
a known-fraud number. Normalise before every lookup.
"""

from __future__ import annotations

import re

DEFAULT_COUNTRY_CODE = "91"

_NON_DIGITS = re.compile(r"[^\d]")


def normalize_phone(value: str, country_code: str = DEFAULT_COUNTRY_CODE) -> str:
    """Return `value` as `+<cc><national number>`.

    Falls back to the stripped input when it doesn't look like a number we can
    place, so an unexpected format still gets an exact-match attempt rather than
    being mangled into something that matches the wrong record.
    """
    digits = _NON_DIGITS.sub("", value or "")
    if not digits:
        return (value or "").strip()

    # 0-prefixed trunk dialling: 09876543210 -> 9876543210
    digits = digits.lstrip("0")

    if digits.startswith(country_code) and len(digits) > 10:
        national = digits[len(country_code):]
    else:
        national = digits

    if len(national) != 10:
        # Not an Indian mobile-length number — don't guess.
        return value.strip()

    return f"+{country_code}{national}"
