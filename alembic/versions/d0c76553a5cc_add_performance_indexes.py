"""add_performance_indexes

Add indexes on frequently queried columns for better query performance:
- impls.spec_id (foreign key, heavily queried)
- impls.library_id (foreign key, heavily queried)
- specs.issue (lookup field)
- impls.quality_score (sorting/filtering)

Revision ID: d0c76553a5cc
Revises: c36d82383e1d
Create Date: 2025-12-28 21:00:41.803150

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d0c76553a5cc"
down_revision: Union[str, None] = "c36d82383e1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add performance indexes for frequently queried columns."""
    # Add index on impls.spec_id (foreign key lookup)
    op.create_index("ix_impls_spec_id", "impls", ["spec_id"], unique=False)

    # Add index on impls.library_id (foreign key lookup)
    op.create_index("ix_impls_library_id", "impls", ["library_id"], unique=False)

    # Add index on specs.issue (lookup by GitHub issue number)
    op.create_index("ix_specs_issue", "specs", ["issue"], unique=False)

    # Add index on impls.quality_score (sorting and filtering by quality)
    op.create_index("ix_impls_quality_score", "impls", ["quality_score"], unique=False)


def downgrade() -> None:
    """Remove performance indexes."""
    op.drop_index("ix_impls_quality_score", table_name="impls")
    op.drop_index("ix_specs_issue", table_name="specs")
    op.drop_index("ix_impls_library_id", table_name="impls")
    op.drop_index("ix_impls_spec_id", table_name="impls")
