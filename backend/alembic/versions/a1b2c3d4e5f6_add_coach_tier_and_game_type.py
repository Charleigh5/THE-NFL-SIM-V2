"""Add coach tier and game_type columns

Revision ID: a1b2c3d4e5f6
Revises: 8a4248fc8fd1
Create Date: 2025-12-12

"""
import sqlalchemy as sa
from sqlalchemy import inspect

from alembic import op

# revision identifiers
revision = 'a1b2c3d4e5f6'
down_revision = '8a4248fc8fd1'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    """Check if a column exists in a table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    # SQLite compatible: Add columns only if they don't exist
    if not column_exists('coach', 'tier'):
        op.add_column('coach', sa.Column('tier', sa.String(length=20), nullable=True, server_default='DEVELOPING'))

    if not column_exists('game', 'game_type'):
        op.add_column('game', sa.Column('game_type', sa.String(length=20), nullable=True, server_default='REGULAR'))


def downgrade():
    if column_exists('coach', 'tier'):
        op.drop_column('coach', 'tier')
    if column_exists('game', 'game_type'):
        op.drop_column('game', 'game_type')
