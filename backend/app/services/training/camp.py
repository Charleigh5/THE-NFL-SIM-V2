#!/usr/bin/env python3
"""
Training Camp Module
====================
Manages offseason training camp schedules and drills.

Phase 7: Training & Development
- Drill selection and intensity
- XP generation vs Injury risk
- Position-specific gains
"""

import random
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================


class DrillType(str, Enum):
    """Types of training drills."""

    OKLAHOMA = "OKLAHOMA"  # High intensity, tackling/blocking
    SEVEN_ON_SEVEN = "7_ON_7"  # Medium intensity, pass/coverage
    INDIVIDUAL = "INDIVIDUAL"  # Low intensity, technique
    FILM_STUDY = "FILM_STUDY"  # Zero physical, awareness gain
    SCRIMMAGE = "SCRIMMAGE"  # Max intensity, all skills
    CONDITIONING = "CONDITIONING"  # Stamina gain, fatigue risk


class TrainingIntensity(str, Enum):
    """Intensity levels for drills."""

    WALKTHROUGH = "WALKTHROUGH"  # Minimal risk, low gain
    STANDARD = "STANDARD"  # Normal risk/gain
    FULL_PADS = "FULL_PADS"  # High risk, high gain


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass(frozen=True)
class DrillConfig:
    """Configuration for a specific drill."""

    name: str
    type: DrillType
    targeted_attributes: list[str]
    xp_multiplier: float
    injury_risk_base: float
    fatigue_cost: float


@dataclass
class CampDay:
    """A single day schedule in training camp."""

    morning_drill: DrillType
    afternoon_drill: DrillType
    intensity: TrainingIntensity
    rest_day: bool = False


@dataclass
class CampResult:
    """Outcome of a processed camp day/week."""

    xp_gained: dict[str, float]  # PlayerID -> XP
    injuries: list[str]  # List of injury descriptions
    fatigue_levels: dict[str, float]


# ============================================================================
# TRAINING CAMP ENGINE
# ============================================================================


