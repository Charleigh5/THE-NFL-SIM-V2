"""
Differential Roster Synchronization Engine.
Reconciles real-time external roster data against database records without destructive resets.
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.player import Player
from app.models.team import Team
from app.models.season import Season
from app.models.depth_chart import DepthChart
from app.models.player_injury import PlayerInjury
from app.engine.event_bus import EventBus, EventType
from app.services.roster_sync.base import (
    BaseRosterProvider,
    RosterPlayerDTO,
    TransactionDTO,
    InjuryDTO,
    DepthOrderDTO,
    SyncResultDTO,
)
from app.services.roster_sync.factory import get_roster_provider
from app.core.roster_cache import invalidate_all_team_roster_caches

logger = logging.getLogger(__name__)


def _player_name(p: Player) -> str:
    """Return formatted full name of a player."""
    return f"{p.first_name} {p.last_name}".strip()


class RosterSyncService:
    """
    Coordinates differential syncing of players, depth charts, transactions, and injuries.
    """

    def __init__(self, provider: Optional[BaseRosterProvider] = None):
        self.provider = provider

    def _resolve_provider(self, override: Optional[str] = None) -> BaseRosterProvider:
        if override:
            return get_roster_provider(override)
        if self.provider:
            return self.provider
        return get_roster_provider()

    def sync_rosters(
        self,
        db: Session,
        dry_run: bool = False,
        provider_override: Optional[str] = None
    ) -> SyncResultDTO:
        """
        Execute differential synchronization against the live database.

        Args:
            db: Active SQLAlchemy Session
            dry_run: If True, calculates diffs without committing changes to DB
            provider_override: Optional provider name ('tank01', 'sportsdataio', 'nflverse')

        Returns:
            SyncResultDTO with counts and items for transfers, depth changes, and injuries.
        """
        provider = self._resolve_provider(provider_override)
        logger.info(f"Starting roster synchronization using provider '{provider.provider_id}' (dry_run={dry_run})...")

        # 1. Fetch active season for event dispatching
        active_season = db.query(Season).filter_by(is_active=True).first()
        season_id = active_season.id if active_season else 1
        current_week = active_season.current_week if active_season else 1

        # 2. Build In-Memory DB Lookups for O(1) matching
        teams = db.query(Team).all()
        team_by_abbr: Dict[str, Team] = {t.abbreviation.upper(): t for t in teams if t.abbreviation}
        team_by_id: Dict[int, Team] = {t.id: t for t in teams}

        players = db.query(Player).all()
        players_by_gsis: Dict[str, Player] = {
            getattr(p, "gsis_id"): p for p in players if getattr(p, "gsis_id", None)
        }
        players_by_name_pos: Dict[Tuple[str, str, str], Player] = {
            (p.first_name.strip().lower(), p.last_name.strip().lower(), p.position.upper()): p
            for p in players if p.first_name and p.last_name and p.position
        }
        players_by_name: Dict[Tuple[str, str], Player] = {
            (p.first_name.strip().lower(), p.last_name.strip().lower()): p
            for p in players
        }

        # 3. Ingest Data from External Provider
        incoming_players = provider.fetch_rosters()
        incoming_depth = provider.fetch_depth_charts()
        incoming_injuries = provider.fetch_injuries()
        incoming_transactions = provider.fetch_transactions()

        transfers: List[Dict[str, Any]] = []
        depth_updates: List[Dict[str, Any]] = []
        injuries_recorded: List[Dict[str, Any]] = []
        unmatched: List[str] = []

        # 4. Reconcile Player Roster Movements (Trades & Signings)
        for dto in incoming_players:
            matched_player: Optional[Player] = None

            if dto.gsis_id and dto.gsis_id in players_by_gsis:
                matched_player = players_by_gsis[dto.gsis_id]
            else:
                key_pos = (dto.first_name.strip().lower(), dto.last_name.strip().lower(), dto.position.upper())
                if key_pos in players_by_name_pos:
                    matched_player = players_by_name_pos[key_pos]
                else:
                    key_name = (dto.first_name.strip().lower(), dto.last_name.strip().lower())
                    if key_name in players_by_name:
                        matched_player = players_by_name[key_name]

            if not matched_player:
                unmatched.append(f"{dto.full_name} ({dto.position} - {dto.team_abbr})")
                continue

            target_team = team_by_abbr.get(dto.team_abbr.upper())
            if target_team and matched_player.team_id != target_team.id:
                from_team = team_by_id.get(matched_player.team_id) if matched_player.team_id else None
                from_abbr = from_team.abbreviation if from_team else "FA"

                p_name = _player_name(matched_player)
                transfer_info = {
                    "player_id": matched_player.id,
                    "player_name": p_name,
                    "position": matched_player.position,
                    "from_team": from_abbr,
                    "to_team": target_team.abbreviation,
                }
                transfers.append(transfer_info)

                if not dry_run:
                    matched_player.team_id = target_team.id
                    # Dispatch transaction to Living League / News Feed
                    try:
                        EventBus.publish(
                            EventType.TRADE_COMPLETED,
                            {
                                "season_id": season_id,
                                "week": current_week,
                                "player_id": matched_player.id,
                                "player_name": p_name,
                                "from_team_id": from_team.id if from_team else 0,
                                "to_team_id": target_team.id,
                                "trade_details": f"{p_name} ({matched_player.position}) acquired by {target_team.name} from {from_abbr}.",
                            },
                        )
                    except Exception as e:
                        logger.warning(f"Failed to publish TRADE_COMPLETED event: {e}")

            # Update jersey number if changed
            if dto.jersey_number is not None and matched_player.jersey_number != dto.jersey_number:
                if not dry_run:
                    matched_player.jersey_number = dto.jersey_number

        # 5. Reconcile Depth Charts
        for d_dto in incoming_depth:
            key_name = (d_dto.player_name.strip().lower().split()[0], d_dto.player_name.strip().lower().split()[-1]) if len(d_dto.player_name.split()) >= 2 else ("", "")
            player = players_by_name.get(key_name)
            if not player or not player.team_id:
                continue

            dc_entry = (
                db.query(DepthChart)
                .filter_by(team_id=player.team_id, player_id=player.id)
                .first()
            )

            current_rank = dc_entry.depth_order if dc_entry else player.depth_chart_rank
            if current_rank != d_dto.rank:
                depth_updates.append({
                    "player_id": player.id,
                    "player_name": _player_name(player),
                    "position": d_dto.position,
                    "team": d_dto.team_abbr,
                    "old_rank": current_rank,
                    "new_rank": d_dto.rank,
                })
                if not dry_run:
                    if dc_entry:
                        dc_entry.depth_order = d_dto.rank
                    player.depth_chart_rank = d_dto.rank

        # 6. Reconcile Injuries
        for inj_dto in incoming_injuries:
            name_parts = inj_dto.player_name.strip().lower().split()
            if len(name_parts) >= 2:
                key = (name_parts[0], name_parts[-1])
                player = players_by_name.get(key)
                if player:
                    injuries_recorded.append({
                        "player_id": player.id,
                        "player_name": _player_name(player),
                        "team": inj_dto.team_abbr,
                        "status": inj_dto.status,
                        "injury_type": inj_dto.injury_type,
                    })
                    if not dry_run:
                        injury_rec = db.query(PlayerInjury).filter_by(player_id=player.id).first()
                        if not injury_rec:
                            injury_rec = PlayerInjury(player_id=player.id)
                            db.add(injury_rec)
                        injury_rec.injury_status = inj_dto.status.upper()
                        injury_rec.injury_type = inj_dto.injury_type

        # 7. Finalize / Commit / Rollback
        if dry_run:
            db.rollback()
            logger.info(f"Dry run complete. Found {len(transfers)} transfers, {len(depth_updates)} depth changes, {len(injuries_recorded)} injuries.")
        else:
            db.commit()
            invalidate_all_team_roster_caches()
            logger.info(f"Sync committed successfully: {len(transfers)} transfers, {len(depth_updates)} depth changes, {len(injuries_recorded)} injuries.")

        return SyncResultDTO(
            provider=provider.provider_id,
            timestamp=datetime.utcnow().isoformat(),
            dry_run=dry_run,
            transfers_count=len(transfers),
            depth_updates_count=len(depth_updates),
            injuries_count=len(injuries_recorded),
            unmatched_count=len(unmatched),
            transfers=transfers,
            depth_updates=depth_updates,
            injuries=injuries_recorded,
            unmatched=unmatched[:50],  # Cap unmatched sample
            message=f"Successfully synchronized rosters via {provider.provider_id}."
        )
