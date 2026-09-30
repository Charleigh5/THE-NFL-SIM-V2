"""
API Endpoints for Real-Time NFL Roster Synchronization.
Provides provider health telemetry, dry-run previews, and execution endpoints.
"""

import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.roster_cache import invalidate_all_team_roster_caches
from app.services.roster_sync.base import ProviderStatusDTO, SyncResultDTO
from app.services.roster_sync.factory import get_roster_provider
from app.services.roster_sync.sync_engine import RosterSyncService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/roster-sync", tags=["roster-sync"])


@router.get("/status", response_model=ProviderStatusDTO)
def get_sync_status(provider: Optional[str] = None) -> ProviderStatusDTO:
    """
    Get connectivity, authentication health, and capability status of the roster provider.
    """
    try:
        active_provider = get_roster_provider(provider)
        return active_provider.get_status()
    except Exception as e:
        logger.error(f"Failed to get roster provider status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
def list_available_providers() -> Dict[str, Any]:
    """
    List supported external roster providers and their configuration status.
    """
    return {
        "current_configured_mode": settings.ROSTER_SYNC_PROVIDER,
        "providers": [
            {
                "id": "tank01",
                "name": "Tank01 NFL Live (RapidAPI)",
                "configured": bool(settings.RAPIDAPI_KEY),
                "cost": "$0 - $10/mo",
                "description": "Hourly updated active rosters, injuries, and transaction news wire.",
            },
            {
                "id": "sportsdataio",
                "name": "SportsDataIO Enterprise",
                "configured": bool(settings.SPORTSDATAIO_API_KEY),
                "cost": "$99 - $500+/mo",
                "description": "Official depth charts, 24/7 data operations, and active roster feeds.",
            },
            {
                "id": "nflverse",
                "name": "NFLVerse & ESPN Wire (Free)",
                "configured": True,
                "cost": "Free / Open Source",
                "description": "Open-source community roster tracking with live public ESPN transactions.",
            },
        ],
    }


@router.post("/execute", response_model=SyncResultDTO)
def execute_roster_sync(
    dry_run: bool = Query(False, description="If True, returns detected diffs without applying to database"),
    provider: Optional[str] = Query(None, description="Optional provider override ('tank01', 'sportsdataio', 'nflverse')"),
    db: Session = Depends(get_db),
) -> SyncResultDTO:
    """
    Execute differential synchronization to update rosters, depth charts, and injuries.
    """
    try:
        sync_service = RosterSyncService()
        result = sync_service.sync_rosters(db=db, dry_run=dry_run, provider_override=provider)
        if not dry_run:
            invalidate_all_team_roster_caches()
        return result
    except Exception as e:
        logger.error(f"Roster synchronization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Roster sync error: {str(e)}")
