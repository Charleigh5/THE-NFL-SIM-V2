"""add_composite_performance_indexes

Revision ID: 4a1b2c3d4e5f
Revises: 3dc5f2df700e
Create Date: 2025-11-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a1b2c3d4e5f'
down_revision: Union[str, Sequence[str], None] = '3dc5f2df700e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add composite indexes for better query performance."""
    # PlayerGameStats composite indexes for common query patterns
    op.create_index(
        'ix_playergamestats_player_game',
        'playergamestats',
        ['player_id', 'game_id'],
        unique=False
    )
    op.create_index(
        'ix_playergamestats_game_team',
        'playergamestats',
        ['game_id', 'team_id'],
        unique=False
    )
    
    # Game composite index for week simulation queries
    op.create_index(
        'ix_game_season_week_played',
        'game',
        ['season_id', 'week', 'is_played'],
        unique=False
    )
    
    # Game index for team matchup queries
    op.create_index(
        'ix_game_teams',
        'game',
        ['home_team_id', 'away_team_id'],
        unique=False
    )
    
    # Player composite index for roster queries
    op.create_index(
        'ix_player_team_position',
        'player',
        ['team_id', 'position'],
        unique=False
    )


def downgrade() -> None:
    """Remove composite indexes."""
    op.drop_index('ix_player_team_position', table_name='player')
    op.drop_index('ix_game_teams', table_name='game')
    op.drop_index('ix_game_season_week_played', table_name='game')
    op.drop_index('ix_playergamestats_game_team', table_name='playergamestats')
    op.drop_index('ix_playergamestats_player_game', table_name='playergamestats')