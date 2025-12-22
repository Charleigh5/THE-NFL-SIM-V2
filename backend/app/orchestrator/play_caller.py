from dataclasses import dataclass, field
from typing import List, Any, Optional, Dict, TYPE_CHECKING
from app.orchestrator.play_commands import (
    PlayCommand, PassPlayCommand, RunPlayCommand,
    PuntCommand, FieldGoalCommand
)
from app.data.coaches import CoachingPhilosophy

if TYPE_CHECKING:
    from app.models.player import Player


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
    def __init__(self, rng: Any, philosophy: Optional['CoachingPhilosophy'] = None, aggression: float = 0.5, run_pass_ratio: float = 0.45) -> None:
        """
        Initialize PlayCaller with coaching personality.

        Args:
            rng: DeterministicRNG instance
            philosophy: CoachingPhilosophy object containing personality traits.
            aggression: Legacy arg (float 0.0-1.0), used if philosophy is None.
            run_pass_ratio: Legacy arg (float 0.0-1.0), used if philosophy is None.
        """
        self.rng = rng
        self.philosophy = philosophy

        # Map 0-100 scales to 0.0-1.0 internal factors
        # Default to 0.5 (Balanced) if no philosophy provided
        if philosophy:
            self.run_pass_ratio = philosophy.run_pass_ratio / 100.0
            self.aggressiveness = philosophy.aggressiveness / 100.0
            self.fourth_down_aggression = philosophy.fourth_down_aggression / 100.0
            self.blitz_frequency = philosophy.blitz_frequency / 100.0
        else:
            # Legacy / Default
            self.run_pass_ratio = run_pass_ratio
            self.aggressiveness = aggression
            self.fourth_down_aggression = aggression # Simple mapping
            self.blitz_frequency = 0.3

    def _get_effective_aggression(self, context: PlayCallingContext) -> float:
        """
        Calculate effective aggression based on game state and personality.
        Urgency (late game/trailing) increases aggression.
        """
        aggression = self.aggressiveness

        # Desperation Logic
        if context.score_diff < 0 and context.time_left_seconds < 300: # Last 5 mins
            if context.score_diff < -8: # Two scores down
                aggression += 0.4
            else: # One score down
                aggression += 0.2

        # Protecting Lead Logic
        elif context.score_diff > 8 and context.time_left_seconds < 600:
            aggression -= 0.2 # Play safer

        return max(0.0, min(1.0, aggression))

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
        in_fg_range = context.distance_to_goal <= 38

        # Base decision primarily driven by Fourth Down Aggression trait
        effective_aggression = self._get_effective_aggression(context)

        # Use the specific fourth_down_aggression trait if available, modulated by effective urgency
        trait_bias = self.fourth_down_aggression
        final_aggression = (effective_aggression + trait_bias) / 2.0

        should_go_for_it = False

        # 1. DESPERATION OVERRIDES (Always trump personality)
        if context.time_left_seconds < 120 and context.score_diff < 0:
             # Losing in last 2 mins - MUST go for it if FG won't tie/win
            if context.score_diff < -3 or not in_fg_range:
                should_go_for_it = True

        # 2. PERSONALITY LOGIC
        elif not should_go_for_it:
            # "The Gambler" (High Aggression)
            if final_aggression > 0.75:
                # Go for it on 4th & Short (< 2) anywhere past own 40
                if context.distance <= 2 and context.distance_to_goal <= 60:
                     should_go_for_it = True
                # Go for it on 4th & Medium (< 5) in opponent territory
                if context.distance <= 5 and context.distance_to_goal <= 40:
                     should_go_for_it = True

            # "Calculated Risk" (Medium Aggression)
            elif final_aggression > 0.5:
                 # Go for it on 4th & 1 past midfield
                 if context.distance <= 1 and context.distance_to_goal <= 50:
                     should_go_for_it = True

            # "Conservative" (Low Aggression)
            else:
                # Goal line stand only
                if context.distance_to_goal < 3 and context.distance <= 2:
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
        Adjusts base ratio based on situation and personality.
        """
        # Start with Coach's philosophy (0.0 = All Pass, 1.0 = All Run)
        # We convert to "Pass Probability" so: 0.0 run_pass_ratio -> 1.0 pass_prob
        pass_prob = 1.0 - self.run_pass_ratio

        # Context Modifiers
        # 3rd Down & Long -> High Pass Prob
        if context.down == 3:
            if context.distance > 6:
                pass_prob += 0.25
            elif context.distance <= 2:
                pass_prob -= 0.15

        # Score Effects (Catchup vs Kill Clock)
        if context.score_diff < -8 and context.time_left_seconds < 900: # Trailing by 2 scores, Q4 or late Q3
             pass_prob += 0.20
        elif context.score_diff > 8 and context.time_left_seconds < 600: # Leading late, run the ball
             pass_prob -= 0.25

        # Hurry Up
        if context.is_hurry_up:
            pass_prob += 0.2

        # 2-Minute Drill Adjustments
        if context.two_minute_adjustments:
            pass_prob += context.two_minute_adjustments.get("pass_probability_boost", 0.0)

        # Aggression Impact (Aggressive coaches throw deeper/more often to step on throat)
        effective_aggression = self._get_effective_aggression(context)
        if effective_aggression > 0.7:
             pass_prob += 0.05
        elif effective_aggression < 0.3:
             pass_prob -= 0.05

        # Clamp
        pass_prob = max(0.05, min(0.95, pass_prob))

        return self.rng.random() < pass_prob

    def call_audible(
        self,
        qb: "Player",
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
        if self.aggressiveness > 0.7:
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
