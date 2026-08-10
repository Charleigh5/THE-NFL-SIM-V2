"""Add preseason support columns

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-12-12

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b2c3d4e5f6g7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add preseason_weeks to season table (idempotent)
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Check season table columns
    season_columns = [col['name'] for col in inspector.get_columns('season')]
    if 'preseason_weeks' not in season_columns:
        op.add_column('season', sa.Column('preseason_weeks', sa.Integer(), nullable=True, server_default='3'))

    # Check game table columns
    game_columns = [col['name'] for col in inspector.get_columns('game')]
    if 'is_preseason' not in game_columns:
        op.add_column('game', sa.Column('is_preseason', sa.Boolean(), nullable=True, server_default='false'))


def downgrade() -> None:
    op.drop_column('game', 'is_preseason')
    op.drop_column('season', 'preseason_weeks')
