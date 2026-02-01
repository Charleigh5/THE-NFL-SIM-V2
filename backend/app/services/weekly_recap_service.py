from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.models.weekly_recap import WeeklyRecap
from app.models.rpg_event import RPGEvent
from app.models.news_item import NewsItem
from app.engine.event_bus import EventType

import logging

logger = logging.getLogger(__name__)

def mock_gemini_recap_script(week: int, events: List[RPGEvent], top_news: List[NewsItem]) -> str:
    lines = [f"# Week {week} Around the League", ""]

    lines.append("## Key Storylines")
    if top_news:
        for news in top_news[:3]:
            lines.append(f"- **{news.headline}**: {news.content[:100]}...")
    else:
        lines.append("No major storylines this week.")

    lines.append("")
    lines.append("## Big Plays")
    if events:
        for event in events[:5]:
            lines.append(f"- {event.event_type}: {event.description}")
    else:
        lines.append("A relatively quiet week on the field.")

    lines.append("")
    lines.append("## Playoff Implications")
    lines.append("As the season progresses, every game counts...")

    return "\n".join(lines)


class WeeklyRecapService:
    """
    Generates weekly recaps using LLM and game data.
    """

    def __init__(self, gemini_client=None):
        self.gemini = gemini_client

    async def generate_recap(self, season_id: int, week: int, db: Session) -> WeeklyRecap:
        """
        Generate or retrieve a weekly recap.
        """
        # Check if exists
        existing = db.query(WeeklyRecap).filter_by(season_id=season_id, week=week).first()
        if existing:
            return existing

        logger.info(f"Generating weekly recap for Season {season_id} Week {week}")

        # Gather data
        # 1. Top News
        top_news = db.query(NewsItem).filter_by(season_id=season_id, week=week)\
            .order_by(NewsItem.importance_score.desc()).limit(5).all()

        # 2. Key Events
        key_events = db.query(RPGEvent).filter(
            RPGEvent.season_id == season_id,
            RPGEvent.week == week,
            RPGEvent.event_type.in_([
                EventType.UPSET_WIN,
                EventType.BIG_GAME,
                EventType.INJURY_MAJOR
            ])
        ).limit(10).all()

        # 3. Generate Script
        script_content = ""
        if self.gemini:
            try:
                # LLM Generation (Future)
                pass
            except Exception as e:
                logger.error(f"Failed to generate recap with Gemini: {e}")

        if not script_content:
            script_content = mock_gemini_recap_script(week, key_events, top_news)

        # Create Recap
        recap = WeeklyRecap(
            season_id=season_id,
            week=week,
            title=f"Week {week} Recap",
            video_url=None, # Placeholder for generated video
            script_content=script_content,
            published_at=datetime.utcnow()
        )

        db.add(recap)
        db.commit()
        db.refresh(recap)

        return recap

    def get_recap(self, db: Session, season_id: int, week: int) -> Optional[WeeklyRecap]:
        return db.query(WeeklyRecap).filter_by(season_id=season_id, week=week).first()
