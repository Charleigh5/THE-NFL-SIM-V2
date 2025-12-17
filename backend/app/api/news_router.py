"""
News & Recap API Router

Following FastAPI best practices:
- Pydantic response models for type safety and OpenAPI docs
- Proper HTTP status codes and error responses
- Dependency injection for database sessions
- Query parameter validation
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from app.core.database import get_db
from app.models.news_item import NewsItem, NewsCategory
from app.models.weekly_recap import WeeklyRecap
from app.services.news_feed_service import NewsFeedService
from app.services.weekly_recap_service import WeeklyRecapService
from app.services.storyline_service import StorylineEventService, StorylineType

router = APIRouter(prefix="/api/news", tags=["News & Recaps"])


# ============================================================================
# Pydantic Response Models (OpenAPI Schema Generation)
# ============================================================================

class NewsItemResponse(BaseModel):
    """Schema for a single news item."""
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
        from_attributes = True  # Pydantic v2 ORM mode


class NewsFeedResponse(BaseModel):
    """Paginated news feed response."""
    items: List[NewsItemResponse]
    total_count: int
    page: int
    page_size: int
    has_more: bool


class WeeklyRecapResponse(BaseModel):
    """Schema for a weekly recap."""
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


class StorylineResponse(BaseModel):
    """Schema for an active storyline."""
    type: str
    team_id: Optional[int] = None
    player_id: Optional[int] = None
    start_week: int
    intensity: int = Field(ge=1, le=5)
    event_count: int


class StorylineListResponse(BaseModel):
    """List of active storylines."""
    storylines: List[StorylineResponse]


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str


# ============================================================================
# API Endpoints
# ============================================================================

@router.get(
    "/feed",
    response_model=NewsFeedResponse,
    responses={
        200: {"description": "News feed retrieved successfully"},
        404: {"model": ErrorResponse, "description": "No news found for the specified criteria"}
    },
    summary="Get News Feed",
    description="Retrieve paginated news items for a specific season and optional week."
)
async def get_news_feed(
    season_id: int = Query(..., description="Season ID to filter news"),
    week: Optional[int] = Query(None, ge=1, le=22, description="Week number (1-22)"),
    category: Optional[str] = Query(None, description="Filter by news category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get the news feed for a season.

    - **season_id**: Required. The season to fetch news for.
    - **week**: Optional. Filter to a specific week.
    - **category**: Optional. Filter by category (TRANSACTION, INJURY, etc.)
    - **page**: Pagination page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    """
    service = NewsFeedService()

    # Get all news for counting
    all_items = service.get_news(db, season_id=season_id, week=week, limit=1000)

    # Apply category filter if specified
    if category:
        all_items = [item for item in all_items if item.category.value == category]

    total_count = len(all_items)

    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = all_items[start_idx:end_idx]

    if not paginated_items and page == 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No news found for season {season_id}" + (f", week {week}" if week else "")
        )

    return NewsFeedResponse(
        items=[NewsItemResponse.model_validate(item) for item in paginated_items],
        total_count=total_count,
        page=page,
        page_size=page_size,
        has_more=end_idx < total_count
    )


@router.get(
    "/recap/{season_id}/{week}",
    response_model=WeeklyRecapResponse,
    responses={
        200: {"description": "Weekly recap retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Recap not found for specified week"}
    },
    summary="Get Weekly Recap",
    description="Retrieve the 'SportsCenter' style weekly recap for a specific week."
)
async def get_weekly_recap(
    season_id: int,
    week: int,
    db: Session = Depends(get_db)
):
    """
    Get the weekly recap for a specific season and week.

    Returns the AI-generated summary, MVP, play of the week, and more.
    """
    service = WeeklyRecapService()
    recap = service.get_recap(db, season_id=season_id, week=week)

    if not recap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No recap found for season {season_id}, week {week}. It may not have been generated yet."
        )

    return WeeklyRecapResponse.model_validate(recap)


@router.post(
    "/recap/{season_id}/{week}/generate",
    response_model=WeeklyRecapResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Recap generated successfully"},
        200: {"description": "Recap already exists (returned existing)"}
    },
    summary="Generate Weekly Recap",
    description="Trigger generation of a weekly recap. Returns existing recap if already created."
)
async def generate_weekly_recap(
    season_id: int,
    week: int,
    db: Session = Depends(get_db)
):
    """
    Generate or retrieve the weekly recap for a specific week.

    This endpoint is idempotent - calling it multiple times returns the same recap.
    """
    service = WeeklyRecapService()
    recap = service.generate_recap(db, season_id=season_id, week=week)

    return WeeklyRecapResponse.model_validate(recap)


@router.get(
    "/storylines",
    response_model=StorylineListResponse,
    summary="Get Active Storylines",
    description="Retrieve all active storylines, optionally filtered by team."
)
async def get_storylines(
    team_id: Optional[int] = Query(None, description="Filter by team ID")
):
    """
    Get all active narrative storylines.

    Storylines are multi-week narratives like "Hot Streak" or "QB Controversy".
    """
    service = StorylineEventService()
    storylines = service.get_active_storylines(team_id=team_id)

    return StorylineListResponse(
        storylines=[StorylineResponse(**s) for s in storylines]
    )


@router.get(
    "/categories",
    response_model=List[str],
    summary="Get News Categories",
    description="Get all available news category types."
)
async def get_news_categories():
    """Return all available news category enum values."""
    return [c.value for c in NewsCategory]
