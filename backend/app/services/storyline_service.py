"""
StorylineEventService - Multi-Week Narrative Arcs

This service tracks developing storylines across multiple weeks.
It detects patterns in events and creates ongoing narratives.

Examples:
- QB Controversy: Backup outperforms starter for 2+ weeks
- Hot Streak: Team wins 5+ games in a row
- Rivalry Renewed: Same teams meet in playoffs after close regular season game
- Redemption Arc: Player returns from injury to make big plays
"""
from enum import Enum

from sqlalchemy.orm import Session

from app.engine.event_bus import EventType
from app.models.news_item import NewsCategory, NewsItem
from app.models.rpg_event import RPGEvent


class StorylineType(str, Enum):
    QB_CONTROVERSY = "QB_CONTROVERSY"
    HOT_STREAK = "HOT_STREAK"
    COLD_STREAK = "COLD_STREAK"
    RIVALRY = "RIVALRY"
    REDEMPTION_ARC = "REDEMPTION_ARC"
    BREAKOUT_PLAYER = "BREAKOUT_PLAYER"
    DECLINE = "DECLINE"
    TRADE_AFTERMATH = "TRADE_AFTERMATH"


class Storyline:
    """Represents an active storyline being tracked."""
    def __init__(self, storyline_type: StorylineType, team_id: int | None = None,
                 player_id: int | None = None, start_week: int = 1):
        self.storyline_type = storyline_type
        self.team_id = team_id
        self.player_id = player_id
        self.start_week = start_week
        self.intensity = 1  # 1-5 scale, increases as storyline develops
        self.events: list[RPGEvent] = []

    def to_dict(self) -> dict:
        return {
            "type": self.storyline_type.value,
            "team_id": self.team_id,
            "player_id": self.player_id,
            "start_week": self.start_week,
            "intensity": self.intensity,
            "event_count": len(self.events)
        }


class StorylineEventService:
    """
    Tracks and manages multi-week storylines.
    """

    def __init__(self):
        # In-memory cache of active storylines (would be persisted in production)
        self._active_storylines: dict[str, Storyline] = {}

    def check_for_storyline_triggers(self, db: Session, team_id: int,
                                      season_id: int, week: int) -> list[Storyline]:
        """
        Check if any new storylines should be created or existing ones updated.

        Args:
            db: Database session
            team_id: Team to analyze
            season_id: Current season
            week: Current week

        Returns:
            List of active/new storylines for this team
        """
        triggered = []

        # Get recent events for this team
        recent_events = db.query(RPGEvent).filter(
            RPGEvent.team_id == team_id,
            RPGEvent.season_id == season_id,
            RPGEvent.week >= max(1, week - 3)  # Last 3 weeks
        ).all()

        # Check for Hot Streak / Cold Streak
        streak_storyline = self._check_streak(team_id, season_id, week, recent_events)
        if streak_storyline:
            triggered.append(streak_storyline)

        # Check for Breakout Player
        breakout = self._check_breakout_player(db, team_id, season_id, week, recent_events)
        if breakout:
            triggered.append(breakout)

        return triggered

    def _check_streak(self, team_id: int, season_id: int, week: int,
                      events: list[RPGEvent]) -> Storyline | None:
        """Check if a team is on a hot or cold streak."""
        key = f"streak_{team_id}_{season_id}"

        # Count wins/losses from touchdown events (simplified)
        td_count = sum(1 for e in events if e.event_type == EventType.TOUCHDOWN_EVENT)
        turnover_count = sum(1 for e in events if e.event_type == EventType.TURNOVER_EVENT)

        if td_count >= 8:  # Lots of scoring
            if key not in self._active_storylines:
                storyline = Storyline(
                    storyline_type=StorylineType.HOT_STREAK,
                    team_id=team_id,
                    start_week=week
                )
                self._active_storylines[key] = storyline
            else:
                self._active_storylines[key].intensity = min(5, self._active_storylines[key].intensity + 1)

            return self._active_storylines[key]

        elif turnover_count >= 6:  # Lots of turnovers
            if key not in self._active_storylines:
                storyline = Storyline(
                    storyline_type=StorylineType.COLD_STREAK,
                    team_id=team_id,
                    start_week=week
                )
                self._active_storylines[key] = storyline
            else:
                self._active_storylines[key].intensity = min(5, self._active_storylines[key].intensity + 1)

            return self._active_storylines[key]

        return None

    def _check_breakout_player(self, db: Session, team_id: int, season_id: int,
                                week: int, events: list[RPGEvent]) -> Storyline | None:
        """Check if any player is having a breakout."""
        # Group events by player
        player_events: dict[int, int] = {}
        for event in events:
            if event.player_id and event.event_type == EventType.TOUCHDOWN_EVENT:
                player_events[event.player_id] = player_events.get(event.player_id, 0) + 1

        # Find players with multiple TDs
        for player_id, td_count in player_events.items():
            if td_count >= 3:
                key = f"breakout_{player_id}_{season_id}"
                if key not in self._active_storylines:
                    storyline = Storyline(
                        storyline_type=StorylineType.BREAKOUT_PLAYER,
                        team_id=team_id,
                        player_id=player_id,
                        start_week=week
                    )
                    self._active_storylines[key] = storyline
                    return storyline

        return None

    def get_active_storylines(self, team_id: int | None = None) -> list[dict]:
        """Get all active storylines, optionally filtered by team."""
        storylines = []
        for storyline in self._active_storylines.values():
            if team_id is None or storyline.team_id == team_id:
                storylines.append(storyline.to_dict())
        return storylines

    def generate_storyline_news(self, db: Session, storyline: Storyline,
                                 season_id: int, week: int) -> NewsItem:
        """Generate a news item for a storyline development."""
        headlines = {
            StorylineType.HOT_STREAK: "On Fire! Team Can't Be Stopped",
            StorylineType.COLD_STREAK: "Struggling: Team Needs Answers",
            StorylineType.BREAKOUT_PLAYER: "Star in the Making: Player Emerges",
            StorylineType.QB_CONTROVERSY: "QB Battle Heats Up",
            StorylineType.REDEMPTION_ARC: "Back and Better: Comeback Story"
        }

        headline = headlines.get(storyline.storyline_type, "Developing Story")
        content = f"A storyline of type {storyline.storyline_type.value} has reached intensity level {storyline.intensity}."

        news = NewsItem(
            season_id=season_id,
            week=week,
            team_id=storyline.team_id,
            player_id=storyline.player_id,
            category=NewsCategory.NARRATIVE,
            headline=headline,
            content=content,
            importance_score=0.3 + (storyline.intensity * 0.1)  # Higher intensity = more important
        )

        db.add(news)
        db.commit()

        return news


storyline_service = StorylineEventService()
