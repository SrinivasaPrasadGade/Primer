"""Unit tests for app.services.phone — pure functions, no DB or Gemini needed.

These guard a safety-critical path: a normalisation miss makes a blacklisted number
look absent from the registry, which the Copilot then reports as a clean number.
"""

import pytest

from app.services.phone import normalize_phone

# +917861999412 is a seeded blacklisted number (seed_data/01_seed.sql). Every way an
# officer might transcribe it off a complaint must reach the same stored value.
SEEDED = "+917861999412"


@pytest.mark.parametrize(
    "raw",
    [
        "7861999412",          # bare national
        "07861999412",         # trunk-prefixed
        "+917861999412",       # already E.164
        "917861999412",        # country code, no plus
        "+91 78619 99412",     # spaced
        "91-7861999412",       # hyphenated
        "  7861999412  ",      # padded
        "(786) 199-9412",      # punctuated
    ],
)
def test_normalizes_every_transcription_to_the_stored_value(raw):
    assert normalize_phone(raw) == SEEDED


@pytest.mark.parametrize("raw", ["", "   ", "abc", "12345", "+1 415 555 0100"])
def test_passes_through_what_it_cannot_place(raw):
    """Unparseable or non-Indian input must not be coerced into a wrong match."""
    result = normalize_phone(raw)
    assert result == raw.strip()
    assert result != SEEDED


def test_is_idempotent():
    assert normalize_phone(normalize_phone("7861999412")) == SEEDED
