"""add_season_id_to_playergamestats

Revision ID: 6e7b75fed3d6
Revises: 4a1b2c3d4e5f
Create Date: 2024-03-24 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e7b75fed3d6'
down_revision: Union[str, None] = '4a1b2c3d4e5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add season_id to player_game_stats
    try:
        with op.batch_alter_table('player_game_stats', schema=None) as batch_op:
            batch_op.add_column(sa.Column('season_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key('fk_player_game_stats_season_id', 'season', ['season_id'], ['id'])
    except Exception:
        pass

    # Add stadium_id to team
    try:
        with op.batch_alter_table('team', schema=None) as batch_op:
            batch_op.add_column(sa.Column('stadium_id', sa.Integer(), nullable=True))
            # DO NOT CREATE FK TO MISSING STADIUM TABLE
            # batch_op.create_foreign_key('fk_team_stadium_id', 'stadium', ['stadium_id'], ['id'])
    except Exception:
        pass


def downgrade() -> None:
    try:
        with op.batch_alter_table('team', schema=None) as batch_op:
            batch_op.drop_column('stadium_id')
    except Exception:
        pass

    try:
        with op.batch_alter_table('player_game_stats', schema=None) as batch_op:
            batch_op.drop_constraint('fk_player_game_stats_season_id', type_='foreignkey')
            batch_op.drop_column('season_id')
    except Exception:
        pass
