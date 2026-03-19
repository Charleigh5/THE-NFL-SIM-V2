from dataclasses import dataclass, field
from typing import List, Any, Optional, Dict
from app.orchestrator.play_commands import (
    PlayCommand, PassPlayCommand, RunPlayCommand,
    PuntCommand, FieldGoalCommand
)


@dataclass
class PlayCallingContext:
    down: int
    distance: int
    distance_to_goal: int
    time_left_seconds: int
    score_diff: int  # Positive means winning, negative means losing
    possession: str  # "home" or "away"
    offense_players: List[Any]
    defense_players: List[Any]
    is_hurry_up: bool = False
    # 2-Minute Drill AI (AI-005) - adjustments from ClockManagementAI
    two_minute_adjustments: Optional[Dict[str, Any]] = None

class PlayCaller:
    """
    Handles situation-aware play selection based on game state and coach personality.
    """
    def __init__(self, rng: Any, aggression: float = 0.5, run_pass_ratio: float = 0.45) -> None:
        """
        Initialize PlayCaller.

        Args:
            rng: DeterministicRNG instance
            aggression (float): 0.0 (conservative) to 1.0 (aggressive).
                               Affects 4th down decisions, deep passes, etc.
            run_pass_ratio (float): 0.0 (all pass) to 1.0 (all run).
                                   Base tendency before situational adjustments.
        """
        self.rng = rng
        self.aggression = aggression
        self.run_pass_ratio = run_pass_ratio

    def select_play(self, context: PlayCallingContext) -> PlayCommand:
        """
        Select the appropriate play command based on the current context.
        """
        # 1. Check for Special Teams situations (4th down)
        if context.down == 4:
            return self._handle_fourth_down(context)

        # 2. Determine Run vs Pass
        is_pass = self._decide_run_vs_pass(context)

        if is_pass:
            return self._create_pass_play(context)
        else:
            return self._create_run_play(context)

    def _handle_fourth_down(self, context: PlayCallingContext) -> PlayCommand:
        """Handle 4th down logic: Punt, FG, or Go for it."""

        # Field Goal Range (approx 35 yard line, so 35+17 = 52 yard FG)
        # distance_to_goal <= 35 means we are at opponent 35 or closer.
        in_fg_range = context.distance_to_goal <= 38

        # Decision Logic
        should_go_for_it = False

        # Desperation (Late game, losing)
        if context.time_left_seconds < 300 and context.score_diff < 0:
            # If losing by more than 3 and in FG range, might still go for it if time is low
            if context.score_diff < -3:
                should_go_for_it = True
            # If losing by <= 3 and in FG range, kick the FG to tie/win
            elif in_fg_range:
                should_go_for_it = False
            else:
                should_go_for_it = True # Must go for it if out of range

        # Aggressive Coach Logic
        elif self.aggression > 0.7:
            if context.distance <= 2 and context.distance_to_goal <= 60:
                should_go_for_it = True

        # Normal Logic
        else:
            if context.distance_to_goal < 3: # Goal line stand
                should_go_for_it = True

        if should_go_for_it:
            # Treat as normal down
            if self._decide_run_vs_pass(context):
                return self._create_pass_play(context)
            else:
                return self._create_run_play(context)

        if in_fg_range:
            return FieldGoalCommand(
                kicking_team=context.offense_players,
                defense=context.defense_players,
                distance=context.distance_to_goal + 17 # +17 for snap and hold
            )
        else:
            return PuntCommand(
                punting_team=context.offense_players,
                receiving_team=context.defense_players
            )

    def _decide_run_vs_pass(self, context: PlayCallingContext) -> bool:
        """
        Returns True for Pass, False for Run.
        Adjusts base ratio based on situation and 2-minute drill adjustments.
        """
        # Start with base probability of passing
        pass_prob = 1.0 - self.run_pass_ratio

        # Adjust for Down and Distance
        if context.down == 3:
            if context.distance > 6:
                pass_prob += 0.3  # Likely pass on 3rd and long
            elif context.distance <= 2:
                pass_prob -= 0.2  # Likely run on 3rd and short

        # Adjust for Score/Time (Catchup logic)
        if context.score_diff < -8 and context.time_left_seconds < 600:
            pass_prob += 0.3  # Throw to catch up
        elif context.score_diff > 8 and context.time_left_seconds < 600:
            pass_prob -= 0.3  # Run to kill clock

        if context.is_hurry_up:
            pass_prob += 0.25

        # 2-Minute Drill AI (AI-005) adjustments
        if context.two_minute_adjustments:
            adj = context.two_minute_adjustments
            pass_prob += adj.get("pass_probability_boost", 0.0)
            # Run penalty effectively increases pass probability
            pass_prob += adj.get("run_penalty", 0.0)

        # Adjust for Aggression
        if self.aggression > 0.7:
            pass_prob += 0.1
        elif self.aggression < 0.3:
            pass_prob -= 0.1

        # Clamp probability
        pass_prob = max(0.05, min(0.95, pass_prob))

        return self.rng.random() < pass_prob

    def call_audible(
        self,
        qb: "Player",  # noqa: F821
        current_play: str,
        new_play: str,
        play_clock_remaining: float
    ) -> tuple[str, float, bool]:
        """
        Process an audible call.

        Returns:
            (final_play, new_clock_remaining, false_start_occurred)
        """
        # Check for Audible Master ability
        from app.models.player import Player
        has_audible_master = False
        if isinstance(qb, Player):
             has_audible_master = (qb.abilities or {}).get("audible_master", False)

        if has_audible_master:
            clock_cost = 2.0  # 2 seconds
            false_start_risk = 0.0
        else:
            clock_cost = 8.0  # 8 seconds
            false_start_risk = 0.05  # 5% chance

        new_clock = max(0, play_clock_remaining - clock_cost)

        # Check for false start
        false_start = self.rng.random() < false_start_risk

        if false_start:
            return current_play, new_clock, True  # Penalty, play stays same

        return new_play, new_clock, False

    def _create_pass_play(self, context: PlayCallingContext) -> PassPlayCommand:
        """Determine pass depth and create command."""
        # Determine depth based on distance needed
        depth_weights = {"short": 1.0, "mid": 1.0, "deep": 1.0}

        if context.distance > 10:
            depth_weights["deep"] += 2
            depth_weights["mid"] += 2
        elif context.distance < 5:
            depth_weights["short"] += 2

        # Aggression factor
        if self.aggression > 0.7:
            depth_weights["deep"] += 1

        # 2-Minute Drill AI (AI-005) adjustments
        if context.two_minute_adjustments:
            adj = context.two_minute_adjustments
            # Penalize deep passes in critical situations (takes too long)
            deep_penalty = adj.get("deep_pass_penalty", 0.0)
            if deep_penalty > 0:
                depth_weights["deep"] = max(0.1, depth_weights["deep"] - deep_penalty * 3)
                depth_weights["short"] += deep_penalty * 2
            # Boost sideline routes (short/mid more likely to stop clock)
            sideline_boost = adj.get("sideline_route_boost", 0.0)
            if sideline_boost > 0:
                depth_weights["short"] += sideline_boost
                depth_weights["mid"] += sideline_boost * 0.5

        # Select depth
        choices = list(depth_weights.keys())
        weights = list(depth_weights.values())
        selected_depth = self.rng.choices(choices, weights=weights, k=1)[0]

        return PassPlayCommand(
            offense_players=context.offense_players,
            defense_players=context.defense_players,
            depth=selected_depth
        )

    def _create_run_play(self, context: PlayCallingContext) -> RunPlayCommand:
        """Determine run direction and create command."""
        directions = ["left", "middle", "right"]
        # Could adjust based on team strengths later
        selected_dir = self.rng.choice(directions)

        return RunPlayCommand(
            offense_players=context.offense_players,
            defense_players=context.defense_players,
            run_direction=selected_dir
        )
