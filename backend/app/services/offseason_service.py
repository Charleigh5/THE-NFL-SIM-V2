from sqlalchemy.orm import Session
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.player import Player, DevelopmentTrait
from app.models.coach import Coach
from app.models.draft import DraftPick
from app.models.playoff import PlayoffMatchup, PlayoffRound
from app.services.standings_calculator import StandingsCalculator
from app.services.rookie_generator import RookieGenerator
import random
from typing import List, Optional
from app.schemas.offseason import TeamNeed, Prospect, DraftPickSummary, PlayerProgressionResult
from app.models.hall_of_fame import HallOfFame
from app.models.stats import PlayerGameStats
from sqlalchemy import func, select
from app.core.random_utils import DeterministicRNG
from app.core.roster_cache import (
    invalidate_team_roster_cache,
    invalidate_all_team_roster_caches,
)

class OffseasonService:
    def __init__(self, db: Session, seed: int = None):
        self.db = db
        self.standings_calculator = StandingsCalculator(db)
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))
        self.rookie_generator = RookieGenerator(db, seed=self.rng.randint(0, 1000000))

    async def start_offseason(self, season_id: int) -> dict:
        """Transition from Super Bowl to Offseason."""
        season = self.db.get(Season, season_id)
        if not season:
            raise ValueError("Season not found")

        season.status = SeasonStatus.OFF_SEASON

        try:
            # 0. Archive completed season stats for all players and teams
            archived_players = self.archive_season_stats(season_id)

            # 0b. Process season-end milestone trait acquisitions
            try:
                from app.services.trait_acquisition_service import TraitAcquisitionService
                TraitAcquisitionService.process_season_end_progression(self.db, season_id)
            except Exception as e:
                print(f"Warning: error during trait progression: {e}")

            # 1. Process Retirements
            self.process_retirements(season_id)

            # 2. Process Contracts
            self.process_contract_expirations()

            # 3. Generate Draft Order
            stmt = select(DraftPick).where(DraftPick.season_id == season_id)
            existing_picks = self.db.execute(stmt).first()
            if not existing_picks:
                self.generate_draft_order(season_id)

            # 4. Generate Rookie Class
            await self.rookie_generator.generate_draft_class(season_id)

            self.db.commit()
            return {
                "message": f"Offseason started. Archived stats for {archived_players} players. Contracts processed, Draft order set, Rookies generated."
            }
        except Exception as e:
            print(f"Error starting offseason: {e}")
            self.db.rollback()
            raise e

    def archive_season_stats(self, season_id: int) -> int:
        """
        Aggregate and archive all player, team, and league stats for a completed season
        into PlayerSeasonStats, TeamSeasonStats, and SeasonHistory.
        """
        season = self.db.get(Season, season_id)
        if not season:
            return 0

        from app.models.history import PlayerSeasonStats, SeasonHistory, TeamSeasonStats

        # Group and sum PlayerGameStats by player_id
        stmt = select(
            PlayerGameStats.player_id,
            PlayerGameStats.team_id,
            func.count(PlayerGameStats.id).label("games_played"),
            func.sum(PlayerGameStats.pass_yards).label("pass_yards"),
            func.sum(PlayerGameStats.pass_tds).label("pass_tds"),
            func.sum(PlayerGameStats.pass_ints).label("pass_ints"),
            func.sum(PlayerGameStats.pass_attempts).label("pass_attempts"),
            func.sum(PlayerGameStats.pass_completions).label("pass_completions"),
            func.sum(PlayerGameStats.rush_yards).label("rush_yards"),
            func.sum(PlayerGameStats.rush_tds).label("rush_tds"),
            func.sum(PlayerGameStats.rush_attempts).label("rush_attempts"),
            func.sum(PlayerGameStats.yards_after_contact).label("yards_after_contact"),
            func.sum(PlayerGameStats.broken_tackles).label("broken_tackles"),
            func.sum(PlayerGameStats.rec_yards).label("rec_yards"),
            func.sum(PlayerGameStats.rec_tds).label("rec_tds"),
            func.sum(PlayerGameStats.receptions).label("receptions"),
            func.sum(PlayerGameStats.drops).label("drops"),
            func.sum(PlayerGameStats.yards_after_catch).label("yards_after_catch"),
            func.sum(PlayerGameStats.tackles_solo).label("tackles_solo"),
            func.sum(PlayerGameStats.tackles_assist).label("tackles_assist"),
            func.sum(PlayerGameStats.sacks).label("sacks"),
            func.sum(PlayerGameStats.interceptions).label("interceptions"),
            func.sum(PlayerGameStats.pass_deflections).label("pass_deflections"),
            func.sum(PlayerGameStats.forced_fumbles).label("forced_fumbles"),
            func.sum(PlayerGameStats.tackles_for_loss).label("tackles_for_loss"),
            func.sum(PlayerGameStats.qb_pressures).label("qb_pressures"),
            func.sum(PlayerGameStats.fg_made).label("fg_made"),
            func.sum(PlayerGameStats.fg_att).label("fg_att"),
            func.sum(PlayerGameStats.punt_yards).label("punt_yards"),
            func.sum(PlayerGameStats.punt_att).label("punt_att"),
            func.sum(PlayerGameStats.pancakes).label("pancakes"),
            func.sum(PlayerGameStats.sacks_allowed).label("sacks_allowed"),
            func.sum(PlayerGameStats.pressures_allowed).label("pressures_allowed")
        ).where(
            PlayerGameStats.season_id == season_id
        ).group_by(PlayerGameStats.player_id, PlayerGameStats.team_id)

        results = self.db.execute(stmt).all()
        archived_count = 0

        for r in results:
            existing = self.db.query(PlayerSeasonStats).filter(
                PlayerSeasonStats.player_id == r.player_id,
                PlayerSeasonStats.season_id == season_id
            ).first()

            total_tackles = int((r.tackles_solo or 0) + (r.tackles_assist or 0))

            if not existing:
                pss = PlayerSeasonStats(
                    player_id=r.player_id,
                    season_id=season_id,
                    team_id=r.team_id,
                    year=season.year,
                    games_played=r.games_played or 0,
                    games_started=r.games_played or 0,
                    pass_yards=int(r.pass_yards or 0),
                    pass_tds=int(r.pass_tds or 0),
                    pass_ints=int(r.pass_ints or 0),
                    pass_attempts=int(r.pass_attempts or 0),
                    pass_completions=int(r.pass_completions or 0),
                    rush_yards=int(r.rush_yards or 0),
                    rush_tds=int(r.rush_tds or 0),
                    rush_attempts=int(r.rush_attempts or 0),
                    yards_after_contact=int(r.yards_after_contact or 0),
                    broken_tackles=int(r.broken_tackles or 0),
                    rec_yards=int(r.rec_yards or 0),
                    rec_tds=int(r.rec_tds or 0),
                    receptions=int(r.receptions or 0),
                    drops=int(r.drops or 0),
                    yards_after_catch=int(r.yards_after_catch or 0),
                    tackles=total_tackles,
                    tackles_solo=int(r.tackles_solo or 0),
                    tackles_assist=int(r.tackles_assist or 0),
                    sacks=float(r.sacks or 0.0),
                    interceptions=int(r.interceptions or 0),
                    pass_deflections=int(r.pass_deflections or 0),
                    forced_fumbles=int(r.forced_fumbles or 0),
                    tackles_for_loss=int(r.tackles_for_loss or 0),
                    qb_pressures=int(r.qb_pressures or 0),
                    fg_made=int(r.fg_made or 0),
                    fg_att=int(r.fg_att or 0),
                    punt_yards=int(r.punt_yards or 0),
                    punt_att=int(r.punt_att or 0),
                    pancakes=int(r.pancakes or 0),
                    sacks_allowed=int(r.sacks_allowed or 0),
                    pressures_allowed=int(r.pressures_allowed or 0)
                )
                self.db.add(pss)
            else:
                existing.games_played = r.games_played or 0
                existing.pass_yards = int(r.pass_yards or 0)
                existing.pass_tds = int(r.pass_tds or 0)
                existing.pass_ints = int(r.pass_ints or 0)
                existing.pass_attempts = int(r.pass_attempts or 0)
                existing.pass_completions = int(r.pass_completions or 0)
                existing.rush_yards = int(r.rush_yards or 0)
                existing.rush_tds = int(r.rush_tds or 0)
                existing.rush_attempts = int(r.rush_attempts or 0)
                existing.rec_yards = int(r.rec_yards or 0)
                existing.rec_tds = int(r.rec_tds or 0)
                existing.receptions = int(r.receptions or 0)
                existing.tackles = total_tackles
                existing.tackles_solo = int(r.tackles_solo or 0)
                existing.tackles_assist = int(r.tackles_assist or 0)
                existing.sacks = float(r.sacks or 0.0)
                existing.interceptions = int(r.interceptions or 0)
                existing.pass_deflections = int(r.pass_deflections or 0)
                existing.forced_fumbles = int(r.forced_fumbles or 0)
                existing.tackles_for_loss = int(r.tackles_for_loss or 0)
                existing.fg_made = int(r.fg_made or 0)
                existing.fg_att = int(r.fg_att or 0)
                existing.punt_yards = int(r.punt_yards or 0)
                existing.pancakes = int(r.pancakes or 0)
                existing.sacks_allowed = int(r.sacks_allowed or 0)
            archived_count += 1

        # 2. Archive TeamSeasonStats
        try:
            standings = self.standings_calculator.calculate_standings(season_id)
            for s in standings:
                team_stat = self.db.query(TeamSeasonStats).filter(
                    TeamSeasonStats.team_id == s.team_id,
                    TeamSeasonStats.year == season.year
                ).first()
                if not team_stat:
                    team_stat = TeamSeasonStats(
                        team_id=s.team_id,
                        year=season.year,
                        wins=s.wins,
                        losses=s.losses,
                        ties=s.ties,
                        points_for=s.points_for,
                        points_against=s.points_against,
                        division_rank=s.division_rank,
                        made_playoffs=(s.playoff_seed is not None)
                    )
                    self.db.add(team_stat)
        except Exception as e:
            print(f"Warning: could not calculate standings for team stats archive: {e}")

        self.db.flush()
        return archived_count


    def simulate_player_progression(self, season_id: int) -> List[PlayerProgressionResult]:
        """Simulate player progression and regression based on age and experience."""
        # Query only active roster players
        stmt = select(Player).where(Player.team_id != None)
        players = list(self.db.execute(stmt).scalars().all())
        progression_results = []

        # Position-specific decline start ages (RPG-003)
        DECLINE_STARTS = {
            "RB": 26, "FB": 27,  # Speed positions decline earliest
            "WR": 29, "TE": 30,  # Receivers slightly later
            "CB": 28, "S": 29,   # DBs rely on speed
            "LB": 29, "DE": 30, "DT": 31,  # Front 7 varies
            "OT": 32, "OG": 32, "C": 32,   # OL peak late
            "QB": 35, "K": 38, "P": 38     # Mental/technique positions
        }

        # Position-specific peak ages (optimal development window)
        PEAK_STARTS = {
            "RB": 24, "FB": 25, "WR": 26, "TE": 26,
            "CB": 25, "S": 26, "LB": 26, "DE": 26, "DT": 27,
            "OT": 27, "OG": 27, "C": 27, "QB": 28, "K": 30, "P": 30
        }

        for player in players:
            old_rating = player.overall_rating

            # Get position-specific thresholds
            decline_age = DECLINE_STARTS.get(player.position, 30)
            peak_start = PEAK_STARTS.get(player.position, 26)

            # Age-based rating change with position-specific curves
            age_change = 0
            if player.age < peak_start - 2:
                # Young players: Strong growth (+1 to +3)
                age_change = self.rng.randint(1, 3)
            elif player.age < peak_start:
                # Approaching peak: Moderate growth (+0 to +2)
                age_change = self.rng.randint(0, 2)
            elif player.age <= decline_age:
                # Peak years: Maintain or slight improvement (-1 to +1)
                age_change = self.rng.randint(-1, 1)
            elif player.age <= decline_age + 3:
                # Gradual decline: (-2 to +0)
                age_change = self.rng.randint(-2, 0)
            else:
                # Significant decline: (-3 to -1)
                age_change = self.rng.randint(-3, -1)

            # Experience factor adjustment
            exp_modifier = 0
            if player.experience <= 2:
                # Young players more likely to improve
                exp_modifier = self.rng.randint(0, 2)
            elif player.experience >= 8:
                # Veterans more likely to decline
                exp_modifier = self.rng.randint(-2, 0)

            # Random variance
            variance = self.rng.randint(-1, 1)

            # Dev Trait Modifier
            dev_trait_mod = 0
            if player.development_trait == DevelopmentTrait.STAR:
                dev_trait_mod = 1
            elif player.development_trait == DevelopmentTrait.SUPERSTAR:
                dev_trait_mod = 2
            elif player.development_trait == DevelopmentTrait.XFACTOR:
                dev_trait_mod = 3

            # Coach Modifier
            coach_mod = 0
            if player.team:
                head_coach = next((c for c in player.team.coaches if c.role == "Head Coach"), None)
                if head_coach:
                    # Rating 50 is neutral. Every 10 points is +/- 1 modifier chance?
                    # Let's just add small bonus for high rating
                    if head_coach.development_rating > 70:
                        coach_mod = 1
                    elif head_coach.development_rating < 30:
                        coach_mod = -1

            # Total change
            total_change = age_change + exp_modifier + variance + dev_trait_mod + coach_mod

            # Apply change and clamp between 40-99
            new_rating = max(40, min(99, old_rating + total_change))
            actual_change = new_rating - old_rating

            # Update player
            player.overall_rating = new_rating
            player.age += 1
            player.experience += 1

            # Store result
            progression_results.append(
                PlayerProgressionResult(
                    player_id=player.id,
                    name=f"{player.first_name} {player.last_name}",
                    position=player.position,
                    change=actual_change,
                    old_rating=old_rating,
                    new_rating=new_rating
                )
            )

        self.db.commit()
        return progression_results

    def process_contract_expirations(self) -> None:
        """Decrement contract years and release expired players."""
        stmt = select(Player).where(Player.team_id != None)
        players = list(self.db.execute(stmt).scalars().all())
        for player in players:
            player.contract_years -= 1
            if player.contract_years <= 0:
                player.team_id = None # Released to Free Agency
                player.contract_years = 0
        invalidate_all_team_roster_caches()

    def generate_draft_order(self, season_id: int) -> None:
        """Generate 7 rounds of draft picks based on reverse standings."""
        # 1. Get Standings
        standings = self.standings_calculator.calculate_standings(season_id)
        if not standings:
            # Fallback: Get all teams if standings are empty (e.g. new season or error)
            # But this shouldn't happen after a played season.
            # If it does, we can't really generate a draft order based on merit.
            # Let's just log and maybe return or use random order?
            # For now, let's assume we need standings.
            print("Error: No standings found for draft order generation.")
            # We could try to fetch teams directly but they won't have win_percentage
            # Let's try to fetch teams and give them default stats so we don't crash
            # But the code below expects objects with win_percentage, etc.
            # So let's just raise an error or return to avoid crash
            raise ValueError("Cannot generate draft order: No standings data found.")

        # 2. Adjust for Playoffs (Super Bowl winner last, etc.)
        # Simplified: Just use reverse standings for non-playoff teams,
        # and append playoff teams based on elimination round?
        # MVP: Just reverse standings for everyone, then swap SB winner to last.

        # Sort by record (worst to best)
        # Note: Standings are already sorted best to worst by calculate_standings
        # We want worst to best for draft order
        standings.sort(key=lambda x: (getattr(x, "win_percentage", getattr(x, "win_pct", 0.0)), x.wins, x.point_differential))

        # Find SB Winner and Loser to move to end
        stmt = select(PlayoffMatchup).where(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.SUPER_BOWL
        )
        sb_matchup = self.db.execute(stmt).scalar_one_or_none()

        ordered_team_ids = [s.team_id for s in standings]

        if sb_matchup and sb_matchup.winner_id:
            winner_id = sb_matchup.winner_id
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id

            if winner_id in ordered_team_ids:
                ordered_team_ids.remove(winner_id)
                ordered_team_ids.append(winner_id) # Last

            if loser_id in ordered_team_ids:
                ordered_team_ids.remove(loser_id)
                ordered_team_ids.insert(len(ordered_team_ids)-1, loser_id) # Second to last
        elif not sb_matchup:
            print("Warning: No Super Bowl matchup found for draft order generation.")

        # Create Picks
        for round_num in range(1, 8):
            for i, team_id in enumerate(ordered_team_ids):
                pick = DraftPick(
                    season_id=season_id,
                    team_id=team_id,
                    original_team_id=team_id,
                    round=round_num,
                    pick_number=(round_num - 1) * 32 + (i + 1),
                    player_id=None
                )
                self.db.add(pick)

    def _get_team_needs(self, team_id: int) -> dict:
        """Analyze roster and return count of players by position."""
        stmt = select(Player).where(Player.team_id == team_id)
        players = list(self.db.execute(stmt).scalars().all())
        position_counts = {}
        for p in players:
            position_counts[p.position] = position_counts.get(p.position, 0) + 1
        return position_counts

    def get_team_needs(self, team_id: int) -> List[TeamNeed]:
        """Get structured team needs analysis."""
        needs_dict = self._get_team_needs(team_id)
        TARGET_COUNTS = {
            "QB": 3, "RB": 4, "WR": 6, "TE": 3, "OT": 4, "OG": 4, "C": 2,
            "DE": 4, "DT": 4, "LB": 6, "CB": 6, "S": 4, "K": 1, "P": 1
        }

        result = []
        for pos, target in TARGET_COUNTS.items():
            current = needs_dict.get(pos, 0)
            diff = target - current
            score = max(0, diff)

            result.append(TeamNeed(
                position=pos,
                current_count=current,
                target_count=target,
                need_score=float(score)
            ))

        result.sort(key=lambda x: x.need_score, reverse=True)
        return result

    def get_top_prospects(self, limit: int = 50) -> List[Prospect]:
        """Get top available rookie prospects."""
        stmt = select(Player).where(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(limit)
        rookies = list(self.db.execute(stmt).scalars().all())

        return [
            Prospect(
                id=p.id,
                name=f"{p.first_name} {p.last_name}",
                position=p.position,
                overall_rating=p.overall_rating
            ) for p in rookies
        ]

    def get_current_pick(self, season_id: int) -> Optional[DraftPick]:
        """Get the next available draft pick."""
        stmt = select(DraftPick).where(
            DraftPick.season_id == season_id,
            DraftPick.player_id == None
        ).order_by(DraftPick.pick_number)
        return self.db.execute(stmt).scalars().first()

    def make_pick(self, season_id: int, player_id: int) -> DraftPick:
        """Make a draft pick for the current slot."""
        pick = self.get_current_pick(season_id)
        if not pick:
            raise ValueError("No picks remaining in the draft.")

        player = self.db.get(Player, player_id)
        if not player:
            raise ValueError("Player not found.")
        if player.team_id is not None:
             raise ValueError("Player already on a team.")

        # Assign player to team
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False

        self.db.commit()
        invalidate_team_roster_cache(pick.team_id)
        return pick

    def trade_current_pick(self, season_id: int, target_team_id: int) -> DraftPick:
        """Trade the current pick to another team."""
        pick = self.get_current_pick(season_id)
        if not pick:
            raise ValueError("No active pick to trade.")

        pick.team_id = target_team_id
        self.db.commit()
        return pick

    def simulate_next_pick(self, season_id: int) -> Optional[DraftPickSummary]:
        """Simulate the next single pick in the draft."""
        pick = self.get_current_pick(season_id)
        if not pick:
            return None

        # Get available rookies
        # Optimization: Just get top 20 to choose from
        stmt = select(Player).where(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(20)
        rookies = list(self.db.execute(stmt).scalars().all())

        if not rookies:
            return None

        rookie_pool = list(rookies)
        team_needs = self._get_team_needs(pick.team_id)

        TARGET_COUNTS = {
            "QB": 3, "RB": 4, "WR": 6, "TE": 3, "OT": 4, "OG": 4, "C": 2,
            "DE": 4, "DT": 4, "LB": 6, "CB": 6, "S": 4, "K": 1, "P": 1
        }

        selected_player = None

        # 1. Look for high-value need
        for i, prospect in enumerate(rookie_pool):
            if i > 10:
                break

            current_count = team_needs.get(prospect.position, 0)
            target = TARGET_COUNTS.get(prospect.position, 5)

            if current_count < target:
                selected_player = prospect
                break

        # 2. BPA
        if not selected_player:
            selected_player = rookie_pool[0]

        # Execute pick
        return self._execute_pick(pick, selected_player)

    def _execute_pick(self, pick: DraftPick, player: Player) -> DraftPickSummary:
        """Internal helper to execute a pick."""
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False

        self.db.commit()
        invalidate_team_roster_cache(pick.team_id)

        return DraftPickSummary(
            round=pick.round,
            pick_number=pick.pick_number,
            team_id=pick.team_id,
            player_name=f"{player.first_name} {player.last_name}",
            player_position=player.position,
            player_overall=player.overall_rating
        )

    def simulate_draft(self, season_id: int) -> List[DraftPickSummary]:
        """Simulate the remainder of the draft."""
        summary = []
        while True:
            result = self.simulate_next_pick(season_id)
            if not result:
                break
            summary.append(result)

        invalidate_all_team_roster_caches()
        return summary

    def simulate_free_agency(self, season_id: int) -> dict:
        """Fill rosters with free agents."""
        stmt = select(Team)
        teams = list(self.db.execute(stmt).scalars().all())

        # Get available FAs
        stmt_fa = select(Player).where(Player.team_id == None).order_by(Player.overall_rating.desc())
        free_agents = list(self.db.execute(stmt_fa).scalars().all())
        fa_pool = list(free_agents)

        for team in teams:
            # Check roster size
            stmt_count = select(func.count()).select_from(Player).where(Player.team_id == team.id)
            roster_count = self.db.execute(stmt_count).scalar() or 0
            needed = 53 - roster_count

            if needed > 0:
                # Sign top available players
                # Real logic would check positions
                for _ in range(needed):
                    if not fa_pool:
                        break
                    player = fa_pool.pop(0)
                    player.team_id = team.id
                    player.contract_years = 1

        self.db.commit()
        invalidate_all_team_roster_caches()
        return {"message": "Free Agency simulated."}

    def process_retirements(self, season_id: int) -> List[str]:
        """Process player retirements based on age and rating."""
        season = self.db.get(Season, season_id)
        if not season:
            return []

        stmt = select(Player).where(
            Player.is_retired == False,
            Player.team_id != None
        )
        players = list(self.db.execute(stmt).scalars().all())

        retired_names = []

        for player in players:
            should_retire = False

            # Base logic
            if player.age >= 40:
                should_retire = True
            elif player.age >= 35:
                # High chance if rating is low
                if player.overall_rating < 75:
                    should_retire = self.rng.random() < 0.5
                else:
                    should_retire = self.rng.random() < 0.1
            elif player.age >= 30:
                if player.overall_rating < 65:
                    should_retire = self.rng.random() < 0.2

            if should_retire:
                player.is_retired = True
                player.retirement_year = season.year
                player.team_id = None
                retired_names.append(f"{player.first_name} {player.last_name}")

                # Check Hall of Fame
                self._check_hall_of_fame(player, season.year)

        self.db.commit()
        invalidate_all_team_roster_caches()
        return retired_names

    def _check_hall_of_fame(self, player: Player, year: int):
        """Check if a retired player qualifies for the Hall of Fame."""
        # Simple criteria for MVP: High Overall or High Legacy Score
        is_hof = False
        if player.overall_rating >= 90: # Lowered slightly for MVP testing
            is_hof = True
        elif player.legacy_score >= 1000:
            is_hof = True

        if is_hof:
            stats = self._calculate_career_stats(player.id)
            hof_entry = HallOfFame(
                player_id=player.id,
                year_inducted=year,
                career_stats_snapshot=stats
            )
            self.db.add(hof_entry)

    def _calculate_career_stats(self, player_id: int) -> dict:
        """Aggregate full multi-position career stats for a player."""
        stmt = select(
            func.sum(PlayerGameStats.pass_yards).label("pass_yards"),
            func.sum(PlayerGameStats.pass_tds).label("pass_tds"),
            func.sum(PlayerGameStats.rush_yards).label("rush_yards"),
            func.sum(PlayerGameStats.rush_tds).label("rush_tds"),
            func.sum(PlayerGameStats.rec_yards).label("rec_yards"),
            func.sum(PlayerGameStats.rec_tds).label("rec_tds"),
            func.sum(PlayerGameStats.tackles_solo).label("tackles_solo"),
            func.sum(PlayerGameStats.tackles_assist).label("tackles_assist"),
            func.sum(PlayerGameStats.sacks).label("sacks"),
            func.sum(PlayerGameStats.interceptions).label("interceptions"),
            func.sum(PlayerGameStats.pass_deflections).label("pass_deflections"),
            func.sum(PlayerGameStats.forced_fumbles).label("forced_fumbles"),
            func.sum(PlayerGameStats.tackles_for_loss).label("tackles_for_loss"),
            func.sum(PlayerGameStats.qb_pressures).label("qb_pressures"),
            func.sum(PlayerGameStats.fg_made).label("fg_made"),
            func.sum(PlayerGameStats.fg_att).label("fg_att"),
            func.sum(PlayerGameStats.punt_yards).label("punt_yards"),
            func.sum(PlayerGameStats.pancakes).label("pancakes"),
            func.sum(PlayerGameStats.sacks_allowed).label("sacks_allowed"),
            func.count(PlayerGameStats.id).label("games_played")
        ).where(PlayerGameStats.player_id == player_id)

        stats = self.db.execute(stmt).first()
        total_tackles = int((stats.tackles_solo or 0) + (stats.tackles_assist or 0)) if stats else 0

        return {
            "games_played": stats.games_played or 0 if stats else 0,
            "pass_yards": int(stats.pass_yards or 0) if stats else 0,
            "pass_tds": int(stats.pass_tds or 0) if stats else 0,
            "rush_yards": int(stats.rush_yards or 0) if stats else 0,
            "rush_tds": int(stats.rush_tds or 0) if stats else 0,
            "rec_yards": int(stats.rec_yards or 0) if stats else 0,
            "rec_tds": int(stats.rec_tds or 0) if stats else 0,
            "tackles": total_tackles,
            "tackles_solo": int(stats.tackles_solo or 0) if stats else 0,
            "tackles_assist": int(stats.tackles_assist or 0) if stats else 0,
            "sacks": float(stats.sacks or 0.0) if stats else 0.0,
            "interceptions": int(stats.interceptions or 0) if stats else 0,
            "pass_deflections": int(stats.pass_deflections or 0) if stats else 0,
            "forced_fumbles": int(stats.forced_fumbles or 0) if stats else 0,
            "tackles_for_loss": int(stats.tackles_for_loss or 0) if stats else 0,
            "qb_pressures": int(stats.qb_pressures or 0) if stats else 0,
            "fg_made": int(stats.fg_made or 0) if stats else 0,
            "fg_att": int(stats.fg_att or 0) if stats else 0,
            "punt_yards": int(stats.punt_yards or 0) if stats else 0,
            "pancakes": int(stats.pancakes or 0) if stats else 0,
            "sacks_allowed": int(stats.sacks_allowed or 0) if stats else 0,
        }
