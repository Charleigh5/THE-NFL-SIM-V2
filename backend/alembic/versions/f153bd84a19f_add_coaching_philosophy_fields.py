"""Add coaching philosophy fields

Revision ID: f153bd84a19f
Revises: b2c3d4e5f6g7
Create Date: 2025-12-14 19:37:54.267392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = 'f153bd84a19f'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6g7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('coach', schema=None) as batch_op:
        batch_op.add_column(sa.Column('offensive_philosophy', sa.String(), server_default='BALANCED', nullable=True))
        batch_op.add_column(sa.Column('defensive_philosophy', sa.String(), server_default='MULTIPLE', nullable=True))
        batch_op.add_column(sa.Column('play_calling_tendency', sa.Integer(), server_default='50', nullable=True))
        batch_op.add_column(sa.Column('aggressiveness', sa.Integer(), server_default='50', nullable=True))
        batch_op.add_column(sa.Column('motivation_style', sa.String(), server_default='BALANCED', nullable=True))
        batch_op.add_column(sa.Column('discipline_enforcement', sa.Integer(), server_default='50', nullable=True))
        batch_op.add_column(sa.Column('practice_intensity', sa.Integer(), server_default='50', nullable=True))
        batch_op.add_column(sa.Column('development_focus', sa.String(), server_default='BALANCED', nullable=True))
        batch_op.add_column(sa.Column('roster_management', sa.String(), server_default='BALANCED', nullable=True))
        batch_op.add_column(sa.Column('clock_management', sa.Integer(), server_default='50', nullable=True))
        batch_op.add_column(sa.Column('challenge_success_rate', sa.Float(), server_default='0.5', nullable=True))

def downgrade() -> None:
    with op.batch_alter_table('coach', schema=None) as batch_op:
        batch_op.drop_column('challenge_success_rate')
        batch_op.drop_column('clock_management')
        batch_op.drop_column('roster_management')
        batch_op.drop_column('development_focus')
        batch_op.drop_column('practice_intensity')
        batch_op.drop_column('discipline_enforcement')
        batch_op.drop_column('motivation_style')
        batch_op.drop_column('aggressiveness')
        batch_op.drop_column('play_calling_tendency')
        batch_op.drop_column('defensive_philosophy')
        batch_op.drop_column('offensive_philosophy')
