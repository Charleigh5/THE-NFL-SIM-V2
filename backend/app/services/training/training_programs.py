"""
Training Programs Service
=========================
Manages position-specific training programs with XP progression and injury risk.

CITATION: ENHANCEMENT_REFERENCE.md - Training System Overhaul

Key Features:
- Position-specific drill effectiveness
- Exponential XP threshold formula: 50 * (1.15 ** rating)
- Season phase training modifiers
- Injury risk calculation per drill
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import math
import random

from pydantic import BaseModel, Field


class SeasonPhase(str, Enum):
    """Training intensity varies by season phase."""
    OFFSEASON = "OFFSEASON"     # High intensity, high volume
    PRESEASON = "PRESEASON"     # Tapering, scheme focus
    REGULAR = "REGULAR"         # Maintenance mode
    POSTSEASON = "POSTSEASON"   # Recovery focus


class TrainingPhilosophy(str, Enum):
    """Different coaching philosophies affect outcomes."""
    VOLUME = "VOLUME"           # +30% XP, +80% injury risk
    INTENSITY = "INTENSITY"     # +50% XP, +100% fatigue
    SMART = "SMART"             # Normal XP, -40% injury risk
    OLD_SCHOOL = "OLD_SCHOOL"   # -10% XP, +5 toughness bonus


@dataclass
class PhaseConfig:
    """Configuration for a season phase."""
    intensity: float = 0.5      # 0.0 - 1.0
    skill_focus: float = 0.5    # % skill work vs physical
    recovery_time: int = 24     # Hours between sessions
    risk_tolerance: float = 0.05


# Phase-specific training parameters
PHASE_CONFIGS: Dict[SeasonPhase, PhaseConfig] = {
    SeasonPhase.OFFSEASON: PhaseConfig(
        intensity=0.85,
        skill_focus=0.60,
        recovery_time=48,
        risk_tolerance=0.15,
    ),
    SeasonPhase.PRESEASON: PhaseConfig(
        intensity=0.70,
        skill_focus=0.75,
        recovery_time=36,
        risk_tolerance=0.08,
    ),
    SeasonPhase.REGULAR: PhaseConfig(
        intensity=0.50,
        skill_focus=0.85,
        recovery_time=24,
        risk_tolerance=0.05,
    ),
    SeasonPhase.POSTSEASON: PhaseConfig(
        intensity=0.40,
        skill_focus=0.90,
        recovery_time=18,
        risk_tolerance=0.03,
    ),
}


# Position-specific stat development rates (how fast each stat can improve)
POSITION_DEVELOPMENT_RATES: Dict[str, Dict[str, float]] = {
    "QB": {
        "throw_power": 0.3,          # Slow (physical limit)
        "throw_accuracy_short": 0.8,
        "throw_accuracy_mid": 0.7,
        "throw_accuracy_deep": 0.6,
        "awareness": 0.85,
        "play_recognition": 0.9,     # Mental stats develop fast
        "throw_on_run": 0.65,
        "speed": 0.2,
        "agility": 0.4,
    },
    "RB": {
        "speed": 0.4,
        "acceleration": 0.6,
        "agility": 0.7,
        "break_tackle": 0.8,
        "carrying": 0.9,             # Ball security improves quickly
        "catching": 0.7,
        "route_running": 0.6,
        "pass_block": 0.75,
        "trucking": 0.5,
        "elusiveness": 0.65,
        "stamina": 0.8,
    },
    "WR": {
        "speed": 0.3,
        "acceleration": 0.5,
        "agility": 0.7,
        "route_running": 1.0,        # Pure technique - fastest development
        "catching": 0.9,
        "catch_in_traffic": 0.8,
        "spectacular_catch": 0.6,
        "release": 0.85,
        "jumping": 0.4,
        "run_after_catch": 0.7,
    },
    "CB": {
        "speed": 0.3,
        "acceleration": 0.5,
        "man_coverage": 0.9,
        "zone_coverage": 0.85,
        "press": 1.0,                # Technique-based
        "change_of_direction": 0.6,
        "awareness": 0.8,
        "ball_skills": 0.7,
    },
    "EDGE": {
        "power_moves": 0.9,
        "finesse_moves": 0.85,
        "block_shedding": 0.8,
        "pursuit": 0.6,
        "strength": 0.4,
        "acceleration": 0.5,
    },
    "OL": {
        "pass_block": 0.9,
        "run_block": 0.85,
        "strength": 0.5,
        "awareness": 0.7,
        "footwork": 0.8,
    },
    # Default for positions not explicitly defined
    "DEFAULT": {
        "speed": 0.4,
        "strength": 0.5,
        "awareness": 0.7,
        "agility": 0.6,
    },
}


class TrainingResult(BaseModel):
    """Result of a training session."""
    xp_gains: Dict[str, float] = Field(default_factory=dict)
    stat_changes: Dict[str, int] = Field(default_factory=dict)
    fatigue_added: float = 0.0
    injury_occurred: bool = False
    injury_type: Optional[str] = None
    injury_severity: Optional[str] = None
    weeks_out: int = 0
    session_grade: str = "B"
    notes: List[str] = Field(default_factory=list)


class TrainingProgramsService:
    """
    Service for managing player training and development.
    """

    def __init__(self, season_phase: SeasonPhase = SeasonPhase.REGULAR, seed: int = None):
        self.season_phase = season_phase
        self.phase_config = PHASE_CONFIGS[season_phase]
        self.rng = random.Random(seed)

    def calculate_xp_threshold(self, current_rating: int) -> int:
        """
        Calculate XP needed to reach next rating point.

        Exponential curve - harder to improve at high ratings.

        Examples:
            70 rating → ~500 XP needed
            80 rating → ~1000 XP needed
            90 rating → ~2500 XP needed
            99 rating → ~10000 XP needed
        """
        return int(50 * (1.15 ** current_rating))

    def get_development_rate(self, position: str, stat: str) -> float:
        """Get the development rate for a specific stat based on position."""
        position_rates = POSITION_DEVELOPMENT_RATES.get(
            position,
            POSITION_DEVELOPMENT_RATES["DEFAULT"]
        )
        return position_rates.get(stat, 0.5)

    def execute_training_session(
        self,
        player_age: int,
        player_position: str,
        player_ratings: Dict[str, int],
        player_fatigue: float,
        drill_name: str,
        drill_target_stat: str,
        drill_difficulty: int,
        drill_duration_minutes: int,
        drill_injury_risk: float,
        development_trait: str = "NORMAL",
    ) -> TrainingResult:
        """
        Execute a training session and calculate XP gains.

        Args:
            player_age: Player's current age
            player_position: Position code (e.g., 'QB', 'WR')
            player_ratings: Current ratings dictionary
            player_fatigue: Current fatigue level (0-100)
            drill_name: Name of the drill
            drill_target_stat: Primary stat being trained
            drill_difficulty: 1-10 difficulty rating
            drill_duration_minutes: Session duration
            drill_injury_risk: Base injury risk (0.0-1.0)
            development_trait: NORMAL, STAR, SUPERSTAR, XFACTOR

        Returns:
            TrainingResult with XP gains, stat changes, and injury info
        """
        result = TrainingResult()

        # Import age curves (avoid circular import)
        from app.services.age_curves import get_development_rate_modifier

        # Calculate base XP
        base_xp = drill_difficulty * 10  # 10-100 base XP per minute

        # Apply modifiers
        age_modifier = get_development_rate_modifier(player_age, development_trait)
        position_modifier = self.get_development_rate(player_position, drill_target_stat)
        intensity_modifier = self.phase_config.intensity

        # Fatigue penalty (high fatigue reduces learning)
        fatigue_penalty = 1.0 - (player_fatigue / 200)  # 50% at max fatigue

        # Calculate final XP
        total_xp = (
            base_xp
            * drill_duration_minutes
            * age_modifier
            * position_modifier
            * intensity_modifier
            * fatigue_penalty
        )

        result.xp_gains[drill_target_stat] = total_xp

        # Calculate fatigue cost
        result.fatigue_added = drill_duration_minutes * self.phase_config.intensity / 10

        # Check for skill level up
        current_rating = player_ratings.get(drill_target_stat, 50)
        threshold = self.calculate_xp_threshold(current_rating)

        # Assume player has accumulated XP from previous sessions
        # This is a simplified check - in practice, XP pools would be stored
        if total_xp >= threshold * 0.5:  # Big session
            result.notes.append(f"Great session! Major progress on {drill_target_stat}")
            result.session_grade = "A"
        elif total_xp >= threshold * 0.25:
            result.notes.append(f"Solid session for {drill_target_stat}")
            result.session_grade = "B"
        else:
            result.notes.append(f"Light session - maintenance work on {drill_target_stat}")
            result.session_grade = "C"

        # Injury risk check
        injury_result = self._check_injury_risk(
            base_risk=drill_injury_risk,
            fatigue=player_fatigue + result.fatigue_added,
            age=player_age,
        )

        if injury_result["occurred"]:
            result.injury_occurred = True
            result.injury_type = injury_result["type"]
            result.injury_severity = injury_result["severity"]
            result.weeks_out = injury_result["weeks_out"]
            result.session_grade = "F"
            result.notes.append(f"⚠️ INJURY: {injury_result['type']} ({injury_result['severity']})")

        return result

    def _check_injury_risk(
        self,
        base_risk: float,
        fatigue: float,
        age: int,
    ) -> Dict:
        """
        Calculate injury probability and determine outcome.

        Args:
            base_risk: Drill's base injury risk (0.0-1.0)
            fatigue: Player's fatigue level (0-100)
            age: Player's age

        Returns:
            Dictionary with injury outcome details
        """
        # Fatigue multiplier (doubles risk at high fatigue)
        fatigue_multiplier = 1.0 + (fatigue / 50)

        # Age penalty (+5% per year over 28)
        age_penalty = max(0, (age - 28) * 0.05)

        # Combined risk
        total_risk = base_risk * fatigue_multiplier + age_penalty

        # Compare to phase tolerance
        if total_risk > self.phase_config.risk_tolerance:
            risk_roll = self.rng.random()
            if risk_roll < (total_risk - self.phase_config.risk_tolerance):
                # Injury occurred
                severity = self._determine_injury_severity(total_risk)
                return {
                    "occurred": True,
                    "type": self._get_random_injury_type(),
                    "severity": severity,
                    "weeks_out": self._calculate_recovery_weeks(severity),
                }

        return {"occurred": False}

    def _determine_injury_severity(self, risk_level: float) -> str:
        """Determine injury severity based on overall risk."""
        roll = self.rng.random()
        if roll < 0.6:
            return "minor"      # 1-2 weeks
        elif roll < 0.9:
            return "moderate"   # 3-6 weeks
        else:
            return "severe"     # 8-16 weeks

    def _get_random_injury_type(self) -> str:
        """Get a random training injury type."""
        injuries = [
            "hamstring_strain",
            "ankle_sprain",
            "knee_sprain",
            "shoulder_strain",
            "groin_pull",
            "back_tightness",
            "calf_strain",
        ]
        return self.rng.choice(injuries)

    def _calculate_recovery_weeks(self, severity: str) -> int:
        """Calculate recovery time based on severity."""
        recovery_ranges = {
            "minor": (1, 2),
            "moderate": (3, 6),
            "severe": (8, 16),
        }
        min_weeks, max_weeks = recovery_ranges.get(severity, (1, 2))
        return self.rng.randint(min_weeks, max_weeks)

    def recommend_drills_for_player(
        self,
        player_position: str,
        player_ratings: Dict[str, int],
        focus_area: Optional[str] = None,
    ) -> List[str]:
        """
        Recommend drills based on player's weakest stats.

        Args:
            player_position: Position code
            player_ratings: Current ratings
            focus_area: Optional specific area to focus on

        Returns:
            List of recommended drill/stat names prioritized by need
        """
        # Get development rates for position
        position_rates = POSITION_DEVELOPMENT_RATES.get(
            player_position,
            POSITION_DEVELOPMENT_RATES["DEFAULT"]
        )

        # Score each stat by: training_value = development_rate * (99 - current_rating)
        # Higher score = more room to grow with good development rate
        recommendations = []

        for stat, dev_rate in position_rates.items():
            current = player_ratings.get(stat, 50)
            room_to_grow = 99 - current
            training_value = dev_rate * room_to_grow

            # Skip if focus_area specified and doesn't match
            if focus_area and stat != focus_area:
                continue

            recommendations.append((stat, training_value))

        # Sort by training value (highest first)
        recommendations.sort(key=lambda x: x[1], reverse=True)

        return [stat for stat, _ in recommendations[:5]]  # Top 5
