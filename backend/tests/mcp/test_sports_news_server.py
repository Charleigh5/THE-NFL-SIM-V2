import pytest
from backend.mcp_servers.sports_news_server.server import get_player_news, get_team_news, get_injury_reports

def test_get_player_news():
    news = get_player_news("Patrick Mahomes")
    assert isinstance(news, list)
    assert len(news) > 0
    assert "Patrick Mahomes" in news[0]["headline"]

def test_get_team_news():
    news = get_team_news("Chiefs")
    assert isinstance(news, list)
    assert len(news) > 0
    assert "Chiefs" in news[0]["headline"]

def test_get_injury_reports():
    report = get_injury_reports(1)
    assert "KC" in report
    assert isinstance(report["KC"], list)
    assert "Patrick Mahomes" in report["KC"][0]
