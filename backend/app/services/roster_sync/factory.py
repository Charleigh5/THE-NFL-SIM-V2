"""
Factory for resolving the active NFL roster provider based on configuration.
"""

import logging
from typing import Optional

from app.core.config import settings
from app.services.roster_sync.base import BaseRosterProvider
from app.services.roster_sync.tank01_provider import Tank01Provider
from app.services.roster_sync.sportsdataio_provider import SportsDataIOProvider
from app.services.roster_sync.nflverse_provider import NflverseProvider

logger = logging.getLogger(__name__)


def get_roster_provider(provider_name: Optional[str] = None) -> BaseRosterProvider:
    """
    Resolve and instantiate the appropriate Roster Provider.

    Args:
        provider_name: Optional explicit provider name override ('tank01', 'sportsdataio', 'nflverse').
                       If omitted, resolves via settings.ROSTER_SYNC_PROVIDER or API key presence.

    Returns:
        Instance of BaseRosterProvider.
    """
    target = (provider_name or settings.ROSTER_SYNC_PROVIDER or "auto").lower()

    if target == "tank01":
        return Tank01Provider(api_key=settings.RAPIDAPI_KEY, host=settings.RAPIDAPI_HOST)

    if target == "sportsdataio":
        return SportsDataIOProvider(api_key=settings.SPORTSDATAIO_API_KEY)

    if target == "nflverse":
        return NflverseProvider()

    # Auto resolution
    if settings.RAPIDAPI_KEY:
        logger.info("Auto-detected RAPIDAPI_KEY: Using Tank01 NFL Live provider.")
        return Tank01Provider(api_key=settings.RAPIDAPI_KEY, host=settings.RAPIDAPI_HOST)

    if settings.SPORTSDATAIO_API_KEY:
        logger.info("Auto-detected SPORTSDATAIO_API_KEY: Using SportsDataIO provider.")
        return SportsDataIOProvider(api_key=settings.SPORTSDATAIO_API_KEY)

    logger.info("No external commercial API keys found. Using NFLVerse / ESPN zero-key provider.")
    return NflverseProvider()
