from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
def get_game_weather(stadium_location: str, date_time: str) -> Dict[str, str]:
    """
    Get weather forecast or historical weather for a game.

    Args:
        stadium_location: City or Stadium name (e.g., "Green Bay", "Lambeau Field")
        date_time: ISO format date time string
    """
    # Mock logic for realism
    location = stadium_location.lower()
    is_winter = "12-" in date_time or "01-" in date_time

    if "green bay" in location or "lambeau" in location:
        if is_winter:
            return {
                "condition": "Snow",
                "temperature": "15 F",
                "wind": "15 mph NW",
                "precipitation": "Heavy Snow"
            }
        return {
            "condition": "Cloudy",
            "temperature": "45 F",
            "wind": "10 mph W",
            "precipitation": "None"
        }

    if "miami" in location or "hard rock" in location:
        return {
            "condition": "Sunny",
            "temperature": "82 F",
            "wind": "5 mph E",
            "precipitation": "None"
        }

    return {
        "condition": "Clear",
        "temperature": "65 F",
        "wind": "5 mph",
        "precipitation": "None"
    }

@mcp.tool()
def get_historical_conditions(location: str, date_range: str) -> str:
    """
    Get summary of historical weather conditions.

    Args:
        location: City name
        date_range: Range string (e.g., "2023-09-01 to 2023-12-31")
    """
    return f"Historical weather data for {location} during {date_range}: Average temp 55F, 3 days of rain."

if __name__ == "__main__":
    mcp.run()
