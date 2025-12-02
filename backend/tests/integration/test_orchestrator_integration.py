import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.models.player import Player
from app.models.game import Game
from app.orchestrator.match_context import MatchContext
# from app.orchestrator.kernels.cortex_kernel import CortexKernel

@pytest.mark.asyncio
async def test_orchestrator_integration_flow():
    """
    Test the full flow of SimulationOrchestrator with MatchContext.
    """
    # Setup Mock Session
    mock_session = AsyncMock()

    # Setup Mock Players
    # Home Team (ID 1)
    home_players = []
    positions = ["QB", "RB", "WR", "WR", "WR", "TE", "OT", "OT", "OG", "OG", "C"]
    for i, pos in enumerate(positions):
        p = Player(id=100+i, team_id=1, first_name=f"Home{i}", last_name=pos, position=pos,
                   overall_rating=80, depth_chart_rank=0, height=75, acceleration=90, speed=90,
                   pass_block=70, run_block=70, strength=80, awareness=80, catching=80, route_running=80,
                   throw_power=80, throw_accuracy_short=80, throw_accuracy_mid=80, throw_accuracy_deep=80)
        home_players.append(p)

    # Away Team (ID 2)
    away_players = []
    def_positions = ["DE", "DE", "DT", "DT", "LB", "LB", "LB", "CB", "CB", "S", "S"]
    for i, pos in enumerate(def_positions):
        p = Player(id=200+i, team_id=2, first_name=f"Away{i}", last_name=pos, position=pos,
                   overall_rating=80, depth_chart_rank=0, height=75, acceleration=90, speed=90,
                   pass_rush_power=70, pass_rush_finesse=70, tackle=80, man_coverage=80, zone_coverage=80,
                   play_recognition=80, hit_power=80, strength=80)
        # Add pass_rush alias if needed by logic (PlayResolver uses pass_rush, Player model has pass_rush_power/finesse)
        # PlayResolver line 103: dl_rating = getattr(dl, "pass_rush", 70)
        # So we should set pass_rush attribute manually or update PlayResolver to use pass_rush_power
        p.pass_rush = 70
        away_players.append(p)

    # Mock Query Results for MatchContext.load_rosters
    # It calls execute twice: once for home, once for away
    mock_result_home = MagicMock()
    mock_result_home.scalars.return_value.all.return_value = home_players

    mock_result_away = MagicMock()
    mock_result_away.scalars.return_value.all.return_value = away_players

    mock_session.execute.side_effect = [mock_result_home, mock_result_away, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
    # Extra mocks for other calls (Game creation, etc.)

    # Mock Game creation
    mock_game = MagicMock(id=1)
    mock_game.game_data = {}
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: setattr(x, 'id', 1)

    # Initialize Orchestrator
    orchestrator = SimulationOrchestrator()

    # Start Game Session
    await orchestrator.start_new_game_session(home_team_id=1, away_team_id=2, db_session=mock_session)

    # Verify MatchContext is created
    assert orchestrator.match_context is not None
    assert len(orchestrator.match_context.home_roster) == len(home_players)
    assert len(orchestrator.match_context.away_roster) == len(away_players)

    # Test new environmental effects system
    weather_config = orchestrator.match_context.weather_config
    assert weather_config is not None
    assert weather_config["temperature"] == 70
    assert weather_config["condition"] == "Sunny"

    # Execute Single Play (Async)
    result = await orchestrator._execute_single_play()

    # Verify Result
    assert result is not None
    assert result.yards_gained is not None
    print(f"Play Result: {result.description}")

    # Verify Fatigue Update
    # Check if fatigue was updated
    qb_id = 100
    fatigue = orchestrator.match_context.get_player_fatigue(qb_id)
    assert isinstance(fatigue, float)
    print(f"QB Fatigue Level: {fatigue}")

    # Cleanup
    await orchestrator.save_game_result()
    assert orchestrator.match_context is None
