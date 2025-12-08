"""Add metadata fields for generation tracking and quality details

Revision ID: 002
Revises: 001
Create Date: 2025-12-08

Adds:
- specs.structured_tags (JSONB) - Structured tags from metadata/*.yaml
- implementations.generated_at (DateTime) - When code was generated
- implementations.generated_by (String) - Model ID that generated the code
- implementations.workflow_run (Integer) - GitHub Actions workflow run ID
- implementations.issue_number (Integer) - GitHub Issue number
- implementations.evaluator_scores (JSONB) - Individual evaluator scores
- implementations.quality_feedback (Text) - Quality evaluation feedback
- implementations.improvements_suggested (JSONB) - Suggested improvements
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add structured_tags to specs table
    op.add_column(
        "specs",
        sa.Column("structured_tags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )

    # Add generation metadata to implementations table
    op.add_column(
        "implementations",
        sa.Column("generated_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "implementations",
        sa.Column("generated_by", sa.String(), nullable=True),
    )
    op.add_column(
        "implementations",
        sa.Column("workflow_run", sa.Integer(), nullable=True),
    )
    op.add_column(
        "implementations",
        sa.Column("issue_number", sa.Integer(), nullable=True),
    )

    # Add quality evaluation details to implementations table
    op.add_column(
        "implementations",
        sa.Column("evaluator_scores", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column(
        "implementations",
        sa.Column("quality_feedback", sa.Text(), nullable=True),
    )
    op.add_column(
        "implementations",
        sa.Column("improvements_suggested", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    # Remove quality evaluation details from implementations
    op.drop_column("implementations", "improvements_suggested")
    op.drop_column("implementations", "quality_feedback")
    op.drop_column("implementations", "evaluator_scores")

    # Remove generation metadata from implementations
    op.drop_column("implementations", "issue_number")
    op.drop_column("implementations", "workflow_run")
    op.drop_column("implementations", "generated_by")
    op.drop_column("implementations", "generated_at")

    # Remove structured_tags from specs
    op.drop_column("specs", "structured_tags")
