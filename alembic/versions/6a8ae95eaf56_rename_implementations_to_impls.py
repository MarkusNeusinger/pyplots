"""rename_implementations_to_impls

Revision ID: 6a8ae95eaf56
Revises: 393d66bd73d9
Create Date: 2025-12-12 21:23:53.707324

"""

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "6a8ae95eaf56"
down_revision: str = "393d66bd73d9"
branch_labels: None = None
depends_on: None = None


def upgrade() -> None:
    # Rename table from implementations to impls
    op.rename_table("implementations", "impls")

    # Rename constraint from uq_spec_library to uq_impl
    op.drop_constraint("uq_spec_library", "impls", type_="unique")
    op.create_unique_constraint("uq_impl", "impls", ["spec_id", "library_id"])


def downgrade() -> None:
    # Rename constraint back
    op.drop_constraint("uq_impl", "impls", type_="unique")
    op.create_unique_constraint("uq_spec_library", "impls", ["spec_id", "library_id"])

    # Rename table back to implementations
    op.rename_table("impls", "implementations")
