from __future__ import annotations

import re

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session, joinedload, noload

from app.models.game import Game
from app.models.history import SeasonHistory
from app.models.player import Player
from app.models.season import Season
from app.models.team import Team
from app.models.trait import PlayerTrait
from app.models.weekly_recap import WeeklyRecap
from app.schemas.narrator import FactItem, FactPacket, NarrationContextRequest
from app.services.storyline_service import storyline_service

_CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]+")
_MAX_FREE_TEXT_LEN = 160


def sanitize_fact_text(text: object | None, max_len: int = _MAX_FREE_TEXT_LEN) -> str:
    """Strip control characters, collapse whitespace, and cap length at max_len."""
    if text is None or text == "":
        return ""
    cleaned = _CONTROL_CHARS_RE.sub(" ", str(text))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) > max_len:
        return cleaned[:max_len].rstrip()
    return cleaned


class NarratorFactsService:
    """Builds grounded FactPacket objects from franchise, season, game, and player state."""

    def __init__(self, db: Session):
        self.db = db

    def build_fact_packet(self, request: NarrationContextRequest) -> FactPacket:
        team = (
            self.db.query(Team)
            .options(joinedload(Team.season_history))
            .filter(Team.id == request.team_id)
            .first()
        )
        if team:
            city = sanitize_fact_text(team.city, 60)
            name = sanitize_fact_text(team.name, 60)
            team_name = f"{city} {name}".strip() or "Franchise"
            wins = int(team.wins or 0)
            losses = int(team.losses or 0)
            ties = int(team.ties or 0)
            team_record = f"{wins}-{losses}-{ties}" if ties > 0 else f"{wins}-{losses}"
        else:
            team_name = f"Team {request.team_id}"
            team_record = "0-0"

        season = (
            self.db.query(Season)
            .order_by(Season.is_active.desc(), desc(Season.year))
            .first()
        )

        season_year = int(season.year) if season and season.year else 2026
        current_week = int(season.current_week) if season and season.current_week else 1
        season_id = int(season.id) if season and season.id else None

        facts: list[FactItem] = []

        computed_record = self._append_last_game_facts(
            facts=facts,
            team=team,
            team_id=request.team_id,
            team_name=team_name,
            season_id=season_id,
            season_year=season_year,
            current_week=current_week,
            explicit_game_id=request.game_id,
        )
        if computed_record and team_record == "0-0":
            team_record = computed_record

        self._append_season_facts(
            facts=facts,
            team=team,
            team_id=request.team_id,
            team_record=team_record,
            season=season,
            season_year=season_year,
            current_week=current_week,
        )
        self._append_franchise_facts(
            facts=facts,
            team=team,
            team_id=request.team_id,
            team_name=team_name,
        )
        self._append_storyline_facts(
            facts=facts,
            team_id=request.team_id,
            season_id=season_id,
            current_week=current_week,
        )
        self._append_player_facts(
            facts=facts,
            team_id=request.team_id,
            player_id=request.player_id,
            season_id=season_id,
            season_year=season_year,
        )

        return FactPacket(
            page=request.page,
            team_name=team_name,
            team_record=team_record,
            season_year=season_year,
            current_week=current_week,
            facts=facts,
        )

    def _append_player_facts(
        self,
        facts: list[FactItem],
        team_id: int,
        player_id: int | None,
        season_id: int | None,
        season_year: int,
    ) -> None:
        player_query = self.db.query(Player).options(
            noload("*"),
            joinedload(Player.season_stats),
            joinedload(Player.player_traits).joinedload(PlayerTrait.trait),
        )
        if player_id is not None:
            player = player_query.filter(Player.id == player_id).first()
        else:
            player = (
                player_query.filter(Player.team_id == team_id)
                .order_by(desc(Player.overall_rating), Player.depth_chart_rank)
                .first()
            )

        if not player:
            return

        first = sanitize_fact_text(player.first_name, 40)
        last = sanitize_fact_text(player.last_name, 40)
        full_name = f"{first} {last}".strip() or f"Player {player.id}"
        pos = sanitize_fact_text(player.position, 10) or "ATH"
        college = sanitize_fact_text(player.college, 40) or "Unknown College"
        age = int(player.age or 22)
        exp = int(player.experience or 0)
        ovr = int(player.overall_rating or 50)
        trust = int(player.trust_in_coach if player.trust_in_coach is not None else 80)

        facts.append(
            FactItem(
                fact_id="player_bio",
                category="player",
                label="Player Bio & Rating",
                value=sanitize_fact_text(
                    f"{full_name} ({pos}, {college}): {ovr} OVR, Age {age}, {exp} yrs exp, {trust} coach trust"
                ),
            )
        )

        matching_stats = [
            s
            for s in (player.season_stats or [])
            if (season_id is None or s.season_id == season_id or s.year == season_year)
        ]
        matching_stats.sort(key=lambda s: s.year or 0, reverse=True)
        stats = matching_stats[0] if matching_stats else None
        if stats:
            gp = int(stats.games_played or 0)
            stat_parts = [f"{gp} GP"]
            if int(stats.pass_yards or 0) > 0 or int(stats.pass_tds or 0) > 0:
                stat_parts.append(
                    f"{int(stats.pass_yards or 0)} pass yds, {int(stats.pass_tds or 0)} pass TDs, {int(stats.pass_ints or 0)} INTs"
                )
            if int(stats.rush_yards or 0) > 0 or int(stats.rush_tds or 0) > 0:
                stat_parts.append(
                    f"{int(stats.rush_yards or 0)} rush yds, {int(stats.rush_tds or 0)} rush TDs"
                )
            if int(stats.rec_yards or 0) > 0 or int(stats.rec_tds or 0) > 0:
                stat_parts.append(
                    f"{int(stats.receptions or 0)} rec, {int(stats.rec_yards or 0)} rec yds, {int(stats.rec_tds or 0)} rec TDs"
                )
            if int(stats.tackles or 0) > 0 or float(stats.sacks or 0.0) > 0.0:
                stat_parts.append(
                    f"{int(stats.tackles or 0)} tackles, {float(stats.sacks or 0.0):.1f} sacks, {int(stats.interceptions or 0)} INTs"
                )
            facts.append(
                FactItem(
                    fact_id="player_season_stats",
                    category="player",
                    label="Player Season Stats",
                    value=sanitize_fact_text(f"{full_name}: " + "; ".join(stat_parts)),
                )
            )

        traits = [pt.trait for pt in (player.player_traits or []) if pt.trait is not None]
        if traits:
            trait_names = ", ".join(
                sanitize_fact_text(t.name, 40) for t in traits[:4] if t.name
            )
            if trait_names:
                facts.append(
                    FactItem(
                        fact_id="player_traits",
                        category="player",
                        label="Player RPG Traits",
                        value=sanitize_fact_text(f"{full_name} active traits: {trait_names}"),
                    )
                )

        dna_text = self._format_json_summary(player.psychological_dna)
        backstory_text = self._format_json_summary(player.backstory)
        combined_lore = " | ".join(part for part in (dna_text, backstory_text) if part)
        if combined_lore:
            facts.append(
                FactItem(
                    fact_id="player_lore",
                    category="player",
                    label="Player DNA & Backstory",
                    value=sanitize_fact_text(combined_lore, _MAX_FREE_TEXT_LEN),
                )
            )

    @staticmethod
    def _format_json_summary(payload: object | None) -> str:
        if not payload:
            return ""
        if isinstance(payload, str):
            return sanitize_fact_text(payload, _MAX_FREE_TEXT_LEN)
        if isinstance(payload, dict):
            parts: list[str] = []
            for k, v in list(payload.items())[:4]:
                if v is not None and str(v).strip():
                    key_clean = sanitize_fact_text(str(k), 24)
                    val_clean = sanitize_fact_text(str(v), 80)
                    parts.append(f"{key_clean}: {val_clean}")
            return sanitize_fact_text(", ".join(parts), _MAX_FREE_TEXT_LEN)
        return sanitize_fact_text(str(payload), _MAX_FREE_TEXT_LEN)

    def _append_last_game_facts(
        self,
        facts: list[FactItem],
        team: Team | None,
        team_id: int,
        team_name: str,
        season_id: int | None,
        season_year: int,
        current_week: int,
        explicit_game_id: int | None,
    ) -> str | None:
        game: Game | None = None
        all_team_games: list[Game] = []
        if explicit_game_id is not None:
            game = (
                self.db.query(Game)
                .options(joinedload(Game.home_team), joinedload(Game.away_team))
                .filter(Game.id == explicit_game_id)
                .first()
            )
            if game:
                all_team_games = [game]

        if not all_team_games:
            query = (
                self.db.query(Game)
                .options(joinedload(Game.home_team), joinedload(Game.away_team))
                .filter(
                    or_(Game.home_team_id == team_id, Game.away_team_id == team_id),
                )
            )
            if season_id is not None:
                query = query.filter(
                    or_(Game.season_id == season_id, Game.season == season_year)
                )
            all_team_games = query.order_by(desc(Game.week), desc(Game.id)).all()

        played_games = [g for g in all_team_games if g.is_played]
        if game is None and played_games:
            game = played_games[0]

        computed_record: str | None = None
        if played_games:
            w = 0
            losses = 0
            t = 0
            for g in played_games:
                home = g.home_team_id == team_id
                ts = int(g.home_score or 0) if home else int(g.away_score or 0)
                os = int(g.away_score or 0) if home else int(g.home_score or 0)
                if ts > os:
                    w += 1
                elif ts < os:
                    losses += 1
                else:
                    t += 1
            computed_record = f"{w}-{losses}-{t}" if t > 0 else f"{w}-{losses}"

        if game and game.is_played:
            is_home = game.home_team_id == team_id
            opp_id = game.away_team_id if is_home else game.home_team_id
            opp_team = game.away_team if is_home else game.home_team
            opp_name = (
                f"{sanitize_fact_text(opp_team.city, 50)} {sanitize_fact_text(opp_team.name, 50)}".strip()
                if opp_team
                else f"Opponent {opp_id or 0}"
            )
            team_score = int(game.home_score or 0) if is_home else int(game.away_score or 0)
            opp_score = int(game.away_score or 0) if is_home else int(game.home_score or 0)
            if team_score > opp_score:
                outcome = "defeated"
            elif team_score < opp_score:
                outcome = "fell to"
            else:
                outcome = "tied"

            game_week = int(game.week or 1)
            facts.append(
                FactItem(
                    fact_id="last_game_result",
                    category="last_game",
                    label="Last Game Result",
                    value=sanitize_fact_text(
                        f"Week {game_week}: {team_name} {outcome} {opp_name} {team_score}-{opp_score}"
                    ),
                )
            )
        else:
            facts.append(
                FactItem(
                    fact_id="last_game_none",
                    category="last_game",
                    label="Season Opener Status",
                    value=sanitize_fact_text(
                        f"{team_name} enters Week {current_week} of the {season_year} campaign with 0 games played"
                    ),
                )
            )

        # Contextual coordinator fact: upcoming game on the schedule for current_week
        upcoming_game = next(
            (g for g in all_team_games if not g.is_played and g.week == current_week),
            None,
        )
        if upcoming_game:
            is_home_next = upcoming_game.home_team_id == team_id
            opp_next_id = (
                upcoming_game.away_team_id if is_home_next else upcoming_game.home_team_id
            )
            opp_next_team = (
                upcoming_game.away_team if is_home_next else upcoming_game.home_team
            )
            opp_next_name = (
                f"{sanitize_fact_text(opp_next_team.city, 50)} {sanitize_fact_text(opp_next_team.name, 50)}".strip()
                if opp_next_team
                else f"Opponent {opp_next_id or 0}"
            )
            venue_txt = "at home" if is_home_next else f"on the road at {opp_next_name}"
            facts.append(
                FactItem(
                    fact_id="upcoming_matchup",
                    category="season",
                    label="Upcoming Matchup",
                    value=sanitize_fact_text(
                        f"Week {current_week}: {team_name} faces {opp_next_name} {venue_txt}"
                    ),
                )
            )

        return computed_record

    def _append_season_facts(
        self,
        facts: list[FactItem],
        team: Team | None,
        team_id: int,
        team_record: str,
        season: Season | None,
        season_year: int,
        current_week: int,
    ) -> None:
        raw_status = (
            str(season.status.value if hasattr(season.status, "value") else season.status)
            if season and season.status
            else "REGULAR_SEASON"
        )
        status_label = raw_status.replace("_", " ").title()
        div_label = (
            f"{sanitize_fact_text(team.conference, 20)} {sanitize_fact_text(team.division, 20)}".strip()
            if team and (team.conference or team.division)
            else "League"
        )
        facts.append(
            FactItem(
                fact_id="season_standing",
                category="season",
                label="Season Record & Standing",
                value=sanitize_fact_text(
                    f"{season_year} Week {current_week} ({status_label}): {team_record} in {div_label}"
                ),
            )
        )

        season_stats = (
            next(
                (s for s in getattr(team, "season_history", []) if s.year == season_year),
                None,
            )
            if team
            else None
        )
        if season_stats:
            pf = int(season_stats.points_for or 0)
            pa = int(season_stats.points_against or 0)
            rank_part = (
                f", Division Rank #{int(season_stats.division_rank)}"
                if season_stats.division_rank is not None
                else ""
            )
            facts.append(
                FactItem(
                    fact_id="season_scoring_diff",
                    category="season",
                    label="Season Scoring Profile",
                    value=sanitize_fact_text(
                        f"{pf} points scored vs {pa} points allowed{rank_part}"
                    ),
                )
            )

    def _append_franchise_facts(
        self,
        facts: list[FactItem],
        team: Team | None,
        team_id: int,
        team_name: str,
    ) -> None:
        history_rows = (
            self.db.query(SeasonHistory)
            .filter(
                or_(
                    SeasonHistory.champion_team_id == team_id,
                    SeasonHistory.runner_up_team_id == team_id,
                )
            )
            .order_by(desc(SeasonHistory.year))
            .all()
        )
        championships = [h for h in history_rows if h.champion_team_id == team_id]
        runner_ups = [h for h in history_rows if h.runner_up_team_id == team_id]

        if championships:
            years_str = ", ".join(str(c.year) for c in championships[:4] if c.year is not None)
            facts.append(
                FactItem(
                    fact_id="franchise_championships",
                    category="franchise",
                    label="Championship Pedigree",
                    value=sanitize_fact_text(
                        f"{len(championships)} league title(s) ({years_str}) and {len(runner_ups)} runner-up finish(es)"
                    ),
                )
            )
        elif team is not None:
            prestige = int(team.prestige or 50)
            elo = int(round(float(team.elo_rating or 1500.0)))
            facts.append(
                FactItem(
                    fact_id="franchise_profile",
                    category="franchise",
                    label="Franchise Prestige & Rating",
                    value=sanitize_fact_text(
                        f"{team_name} holds {prestige} franchise prestige and a {elo} Elo rating with 0 league titles recorded"
                    ),
                )
            )
        else:
            facts.append(
                FactItem(
                    fact_id="franchise_profile",
                    category="franchise",
                    label="Franchise Status",
                    value=sanitize_fact_text(f"{team_name} active in the {team_id} franchise slot"),
                )
            )

    def _append_storyline_facts(
        self,
        facts: list[FactItem],
        team_id: int,
        season_id: int | None,
        current_week: int,
    ) -> None:
        active_storylines = storyline_service.get_active_storylines(team_id=team_id)
        for idx, sl in enumerate(active_storylines[:2]):
            sl_type = sanitize_fact_text(str(sl.get("type", "STORYLINE")), 40)
            intensity = int(sl.get("intensity", 1))
            start_week = int(sl.get("start_week", current_week))
            facts.append(
                FactItem(
                    fact_id=f"storyline_active_{idx + 1}",
                    category="storyline",
                    label="Developing Storyline",
                    value=sanitize_fact_text(
                        f"{sl_type} storyline active since Week {start_week} (intensity {intensity})"
                    ),
                )
            )

        recap_query = self.db.query(WeeklyRecap)
        if season_id is not None:
            recap_query = recap_query.filter(WeeklyRecap.season_id == season_id)
        latest_recap = recap_query.order_by(desc(WeeklyRecap.week), desc(WeeklyRecap.id)).first()
        if latest_recap and latest_recap.summary_text:
            facts.append(
                FactItem(
                    fact_id="storyline_weekly_recap",
                    category="storyline",
                    label=f"Week {int(latest_recap.week)} League Recap",
                    value=sanitize_fact_text(latest_recap.summary_text),
                )
            )

        if not any(f.category == "storyline" for f in facts):
            facts.append(
                FactItem(
                    fact_id="storyline_default",
                    category="storyline",
                    label="Broadcast Storyline",
                    value=sanitize_fact_text(
                        f"Week {current_week} preparation underway across the front office"
                    ),
                )
            )
