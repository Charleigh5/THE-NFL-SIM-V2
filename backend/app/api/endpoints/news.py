"""
News API Endpoints

Provides REST API for fetching league news, player news, and injury reports
from the MCP sports_news server.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel

router = APIRouter(prefix="/news", tags=["news"])
logger = logging.getLogger(__name__)


# ============================================================================
# SCHEMAS
# ============================================================================


class NewsItem(BaseModel):
    """Individual news item"""

    headline: str
    source: str
    date: str
    category: str = "general"
    team_id: int | None = None
    player_id: int | None = None
    is_breaking: bool = False


class NewsResponse(BaseModel):
    """News feed response"""

    items: list[NewsItem]
    total: int
    last_updated: str


class InjuryReport(BaseModel):
    """Injury report item"""

    team_abbreviation: str
    player_name: str
    status: str
    injury_type: str


class InjuryReportResponse(BaseModel):
    """Injury reports response"""

    week: int
    reports: dict[str, list[InjuryReport]]
    last_updated: str


# ============================================================================
# MOCK DATA GENERATOR
# ============================================================================


def _generate_mock_league_news() -> list[NewsItem]:
    """Generate simulated league news for immersion."""
    return [
        NewsItem(
            headline="Chiefs look to extend historic dynasty with 4th consecutive Super Bowl appearance",
            source="NFL Network",
            date="2024-12-04",
            category="league",
            is_breaking=False,
        ),
        NewsItem(
            headline="Trade deadline looming: Multiple teams seeking QB help before playoffs",
            source="ESPN",
            date="2024-12-03",
            category="trades",
            is_breaking=True,
        ),
        NewsItem(
            headline="Week 14 Power Rankings: Eagles surge to #1 after dominant win",
            source="The Athletic",
            date="2024-12-03",
            category="rankings",
            is_breaking=False,
        ),
        NewsItem(
            headline="Injury Report: Multiple stars questionable for crucial week 14 matchups",
            source="NFL Network",
            date="2024-12-02",
            category="injuries",
            is_breaking=False,
        ),
        NewsItem(
            headline="Rookie Watch: No. 1 pick already drawing MVP comparisons",
            source="PFF",
            date="2024-12-02",
            category="rookies",
            is_breaking=False,
        ),
        NewsItem(
            headline="Contract negotiations stall for Pro Bowl wide receiver seeking extension",
            source="Schefter",
            date="2024-12-01",
            category="contracts",
            is_breaking=True,
        ),
    ]


def _generate_mock_team_news(team_name: str) -> list[NewsItem]:
    """Generate simulated team-specific news."""
    return [
        NewsItem(
            headline=f"{team_name} looking to shore up offensive line depth before playoffs",
            source="Team Insider",
            date="2024-12-04",
            category="team",
            is_breaking=False,
        ),
        NewsItem(
            headline=f"Coaching staff impressed with {team_name}'s young defensive core",
            source="Local Beat",
            date="2024-12-03",
            category="team",
            is_breaking=False,
        ),
        NewsItem(
            headline=f"{team_name} fans react to controversial fourth-quarter playcall",
            source="Fan Nation",
            date="2024-12-02",
            category="team",
            is_breaking=False,
        ),
    ]


def _generate_mock_player_news(player_name: str) -> list[NewsItem]:
    """Generate simulated player-specific news."""
    return [
        NewsItem(
            headline=f"{player_name} named to Pro Bowl roster for the 3rd consecutive year",
            source="NFL Network",
            date="2024-12-04",
            category="player",
            is_breaking=False,
        ),
        NewsItem(
            headline=f"{player_name} discusses playoff preparation in exclusive interview",
            source="Team Media",
            date="2024-12-03",
            category="player",
            is_breaking=False,
        ),
    ]


def generate_rivalry_headline(
    team_a: str, team_b: str, score_diff: int, is_renewal: bool = True
) -> NewsItem:
    """
    NFL Identity Blueprint: Generate rivalry headlines for close games.

    Args:
        team_a: First team name
        team_b: Second team name
        score_diff: Absolute score difference
        is_renewal: Whether this is renewing an existing rivalry

    Returns:
        NewsItem with rivalry headline
    """
    if score_diff == 0:
        headline = f"INSTANT CLASSIC: {team_a} and {team_b} battle to OT thriller!"
    elif score_diff == 1:
        headline = f"ONE-POINT HEARTBREAKER: {team_a} edges {team_b} in nail-biter!"
    elif score_diff == 2:
        headline = f"SAFETY MARGIN: {team_a} holds off {team_b} by just 2 points!"
    elif score_diff == 3:
        headline = f"FIELD GOAL DECIDES IT: {team_a} survives {team_b} thriller!"
    else:
        headline = f"RIVALRY RENEWED: {team_a} vs {team_b} delivers another classic!"

    if is_renewal:
        headline = "RIVALRY RENEWED: " + headline.replace("RIVALRY RENEWED: ", "")

    return NewsItem(
        headline=headline,
        source="NFL Network",
        date=datetime.now().strftime("%Y-%m-%d"),
        category="rivalry",
        is_breaking=True,
    )


# ============================================================================
# ENDPOINTS
# ============================================================================


@router.get("/league", response_model=NewsResponse)
async def get_league_news(
    limit: int = Query(10, ge=1, le=50, description="Number of news items to return"),
    category: str | None = Query(None, description="Filter by category"),
):
    """
    Get latest league-wide news.

    Integrates with MCP sports_news server for dynamic content.
    Falls back to mock data for simulation immersion.
    """
    logger.info(f"Fetching league news (limit={limit}, category={category})")

    try:
        # TODO: Integrate with actual MCP sports_news server when available
        # For now, use mock data for simulation immersion
        news_items = _generate_mock_league_news()

        if category:
            news_items = [item for item in news_items if item.category == category]

        return NewsResponse(
            items=news_items[:limit], total=len(news_items), last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching league news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news")


@router.get("/team/{team_name}", response_model=NewsResponse)
async def get_team_news(
    team_name: str, limit: int = Query(5, ge=1, le=20, description="Number of news items to return")
):
    """
    Get news specific to a team.

    Args:
        team_name: Team name or abbreviation
        limit: Maximum number of items to return
    """
    logger.info(f"Fetching news for team: {team_name}")

    try:
        news_items = _generate_mock_team_news(team_name)

        return NewsResponse(
            items=news_items[:limit], total=len(news_items), last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching team news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch team news")


@router.get("/player/{player_name}", response_model=NewsResponse)
async def get_player_news(
    player_name: str,
    limit: int = Query(5, ge=1, le=20, description="Number of news items to return"),
):
    """
    Get news specific to a player.

    Args:
        player_name: Player's full name
        limit: Maximum number of items to return
    """
    logger.info(f"Fetching news for player: {player_name}")

    try:
        news_items = _generate_mock_player_news(player_name)

        return NewsResponse(
            items=news_items[:limit], total=len(news_items), last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching player news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch player news")


@router.get("/injuries/week/{week}", response_model=InjuryReportResponse)
async def get_injury_reports(week: int = Path(..., ge=1, le=18, description="NFL week number")):
    """
    Get injury reports for a specific week.

    Returns injury status for players across all teams.
    """
    logger.info(f"Fetching injury reports for week {week}")

    try:
        # Mock injury report data
        mock_reports = {
            "KC": [
                InjuryReport(
                    team_abbreviation="KC",
                    player_name="Patrick Mahomes",
                    status="Probable",
                    injury_type="Ankle",
                ),
            ],
            "SF": [
                InjuryReport(
                    team_abbreviation="SF",
                    player_name="Christian McCaffrey",
                    status="Questionable",
                    injury_type="Calf",
                ),
                InjuryReport(
                    team_abbreviation="SF",
                    player_name="Deebo Samuel",
                    status="Out",
                    injury_type="Shoulder",
                ),
            ],
            "PHI": [
                InjuryReport(
                    team_abbreviation="PHI",
                    player_name="A.J. Brown",
                    status="Questionable",
                    injury_type="Knee",
                ),
            ],
        }

        return InjuryReportResponse(
            week=week, reports=mock_reports, last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching injury reports: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch injury reports")


# ============================================================================
# LIVING WORLD ENDPOINTS (Database-backed AI-generated content)
# ============================================================================

from fastapi import Depends
from pydantic import Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.news_item import NewsCategory
from app.services.news_feed_service import NewsFeedService
from app.services.storyline_service import StorylineEventService
from app.services.weekly_recap_service import WeeklyRecapService


class LivingNewsItem(BaseModel):
    """AI-generated news item from the Living World Engine."""

    id: int
    season_id: int
    week: int
    team_id: int | None = None
    player_id: int | None = None
    category: str
    headline: str
    content: str
    image_url: str | None = None
    importance_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime

    class Config:
        from_attributes = True


class LivingNewsFeedResponse(BaseModel):
    """Paginated Living World news feed."""

    items: list[LivingNewsItem]
    total_count: int
    page: int
    page_size: int
    has_more: bool


class WeeklyRecapResponse(BaseModel):
    """Weekly recap from the Living World Engine."""

    id: int
    season_id: int
    week: int
    summary_text: str
    mvp_player_id: int | None = None
    play_of_the_week_id: str | None = None
    surprising_result: str | None = None
    media_assets: list[str] | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class StorylineItem(BaseModel):
    """Active storyline from the Living World Engine."""

    type: str
    team_id: int | None = None
    player_id: int | None = None
    start_week: int
    intensity: int = Field(ge=1, le=5)
    event_count: int


class StorylineListResponse(BaseModel):
    """List of active storylines."""

    storylines: list[StorylineItem]


@router.get(
    "/living/feed",
    response_model=LivingNewsFeedResponse,
    summary="Get Living World News Feed",
    description="AI-generated news from in-game events.",
)
async def get_living_news_feed(
    season_id: int = Query(..., description="Season ID"),
    week: int | None = Query(None, ge=1, le=22, description="Week number"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """
    Get AI-generated news from the Living World Engine.

    This news is generated from actual in-game events (touchdowns, sacks, trades, etc.)
    and persisted in the database.
    """
    logger.info(f"Fetching Living World news for season {season_id}, week {week}")

    service = NewsFeedService()
    all_items = service.get_news(db, season_id=season_id, week=week, limit=1000)

    total_count = len(all_items)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = all_items[start_idx:end_idx]

    return LivingNewsFeedResponse(
        items=[LivingNewsItem.model_validate(item) for item in paginated_items],
        total_count=total_count,
        page=page,
        page_size=page_size,
        has_more=end_idx < total_count,
    )


@router.get(
    "/living/recap/{season_id}/{week}",
    response_model=WeeklyRecapResponse,
    summary="Get Weekly Recap",
    description="Get the 'SportsCenter' style weekly recap.",
)
async def get_living_weekly_recap(season_id: int, week: int, db: Session = Depends(get_db)):
    """
    Get the AI-generated weekly recap.

    Includes summary text, MVP, play of the week, and surprising results.
    """
    logger.info(f"Fetching weekly recap for season {season_id}, week {week}")

    service = WeeklyRecapService()
    recap = service.get_recap(db, season_id=season_id, week=week)

    if not recap:
        raise HTTPException(
            status_code=404,
            detail=f"No recap found for season {season_id}, week {week}. Generate one first.",
        )

    return WeeklyRecapResponse.model_validate(recap)


@router.post(
    "/living/recap/{season_id}/{week}/generate",
    response_model=WeeklyRecapResponse,
    status_code=201,
    summary="Generate Weekly Recap",
    description="Trigger AI generation of the weekly recap.",
)
async def generate_living_weekly_recap(season_id: int, week: int, db: Session = Depends(get_db)):
    """
    Generate the weekly recap for a specific week.

    This aggregates all events from the week and creates the recap.
    Idempotent - returns existing recap if already generated.
    """
    logger.info(f"Generating weekly recap for season {season_id}, week {week}")

    service = WeeklyRecapService()
    recap = service.generate_recap(db, season_id=season_id, week=week)

    return WeeklyRecapResponse.model_validate(recap)


@router.get(
    "/living/storylines",
    response_model=StorylineListResponse,
    summary="Get Active Storylines",
    description="Get all active multi-week narrative storylines.",
)
async def get_living_storylines(team_id: int | None = Query(None, description="Filter by team ID")):
    """
    Get active storylines from the Living World Engine.

    Storylines are multi-week narratives like "Hot Streak" or "QB Controversy"
    that develop based on in-game events.
    """
    logger.info(f"Fetching active storylines (team_id={team_id})")

    service = StorylineEventService()
    storylines = service.get_active_storylines(team_id=team_id)

    return StorylineListResponse(storylines=[StorylineItem(**s) for s in storylines])


@router.get(
    "/categories",
    response_model=list[str],
    summary="Get News Categories",
    description="Get all available news category types.",
)
async def get_available_news_categories():
    """Return all available Living World news category values."""
    return [c.value for c in NewsCategory]
