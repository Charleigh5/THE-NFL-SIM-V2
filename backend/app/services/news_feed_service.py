from typing import Any

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.engine.event_bus import EventBus, EventType
from app.models.news_item import NewsCategory, NewsItem
from app.models.rpg_event import RPGEvent


# Simple "Gemini" placeholder for now, will replace with actual LLM call later
def mock_gemini_headline(event_type: str, payload: dict) -> str:
    player_name = "Unknown Player"
    if "player_id" in payload:
         # In real app, we'd fetch player name. Here we might guess or just use generic.
         player_name = f"Player {payload['player_id']}"

    if event_type == EventType.SACK_EVENT:
        return f"Defense dominates! {player_name} records a massive sack."
    elif event_type == EventType.TOUCHDOWN_EVENT:
        return f"Touchdown! {player_name} finds the endzone!"
    elif event_type == EventType.TURNOVER_EVENT:
        return f"Turnover! {player_name} coughs up the ball."
    return f"Update: {event_type.replace('_', ' ').title()}"

class NewsFeedService:
    """
    Service to manage the Living World news feed.
    Subscribes to EventBus to auto-generate news from RPG events.
    """

    def __init__(self):
        # Subscribe to key events
        # We can subscribe to ALL events and filter, or subscribe individually
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        # List of events that generate news
        news_worthy_events = [
            EventType.SACK_EVENT,
            EventType.TOUCHDOWN_EVENT,
            EventType.TURNOVER_EVENT,
            EventType.PLAYER_INJURED,
            EventType.TRADE_COMPLETED,
            EventType.COACH_HIRED,
            EventType.COACH_FIRED,
            # Add more as needed
        ]

        for event_type in news_worthy_events:
            EventBus.subscribe(event_type, self.handle_event)

    def handle_event(self, payload: dict[str, Any]):
        """
        Callback for EventBus. 
        Note: This runs in the context of the publisher (synchronous usually).
        We need to be careful about DB sessions here.
        """
        # We don't have the EventType here because current EventBus callback only passes payload (Dict).
        # We might need to change EventBus to pass (event_type, payload) OR include type in payload.
        # But wait, looking at EventBus in previous view, `subscribe` takes `event_type`.
        # So we know the type because we subscribed to it.
        # However, `handle_event` is a single method.
        # We need a wrapper or partial to know WHICH event triggered it.
        pass

    @staticmethod
    def process_event(event_type: str, payload: dict[str, Any], db: Session):
        """
        Core logic to turn an event into a NewsItem.
        """
        # 1. Create RPGEvent record (The Memory)
        rpg_event = RPGEvent(
            event_type=event_type,
            player_id=payload.get("player_id") or payload.get("sacker_id") or payload.get("scoring_player_id"),
            team_id=payload.get("team_id") or payload.get("scoring_team_id"),
            season_id=payload.get("season_id", 0),
            week=payload.get("week", 0),
            game_id=payload.get("game_id"),
            payload=payload,
            processed=False
        )
        db.add(rpg_event)
        db.flush() # Get ID

        # 2. Generate News (AI Step)
        # For MVP, we use templates/logic. Later, Gemini.
        headline = mock_gemini_headline(event_type, payload)
        content = f"Dateline NFL Sim: {headline} More details to follow as the situation develops."

        category = NewsCategory.GAME_RESULT
        if "INJURY" in event_type: category = NewsCategory.INJURY
        elif "TRADE" in event_type: category = NewsCategory.TRANSACTION

        news_item = NewsItem(
            season_id=payload.get("season_id", 0),
            week=payload.get("week", 0),
            team_id=rpg_event.team_id,
            player_id=rpg_event.player_id,
            category=category,
            headline=headline,
            content=content,
            importance_score=0.7 if "TOUCHDOWN" in event_type else 0.4
        )
        db.add(news_item)

        # Mark event as processed
        rpg_event.processed = True

        db.commit()

    def get_news(self, db: Session, season_id: int, week: int | None = None, limit: int = 20) -> list[NewsItem]:
        query = db.query(NewsItem).filter(NewsItem.season_id == season_id)
        if week:
            query = query.filter(NewsItem.week == week)
        return query.order_by(desc(NewsItem.created_at)).limit(limit).all()

# Global instance
news_feed_service = NewsFeedService()
