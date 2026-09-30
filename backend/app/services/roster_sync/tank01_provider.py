"""
Tank01 NFL Live Provider (RapidAPI).
Connects to Tank01's low-latency endpoints for rosters, depth orders, and injury lists.
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

# List of 32 official NFL team abbreviations
NFL_TEAMS = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LV", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS"
]


class Tank01Provider(BaseRosterProvider):
    """
    Tank01 API provider utilizing RapidAPI authentication.
    """

    BASE_URL = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"

    def __init__(self, api_key: Optional[str] = None, host: Optional[str] = None):
        self.api_key = api_key
        self.host = host or "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
        self._last_sync: Optional[str] = None

    @property
    def provider_id(self) -> str:
        return "tank01"

    def _get_headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("Tank01 RapidAPI key is missing. Configure RAPIDAPI_KEY in .env.")
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host,
            "Accept": "application/json",
        }

    def get_status(self) -> ProviderStatusDTO:
        masked = f"****{self.api_key[-4:]}" if self.api_key and len(self.api_key) >= 4 else None
        return ProviderStatusDTO(
            provider_name="Tank01 NFL Live (RapidAPI)",
            is_authenticated=bool(self.api_key),
            masked_key=masked,
            description="Hourly updated real-time rosters, transactions, and injury reports via RapidAPI.",
            last_sync_timestamp=self._last_sync,
            available_features=["Roster Ingestion", "Injury Wire", "Transactions Feed", "Hourly Refresh"],
        )

    def fetch_rosters(self) -> List[RosterPlayerDTO]:
        """Fetch current team rosters across all 32 franchises."""
        if not self.api_key:
            logger.warning("Tank01 API key missing, returning empty roster list.")
            return []

        headers = self._get_headers()
        players: List[RosterPlayerDTO] = []

        with httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=15.0) as client:
            for team_abbr in NFL_TEAMS:
                try:
                    resp = client.get("/getNFLTeamRoster", params={"teamAbv": team_abbr, "getStats": "false"})
                    if resp.status_code == 200:
                        data = resp.json()
                        body = data.get("body", {})
                        roster_list = body.get("roster", [])
                        for item in roster_list:
                            # Tank01 player fields: longName, pos, playerID, jerseyNum, college, etc.
                            full_name = item.get("longName", "")
                            parts = full_name.split(" ", 1)
                            first_name = parts[0] if parts else "Unknown"
                            last_name = parts[1] if len(parts) > 1 else ""

                            jersey_raw = item.get("jerseyNum")
                            try:
                                jersey_num = int(jersey_raw) if jersey_raw is not None else None
                            except (ValueError, TypeError):
                                jersey_num = None

                            mapped_team = map_team_abbr(team_abbr)
                            mapped_pos = map_position(item.get("pos", "WR"))

                            players.append(
                                RosterPlayerDTO(
                                    espn_id=item.get("playerID") or item.get("espnID"),
                                    first_name=first_name,
                                    last_name=last_name,
                                    position=mapped_pos,
                                    team_abbr=mapped_team,
                                    jersey_number=jersey_num,
                                    college=item.get("college"),
                                    status=item.get("injuryStatus", "ACTIVE") if item.get("injuryStatus") else "ACTIVE",
                                    injury_designation=item.get("injuryDesignation"),
                                )
                            )
                    elif resp.status_code == 429:
                        logger.error("Tank01 RapidAPI rate limit reached (429).")
                        break
                    else:
                        logger.warning(f"Tank01 error for {team_abbr}: {resp.status_code}")
                except Exception as e:
                    logger.error(f"Failed to fetch Tank01 roster for {team_abbr}: {e}")

        self._last_sync = datetime.utcnow().isoformat()
        return players

    def fetch_transactions(self) -> List[TransactionDTO]:
        """Fetch latest transaction events from Tank01 news endpoint."""
        if not self.api_key:
            return []

        headers = self._get_headers()
        transactions: List[TransactionDTO] = []

        try:
            with httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=15.0) as client:
                resp = client.get("/getNFLNews", params={"recentNews": "true", "maxItems": 50})
                if resp.status_code == 200:
                    news_items = resp.json().get("body", [])
                    for item in news_items:
                        title = item.get("title", "")
                        desc = item.get("description", "")
                        # Classify transaction keywords
                        lower = (title + " " + desc).lower()
                        trans_type = "UPDATE"
                        if "trade" in lower:
                            trans_type = "TRADE"
                        elif "sign" in lower:
                            trans_type = "SIGNING"
                        elif "waive" in lower or "cut" in lower or "release" in lower:
                            trans_type = "CUT"
                        elif "injured reserve" in lower or " ir " in lower:
                            trans_type = "RESERVE"

                        transactions.append(
                            TransactionDTO(
                                player_name=item.get("player", title),
                                transaction_type=trans_type,
                                description=desc or title,
                                date=datetime.utcnow().date(),
                            )
                        )
        except Exception as e:
            logger.warning(f"Error fetching Tank01 transactions: {e}")

        return transactions

    def fetch_injuries(self) -> List[InjuryDTO]:
        """Fetch injury designations across all NFL teams."""
        if not self.api_key:
            return []

        headers = self._get_headers()
        injuries: List[InjuryDTO] = []

        try:
            with httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=15.0) as client:
                resp = client.get("/getNFLInjuryList")
                if resp.status_code == 200:
                    body = resp.json().get("body", [])
                    for item in body:
                        injuries.append(
                            InjuryDTO(
                                player_name=item.get("longName", item.get("player", "Unknown")),
                                team_abbr=map_team_abbr(item.get("teamAbv", "")),
                                position=item.get("pos"),
                                status=item.get("injStatus", "Questionable"),
                                injury_type=item.get("injury", "Undisclosed"),
                            )
                        )
        except Exception as e:
            logger.warning(f"Error fetching Tank01 injuries: {e}")

        return injuries

    def fetch_depth_charts(self) -> List[DepthOrderDTO]:
        """Fetch depth orders (inferred from active rosters or rankings)."""
        return []
