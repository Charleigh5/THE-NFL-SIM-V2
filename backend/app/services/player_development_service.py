from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.player import Player, DevelopmentTrait, InjuryStatus
from app.models.team import Team
from app.models.coach import Coach
import random
from typing import List, Dict
from app.core.random_utils import DeterministicRNG

class TrainingFocus(str):
    GENERAL = "GENERAL"
    CONDITIONING = "CONDITIONING" # Recovery + Stamina
    FILM_STUDY = "FILM_STUDY" # Awareness + Play Rec
    DRILLS = "DRILLS" # Skill specific

class PlayerDevelopmentService:
    def __init__(self, db: AsyncSession, seed: int = None):
        self.db = db
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

    async def process_weekly_development(self, season_id: int, week: int):
        """
        Main entry point for weekly player updates during the season.
        Handles training XP, injury recovery, and morale updates.
        """
        stmt = select(Team).options(
            selectinload(Team.players),
            selectinload(Team.coaches)
        )
        result = await self.db.execute(stmt)
        teams = result.scalars().all()

        for team in teams:
            self._apply_team_training(team)
            self._process_team_injuries(team)
            self._update_team_morale(team)

        await self.db.commit()

    def _apply_team_training(self, team: Team):
        """Apply weekly training XP to all players on the team."""
        # Get Head Coach for development bonus
        head_coach = next((c for c in team.coaches if c.role == "Head Coach"), None)
        coach_bonus = 0
        if head_coach:
            # 0-100 rating -> 0.5 - 1.5 multiplier or flat bonus?
            # Let's say rating 50 is baseline.
            coach_bonus = (head_coach.development_rating - 50) / 100.0 # -0.5 to +0.5

        players = team.players
        for player in players:
            # Base XP
            xp_gain = 50

            # Dev Trait Multiplier
            if player.development_trait == DevelopmentTrait.STAR:
                xp_gain *= 1.25
            elif player.development_trait == DevelopmentTrait.SUPERSTAR:
                xp_gain *= 1.5
            elif player.development_trait == DevelopmentTrait.XFACTOR:
                xp_gain *= 2.0

            # Coach Bonus
            xp_gain *= (1.0 + coach_bonus)

            # Age Penalty/Bonus
            if player.age > 30:
                xp_gain *= 0.8
            elif player.age < 24:
                xp_gain *= 1.2

            player.xp += int(xp_gain)

            # Level Up Logic
            # Simple: 1000 XP = 1 Skill Point
            while player.xp >= 1000:
                player.xp -= 1000
                player.skill_points += 1
                # Auto-spend skill point for now or let user do it?
                # For MVP, auto-spend to increase Overall
                self._auto_upgrade_player(player)

    def _auto_upgrade_player(self, player: Player):
        """Automatically spend skill point to upgrade attributes."""
        # Pick 3 relevant attributes based on position and upgrade one
        # This effectively raises overall rating eventually
        # For simplicity, we just bump overall rating directly occasionally
        # or bump specific stats.

        # Let's bump specific stats based on position
        relevant_stats = self._get_relevant_stats(player.position)
        stat_to_boost = self.rng.choice(relevant_stats)

        current_val = getattr(player, stat_to_boost)
        if current_val < 99:
            setattr(player, stat_to_boost, current_val + 1)
            player.skill_points -= 1

            # Recalculate Overall (Simplified)
            # In a real system, overall is a formula of stats.
            # Here, we might just nudge it if enough stats improve.
            # For now, let's just assume overall ~ average of key stats
            # Or just leave overall as is and let a separate calculator handle it.
            # But we need overall to change for the user to see progress.
            player.overall_rating = min(99, player.overall_rating + 1)

    def _get_relevant_stats(self, position: str) -> List[str]:
        common = ["speed", "agility", "awareness", "strength"]
        if position == "QB":
            return common + ["throw_power", "throw_accuracy_short", "throw_accuracy_mid", "throw_accuracy_deep"]
        elif position in ["RB", "WR", "TE"]:
            return common + ["catching", "route_running"]
        elif position in ["OT", "OG", "C"]:
            return common + ["pass_block", "run_block"]
        elif position in ["DE", "DT", "LB"]:
            return common + ["tackle", "pass_rush_power", "block_shed"]
        elif position in ["CB", "S"]:
            return common + ["man_coverage", "zone_coverage", "tackle"]
        elif position in ["K", "P"]:
            return ["kick_power", "kick_accuracy"]
        return common

    def _process_team_injuries(self, team: Team):
        """Update recovery time for injured players."""
        for player in team.players:
            if player.injury_status != InjuryStatus.ACTIVE:
                if player.weeks_to_recovery > 0:
                    player.weeks_to_recovery -= 1

                if player.weeks_to_recovery <= 0:
                    player.injury_status = InjuryStatus.ACTIVE
                    player.injury_type = None
                    # Reset injury? Or keep history?

    def _update_team_morale(self, team: Team):
        """Update morale based on team performance and playing time."""
        # Simplified: Random fluctuation + Team Record influence
        win_pct = 0.5
        if (team.wins + team.losses) > 0:
            win_pct = team.wins / (team.wins + team.losses)

        for player in team.players:
            change = 0
            # Winning helps
            if win_pct > 0.6:
                change += self.rng.randint(0, 2)
            elif win_pct < 0.4:
                change -= self.rng.randint(0, 2)

            # Playing time (Starter vs Bench)
            if player.depth_chart_rank == 1:
                change += 1
            elif player.depth_chart_rank > 2:
                change -= 1

            # Clamp 0-100
            player.morale = max(0, min(100, player.morale + change))

    def generate_injury(self, player: Player, severity_roll: int):
        """
        Called when an injury event occurs (e.g. during game simulation).
        severity_roll: 0-100 scale of impact.
        """
        if severity_roll < 50:
            # Minor
            player.injury_type = "Minor Sprain"
            player.weeks_to_recovery = self.rng.randint(1, 2)
            player.injury_status = InjuryStatus.QUESTIONABLE
        elif severity_roll < 80:
            # Moderate
            player.injury_type = "Muscle Tear"
            player.weeks_to_recovery = self.rng.randint(3, 6)
            player.injury_status = InjuryStatus.OUT
        else:
            # Severe
            player.injury_type = "Major Fracture"
            player.weeks_to_recovery = self.rng.randint(8, 52)
            player.injury_status = InjuryStatus.IR
