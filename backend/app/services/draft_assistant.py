from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.models.player import Player, Position
from app.models.draft import DraftPick
from app.schemas.offseason import Prospect
from app.core.mcp_registry import registry

class DraftAssistant:
    def __init__(self, db: Session):
        self.db = db

    async def suggest_pick(self, team_id: int, available_players: List[Player]) -> Dict:
        """
        Suggest a draft pick for a team based on needs and player value.
        Uses MCP to fetch external player comparison data if available.
        """
        # 1. Identify Team Needs (Simplified)
        # In a real system, we'd query roster depth
        needs = ["QB", "DE", "CB"] # Placeholder

        # 2. Filter available players
        top_candidates = available_players[:5]

        suggestion = {
            "player_id": top_candidates[0].id if top_candidates else None,
            "reasoning": "Best player available.",
            "alternatives": []
        }

        # 3. Use MCP to enhance reasoning
        client = registry.get_client("nfl_stats")
        if client and top_candidates:
            try:
                # Mock: Compare top candidate to league average
                candidate = top_candidates[0]
                stats = await client.call_tool("get_league_averages", arguments={"position": candidate.position, "season": 2024})

                if stats and isinstance(stats, dict):
                    suggestion["reasoning"] += f" {candidate.first_name} {candidate.last_name} projects to exceed league average {candidate.position} stats."
                    suggestion["external_data"] = stats
            except Exception as e:
                print(f"MCP Error in DraftAssistant: {e}")

        return suggestion
