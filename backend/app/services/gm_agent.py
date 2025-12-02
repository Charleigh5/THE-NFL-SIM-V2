from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.team import Team
from app.core.mcp_registry import registry
from app.core.mcp_cache import mcp_cache

class GMAgent:
    def __init__(self, db: Session, team_id: int):
        self.db = db
        self.team_id = team_id
        self.team = db.get(Team, team_id)

    async def evaluate_trade(self, offered_players: list[int], requested_players: list[int]) -> Dict[str, Any]:
        """
        Evaluate a trade proposal using MCP for news and sentiment.
        """
        score = 0
        reasoning = []

        # 1. Basic Value Calculation (Placeholder)
        offered_value = len(offered_players) * 10
        requested_value = len(requested_players) * 10

        score = offered_value - requested_value

        # 2. Use MCP for Context
        news_client = registry.get_client("sports_news")
        if news_client:
            try:
                # Check news for offered players
                for pid in offered_players:
                    player = self.db.get(Player, pid)
                    if player:
                        # Check cache first
                        cache_key = f"player_news_{player.id}"
                        news = mcp_cache.get(cache_key, "player_news")

                        if not news:
                            news = await news_client.call_tool("get_player_news", arguments={"player_name": f"{player.first_name} {player.last_name}"})
                            if news:
                                mcp_cache.set(cache_key, news, "player_news")

                        if news and isinstance(news, list) and len(news) > 0:
                            # Simple sentiment analysis mock
                            latest = news[0]
                            if "injury" in latest.get("headline", "").lower():
                                score -= 20
                                reasoning.append(f"Concern about injury for {player.last_name}: {latest['headline']}")
                            else:
                                score += 5
                                reasoning.append(f"Positive buzz for {player.last_name}")
            except Exception as e:
                print(f"MCP Error in GMAgent: {e}")

        decision = "ACCEPT" if score >= 0 else "REJECT"

        return {
            "decision": decision,
            "score": score,
            "reasoning": "; ".join(reasoning) if reasoning else "Value based evaluation."
        }
