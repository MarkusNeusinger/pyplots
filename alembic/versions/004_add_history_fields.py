"""Add history tracking fields

Revision ID: 004
Revises: 003
Create Date: 2025-12-09

Adds:
- specs.updates (JSONB) - Spec modification history
- implementations.history (JSONB) - Implementation version history
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add updates history to specs table
    op.add_column(
        "specs",
        sa.Column("updates", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )

    # Add version history to implementations table
    op.add_column(
        "implementations",
        sa.Column("history", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    # Remove history from implementations
    op.drop_column("implementations", "history")

    # Remove updates from specs
    op.drop_column("specs", "updates")
