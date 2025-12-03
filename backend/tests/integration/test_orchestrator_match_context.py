import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.game import Game
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.orchestrator.match_context import MatchContext
from app.orchestrator.kernels.cortex_kernel import CortexKernel
from app.orchestrator.kernels.genesis_kernel import GenesisKernel

def create_full_team(session: Session, team_id: int):
    """
    Helper to create a full roster for a team to satisfy DepthChartService.
    """
    players = []

    # Offense
    positions = [
        ("QB", 2), ("RB", 3), ("WR", 5), ("TE", 3),
        ("OT", 4), ("OG", 4), ("C", 2)
    ]

    # Defense
    positions += [
        ("DE", 4), ("DT", 4), ("LB", 6), ("CB", 5), ("S", 4)
    ]

    # Special Teams
    positions += [("K", 1), ("P", 1)]

    pid_counter = team_id * 100

    for pos, count in positions:
        for i in range(count):
            pid_counter += 1
            p = Player(
                id=pid_counter,
                team_id=team_id,
                first_name=f"Player{pid_counter}",
                last_name=f"{pos}",
                position=pos,
                depth_chart_rank=i+1,
                overall_rating=80 - i,
                # Physical stats for fatigue calculation
                acceleration=80,
                height=72,
                weight=200,
                stamina=90,
                injury_status="ACTIVE"
            )
            players.append(p)
            session.add(p)

    session.commit()
    return players


@pytest.mark.asyncio
async def test_full_game_simulation_with_fatigue_mocked():
    from unittest.mock import AsyncMock, MagicMock
    from app.orchestrator.play_commands import RunPlayCommand

    # 1. Setup Mocks
    mock_db = AsyncMock()

    # Mock Players
    home_players = [
        Player(id=101, team_id=1, first_name="Home", last_name="QB", position="QB", overall_rating=90, speed=80, throw_power=90, throw_accuracy_short=90, throw_accuracy_mid=90, throw_accuracy_deep=90),
        Player(id=102, team_id=1, first_name="Home", last_name="RB", position="RB", overall_rating=85, speed=90, strength=80, agility=85)
    ]
    away_players = [
        Player(id=201, team_id=2, first_name="Away", last_name="DE", position="DE", overall_rating=85, speed=80, strength=85, tackle=85, pass_rush_power=85, hit_power=80)
    ]

    # Mock DB Execute Results for load_rosters
    mock_result_home = MagicMock()
    mock_result_home.scalars.return_value.all.return_value = home_players

    mock_result_away = MagicMock()
    mock_result_away.scalars.return_value.all.return_value = away_players

    mock_db.execute.side_effect = [mock_result_home, mock_result_away, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]

    # 2. Initialize Orchestrator
    orchestrator = SimulationOrchestrator()
    await orchestrator.start_new_game_session(home_team_id=1, away_team_id=2, db_session=mock_db)
    orchestrator.current_game_id = 1 # Manually set ID since mock DB doesn't generate it

    assert orchestrator.match_context is not None

    # Verify initial fatigue is 0
    initial_fatigue = orchestrator.match_context.get_player_fatigue(101)
    assert initial_fatigue == 0.0

    # 3. Simulate Plays
    orchestrator.play_caller = MagicMock()
    orchestrator.play_caller.select_play.return_value = RunPlayCommand(
        offense_players=[home_players[1]],
        defense_players=[away_players[0]],
        run_direction="middle"
    )

    num_plays = 5
    for i in range(num_plays):
        await orchestrator._execute_single_play()

    # 4. Verify Fatigue Accumulation
    # RB (102) should have fatigue
    rb_fatigue = orchestrator.match_context.get_player_fatigue(102)
    assert rb_fatigue > 0.0

    # 5. Save Game Result
    await orchestrator.save_game_result()

    assert orchestrator.match_context is None
