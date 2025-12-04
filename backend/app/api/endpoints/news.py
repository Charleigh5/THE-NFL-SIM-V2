"""
News API Endpoints

Provides REST API for fetching league news, player news, and injury reports
from the MCP sports_news server.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from datetime import datetime

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
    team_id: Optional[int] = None
    player_id: Optional[int] = None
    is_breaking: bool = False


class NewsResponse(BaseModel):
    """News feed response"""
    items: List[NewsItem]
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
    reports: Dict[str, List[InjuryReport]]
    last_updated: str


# ============================================================================
# MOCK DATA GENERATOR
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
# ENDPOINTS
# ============================================================================

@router.get("/league", response_model=NewsResponse)
async def get_league_news(
    limit: int = Query(10, ge=1, le=50, description="Number of news items to return"),
    category: Optional[str] = Query(None, description="Filter by category")
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
