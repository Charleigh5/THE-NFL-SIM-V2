import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.orchestrator.match_context import MatchContext
from app.models.player import Player

def test_match_context_initialization():
    # Mock Session
    mock_session = MagicMock(spec=Session)
    
    # Mock Players
    home_players = [
        Player(id=1, team_id=101, position="QB", depth_chart_rank=1, overall_rating=90, acceleration=80, height=75),
        Player(id=2, team_id=101, position="WR", depth_chart_rank=1, overall_rating=85, acceleration=90, height=72)
    ]
    away_players = [
        Player(id=3, team_id=102, position="CB", depth_chart_rank=1, overall_rating=88, acceleration=92, height=70)
    ]
    
    # Setup Mock Query Return
    # The MatchContext calls query(Player).filter(...).all() twice.
    # We need to simulate that.
    mock_query = MagicMock()
    mock_query.filter.return_value.all.side_effect = [home_players, away_players]
    mock_session.query.return_value = mock_query
    
    # Initialize MatchContext
    ctx = MatchContext(home_team_id=101, away_team_id=102, session=mock_session)
    
    # Assertions
    assert len(ctx.home_roster) == 2
    assert len(ctx.away_roster) == 1
    assert ctx.genesis is not None
    assert ctx.cortex is not None
    
    # Verify Genesis Registration
    assert 1 in ctx.genesis.player_states
    assert 2 in ctx.genesis.player_states
    assert 3 in ctx.genesis.player_states

def test_get_fielded_players():
    mock_session = MagicMock(spec=Session)
    
    # Create enough players for a formation
    # Offense: QB, RB, WR1, WR2, WR3, TE, LT, LG, C, RG, RT
    home_players = []
    positions = ["QB", "RB", "WR", "WR", "WR", "TE", "OT", "OG", "C", "OG", "OT"]
    for i, pos in enumerate(positions):
        home_players.append(Player(id=i+1, team_id=101, position=pos, depth_chart_rank=1, overall_rating=80))
        
    away_players = [Player(id=100, team_id=102, position="CB")] # Minimal away team
    
    mock_query = MagicMock()
    mock_query.filter.return_value.all.side_effect = [home_players, away_players]
    mock_session.query.return_value = mock_query
    
    ctx = MatchContext(home_team_id=101, away_team_id=102, session=mock_session)
    
    # Test Offense Formation
    fielded = ctx.get_fielded_players("home", "standard_offense")
    assert len(fielded) == 11
    
    # Verify we got the right positions (roughly)
    fielded_ids = [p.id for p in fielded]
    assert len(set(fielded_ids)) == 11 # Unique players

def test_load_roster_error():
    mock_session = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = [] # Empty roster
    mock_session.query.return_value = mock_query
    
    with pytest.raises(ValueError, match="No players found"):
        MatchContext(home_team_id=101, away_team_id=102, session=mock_session)