class TrainingCampEngine:
    """
    Manages the training camp simulation.

    Principles:
    - Risk vs Reward (Harder drills = more XP but more injury/fatigue)
    - Specificity (Drills target specific attribute groups)
    """

    DRILL_REGISTRY = {
        DrillType.OKLAHOMA: DrillConfig(
            name="Oklahoma Drill",
            type=DrillType.OKLAHOMA,
            targeted_attributes=["strength", "tackling", "blocking", "toughness"],
            xp_multiplier=1.5,
            injury_risk_base=0.05,
            fatigue_cost=15.0,
        ),
        DrillType.SEVEN_ON_SEVEN: DrillConfig(
            name="7-on-7",
            type=DrillType.SEVEN_ON_SEVEN,
            targeted_attributes=["passing", "catching", "coverage", "route_running"],
            xp_multiplier=1.2,
            injury_risk_base=0.02,
            fatigue_cost=10.0,
        ),
        DrillType.INDIVIDUAL: DrillConfig(
            name="Individual Period",
            type=DrillType.INDIVIDUAL,
            targeted_attributes=["technique"],  # Generic placeholder for pos-specific
            xp_multiplier=1.0,
            injury_risk_base=0.01,
            fatigue_cost=5.0,
        ),
        DrillType.FILM_STUDY: DrillConfig(
            name="Film Study",
            type=DrillType.FILM_STUDY,
            targeted_attributes=["awareness", "play_recognition"],
            xp_multiplier=0.8,
            injury_risk_base=0.0,
            fatigue_cost=0.0,
        ),
        DrillType.SCRIMMAGE: DrillConfig(
            name="Full Scrimmage",
            type=DrillType.SCRIMMAGE,
            targeted_attributes=["all"],
            xp_multiplier=2.0,
            injury_risk_base=0.08,
            fatigue_cost=25.0,
        ),
        DrillType.CONDITIONING: DrillConfig(
            name="Conditioning",
            type=DrillType.CONDITIONING,
            targeted_attributes=["stamina", "speed"],
            xp_multiplier=0.9,
            injury_risk_base=0.03,
            fatigue_cost=20.0,
        ),
    }

    def process_day(
        self,
        day_schedule: CampDay,
        roster: list[str],  # List of player IDs
        rng_seed: int = 0,
    ) -> CampResult:
        """
        Process a single day of training camp.
        """
        if day_schedule.rest_day:
            # Recover fatigue
            return CampResult(
                xp_gained={},
                injuries=[],
                fatigue_levels=dict.fromkeys(roster, -20.0),  # Recover
            )

        random.seed(rng_seed)
        xp_gained = {}
        injuries = []
        fatigue_update = {}

        # Calculate modifiers based on intensity
        intensity_mod = {
            TrainingIntensity.WALKTHROUGH: 0.5,
            TrainingIntensity.STANDARD: 1.0,
            TrainingIntensity.FULL_PADS: 1.5,
        }[day_schedule.intensity]

        drills = [day_schedule.morning_drill, day_schedule.afternoon_drill]

        for pid in roster:
            player_total_xp = 0.0
            player_fatigue = 0.0

            for drill_type in drills:
                config = self.DRILL_REGISTRY[drill_type]

                # XP Gain
                base_gain = 10.0 * config.xp_multiplier * intensity_mod
                # Randomized minor fluctuation
                gain = base_gain * random.uniform(0.9, 1.1)
                player_total_xp += gain

                # Fatigue
                player_fatigue += config.fatigue_cost * intensity_mod

                # Injury Check
                risk = config.injury_risk_base * intensity_mod
                # Simplistic roll - would normally check player health stats
                if random.random() < (risk / 100.0):  # Convert percent to probability
                    injuries.append(f"{pid} injured during {config.name}")
                    player_total_xp *= 0.5  # Reduced gain if injured

            xp_gained[pid] = player_total_xp
            fatigue_update[pid] = player_fatigue

        return CampResult(xp_gained, injuries, fatigue_update)

    def recommend_schedule(self, team_needs: list[str]) -> list[CampDay]:
        """
        Generate a recommended weekly schedule based on team needs.

        Args:
            team_needs: List of attributes to prioritize (e.g. ['tackling', 'stamina'])
        """
        schedule = []
        # Standard 7 day camp week: 6 on, 1 off

        # Day 1: Acclimation
        schedule.append(
            CampDay(DrillType.INDIVIDUAL, DrillType.SEVEN_ON_SEVEN, TrainingIntensity.STANDARD)
        )

        # Day 2: Install
        schedule.append(
            CampDay(DrillType.FILM_STUDY, DrillType.INDIVIDUAL, TrainingIntensity.STANDARD)
        )

        # Day 3: PADS
        schedule.append(
            CampDay(DrillType.OKLAHOMA, DrillType.SCRIMMAGE, TrainingIntensity.FULL_PADS)
        )

        # Day 4: Recovery/Film
        schedule.append(
            CampDay(DrillType.FILM_STUDY, DrillType.FILM_STUDY, TrainingIntensity.WALKTHROUGH)
        )

        # Day 5: Specifics
        if "stamina" in team_needs or "speed" in team_needs:
            pm_drill = DrillType.CONDITIONING
        elif "tackling" in team_needs:
            pm_drill = DrillType.OKLAHOMA
        else:
            pm_drill = DrillType.SEVEN_ON_SEVEN

        schedule.append(CampDay(DrillType.INDIVIDUAL, pm_drill, TrainingIntensity.STANDARD))

        # Day 6: Final Scrimmage
        schedule.append(
            CampDay(DrillType.SCRIMMAGE, DrillType.CONDITIONING, TrainingIntensity.FULL_PADS)
        )

        # Day 7: Rest
        schedule.append(
            CampDay(
                DrillType.FILM_STUDY,
                DrillType.FILM_STUDY,
                TrainingIntensity.WALKTHROUGH,
                rest_day=True,
            )
        )

        return schedule
