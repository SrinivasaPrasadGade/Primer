"""add scam_sessions.transcript_text + repair demo user password hashes

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-21

Two fixes that both only surface on a database that has already been migrated:

1. `scam_sentinel.scam_sessions` had nowhere to store a call transcript, but
   compute_signal_scores reads `transcript_text` off the session. It was always
   absent, so `script_similarity` and `urgency_phrases` — 35% of the scoring
   weight — scored 0.0 on every classification, and overall_confidence could not
   structurally reach AMBER (60) let alone RED (85).

2. Databases created from an early cut of 0001 hold placeholder password hashes
   (`$2b$12$demo_hash_yas`, 22 chars) rather than real bcrypt digests, so none of
   the three demo accounts can log in. 0001 is already stamped in
   `alembic_version`, so re-running migrations never repairs them.
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Same digests as the seed block in 0001 — all bcrypt for "Primer@2026".
DEMO_HASHES = {
    "yashi@primer.demo": "$2b$12$bCkzPbE9K9OjikpAT3Kzde03m8xpVeQ1NpK3k6Ewmwuv7DqLT0T7O",
    "srinivas@primer.demo": "$2b$12$mbTtMKweslk.4xrUFrqcEu2Cnv00qUDDRkAe4IU5HqA.IYXKHTQNe",
    "sumanth@primer.demo": "$2b$12$vsLv809.lvAc46JpXzgTMuOlQu0kVUdaxqtZ7RhbGoYXY8tn2yD5a",
}

# A bcrypt digest is always 60 characters. Restricting the repair to rows whose
# hash is a different length fixes the placeholders without overwriting a password
# someone has legitimately changed.
_REPAIR_SQL = "\n".join(
    f"""
    UPDATE core.users SET password_hash = '{h}'
    WHERE email = '{email}' AND length(password_hash) <> 60;
    """
    for email, h in DEMO_HASHES.items()
)

UPGRADE_SQL = f"""
ALTER TABLE scam_sentinel.scam_sessions ADD COLUMN IF NOT EXISTS transcript_text TEXT;
{_REPAIR_SQL}
"""

# Only the column is reversible. The hash repair is deliberately not undone: the
# placeholders it replaces were never usable, so restoring them has no value.
DOWNGRADE_SQL = """
ALTER TABLE scam_sentinel.scam_sessions DROP COLUMN IF EXISTS transcript_text;
"""


def upgrade() -> None:
    op.execute(UPGRADE_SQL)


def downgrade() -> None:
    op.execute(DOWNGRADE_SQL)
