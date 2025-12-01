from typing import Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sports_news")

@mcp.tool()
def get_player_news(player_name: str) -> List[Dict[str, str]]:
    """
    Get recent news headlines for a player.

    Args:
        player_name: Name of the player
    """
    return [
        {
            "headline": f"{player_name} shows promise in training camp",
            "source": "NFL Network",
            "date": "2024-08-15"
        },
        {
            "headline": f"Contract talks stall for {player_name}",
            "source": "ESPN",
            "date": "2024-07-20"
        }
    ]

@mcp.tool()
def get_team_news(team_name: str) -> List[Dict[str, str]]:
    """
    Get recent news for a team.

    Args:
        team_name: Name of the team
    """
    return [
        {
            "headline": f"{team_name} looking to trade up in draft",
            "source": "The Athletic",
            "date": "2024-04-10"
        }
    ]

@mcp.tool()
def get_injury_reports(week: int) -> Dict[str, List[str]]:
    """
    Get injury reports for a specific week.

    Args:
        week: Week number (1-18)
    """
    return {
        "KC": ["Patrick Mahomes (Ankle) - Probable"],
        "SF": ["Christian McCaffrey (Calf) - Questionable"]
    }

if __name__ == "__main__":
    mcp.run()
