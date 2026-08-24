"""
News API Endpoints
==================
Consolidated REST API for league news, team news, player news, injury reports,
AI-generated living world feeds, weekly recaps, storylines, and category metadata.
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

from fastapi import APIRouter, HTTPException, Query, Path, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.news_item import NewsItem as NewsItemModel, NewsCategory
from app.models.weekly_recap import WeeklyRecap as WeeklyRecapModel
from app.services.news_feed_service import NewsFeedService
from app.services.weekly_recap_service import WeeklyRecapService
from app.services.storyline_service import StorylineEventService

router = APIRouter(prefix="/news", tags=["news"])
logger = logging.getLogger(__name__)


# ============================================================================
# SCHEMAS
# ============================================================================

class NewsItem(BaseModel):
    """Individual news item schema."""
    headline: str
    source: str
    date: str
    category: str = "general"
    team_id: Optional[int] = None
    player_id: Optional[int] = None
    is_breaking: bool = False


class NewsResponse(BaseModel):
    """News feed response schema."""
    items: List[NewsItem]
    total: int
    last_updated: str


class InjuryReport(BaseModel):
    """Injury report item schema."""
    team_abbreviation: str
    player_name: str
    status: str
    injury_type: str


class InjuryReportResponse(BaseModel):
    """Injury reports response schema."""
    week: int
    reports: Dict[str, List[InjuryReport]]
    last_updated: str


class LivingNewsItem(BaseModel):
    """AI-generated news item from the Living World Engine."""
    id: int
    season_id: int
    week: int
    team_id: Optional[int] = None
    player_id: Optional[int] = None
    category: str
    headline: str
    content: str
    image_url: Optional[str] = None
    importance_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime

    class Config:
        from_attributes = True


class NewsFeedResponse(BaseModel):
    """Paginated Living World news feed."""
    items: List[LivingNewsItem]
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
    mvp_player_id: Optional[int] = None
    play_of_the_week_id: Optional[str] = None
    surprising_result: Optional[str] = None
    media_assets: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StorylineItem(BaseModel):
    """Active storyline from the Living World Engine."""
    type: str
    team_id: Optional[int] = None
    player_id: Optional[int] = None
    start_week: int
    intensity: int = Field(ge=1, le=5)
    event_count: int


class StorylineListResponse(BaseModel):
    """List of active storylines."""
    storylines: List[StorylineItem]


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str


# ============================================================================
# MOCK / FALLBACK DATA GENERATORS
# ============================================================================

def _generate_mock_league_news() -> List[NewsItem]:
    """Generate simulated league news for immersion."""
    return [
        NewsItem(
            headline="Chiefs look to extend historic dynasty with 4th consecutive Super Bowl appearance",
            source="NFL Network",
            date="2024-12-04",
            category="league",
            is_breaking=False
        ),
        NewsItem(
            headline="Trade deadline looming: Multiple teams seeking QB help before playoffs",
            source="ESPN",
            date="2024-12-03",
            category="trades",
            is_breaking=True
        ),
        NewsItem(
            headline="Week 14 Power Rankings: Eagles surge to #1 after dominant win",
            source="The Athletic",
            date="2024-12-03",
            category="rankings",
            is_breaking=False
        ),
        NewsItem(
            headline="Injury Report: Multiple stars questionable for crucial week 14 matchups",
            source="NFL Network",
            date="2024-12-02",
            category="injuries",
            is_breaking=False
        ),
        NewsItem(
            headline="Rookie Watch: No. 1 pick already drawing MVP comparisons",
            source="PFF",
            date="2024-12-02",
            category="rookies",
            is_breaking=False
        ),
        NewsItem(
            headline="Contract negotiations stall for Pro Bowl wide receiver seeking extension",
            source="Schefter",
            date="2024-12-01",
            category="contracts",
            is_breaking=True
        ),
    ]


def _generate_mock_team_news(team_name: str) -> List[NewsItem]:
    """Generate simulated team-specific news."""
    return [
        NewsItem(
            headline=f"{team_name} looking to shore up offensive line depth before playoffs",
            source="Team Insider",
            date="2024-12-04",
            category="team",
            is_breaking=False
        ),
        NewsItem(
            headline=f"Coaching staff impressed with {team_name}'s young defensive core",
            source="Local Beat",
            date="2024-12-03",
            category="team",
            is_breaking=False
        ),
        NewsItem(
            headline=f"{team_name} fans react to controversial fourth-quarter playcall",
            source="Fan Nation",
            date="2024-12-02",
            category="team",
            is_breaking=False
        ),
    ]


def _generate_mock_player_news(player_name: str) -> List[NewsItem]:
    """Generate simulated player-specific news."""
    return [
        NewsItem(
            headline=f"{player_name} named to Pro Bowl roster for the 3rd consecutive year",
            source="NFL Network",
            date="2024-12-04",
            category="player",
            is_breaking=False
        ),
        NewsItem(
            headline=f"{player_name} discusses playoff preparation in exclusive interview",
            source="Team Media",
            date="2024-12-03",
            category="player",
            is_breaking=False
        ),
    ]


# ============================================================================
# LEAGUE, TEAM & PLAYER NEWS ENDPOINTS
# ============================================================================

@router.get("/league", response_model=NewsResponse)
async def get_league_news(
    limit: int = Query(10, ge=1, le=50, description="Number of news items to return"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Get latest league-wide news."""
    logger.info(f"Fetching league news (limit={limit}, category={category})")
    try:
        news_items = _generate_mock_league_news()
        if category:
            news_items = [item for item in news_items if item.category == category]

        return NewsResponse(
            items=news_items[:limit],
            total=len(news_items),
            last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching league news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news")


@router.get("/team/{team_name}", response_model=NewsResponse)
async def get_team_news(
    team_name: str,
    limit: int = Query(5, ge=1, le=20, description="Number of news items to return")
):
    """Get news specific to a team."""
    logger.info(f"Fetching news for team: {team_name}")
    try:
        news_items = _generate_mock_team_news(team_name)
        return NewsResponse(
            items=news_items[:limit],
            total=len(news_items),
            last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching team news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch team news")


@router.get("/player/{player_name}", response_model=NewsResponse)
async def get_player_news(
    player_name: str,
    limit: int = Query(5, ge=1, le=20, description="Number of news items to return")
):
    """Get news specific to a player."""
    logger.info(f"Fetching news for player: {player_name}")
    try:
        news_items = _generate_mock_player_news(player_name)
        return NewsResponse(
            items=news_items[:limit],
            total=len(news_items),
            last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching player news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch player news")


@router.get("/injuries/week/{week}", response_model=InjuryReportResponse)
async def get_injury_reports(
    week: int = Path(..., ge=1, le=18, description="NFL week number")
):
    """Get injury reports for a specific week."""
    logger.info(f"Fetching injury reports for week {week}")
    try:
        mock_reports = {
            "KC": [
                InjuryReport(
                    team_abbreviation="KC",
                    player_name="Patrick Mahomes",
                    status="Probable",
                    injury_type="Ankle"
                ),
            ],
            "SF": [
                InjuryReport(
                    team_abbreviation="SF",
                    player_name="Christian McCaffrey",
                    status="Questionable",
                    injury_type="Calf"
                ),
                InjuryReport(
                    team_abbreviation="SF",
                    player_name="Deebo Samuel",
                    status="Out",
                    injury_type="Shoulder"
                ),
            ],
            "PHI": [
                InjuryReport(
                    team_abbreviation="PHI",
                    player_name="A.J. Brown",
                    status="Questionable",
                    injury_type="Knee"
                ),
            ],
        }

        return InjuryReportResponse(
            week=week,
            reports=mock_reports,
            last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching injury reports: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch injury reports")


# ============================================================================
# LIVING WORLD / RECAPS / STORYLINES ENDPOINTS (Consolidated)
# ============================================================================

@router.get(
    "/feed",
    response_model=NewsFeedResponse,
    summary="Get Living World News Feed"
)
@router.get(
    "/living/feed",
    response_model=NewsFeedResponse,
    include_in_schema=False
)
async def get_living_news_feed(
    season_id: int = Query(2025, description="Season ID"),
    week: Optional[int] = Query(None, ge=1, le=22, description="Week number"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get AI-generated news from the Living World Engine."""
    logger.info(f"Fetching Living World news for season {season_id}, week {week}")

    service = NewsFeedService()
    all_items = service.get_news(db, season_id=season_id, week=week, limit=1000)

    if category:
        all_items = [
            item for item in all_items
            if (hasattr(item.category, "value") and item.category.value == category) or str(item.category) == category
        ]

    total_count = len(all_items)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = all_items[start_idx:end_idx]

    return NewsFeedResponse(
        items=[LivingNewsItem.model_validate(item) for item in paginated_items],
        total_count=total_count,
        page=page,
        page_size=page_size,
        has_more=end_idx < total_count
    )


@router.get(
    "/recap/{season_id}/{week}",
    response_model=WeeklyRecapResponse,
    summary="Get Weekly Recap"
)
@router.get(
    "/living/recap/{season_id}/{week}",
    response_model=WeeklyRecapResponse,
    include_in_schema=False
)
async def get_living_weekly_recap(
    season_id: int,
    week: int,
    db: Session = Depends(get_db)
):
    """Get the AI-generated weekly recap."""
    logger.info(f"Fetching weekly recap for season {season_id}, week {week}")

    service = WeeklyRecapService()
    recap = service.get_recap(db, season_id=season_id, week=week)

    if not recap:
        raise HTTPException(
            status_code=404,
            detail=f"No recap found for season {season_id}, week {week}. Generate one first."
        )

    return WeeklyRecapResponse.model_validate(recap)


@router.post(
    "/recap/{season_id}/{week}/generate",
    response_model=WeeklyRecapResponse,
    status_code=201,
    summary="Generate Weekly Recap"
)
@router.post(
    "/living/recap/{season_id}/{week}/generate",
    response_model=WeeklyRecapResponse,
    status_code=201,
    include_in_schema=False
)
async def generate_living_weekly_recap(
    season_id: int,
    week: int,
    db: Session = Depends(get_db)
):
    """Generate or retrieve the weekly recap for a specific week."""
    logger.info(f"Generating weekly recap for season {season_id}, week {week}")

    service = WeeklyRecapService()
    recap = service.generate_recap(db, season_id=season_id, week=week)

    return WeeklyRecapResponse.model_validate(recap)


@router.get(
    "/storylines",
    response_model=StorylineListResponse,
    summary="Get Active Storylines"
)
@router.get(
    "/living/storylines",
    response_model=StorylineListResponse,
    include_in_schema=False
)
async def get_living_storylines(
    team_id: Optional[int] = Query(None, description="Filter by team ID")
):
    """Get all active multi-week narrative storylines."""
    logger.info(f"Fetching active storylines (team_id={team_id})")

    service = StorylineEventService()
    storylines = service.get_active_storylines(team_id=team_id)

    return StorylineListResponse(
        storylines=[StorylineItem(**s) for s in storylines]
    )


@router.get(
    "/categories",
    response_model=List[str],
    summary="Get News Categories"
)
async def get_available_news_categories():
    """Return all available Living World news category values."""
    return [c.value for c in NewsCategory]
