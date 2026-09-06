"""add username to users

Revision ID: dc7990a7a304
Revises: c2f2d35bcad3
Create Date: 2026-09-06 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'dc7990a7a304'
down_revision: Union[str, Sequence[str], None] = 'c2f2d35bcad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _username_from_email(email: str) -> str:
    """Derive a safe username from an email local-part."""
    local = email.split("@", 1)[0].lower()
    cleaned = "".join(c for c in local if c.isalnum() or c == "_")
    cleaned = cleaned.strip("_")[:32]
    if len(cleaned) < 3:
        cleaned = "user_" + cleaned if cleaned else "user"
    return cleaned


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    # 1. Add username as nullable first so existing rows can be backfilled.
    op.add_column(
        "users", sa.Column("username", sa.String(length=32), nullable=True)
    )

    # 2. Backfill every existing row from its email local-part, de-duplicating
    #    collisions by appending a counter until the name is free.
    rows = conn.execute(
        text("SELECT id, email FROM users ORDER BY created_at")
    ).fetchall()
    used: set[str] = set()
    for user_id, email in rows:
        base = _username_from_email(email)
        candidate = base
        suffix = 2
        while candidate in used:
            candidate = f"{base[: 32 - len(str(suffix))]}{suffix}"
            suffix += 1
        used.add(candidate)
        conn.execute(
            text("UPDATE users SET username = :username WHERE id = :id"),
            {"username": candidate, "id": user_id},
        )

    # 3. Now enforce NOT NULL and uniqueness.
    op.alter_column("users", "username", nullable=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_column("users", "username")
