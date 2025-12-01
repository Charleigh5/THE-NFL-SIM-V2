from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("nfl_stats")

@mcp.tool()
def get_player_career_stats(player_name: str, start_year: int = 2020, end_year: int = 2024) -> Dict[str, str]:
    """
    Get career statistics for a specific player.

    Args:
        player_name: Name of the player (e.g., "Patrick Mahomes")
        start_year: Start year for stats (default: 2020)
        end_year: End year for stats (default: 2024)
    """
    # Mock data - in production this would call ESPN/NFL API
    return {
        "player": player_name,
        "period": f"{start_year}-{end_year}",
        "stats": {
            "games_played": 17,
            "passing_yards": 4500,
            "touchdowns": 35,
            "interceptions": 10,
            "completion_percentage": 67.5
        }
    }

@mcp.tool()
def get_league_averages(position: str, season: int = 2024) -> Dict[str, float]:
    """
    Get league average statistics for a specific position.

    Args:
        position: Player position (e.g., "QB", "WR")
        season: Season year
    """
    # Mock data
    if position == "QB":
        return {
            "passing_yards": 3500.0,
            "touchdowns": 22.5,
            "interceptions": 12.0
        }
    elif position == "RB":
        return {
            "rushing_yards": 850.0,
            "touchdowns": 7.5,
            "yards_per_carry": 4.2
        }
    return {"message": "No data for position"}

@mcp.tool()
def get_team_historical_performance(team_id: str, years: int = 5) -> List[Dict[str, str]]:
    """
    Get historical performance records for a team.

    Args:
        team_id: Team identifier (e.g., "KC", "SF")
        years: Number of years to look back
    """
    # Mock data
    return [
        {"season": "2024", "record": "12-5", "playoff_result": "Conference Championship"},
        {"season": "2023", "record": "11-6", "playoff_result": "Super Bowl Winner"},
        {"season": "2022", "record": "14-3", "playoff_result": "Super Bowl Winner"}
    ]

if __name__ == "__main__":
    mcp.run()
