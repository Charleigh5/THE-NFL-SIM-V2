"""expand_draft_pick_trade_ledger

Revision ID: e4f5a6b7c8d9
Revises: da6e871020ca
Create Date: 2026-10-24 14:32:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e4f5a6b7c8d9'
down_revision: Union[str, Sequence[str], None] = 'da6e871020ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade draft_pick table to support future picks and conditional assets."""
    with op.batch_alter_table('draft_pick', schema=None) as batch_op:
        batch_op.add_column(sa.Column('year', sa.Integer(), nullable=False, server_default='2025'))
        batch_op.add_column(sa.Column('is_compensatory', sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column('conditions', sa.JSON(), nullable=True))
        batch_op.alter_column('season_id', existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column('pick_number', existing_type=sa.Integer(), nullable=True)
        batch_op.create_index(batch_op.f('ix_draft_pick_year'), ['year'], unique=False)


def downgrade() -> None:
    """Downgrade draft_pick table."""
    with op.batch_alter_table('draft_pick', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_draft_pick_year'))
        batch_op.alter_column('pick_number', existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column('season_id', existing_type=sa.Integer(), nullable=False)
        batch_op.drop_column('conditions')
        batch_op.drop_column('is_compensatory')
        batch_op.drop_column('year')
