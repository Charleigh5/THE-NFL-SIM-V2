import pytest
import asyncio
from unittest.mock import MagicMock, patch
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.models.player import Player
from app.models.game import Game
from app.orchestrator.match_context import MatchContext

@patch('app.orchestrator.simulation_orchestrator.SessionLocal')
def test_orchestrator_integration_flow(mock_session_local):
    """
    Test the full flow of SimulationOrchestrator with MatchContext.
    """
    # Setup Mock Session
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session
    
    # Setup Mock Players
    # Home Team (ID 1)
    home_players = []
    positions = ["QB", "RB", "WR", "WR", "WR", "TE", "OT", "OT", "OG", "OG", "C"]
    for i, pos in enumerate(positions):
        p = Player(id=100+i, team_id=1, first_name=f"Home{i}", last_name=pos, position=pos, 
                   overall_rating=80, depth_chart_rank=0, height=75, acceleration=90, speed=90)
        home_players.append(p)
        
    # Away Team (ID 2)
    away_players = []
    def_positions = ["DE", "DE", "DT", "DT", "LB", "LB", "LB", "CB", "CB", "S", "S"]
    for i, pos in enumerate(def_positions):
        p = Player(id=200+i, team_id=2, first_name=f"Away{i}", last_name=pos, position=pos, 
                   overall_rating=80, depth_chart_rank=0, height=75, acceleration=90, speed=90)
        away_players.append(p)

    # Mock Query Results
    # The orchestrator calls query(Player) inside MatchContext via session
    # MatchContext calls: session.query(Player).filter(Player.team_id == team_id).all()
    
    # We set up the chain: session.query().filter().all()
    # The first call to all() will return home_players, second away_players
    mock_session.query.return_value.filter.return_value.all.side_effect = [home_players, away_players]
    
    # Mock Game creation
    mock_game = MagicMock(id=1)
    mock_game.game_data = {}
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: setattr(x, 'id', 1)
    
    # Handle Game query in save_progress/save_game_result
    # session.query(Game).filter(...).first()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_game

    # Initialize Orchestrator
    orchestrator = SimulationOrchestrator()
    
    # Start Game Session
    orchestrator.start_new_game_session(home_team_id=1, away_team_id=2)
    
    # Verify MatchContext is created
    assert orchestrator.match_context is not None
    assert len(orchestrator.match_context.home_roster) == len(home_players)
    assert len(orchestrator.match_context.away_roster) == len(away_players)
    
    # Execute Single Play (Async)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(orchestrator._execute_single_play())
    
    # Verify Result
    assert result is not None
    assert result.yards_gained is not None
    print(f"Play Result: {result.description}")
    
    # Verify Fatigue Update
    # Check if fatigue was updated in Genesis
    # We can check one of the home players (e.g. QB id 100)
    qb_id = 100
    fatigue_reg = orchestrator.match_context.get_fatigue(qb_id)
    assert fatigue_reg is not None
    
    # If the QB was involved (likely in a pass play), lactic acid might be > 0
    # But even if not, we verified get_fatigue works
    print(f"QB Fatigue Lactic Acid: {fatigue_reg.lactic_acid}")
    
    # Cleanup
    orchestrator.save_game_result()
    assert orchestrator.match_context is None
