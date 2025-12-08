#!/usr/bin/env python3
"""
4-Compartment Fatigue System - GENESIS Biological
==================================================
Energy and fatigue modeling for realistic player stamina.

Phase 2: GENESIS Biological Player Modeling
- ATP-PC (phosphocreatine) burst energy
- Glycolytic (lactate) system
- Aerobic baseline
- Neural fatigue

Context7 Best Practices:
- Physics-based energy calculations
- Dataclasses for state management
- Pure functions for updates
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import math


# ============================================================================
# ENUMS
# ============================================================================

class ActivityLevel(str, Enum):
    """Current activity level."""
    REST = "REST"               # Sideline, huddle
    WALK = "WALK"               # Walking to position
    JOG = "JOG"                 # Light movement
    RUN = "RUN"                 # Standard running
    SPRINT = "SPRINT"           # Maximum effort
    EXPLOSIVE = "EXPLOSIVE"     # Jumps, cuts, tackles


class FatigueLevel(str, Enum):
    """Overall fatigue state."""
    FRESH = "FRESH"             # Full energy
    NORMAL = "NORMAL"           # Sustainable effort
    TIRED = "TIRED"             # Performance degradation begins
    EXHAUSTED = "EXHAUSTED"     # Significant impairment
    GASSED = "GASSED"           # Risk of injury, major impairment


# ============================================================================
# ENERGY COSTS (per tick at 60Hz = per 16.67ms)
# ============================================================================

# Values in arbitrary energy units per tick
ENERGY_COSTS = {
    ActivityLevel.REST: 0.0,
    ActivityLevel.WALK: 0.1,
    ActivityLevel.JOG: 0.5,
    ActivityLevel.RUN: 1.5,
    ActivityLevel.SPRINT: 4.0,
    ActivityLevel.EXPLOSIVE: 8.0,
}

# ATP-PC recovery rate per tick (when not using)
ATP_PC_RECOVERY_RATE = 0.3

# Glycolytic recovery (slower)
GLYCOLYTIC_RECOVERY_RATE = 0.05

# Aerobic recovery (very slow but unlimited capacity)
AEROBIC_RECOVERY_RATE = 0.02


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class EnergyCompartment:
    """
    Single energy compartment with capacity and current level.
    """
    name: str
    capacity: float
    current: float
    recovery_rate: float = 0.1
    depletion_threshold: float = 0.2  # Below this, compartment is "depleted"

    @property
    def percentage(self) -> float:
        """Current fill percentage (0-100)."""
        return (self.current / self.capacity) * 100.0

    @property
    def is_depleted(self) -> bool:
        """Check if compartment is effectively empty."""
        return self.current < (self.capacity * self.depletion_threshold)

    def consume(self, amount: float) -> float:
        """
        Consume energy from this compartment.

        Returns:
            Amount that couldn't be provided (overflow to next compartment)
        """
        if amount <= self.current:
            self.current -= amount
            return 0.0
        else:
            deficit = amount - self.current
            self.current = 0.0
            return deficit

    def recover(self, time_units: float = 1.0) -> None:
        """Recover energy based on time."""
        recovery = self.recovery_rate * time_units
        self.current = min(self.capacity, self.current + recovery)


@dataclass
class FatigueState:
    """
    Complete 4-compartment fatigue model.

    Compartments:
    1. ATP-PC (Phosphocreatine) - Burst energy, depletes in 6-10s of max effort
    2. Glycolytic - Medium-term energy, builds lactate (affects coordination)
    3. Aerobic - Long-term energy, essentially unlimited but slow
    4. Neural - Mental fatigue, affects reaction time and decisions
    """
    # Compartment 1: ATP-PC (explosive burst)
    atp_pc: EnergyCompartment = field(
        default_factory=lambda: EnergyCompartment(
            name="ATP-PC",
            capacity=100.0,
            current=100.0,
            recovery_rate=ATP_PC_RECOVERY_RATE,
            depletion_threshold=0.1,
        )
    )

    # Compartment 2: Glycolytic (medium-term, lactate buildup)
    glycolytic: EnergyCompartment = field(
        default_factory=lambda: EnergyCompartment(
            name="Glycolytic",
            capacity=200.0,
            current=200.0,
            recovery_rate=GLYCOLYTIC_RECOVERY_RATE,
            depletion_threshold=0.3,
        )
    )

    # Compartment 3: Aerobic (long-term)
    aerobic: EnergyCompartment = field(
        default_factory=lambda: EnergyCompartment(
            name="Aerobic",
            capacity=500.0,
            current=500.0,
            recovery_rate=AEROBIC_RECOVERY_RATE,
            depletion_threshold=0.5,
        )
    )

    # Compartment 4: Neural (mental fatigue)
    neural: EnergyCompartment = field(
        default_factory=lambda: EnergyCompartment(
            name="Neural",
            capacity=100.0,
            current=100.0,
            recovery_rate=0.02,
            depletion_threshold=0.4,
        )
    )

    # Tracking
    lactate_level: float = 0.0  # 0-100, high = coordination loss
    current_activity: ActivityLevel = ActivityLevel.REST
    fatigue_level: FatigueLevel = FatigueLevel.FRESH

    @property
    def overall_energy_percentage(self) -> float:
        """Weighted average of all compartments."""
        weights = [0.3, 0.3, 0.2, 0.2]  # ATP-PC and Glycolytic most important
        percentages = [
            self.atp_pc.percentage,
            self.glycolytic.percentage,
            self.aerobic.percentage,
            self.neural.percentage,
        ]
        return sum(w * p for w, p in zip(weights, percentages))

    @property
    def speed_modifier(self) -> float:
        """
        Speed reduction based on fatigue.
        1.0 = full speed, lower = slower.
        """
        # ATP-PC depletion directly affects burst speed
        atp_factor = 0.7 + (self.atp_pc.percentage / 100.0) * 0.3

        # Lactate affects coordination/speed
        lactate_factor = 1.0 - (self.lactate_level / 200.0)

        return max(0.5, atp_factor * lactate_factor)

    @property
    def strength_modifier(self) -> float:
        """
        Strength reduction based on fatigue.
        1.0 = full strength, lower = weaker.
        """
        # Glycolytic and aerobic affect sustained strength
        glyco_factor = 0.6 + (self.glycolytic.percentage / 100.0) * 0.4
        aerobic_factor = 0.8 + (self.aerobic.percentage / 100.0) * 0.2

        return max(0.4, glyco_factor * aerobic_factor)

    @property
    def reaction_time_modifier(self) -> float:
        """
        Reaction time increase due to fatigue.
        1.0 = normal, higher = slower reactions.
        """
        # Neural fatigue directly affects reactions
        neural_factor = 2.0 - (self.neural.percentage / 100.0)

        # High lactate also affects reactions
        lactate_factor = 1.0 + (self.lactate_level / 100.0) * 0.3

        return min(2.0, neural_factor * lactate_factor)

    @property
    def injury_risk_modifier(self) -> float:
        """
        Increase in injury risk due to fatigue.
        1.0 = normal, higher = more likely to get injured.
        """
        # Low energy = higher injury risk
        energy_factor = 2.0 - (self.overall_energy_percentage / 100.0)

        # High lactate = coordination loss = injury risk
        lactate_factor = 1.0 + (self.lactate_level / 100.0) * 0.5

        return min(3.0, energy_factor * lactate_factor)

    def update_fatigue_level(self) -> None:
        """Update the overall fatigue level category."""
        energy = self.overall_energy_percentage

        if energy > 85:
            self.fatigue_level = FatigueLevel.FRESH
        elif energy > 65:
            self.fatigue_level = FatigueLevel.NORMAL
        elif energy > 45:
            self.fatigue_level = FatigueLevel.TIRED
        elif energy > 25:
            self.fatigue_level = FatigueLevel.EXHAUSTED
        else:
            self.fatigue_level = FatigueLevel.GASSED


# ============================================================================
# FATIGUE ENGINE
# ============================================================================

class FatigueEngine:
    """
    Engine for processing player fatigue over time.

    Handles:
    - Energy consumption based on activity
    - Cascading energy system (ATP-PC -> Glycolytic -> Aerobic)
    - Lactate accumulation and clearance
    - Recovery during rest
    """

    def __init__(
        self,
        state: Optional[FatigueState] = None,
        stamina_rating: int = 80,
        injury_resistance: int = 80,
    ):
        self.state = state or FatigueState()
        self.stamina_rating = stamina_rating
        self.injury_resistance = injury_resistance

        # Modify capacities based on stamina
        stamina_modifier = stamina_rating / 80.0
        self.state.atp_pc.capacity *= stamina_modifier
        self.state.glycolytic.capacity *= stamina_modifier
        self.state.aerobic.capacity *= stamina_modifier

        # Reset current to new capacities
        self.state.atp_pc.current = self.state.atp_pc.capacity
        self.state.glycolytic.current = self.state.glycolytic.capacity
        self.state.aerobic.current = self.state.aerobic.capacity

    def process_activity(
        self,
        activity: ActivityLevel,
        elapsed_ticks: int = 1,
    ) -> None:
        """
        Process energy consumption for an activity.

        Args:
            activity: Current activity level
            elapsed_ticks: Number of simulation ticks (default 1)
        """
        self.state.current_activity = activity

        # Calculate energy cost
        base_cost = ENERGY_COSTS.get(activity, 0.0) * elapsed_ticks

        # Consume from compartments in order (cascade)
        remaining = base_cost

        # First: ATP-PC for explosive/sprint
        if activity in [ActivityLevel.EXPLOSIVE, ActivityLevel.SPRINT]:
            remaining = self.state.atp_pc.consume(remaining)

        # Second: Glycolytic
        if remaining > 0:
            remaining = self.state.glycolytic.consume(remaining)
            # Glycolytic use builds lactate
            self.state.lactate_level += remaining * 0.1

        # Third: Aerobic
        if remaining > 0:
            remaining = self.state.aerobic.consume(remaining)

        # Neural cost for high-intensity activities
        if activity in [ActivityLevel.EXPLOSIVE, ActivityLevel.SPRINT, ActivityLevel.RUN]:
            neural_cost = base_cost * 0.1
            self.state.neural.consume(neural_cost)

        # Clamp lactate
        self.state.lactate_level = min(100.0, self.state.lactate_level)

        # Update overall fatigue level
        self.state.update_fatigue_level()

    def process_recovery(self, elapsed_ticks: int = 1) -> None:
        """
        Process recovery during rest or low activity.

        Args:
            elapsed_ticks: Number of simulation ticks
        """
        recovery_factor = elapsed_ticks

        # Recover all compartments
        self.state.atp_pc.recover(recovery_factor)
        self.state.glycolytic.recover(recovery_factor)
        self.state.aerobic.recover(recovery_factor)
        self.state.neural.recover(recovery_factor)

        # Clear lactate (slower process)
        lactate_clearance = 0.02 * elapsed_ticks
        self.state.lactate_level = max(0.0, self.state.lactate_level - lactate_clearance)

        # Update fatigue level
        self.state.update_fatigue_level()

    def apply_rest_between_plays(self, huddle_ticks: int = 1200) -> None:
        """
        Apply rest recovery between plays (huddle time).

        Args:
            huddle_ticks: Ticks of rest (default 1200 = 20 seconds at 60Hz)
        """
        # Full ATP-PC recovery during huddle (it's fast)
        self.state.atp_pc.current = self.state.atp_pc.capacity

        # Partial glycolytic recovery
        self.process_recovery(huddle_ticks)

    def get_attribute_modifiers(self) -> Dict[str, float]:
        """
        Get all attribute modifiers based on current fatigue.

        Returns:
            Dictionary of attribute modifiers (1.0 = no change)
        """
        return {
            "speed": self.state.speed_modifier,
            "strength": self.state.strength_modifier,
            "reaction_time": self.state.reaction_time_modifier,
            "injury_risk": self.state.injury_risk_modifier,
            "overall_energy": self.state.overall_energy_percentage / 100.0,
        }

    def can_perform_explosive_action(self) -> bool:
        """Check if player has enough burst energy for explosive action."""
        return not self.state.atp_pc.is_depleted

    def should_be_subbed(self) -> bool:
        """Check if player should be substituted due to fatigue."""
        return (
            self.state.fatigue_level == FatigueLevel.GASSED or
            (self.state.fatigue_level == FatigueLevel.EXHAUSTED and
             self.state.lactate_level > 70)
        )
