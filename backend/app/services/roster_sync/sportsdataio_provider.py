"""
SportsDataIO NFL Data Provider.
Commercial production-grade feed for NFL rosters, official depth charts, and injuries.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import httpx

from app.services.roster_sync.base import (
    BaseRosterProvider,
    RosterPlayerDTO,
    TransactionDTO,
    InjuryDTO,
    DepthOrderDTO,
    ProviderStatusDTO,
)
from app.services.nflverse_service import map_team_abbr, map_position

logger = logging.getLogger(__name__)


class SportsDataIOProvider(BaseRosterProvider):
    """
    SportsDataIO API provider using subscription key authentication.
    """

    BASE_URL = "https://api.sportsdata.io"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._last_sync: Optional[str] = None

    @property
    def provider_id(self) -> str:
        return "sportsdataio"

    def _get_headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("SportsDataIO API key is missing. Configure SPORTSDATAIO_API_KEY in .env.")
        return {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Accept": "application/json",
        }

    def get_status(self) -> ProviderStatusDTO:
        masked = f"****{self.api_key[-4:]}" if self.api_key and len(self.api_key) >= 4 else None
        return ProviderStatusDTO(
            provider_name="SportsDataIO NFL Enterprise",
            is_authenticated=bool(self.api_key),
            masked_key=masked,
            description="Enterprise curated NFL feeds featuring granular 1-4 depth charts, injuries, and transactions.",
            last_sync_timestamp=self._last_sync,
            available_features=["Full Roster Feed", "1-4 Depth Charts", "Official Injury Wire", "24/7 Curation"],
        )

    def fetch_rosters(self) -> List[RosterPlayerDTO]:
        """Fetch all active NFL players."""
        if not self.api_key:
            logger.warning("SportsDataIO API key missing, returning empty list.")
            return []

        headers = self._get_headers()
        players: List[RosterPlayerDTO] = []

        try:
            with httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=20.0) as client:
                resp = client.get("/v3/nfl/scores/json/Players")
                if resp.status_code == 200:
                    raw_players = resp.json()
                    for item in raw_players:
                        team = map_team_abbr(item.get("Team") or "")
                        pos = map_position(item.get("Position") or "WR")
                        status = item.get("Status") or "Active"

                        players.append(
                            RosterPlayerDTO(
                                gsis_id=item.get("UsaTodayPlayerID") or str(item.get("PlayerID", "")),
                                first_name=item.get("FirstName", "Unknown"),
                                last_name=item.get("LastName", "Player"),
                                position=pos,
                                team_abbr=team,
                                jersey_number=item.get("Number"),
                                college=item.get("College"),
                                status=status.upper(),
                                injury_designation=item.get("InjuryStatus"),
                            )
                        )
                else:
                    logger.warning(f"SportsDataIO Players response: {resp.status_code}")
        except Exception as e:
            logger.error(f"Failed to fetch SportsDataIO players: {e}")

        self._last_sync = datetime.utcnow().isoformat()
        return players

    def fetch_transactions(self) -> List[TransactionDTO]:
        """SportsDataIO transactions / roster movements."""
        return []

    def fetch_injuries(self) -> List[InjuryDTO]:
        """Fetch current injury statuses."""
        if not self.api_key:
            return []

        headers = self._get_headers()
        injuries: List[InjuryDTO] = []

        try:
            with httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=15.0) as client:
                resp = client.get("/v3/nfl/scores/json/Injuries")
                if resp.status_code == 200:
                    raw_injuries = resp.json()
                    for item in raw_injuries:
                        injuries.append(
                            InjuryDTO(
                                player_name=item.get("Name", "Unknown"),
                                team_abbr=map_team_abbr(item.get("Team", "")),
                                position=item.get("Position"),
                                status=item.get("DeclaredInjuryStatus") or item.get("InjuryStatus", "Questionable"),
                                injury_type=item.get("BodyPart", "Undisclosed"),
                            )
                        )
        except Exception as e:
            logger.warning(f"Failed to fetch SportsDataIO injuries: {e}")

        return injuries

    def fetch_depth_charts(self) -> List[DepthOrderDTO]:
        """Fetch official team depth charts."""
        if not self.api_key:
            return []

        headers = self._get_headers()
        depth_list: List[DepthOrderDTO] = []

        try:
            with httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=15.0) as client:
                resp = client.get("/v3/nfl/scores/json/DepthCharts")
                if resp.status_code == 200:
                    raw_depth = resp.json()
                    for item in raw_depth:
                        depth_list.append(
                            DepthOrderDTO(
                                team_abbr=map_team_abbr(item.get("Team", "")),
                                position=map_position(item.get("Position", "WR")),
                                player_name=item.get("Name", "Unknown"),
                                rank=int(item.get("DepthOrder", 1)),
                            )
                        )
        except Exception as e:
            logger.warning(f"Failed to fetch SportsDataIO depth charts: {e}")

        return depth_list
