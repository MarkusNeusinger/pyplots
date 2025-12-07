"""Initial schema with specs, libraries, and implementations

Revision ID: 001
Revises:
Create Date: 2025-12-07

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create specs table
    op.create_table(
        "specs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("data_requirements", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("optional_params", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create libraries table
    op.create_table(
        "libraries",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("documentation_url", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create implementations table
    op.create_table(
        "implementations",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("spec_id", sa.String(), nullable=False),
        sa.Column("library_id", sa.String(), nullable=False),
        sa.Column("plot_function", sa.String(), nullable=False),
        sa.Column("variant", sa.String(), nullable=False, server_default=sa.text("'default'")),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("preview_url", sa.String(), nullable=True),
        sa.Column("python_version", sa.String(), nullable=False, server_default=sa.text("'3.12+'")),
        sa.Column("tested", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["library_id"], ["libraries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["spec_id"], ["specs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("spec_id", "library_id", "variant", name="uq_implementation"),
    )

    # Create indexes
    op.create_index("idx_implementations_spec", "implementations", ["spec_id"])
    op.create_index("idx_implementations_library", "implementations", ["library_id"])

    # Seed libraries data
    op.execute("""
        INSERT INTO libraries (id, name, version, documentation_url) VALUES
        ('matplotlib', 'Matplotlib', '3.9.0', 'https://matplotlib.org'),
        ('seaborn', 'Seaborn', '0.13.0', 'https://seaborn.pydata.org'),
        ('plotly', 'Plotly', '5.18.0', 'https://plotly.com/python'),
        ('bokeh', 'Bokeh', '3.4.0', 'https://bokeh.org'),
        ('altair', 'Altair', '5.2.0', 'https://altair-viz.github.io'),
        ('plotnine', 'plotnine', '0.13.0', 'https://plotnine.readthedocs.io'),
        ('pygal', 'Pygal', '3.0.0', 'http://www.pygal.org'),
        ('highcharts', 'Highcharts', '1.10.0', 'https://www.highcharts.com'),
        ('letsplot', 'lets-plot', '4.5.0', 'https://lets-plot.org')
        ON CONFLICT (id) DO NOTHING;
    """)


def downgrade() -> None:
    op.drop_index("idx_implementations_library", table_name="implementations")
    op.drop_index("idx_implementations_spec", table_name="implementations")
    op.drop_table("implementations")
    op.drop_table("libraries")
    op.drop_table("specs")
