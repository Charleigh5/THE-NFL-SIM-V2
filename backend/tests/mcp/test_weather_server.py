import pytest
from backend.mcp_servers.weather_server.server import get_game_weather, get_historical_conditions

def test_get_game_weather_lambeau_winter():
    weather = get_game_weather("Lambeau Field", "2024-12-25T13:00:00")
    assert weather["condition"] == "Snow"
    assert weather["temperature"] == "15 F"

def test_get_game_weather_miami():
    weather = get_game_weather("Hard Rock Stadium", "2024-12-25T13:00:00")
    assert weather["condition"] == "Sunny"
    assert weather["temperature"] == "82 F"

def test_get_game_weather_default():
    weather = get_game_weather("Generic Stadium", "2024-09-10T13:00:00")
    assert weather["condition"] == "Clear"
    assert weather["temperature"] == "65 F"

def test_get_historical_conditions():
    summary = get_historical_conditions("Green Bay", "2023-09-01 to 2023-12-31")
    assert "Green Bay" in summary
    assert "Average temp" in summary
