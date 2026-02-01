"""Add coach intelligence field

Revision ID: 8a4248fc8fd1
Revises: 870837d208c2
Create Date: 2025-12-11 00:39:07.287022

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8a4248fc8fd1'
down_revision: str | Sequence[str] | None = '870837d208c2'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add intelligence column to coach table."""
    with op.batch_alter_table('coach', schema=None) as batch_op:
        batch_op.add_column(sa.Column('intelligence', sa.Integer(), nullable=True, server_default='70'))


def downgrade() -> None:
    """Remove intelligence column from coach table."""
    with op.batch_alter_table('coach', schema=None) as batch_op:
        batch_op.drop_column('intelligence')
