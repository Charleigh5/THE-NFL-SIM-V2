from .play_commands import PlayCommand, PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult
import random
from app.orchestrator.kernels_interface import KernelInterface
from app.engine.probability_engine import ProbabilityEngine
from typing import Optional, Any

class PlayResolver:
    """
    Resolves a PlayCommand by orchestrating the various simulation kernels.
    """
    def __init__(self, kernels: Optional[KernelInterface] = None) -> None:
        self.kernels = kernels or KernelInterface()
        self.current_match_context = None

    def register_players(self, match_context: Any) -> None:
        """Register all players from the match context with the kernels."""
        self.current_match_context = match_context
        all_players = list(match_context.home_roster.values()) + list(match_context.away_roster.values())

        for p in all_players:
            # Extract initialized state from MatchContext
            fatigue_reg = match_context.get_fatigue(p.id)
            bio_profile = match_context.get_player_bio(p.id)

            fatigue_data = fatigue_reg.model_dump() if fatigue_reg else {}
            # anatomy data placeholder for now

            # Register with Genesis (Biology/Fatigue)
            self.kernels.genesis.register_player(p.id, {
                "anatomy": {},
                "fatigue": fatigue_data
            })

    def resolve_play(self, command: PlayCommand) -> PlayResult:
        """
        Executes the logic for a given play command.
        """
        if isinstance(command, PassPlayCommand):
            return self._resolve_pass_play(command)
        elif isinstance(command, RunPlayCommand):
            return self._resolve_run_play(command)

        # Add resolvers for other command types here
        return command.execute({})

    def _get_player_by_position(self, players: list, position_prefix: str) -> Optional[Any]:
        """Helper to find a player by position prefix (e.g., 'QB', 'WR')."""
        if not players:
            return None

        # Try to find exact match or prefix match
        for p in players:
            if p.position == position_prefix or p.position.startswith(position_prefix):
                return p

        # Fallback to first player if specific position not found
        return players[0]

    def _get_weather_temp(self) -> float:
        if self.current_match_context and self.current_match_context.weather_config:
            return self.current_match_context.weather_config.get("temperature", 75.0)
        return 75.0

    def _resolve_pass_play(self, command: PassPlayCommand) -> PlayResult:
        """
        Resolves a pass play using Kernel logic with attribute-based calculations.
        """
        # 1. Identify key players
        if not command.offense or not command.defense:
            return self._resolve_legacy_random_pass(command)

        qb = self._get_player_by_position(command.offense, "QB")
        target = self._get_player_by_position(command.offense, "WR") or \
                 self._get_player_by_position(command.offense, "TE") or \
                 command.offense[0]

        defender = self._get_player_by_position(command.defense, "CB") or \
                   self._get_player_by_position(command.defense, "S") or \
                   command.defense[0]

        # 2. Genesis Kernel: Calculate Fatigue & Injury Risk
        temp = self._get_weather_temp()
        current_fatigue = self.kernels.genesis.calculate_fatigue(qb.id, exertion=0.8, temperature=temp)
        # Injury Check
        injury_check = self.kernels.genesis.check_injury_risk(qb.id, impact_force=600.0, body_part="ACL")
        injuries = [injury_check] if injury_check["is_injured"] else []

        # 3. Attribute-Based Core Logic via ProbabilityEngine

        # A. Throw Accuracy vs Depth
        throw_accuracy = 50 # Default base
        if hasattr(qb, "throw_accuracy_short"):
             if command.depth == "short":
                 throw_accuracy = qb.throw_accuracy_short
             elif command.depth == "mid":
                 throw_accuracy = qb.throw_accuracy_mid
             elif command.depth == "deep":
                 throw_accuracy = qb.throw_accuracy_deep

        # B. Receiver vs Defender (Speed & Route Running)
        speed_diff = ProbabilityEngine.compare_speed(
            target.speed if hasattr(target, "speed") else 50,
            defender.speed if hasattr(defender, "speed") else 50
        )

        matchup_factor = ProbabilityEngine.compare_skill(
            target.route_running if hasattr(target, "route_running") else 50,
            defender.man_coverage if hasattr(defender, "man_coverage") else 50
        )

        # C. Weather Impact
        weather_penalty = 0
        if temp < 32: weather_penalty = 0.05
        elif temp > 90: weather_penalty = 0.02

        # D. Fatigue Impact
        fatigue_penalty = (current_fatigue / 100.0) * 0.10

        # E. Final Probability Calculation
        # Normalize throw accuracy (0-100) to 0.0-1.0 base probability
        base_prob = throw_accuracy / 100.0

        # Modifiers are already in float format (-0.2 to 0.2)
        attr_modifiers = speed_diff + matchup_factor

        success_chance = ProbabilityEngine.calculate_success_chance(
            base_probability=base_prob,
            attribute_modifiers=attr_modifiers,
            context_modifiers=-weather_penalty,
            fatigue_penalty=fatigue_penalty
        )

        # F. Resolve Outcome
        is_complete = ProbabilityEngine.resolve_outcome(success_chance)

        if is_complete:
            # Calculate Yards Gained
            if command.depth == "short":
                base_yards = 5.0
                variance = 3.0
            elif command.depth == "mid":
                base_yards = 12.0
                variance = 5.0
            else: # deep
                base_yards = 25.0
                variance = 10.0

            # YAC Bonus if WR is faster
            yac_bonus = 0.0
            if speed_diff > 0:
                yac_bonus = speed_diff * 50.0 # e.g. 0.10 diff * 50 = 5 yards

            yards_gained = int(ProbabilityEngine.calculate_variable_outcome(
                base_value=base_yards,
                variance=variance,
                modifiers=yac_bonus
            ))
            yards_gained = max(1, yards_gained) # Minimum 1 yard on completion

            # Touchdown check
            is_touchdown = False
            if yards_gained > 80:
                is_touchdown = True
            elif yards_gained > 20 and ProbabilityEngine.resolve_outcome(0.1):
                is_touchdown = True

            # 4. Empire Kernel: XP Awards
            xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})

            return PlayResult(
                yards_gained=yards_gained,
                is_touchdown=is_touchdown,
                description=f"Pass complete to {target.last_name} for {yards_gained} yards. (Prob: {int(success_chance*100)}%)",
                headline=f"Big play! {qb.last_name} connects with {target.last_name}!" if yards_gained > 20 else None,
                is_highlight_worthy=is_touchdown or yards_gained > 20,
                injuries=injuries,
                xp_awards=xp_result.get("xp_awards", {}),
                passer_id=qb.id,
                receiver_id=target.id
            )
        else:
            return PlayResult(
                yards_gained=0,
                description=f"Incomplete pass intended for {target.last_name}. (Prob: {int(success_chance*100)}%)",
                headline=None,
                injuries=injuries,
                passer_id=qb.id,
                receiver_id=target.id
            )


    def _resolve_run_play(self, command: RunPlayCommand) -> PlayResult:
        """
        Resolves a run play using Kernel logic with attribute-based calculations.
        """
        # 1. Identify key players
        if not command.offense or not command.defense:
            return PlayResult(yards_gained=random.randint(1, 5), description="Run play (Legacy)")

        rb = self._get_player_by_position(command.offense, "RB") or command.offense[0]

        # Find a defender based on run direction
        defender_pos = "DT" if command.run_direction == "middle" else "DE"
        defender = self._get_player_by_position(command.defense, defender_pos) or \
                   self._get_player_by_position(command.defense, "LB") or \
                   command.defense[0]

        # 2. Genesis Kernel: Fatigue
        temp = self._get_weather_temp()
        print(f"DEBUG: Resolving Run Play. RB ID: {rb.id}, Temp: {temp}")
        current_fatigue = self.kernels.genesis.calculate_fatigue(rb.id, exertion=1.0, temperature=temp)
        print(f"DEBUG: Calculated Fatigue: {current_fatigue}")

        # 3. Attribute Logic via ProbabilityEngine

        # Power Run (Strength vs Tackle)
        power_diff = ProbabilityEngine.compare_strength(
            rb.strength if hasattr(rb, "strength") else 50,
            defender.tackle if hasattr(defender, "tackle") else 50
        )

        # Speed (for outside runs)
        speed_diff = 0.0
        if command.run_direction != "middle":
            speed_diff = ProbabilityEngine.compare_speed(
                rb.speed if hasattr(rb, "speed") else 50,
                defender.speed if hasattr(defender, "speed") else 50
            )

        # Fatigue Penalty
        fatigue_penalty = (current_fatigue / 100.0) * 2.0 # Yards penalty

        # Calculate Base Yards
        # Middle run: consistent but lower ceiling
        # Outside run: higher variance
        if command.run_direction == "middle":
            base_yards = 3.0 + (power_diff * 10.0) # +/- 2 yards based on strength
            variance = 2.0
        else:
            base_yards = 2.0 + (speed_diff * 20.0) # +/- 4 yards based on speed
            variance = 4.0

        # Calculate Total Yards
        yards_gained = ProbabilityEngine.calculate_variable_outcome(
            base_value=base_yards,
            variance=variance,
            modifiers=-fatigue_penalty
        )

        # Breakaway Chance (Big Play)
        # If RB is much faster or stronger, chance to break free
        breakaway_chance = 0.05 + speed_diff + power_diff
        if yards_gained > 5 and ProbabilityEngine.resolve_outcome(breakaway_chance):
            bonus_yards = ProbabilityEngine.calculate_variable_outcome(20.0, 10.0)
            yards_gained += bonus_yards

        yards_gained = int(yards_gained)

        # Fumble Check
        # Base fumble rate 1%
        # Increased by fatigue and big hits (high defender strength)
        fumble_chance = 0.01
        if current_fatigue > 70: fumble_chance += 0.02
        if hasattr(defender, "hit_power") and defender.hit_power > 85: fumble_chance += 0.01
        if hasattr(rb, "ball_security") and rb.ball_security < 70: fumble_chance += 0.01

        is_fumble = ProbabilityEngine.resolve_outcome(fumble_chance)
        is_turnover = is_fumble # Simplified turnover logic

        is_touchdown = False
        if yards_gained > 80:
            is_touchdown = True
        elif yards_gained > 10 and yards_gained >= (100 - 20): # Assuming red zone logic handled elsewhere, simplified here
             # If yards gained is huge, likely TD
             pass

        # XP
        xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})

        return PlayResult(
            yards_gained=yards_gained,
            is_touchdown=is_touchdown,
            is_turnover=is_turnover,
            description=f"Run {command.run_direction} by {rb.last_name} for {yards_gained} yards.",
            headline=f"Big run! {rb.last_name} breaks free!" if yards_gained > 15 else None,
            is_highlight_worthy=is_touchdown or yards_gained > 15,
            xp_awards=xp_result.get("xp_awards", {}),
            rusher_id=rb.id
        )

    def _resolve_legacy_random_pass(self, command: PassPlayCommand) -> PlayResult:
        """Fallback for when no player data is available."""
        success_chance = 0.60
        is_complete = random.random() < success_chance

        if is_complete:
            yards_gained = random.randint(5, 25)
            is_touchdown = (yards_gained > 20) and (random.random() < 0.2)
            return PlayResult(
                yards_gained=yards_gained,
                is_touchdown=is_touchdown,
                description=f"Pass completed for {yards_gained} yards. (Legacy Mode)",
                is_highlight_worthy=is_touchdown or yards_gained > 20
            )
        else:
            return PlayResult(
                yards_gained=0,
                description="Incomplete pass. (Legacy Mode)"
            )
