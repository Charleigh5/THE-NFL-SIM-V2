from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime

from app.models.weekly_recap import WeeklyRecap
from app.models.rpg_event import RPGEvent
from app.models.news_item import NewsItem
from app.engine.event_bus import EventType

def mock_gemini_recap_script(week: int, events: List[RPGEvent], top_news: List[NewsItem]) -> str:
    lines = [f"# Week {week} Around the League", ""]

    if top_news:
        lines.append("## Top Stories")
        for news in top_news:
             lines.append(f"**{news.headline}**: {news.content[:100]}...")
        lines.append("")

    lines.append("## Action Report")
    lines.append(f"A total of {len(events)} major events were recorded this week.")

    return "\n".join(lines)

class WeeklyRecapService:
    """
    Orchestrates the 'End of Week' logic to generate the Weekly Wrap-Up Show content.
    """

    def generate_recap(self, db: Session, season_id: int, week: int) -> WeeklyRecap:
        # Check if exists
        existing = self.get_recap(db, season_id, week)
        if existing:
            return existing

        # 1. Fetch all RPG events for the week
        events = db.query(RPGEvent).filter_by(season_id=season_id, week=week).all()

        # 2. Identify top stories (using NewsItems created by NewsFeedService)
        top_news = db.query(NewsItem).filter_by(season_id=season_id, week=week)\
                     .order_by(NewsItem.importance_score.desc()).limit(5).all()

        # 3. Calculate "Play of the Week" (e.g. longest TD or Game Winning Play)
        best_play_id = None
        max_excitement = 0
        surprising_result = "No major upsets."

        for e in events:
            # Simple heuristic: Longest play that scored
            if e.event_type == EventType.TOUCHDOWN_EVENT:
                yards = e.payload.get("yards", 0)
                if yards > max_excitement:
                     max_excitement = yards
                     # Format: GAMEID_PLAYID
                     best_play_id = f"{e.game_id}_{e.payload.get('play_id')}"

        # 4. Generate AI Script (Simulated)
        summary = mock_gemini_recap_script(week, events, top_news)

        # 5. Persist
        recap = WeeklyRecap(
            season_id=season_id,
            week=week,
            summary_text=summary,
            play_of_the_week_id=best_play_id,
            surprising_result=surprising_result,
            media_assets=[]
        )
        db.add(recap)
        db.commit()
        db.refresh(recap)
        return recap

    def get_recap(self, db: Session, season_id: int, week: int) -> Optional[WeeklyRecap]:
        return db.query(WeeklyRecap).filter_by(season_id=season_id, week=week).first()

weekly_recap_service = WeeklyRecapService()
