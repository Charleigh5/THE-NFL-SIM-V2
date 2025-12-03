import pytest
from backend.mcp_servers.nfl_stats_server.server import get_player_career_stats, get_league_averages, get_team_historical_performance

def test_get_player_career_stats():
    result = get_player_career_stats("Patrick Mahomes")
    assert result["player"] == "Patrick Mahomes"
    assert "stats" in result
    assert result["stats"]["passing_yards"] == 4500

def test_get_league_averages():
    qb_stats = get_league_averages("QB")
    assert "passing_yards" in qb_stats
    assert qb_stats["passing_yards"] == 3500.0

    rb_stats = get_league_averages("RB")
    assert "rushing_yards" in rb_stats
    assert rb_stats["rushing_yards"] == 850.0

    unknown = get_league_averages("K")
    assert "message" in unknown

def test_get_team_historical_performance():
    result = get_team_historical_performance("KC")
    assert isinstance(result, list)
    assert len(result) >= 3
    assert result[0]["season"] == "2024"
    assert result[0]["record"] == "12-5"
