"""Add content and code fields, remove plot_function

Revision ID: 003
Revises: 002
Create Date: 2025-12-09

Adds:
- specs.content (Text) - Full markdown content from spec.md
- implementations.code (Text) - Python source code

Removes:
- implementations.plot_function (no longer needed with new structure)
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add content to specs table
    op.add_column(
        "specs",
        sa.Column("content", sa.Text(), nullable=True),
    )

    # Add code to implementations table
    op.add_column(
        "implementations",
        sa.Column("code", sa.Text(), nullable=True),
    )

    # Remove plot_function from implementations (no longer needed)
    op.drop_column("implementations", "plot_function")


def downgrade() -> None:
    # Add plot_function back
    op.add_column(
        "implementations",
        sa.Column("plot_function", sa.String(), nullable=False, server_default="unknown"),
    )

    # Remove code from implementations
    op.drop_column("implementations", "code")

    # Remove content from specs
    op.drop_column("specs", "content")
