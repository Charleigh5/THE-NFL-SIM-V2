from app.kernels.core.ecs_manager import Component
from typing import Dict, Optional, List, Any, ClassVar
from pydantic import Field
import random


class TrainingEngine(Component):
    """
    Enhanced Training Engine (B-027)

    Manages player training with:
    - Position-specific drills (B-027)
    - Seasonal periodization (B-028)
    - Weekly load management (B-029)
    - Injury risk calculations (B-030)
    - XP multipliers per drill (B-031)
    """

    # Fatigue tracking
    current_fatigue: float = 0.0  # 0-100
    chronic_fatigue: float = 0.0  # Accumulated wear
    weekly_load: float = 0.0      # B-029: Weekly training load

    # B-028: Seasonal periodization multipliers (ClassVar so Pydantic ignores it)
    SEASONAL_INTENSITY: ClassVar[Dict[str, float]] = {
        "offseason": 0.85,
        "preseason": 0.70,
        "regular": 0.50,
        "playoffs": 0.30,
    }

    # Directive 9: Real-World Weekly Periodization
    intensity_schedule: Dict[str, float] = {
        "Monday": 0.0,    # Recovery
        "Tuesday": 0.0,   # Recovery
        "Wednesday": 0.8, # Practice
        "Thursday": 0.6,  # Practice
        "Friday": 0.3,    # Walkthrough
        "Saturday": 0.0,  # Rest
        "Sunday": 1.0     # Game Day
    }

    def train_with_drill(
        self,
        drill: Any,  # Drill from drills.py
        player_age: int,
        coaching_style: Any = None,  # CoachingStyle from coaching_philosophy.py
        season_phase: str = "regular",
        rng_seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        B-027: Execute a specific drill from the catalog.

        Returns dict with xp_gained, injury_occurred, fatigue_added, target_stat
        """
        if rng_seed is not None:
            random.seed(rng_seed)

        # B-028: Get seasonal intensity cap
        season_cap = self.SEASONAL_INTENSITY.get(season_phase, 0.50)

        # Base values from drill
        base_xp = 10.0 * drill.xp_multiplier
        base_injury_risk = drill.injury_risk
        base_fatigue = drill.fatigue_cost

        # Apply coaching style modifiers if provided
        if coaching_style:
            # Age-based bonus
            age_bonus = 0.0
            if player_age < 26:
                age_bonus = getattr(coaching_style, 'young_player_bonus', 0.0)
            elif player_age > 30:
                age_bonus = getattr(coaching_style, 'veteran_bonus', 0.0)

            xp_mult = getattr(coaching_style, 'xp_multiplier', 1.0)
            injury_mult = getattr(coaching_style, 'injury_risk_multiplier', 1.0)
            fatigue_mult = getattr(coaching_style, 'fatigue_multiplier', 1.0)

            base_xp *= xp_mult * (1.0 + age_bonus)
            base_injury_risk *= injury_mult
            base_fatigue *= fatigue_mult

        # B-028: Apply seasonal cap
        effective_intensity = season_cap
        base_xp *= effective_intensity

        # B-030: Injury risk calculation
        # Risk increases with fatigue
        fatigue_injury_mult = 1.0 + (self.current_fatigue / 100.0) * 0.5
        final_injury_risk = min(base_injury_risk * fatigue_injury_mult, 1.0)

        # Roll for injury
        injury_occurred = random.random() < final_injury_risk

        # If injured, reduce XP gain
        if injury_occurred:
            base_xp *= 0.25

        # B-029: Weekly load management
        self.weekly_load += base_fatigue

        # Higher weekly load increases chronic fatigue
        if self.weekly_load > 100.0:
            self.chronic_fatigue += 0.5

        # Fatigue accumulation
        self.current_fatigue += base_fatigue
        if self.current_fatigue > 80.0:
            self.chronic_fatigue += 1.0

        # Cap fatigue at 100
        self.current_fatigue = min(100.0, self.current_fatigue)

        return {
            "xp_gained": round(base_xp, 2),
            "target_stat": drill.target_stat,
            "secondary_stats": drill.secondary_stats,
            "injury_occurred": injury_occurred,
            "fatigue_added": base_fatigue,
            "final_injury_risk": round(final_injury_risk, 4),
            "weekly_load": round(self.weekly_load, 2),
        }

    def train_player(self, intensity: float, injury_risk_mult: float) -> float:
        """
        Legacy method for backward compatibility.
        Returns XP gained.
        """
        effective_fatigue = self.current_fatigue + self.chronic_fatigue

        # XP Gain logic
        xp_gain = intensity * 10.0

        # Fatigue Accumulation
        self.current_fatigue += intensity * 5.0
        if self.current_fatigue > 80.0:
            self.chronic_fatigue += 1.0

        return xp_gain

    def recover(self, rest_quality: float, coaching_style: Any = None) -> float:
        """
        Recover fatigue based on rest quality.

        Args:
            rest_quality: 0.0-1.0 quality of rest
            coaching_style: Optional coaching style with recovery modifier

        Returns:
            Amount of fatigue recovered
        """
        recovery_mult = 1.0
        if coaching_style:
            recovery_mult = getattr(coaching_style, 'recovery_multiplier', 1.0)

        recovery_amount = rest_quality * 20.0 * recovery_mult
        old_fatigue = self.current_fatigue
        self.current_fatigue = max(0.0, self.current_fatigue - recovery_amount)

        return old_fatigue - self.current_fatigue

    def reset_weekly_load(self) -> None:
        """Reset weekly load counter. Call at start of each week."""
        self.weekly_load = 0.0

    def get_training_recommendation(
        self,
        current_fatigue: float,
        season_phase: str = "regular"
    ) -> str:
        """
        Get recommended training intensity based on current state.

        Returns: 'rest', 'light', 'moderate', 'heavy'
        """
        season_cap = self.SEASONAL_INTENSITY.get(season_phase, 0.50)

        # Factor in fatigue
        if current_fatigue > 70:
            return "rest"
        elif current_fatigue > 50:
            return "light"
        elif current_fatigue > 30:
            return "moderate" if season_cap >= 0.5 else "light"
        else:
            return "heavy" if season_cap >= 0.7 else "moderate"

