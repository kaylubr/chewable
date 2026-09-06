"""oauth identities and nullable password hash

Revision ID: 699df6b3f8cb
Revises: dc7990a7a304
Create Date: 2026-09-06 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '699df6b3f8cb'
down_revision: Union[str, Sequence[str], None] = 'dc7990a7a304'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Social-only accounts have no password.
    op.alter_column("users", "password_hash", nullable=True)

    op.create_table(
        "oauth_identities",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider", "subject", name="uq_oauth_identities_provider_subject"),
    )
    op.create_index(op.f("ix_oauth_identities_user_id"), "oauth_identities", ["user_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_oauth_identities_user_id"), table_name="oauth_identities")
    op.drop_table("oauth_identities")
    op.alter_column("users", "password_hash", nullable=False)
