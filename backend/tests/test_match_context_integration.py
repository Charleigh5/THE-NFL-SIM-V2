import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.orchestrator.match_context import MatchContext
from app.orchestrator.play_resolver import PlayResolver
from app.models.player import Player
from app.orchestrator.play_commands import PassPlayCommand

def test_match_context_integration():
    """
    Verify that MatchContext correctly initializes from players,
    registers with the Kernel, and impacts play resolution (fatigue).
    """
    # Create Mock Players with Stats
    qb = Player(id=1, team_id=1, first_name="Test", last_name="QB", position="QB", 
                throw_accuracy_short=90, throw_accuracy_mid=85, throw_accuracy_deep=80,
                acceleration=80, height=75, overall_rating=85)
    
    wr = Player(id=2, team_id=1, first_name="Test", last_name="WR", position="WR", 
                speed=95, route_running=90, acceleration=95, height=72, overall_rating=90)
    
    cb = Player(id=3, team_id=2, first_name="Test", last_name="CB", position="CB", 
                speed=85, man_coverage=80, acceleration=90, height=70, overall_rating=82)
                
    home_roster = [qb, wr]
    away_roster = [cb]
    
    # Mock Session
    mock_session = MagicMock(spec=Session)
    mock_query = MagicMock()
    # The first call is for home team, second for away team
    mock_query.filter.return_value.all.side_effect = [home_roster, away_roster]
    mock_session.query.return_value = mock_query
    
    # Initialize MatchContext
    ctx = MatchContext(home_team_id=1, away_team_id=2, session=mock_session, weather_config={"temperature": 20, "condition": "Snow"})
    
    # Verify Initialization
    # Check Genesis state directly
    assert ctx.genesis.player_states[1]["anatomy"] is not None
    assert ctx.genesis.player_states[1]["fatigue"] is not None
    assert ctx.genesis.player_states[1]["fatigue"].home_climate == "Cold" # Temp 20 < 40
    
    # Initialize PlayResolver
    resolver = PlayResolver()
    resolver.register_players(ctx)
    
    assert resolver.current_match_context == ctx
    
    # Execute Play
    command = PassPlayCommand(
        offense_players=[qb, wr],
        defense_players=[cb],
        depth="deep"
    )
    
    result = resolver.resolve_play(command)
    
    # Verify Result Structure
    assert result is not None
    assert result.yards_gained >= 0
    
    # Verify Kernel State Update (Fatigue)
    # Access internal kernel state to verify update
    kernel_fatigue = resolver.kernels.genesis.player_states[1]["fatigue"].lactic_acid
    assert kernel_fatigue > 0.0
