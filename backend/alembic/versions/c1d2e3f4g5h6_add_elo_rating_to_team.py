"""Add elo_rating column to Team table

Revision ID: c1d2e3f4g5h6
Revises: f153bd84a19f
Create Date: 2025-12-15

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c1d2e3f4g5h6'
down_revision: str | None = 'f153bd84a19f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add elo_rating column to team table with default of 1500."""
    op.add_column('team', sa.Column('elo_rating', sa.Float(), nullable=True, server_default='1500.0'))

    # Update existing rows to have the default value
    op.execute("UPDATE team SET elo_rating = 1500.0 WHERE elo_rating IS NULL")


def downgrade() -> None:
    """Remove elo_rating column from team table."""
    op.drop_column('team', 'elo_rating')
