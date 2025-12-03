"""
Integration test for OL Unit Chemistry feature.
Validates that OL gets blocking bonuses after starting together for 5+ consecutive games.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.team import Team
from app.models.player import Player, Position
from app.models.game import Game
from app.models.stats import PlayerGameStart
from app.services.pre_game_service import PreGameService
from app.orchestrator.match_context import MatchContext
from datetime import datetime


# Test database setup
@pytest.fixture
async def test_db():
    """Create an in-memory test database"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def setup_teams(test_db):
    """Create test teams and players"""
    # Create teams
    team1 = Team(id=1, name="Test Team 1", city="City1", abbreviation="TT1")
    team2 = Team(id=2, name="Test Team 2", city="City2", abbreviation="TT2")

    test_db.add(team1)
    test_db.add(team2)

    # Create OL players for team 1
    ol_positions = ["LT", "LG", "C", "RG", "RT"]
    ol_players = []

    for i, pos in enumerate(ol_positions):
        player = Player(
            id=i + 1,
            first_name=f"Player",
            last_name=f"{pos}",
            position=pos,
            team_id=1,
            overall_rating=75,
            pass_block=70,
            run_block=70,
            awareness=65
        )
        ol_players.append(player)
        test_db.add(player)

    # Create some other players for team 2
    for i in range(5):
        player = Player(
            id=i + 10,
            first_name=f"Opponent",
            last_name=f"{i}",
            position="DE",
            team_id=2,
            overall_rating=70
        )
        test_db.add(player)

    await test_db.commit()

    return {
        'team1': team1,
        'team2': team2,
        'ol_players': ol_players
    }


async def create_game_with_starts(test_db, game_id, week, ol_player_ids):
    """Helper to create a game and record OL starts"""
    game = Game(
        id=game_id,
        home_team_id=1,
        away_team_id=2,
        season_id=1,
        week=week,
        season=2025,
        date=datetime.utcnow(),
        is_played=True
    )
    test_db.add(game)

    # Record starts
    ol_positions = ["LT", "LG", "C", "RG", "RT"]
    for pos, player_id in zip(ol_positions, ol_player_ids):
        start = PlayerGameStart(
            player_id=player_id,
            game_id=game_id,
            team_id=1,
            season_id=1,
            week=week,
            position=pos
        )
        test_db.add(start)

    await test_db.commit()


@pytest.mark.asyncio
async def test_ol_chemistry_bonus_after_5_games(test_db, setup_teams):
    """
    Test that OL players get chemistry bonus after starting 5 consecutive games together
    """
    ol_players = setup_teams['ol_players']
    ol_player_ids = [p.id for p in ol_players]  # [1, 2, 3, 4, 5]

    # Create 5 games where same OL started together
    for i in range(1, 6):
        await create_game_with_starts(test_db, game_id=i, week=i, ol_player_ids=ol_player_ids)

    # Create match context
    match_context = MatchContext(
        home_team_id=1,
        away_team_id=2,
        db_session=test_db
    )

    # Load rosters
    await match_context.load_rosters()

    # Verify players loaded
    assert len(match_context.home_roster) == 5, "Should have 5 OL players"

    # Create PreGameService and apply chemistry
    pre_game_service = PreGameService(test_db)
    await pre_game_service.apply_chemistry_boosts(match_context)

    # Verify chemistry bonuses were applied
    for player_id, player in match_context.home_roster.items():
        assert hasattr(player, 'active_modifiers'), f"Player {player_id} should have active_modifiers"

        # Check for chemistry bonuses
        assert 'pass_block' in player.active_modifiers, "Should have pass_block modifier"
        assert 'run_block' in player.active_modifiers, "Should have run_block modifier"
        assert 'awareness' in player.active_modifiers, "Should have awareness modifier"

        # Verify bonus values (+5 for 5 games)
        assert player.active_modifiers['pass_block'] == 5, f"Expected +5 pass_block, got {player.active_modifiers['pass_block']}"
        assert player.active_modifiers['run_block'] == 5, f"Expected +5 run_block, got {player.active_modifiers['run_block']}"
        assert player.active_modifiers['awareness'] == 5, f"Expected +5 awareness, got {player.active_modifiers['awareness']}"

    print("\n✅ OL Chemistry Test PASSED")
    print(f"   All 5 OL players received +5 blocking bonus after 5 consecutive starts")


@pytest.mark.asyncio
async def test_chemistry_resets_when_lineup_changes(test_db, setup_teams):
    """
    Test that chemistry bonus does NOT apply when OL lineup changes
    """
    ol_players = setup_teams['ol_players']

    # Create 4 games with one OL lineup
    original_ol = [1, 2, 3, 4, 5]
    for i in range(1, 5):
        await create_game_with_starts(test_db, game_id=i, week=i, ol_player_ids=original_ol)

    # Game 5: Change one OL player (broke the streak)
    changed_ol = [1, 2, 3, 4, 99]  # Different RT
    await create_game_with_starts(test_db, game_id=5, week=5, ol_player_ids=changed_ol)

    # Now try to apply chemistry with original lineup
    match_context = MatchContext(
        home_team_id=1,
        away_team_id=2,
        db_session=test_db
    )
    await match_context.load_rosters()

    pre_game_service = PreGameService(test_db)
    await pre_game_service.apply_chemistry_boosts(match_context)

    # Verify NO chemistry bonuses (streak was broken)
    for player_id, player in match_context.home_roster.items():
        # Either no active_modifiers or empty dict
        if hasattr(player, 'active_modifiers'):
            assert player.active_modifiers.get('pass_block', 0) == 0, \
                "Should NOT have chemistry bonus after lineup change"

    print("\n✅ Chemistry Reset Test PASSED")
    print(f"   No bonus applied when OL lineup changed")


@pytest.mark.asyncio
async def test_no_chemistry_with_less_than_5_games(test_db, setup_teams):
    """
    Test that chemistry bonus does NOT apply with less than 5 consecutive games
    """
    ol_players = setup_teams['ol_players']
    ol_player_ids = [p.id for p in ol_players]

# Create only 3 games
    for i in range(1, 4):
        await create_game_with_starts(test_db, game_id=i, week=i, ol_player_ids=ol_player_ids)

    match_context = MatchContext(
        home_team_id=1,
        away_team_id=2,
        db_session=test_db
    )
    await match_context.load_rosters()

    pre_game_service = PreGameService(test_db)
    await pre_game_service.apply_chemistry_boosts(match_context)

    # Verify NO chemistry bonuses (not enough games)
    for player_id, player in match_context.home_roster.items():
        if hasattr(player, 'active_modifiers'):
            assert player.active_modifiers.get('pass_block', 0) == 0, \
                "Should NOT have chemistry bonus with only 3 games"

    print("\n✅ Insufficient Games Test PASSED")
    print(f"   No bonus applied with only 3 consecutive starts")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
