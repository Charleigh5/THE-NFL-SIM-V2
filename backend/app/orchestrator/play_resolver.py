from .play_commands import PlayCommand, PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult
import random
from app.orchestrator.kernels_interface import KernelInterface
from app.engine.probability_engine import ProbabilityEngine, OutcomeType
from app.engine.blocking import BlockingEngine, BlockingResult
from app.engine.event_bus import EventBus, EventType
from app.engine.offensive_line_ai import OffensiveLineAI
from typing import Optional, Any, List, Tuple

class PlayResolver:
    """
    Resolves a PlayCommand by orchestrating the various simulation kernels.
    """
    def __init__(self, kernels: Optional[KernelInterface] = None) -> None:
        self.kernels = kernels or KernelInterface()
        self.current_match_context = None
        self.offensive_line_ai = OffensiveLineAI()

    def register_players(self, match_context: Any) -> None:
        """Register all players from the match context with the kernels."""
        self.current_match_context = match_context

        # Sync Genesis Kernel if MatchContext has one
        if hasattr(match_context, 'genesis') and match_context.genesis:
            self.kernels.genesis = match_context.genesis

        all_players = list(match_context.home_roster.values()) + list(match_context.away_roster.values())

        for p in all_players:
            # Extract initialized state from MatchContext
            fatigue_val = match_context.get_player_fatigue(p.id)
            # bio_profile = match_context.get_player_bio(p.id)

            fatigue_data = {"current_fatigue": fatigue_val}
            # anatomy data placeholder for now

            # Register with Genesis (Biology/Fatigue)
            # Note: MatchContext already registers players, so this might be redundant if we synced the kernel
            # But we keep it for safety or if using a different kernel instance
            if not hasattr(match_context, 'genesis') or not match_context.genesis:
                self.kernels.genesis.register_player(p.id, {
                    "anatomy": {},
                    "fatigue": fatigue_data
                })

    def resolve_play(self, command: PlayCommand) -> PlayResult:
        """
        Executes the logic for a given play command.
        """
        result = None
        if isinstance(command, PassPlayCommand):
            result = self._resolve_pass_play(command)
        elif isinstance(command, RunPlayCommand):
            result = self._resolve_run_play(command)
        else:
            # Add resolvers for other command types here
            result = command.execute({})

        # Decrement debuffs after every play
        self.offensive_line_ai.decrement_debuffs()
        return result

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

    def _resolve_line_battle(self, offense: List[Any], defense: List[Any]) -> Tuple[List[BlockingResult], List[Any], List[Any]]:
        """
        Simulate the battle between OL and DL.
        Returns (results, winning_defenders, beaten_linemen)
        """
        matchups = [
            ("LT", "RE"),
            ("RT", "LE"),
            ("C", "DT"),
            ("LG", "DT"),
            ("RG", "DT")
        ]

        results = []
        winning_defenders = []
        beaten_linemen = []

        for ol_pos, dl_pos in matchups:
            ol = self._get_player_by_position(offense, ol_pos)
            dl = self._get_player_by_position(defense, dl_pos)

            if not ol or not dl:
                continue

            # Get attributes
            ol_rating = getattr(ol, "pass_block", None) or 70
            dl_rating = getattr(dl, "pass_rush", None) or 70 # Assuming pass_rush attribute exists, else use power/finessef
            modifier = self.offensive_line_ai.get_player_modifier(ol.id)
            ol_rating += modifier

            # Resolve block
            result = BlockingEngine.resolve_pass_block(ol_rating, dl_rating)

            results.append(result)
            if result == BlockingResult.LOSS or result == BlockingResult.PANCAKE:
                winning_defenders.append(dl)
                beaten_linemen.append(ol)

        return results, winning_defenders, beaten_linemen

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
        # Use get_current_fatigue (read-only) for penalty calculation
        # Fatigue update happens in Orchestrator
        current_fatigue = self.kernels.genesis.get_current_fatigue(qb.id)

        # Injury Check
        injury_check = self.kernels.genesis.check_injury_risk(qb.id, impact_force=600.0, body_part="ACL")
        injuries = [injury_check] if injury_check["is_injured"] else []

        # 3. Line Battle & Sack Check
        block_results, sackers, beaten_ols = self._resolve_line_battle(command.offense, command.defense)

        # Determine if Sack occurred
        is_sack = False
        sacker = None
        beaten_ol = None

        # Pancake = Automatic Sack
        if BlockingResult.PANCAKE in block_results:
            is_sack = True
            idx = block_results.index(BlockingResult.PANCAKE)
            # Find corresponding sacker (approximate since we don't track idx in lists perfectly aligned if skips happen)
            # But sackers list only contains winners.
            # Let's just take the first one for simplicity or improve _resolve_line_battle to return structured data.
            if sackers:
                sacker = sackers[0]
                beaten_ol = beaten_ols[0]

        # Loss = Chance of Sack (with QB Pocket Presence mitigation)
        elif BlockingResult.LOSS in block_results:
            # Chance increases with number of losses
            loss_count = block_results.count(BlockingResult.LOSS)
            base_sack_chance = 0.20 * loss_count

            # QB POCKET PRESENCE MITIGATION (INT-001)
            # QB's ability to sense pressure reduces sack probability
            pocket_presence = getattr(qb, 'pocket_presence', 50) if qb else 50

            # Scale reduction: 0% at PP=0, up to 50% at PP=100
            sack_reduction_factor = (pocket_presence / 200.0)  # Max 0.5 reduction

            # Apply mitigation
            adjusted_sack_chance = base_sack_chance * (1 - sack_reduction_factor)

            if ProbabilityEngine.resolve_outcome(adjusted_sack_chance):
                is_sack = True
                if sackers:
                    sacker = sackers[0]
                    beaten_ol = beaten_ols[0]

        if is_sack:
            # SACK!
            loss_yards = random.randint(5, 10)

            # Publish Event
            if sacker and beaten_ol:
                intimidation_factor = 1.0
                # Check for Intimidation trait
                if hasattr(sacker, "traits"):
                    for trait in sacker.traits:
                        if trait.name == "Intimidation":
                            intimidation_factor = 1.5
                            break

                EventBus.publish(EventType.SACK_EVENT, {
                    "beaten_linemen_ids": [beaten_ol.id],
                    "sacker_id": sacker.id,
                    "intimidation_factor": intimidation_factor
                })

            return PlayResult(
                yards_gained=-loss_yards,
                is_touchdown=False,
                description=f"SACKED! {qb.last_name} is taken down by {sacker.last_name if sacker else 'the defense'} for a loss of {loss_yards} yards.",
                headline=f"Sack! {sacker.last_name if sacker else 'Defense'} gets home!",
                is_highlight_worthy=True,
                injuries=injuries,
                passer_id=qb.id
            )

        # 4. Attribute-Based Core Logic via ProbabilityEngine

        # A. Throw Accuracy vs Depth
        throw_accuracy = 50 # Default base
        if command.depth == "short":
             throw_accuracy = getattr(qb, "throw_accuracy_short", None) or 50
        elif command.depth == "mid":
             throw_accuracy = getattr(qb, "throw_accuracy_mid", None) or 50
        elif command.depth == "deep":
             throw_accuracy = getattr(qb, "throw_accuracy_deep", None) or 50

        # B. Receiver vs Defender (Speed & Route Running)
        speed_diff = ProbabilityEngine.compare_speed(
            getattr(target, "speed", None) or 50,
            getattr(defender, "speed", None) or 50
        )

        matchup_factor = ProbabilityEngine.compare_skill(
            getattr(target, "route_running", None) or 50,
            getattr(defender, "man_coverage", None) or 50
        )

        # C. Weather Impact
        weather_penalty = 0
        if temp < 32: weather_penalty = 0.05
        elif temp > 90: weather_penalty = 0.02

        # D. Fatigue Impact
        fatigue_penalty = (current_fatigue / 100.0) * 0.10

        # E. Pressure Impact
        pressure_penalty = 0.0
        if BlockingResult.LOSS in block_results:
             # Heavy pressure
             pressure_penalty = 0.25
        elif BlockingResult.STALEMATE in block_results:
             # Mild pressure
             pressure_penalty = 0.10

        # F. Final Probability Calculation
        # Normalize throw accuracy (0-100) to 0.0-1.0 base probability
        base_prob = throw_accuracy / 100.0

        # Modifiers are already in float format (-0.2 to 0.2)
        attr_modifiers = speed_diff + matchup_factor

        success_chance = ProbabilityEngine.calculate_success_chance(
            base_probability=base_prob,
            attribute_modifiers=attr_modifiers,
            context_modifiers=-weather_penalty - pressure_penalty,
            fatigue_penalty=fatigue_penalty
        )

        # G. Resolve Outcome
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
            # Normal Incomplete
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
        # print(f"DEBUG: Resolving Run Play. RB ID: {rb.id}, Temp: {temp}")
        # Use get_current_fatigue (read-only)
        current_fatigue = self.kernels.genesis.get_current_fatigue(rb.id)
        # print(f"DEBUG: Calculated Fatigue: {current_fatigue}")

        # 3. Attribute Logic via ProbabilityEngine

        # Power Run (Strength vs Tackle)
        power_diff = ProbabilityEngine.compare_strength(
            getattr(rb, "strength", None) or 50,
            getattr(defender, "tackle", None) or 50
        )

        # Speed (for outside runs)
        speed_diff = 0.0
        if command.run_direction != "middle":
            speed_diff = ProbabilityEngine.compare_speed(
                getattr(rb, "speed", None) or 50,
                getattr(defender, "speed", None) or 50
            )

        # Fatigue Penalty
        fatigue_penalty = (current_fatigue / 100.0) * 2.0 # Yards penalty

        # Calculate Base Yards
        # Middle run: consistent but lower ceiling
        # Outside run: higher variance
        if command.run_direction == "middle":
            base_yards = 3.5 + (power_diff * 10.0) # +/- 2 yards based on strength
            std_dev = 1.5
        else:
            base_yards = 2.5 + (speed_diff * 20.0) # +/- 4 yards based on speed
            std_dev = 3.0

        # Calculate Total Yards using Normal Distribution
        yards_gained = ProbabilityEngine.calculate_normal_outcome(
            mean=base_yards - fatigue_penalty,
            std_dev=std_dev,
            min_val=-5.0, # Can lose yards
            max_val=99.0
        )

        # Breakaway / Big Play Check
        # If RB is much faster or stronger, chance to break free
        breakaway_chance = 0.05 + speed_diff + power_diff

        # Use tiered outcome for the "Breakaway" check
        breakaway_outcome = ProbabilityEngine.resolve_tiered_outcome(breakaway_chance, critical_threshold=0.20)

        headline = None
        is_highlight_worthy = False

        if breakaway_outcome == OutcomeType.SUCCESS:
             # Good run, add some yards
             yards_gained += 5.0
             headline = f"Nice run by {rb.last_name}."
        elif breakaway_outcome == OutcomeType.CRITICAL_SUCCESS:
             # HUGE run
             bonus = ProbabilityEngine.calculate_normal_outcome(25.0, 10.0)
             yards_gained += bonus
             headline = f"BREAKAWAY! {rb.last_name} is loose!"
             is_highlight_worthy = True

        yards_gained = int(yards_gained)

        # Fumble Check
        # Base fumble rate 1%
        # Increased by fatigue and big hits (high defender strength)
        fumble_chance = 0.01
        if current_fatigue > 70: fumble_chance += 0.02
        # Fumble Chance
        fumble_chance = 0.01
        hit_power = getattr(defender, "hit_power", None) or 50
        if hit_power > 85: fumble_chance += 0.01
        if hasattr(rb, "ball_security") and rb.ball_security < 70: fumble_chance += 0.01

        # Use resolve_outcome for simple binary check
        is_fumble = ProbabilityEngine.resolve_outcome(fumble_chance)
        is_turnover = is_fumble

        is_touchdown = False
        if yards_gained > 80:
            is_touchdown = True
        elif yards_gained > 15 and yards_gained >= (100 - 20):
             # Simplified red zone logic
             pass

        if is_turnover:
            headline = f"FUMBLE! {rb.last_name} loses the ball!"
            is_highlight_worthy = True
            yards_gained = 0 # Or yards until fumble? Simplified to 0.

        # XP
        xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})

        return PlayResult(
            yards_gained=yards_gained,
            is_touchdown=is_touchdown,
            is_turnover=is_turnover,
            description=f"Run {command.run_direction} by {rb.last_name} for {yards_gained} yards.",
            headline=headline,
            is_highlight_worthy=is_highlight_worthy or is_touchdown,
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
