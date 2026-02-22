#!/usr/bin/env python3
"""
Stadium Module
==============
Manages stadium characteristics and home field advantage.

Phase 10: Stadium Effects
- Stadium configurations
- Home field advantage calculations
- Crowd noise levels
"""

from dataclasses import dataclass
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================


class StadiumType(str, Enum):
    """Type of stadium."""

    OPEN_AIR = "OPEN_AIR"
    DOME = "DOME"
    RETRACTABLE = "RETRACTABLE"


class SurfaceType(str, Enum):
    """Playing surface."""

    NATURAL_GRASS = "NATURAL_GRASS"
    FIELD_TURF = "FIELD_TURF"
    HYBRID = "HYBRID"


class NoiseLevel(str, Enum):
    """Crowd noise intensity."""

    QUIET = "QUIET"  # <70 dB
    MODERATE = "MODERATE"  # 70-85 dB
    LOUD = "LOUD"  # 85-100 dB
    DEAFENING = "DEAFENING"  # >100 dB (Arrowhead, CenturyLink)


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class StadiumConfig:
    """Stadium configuration."""

    stadium_id: str
    name: str
    team_id: str
    capacity: int
    stadium_type: StadiumType
    surface: SurfaceType
    altitude: int = 0  # Feet above sea level (Denver = 5280)
    base_noise_rating: int = 70  # 1-100 scale


@dataclass
class CrowdState:
    """Current crowd conditions."""

    attendance: int
    attendance_pct: float  # 0.0 - 1.0
    noise_level: NoiseLevel
    energy: float = 0.5  # 0.0 - 1.0 (momentum-based)


@dataclass
class HomeFieldBonus:
    """Calculated home field effects."""

    false_start_modifier: float  # Increases opponent false starts
    snap_count_modifier: float  # Makes it harder to hear snap
    fatigue_modifier: float  # Altitude effect
    crowd_energy_bonus: float  # Performance boost


# ============================================================================
# STADIUM ENGINE
# ============================================================================


class StadiumEngine:
    """
    Calculates home field advantage effects.
    """

    # Kown loud stadiums (NFL calibrated)
    LOUD_STADIUMS = {"KC", "SEA", "NO", "DEN", "BAL", "MIN", "BUF"}

    def __init__(self, config: StadiumConfig):
        self.config = config

    def calculate_noise_level(self, crowd: CrowdState, game_situation: str) -> NoiseLevel:
        """
        Determine current noise level based on crowd and situation.
        """
        # Base from stadium rating
        base = self.config.base_noise_rating

        # Attendance modifier
        attendance_mod = crowd.attendance_pct * 20

        # Situation modifier
        situation_mod = 0
        if game_situation == "CRITICAL":  # 3rd down, red zone
            situation_mod = 15
        elif game_situation == "BIG_PLAY":
            situation_mod = 25

        # Energy modifier
        energy_mod = crowd.energy * 10

        # Dome / Known Loud Stadium Bonus
        dome_bonus = 0
        if (
            self.config.stadium_type == StadiumType.DOME
            or self.config.stadium_id in self.LOUD_STADIUMS
        ):
            dome_bonus = 10  # Reflective acoustics

        total = base + attendance_mod + situation_mod + energy_mod + dome_bonus

        if total >= 95:
            return NoiseLevel.DEAFENING
        elif total >= 80:
            return NoiseLevel.LOUD
        elif total >= 65:
            return NoiseLevel.MODERATE
        else:
            return NoiseLevel.QUIET

    def calculate_home_field_bonus(self, crowd: CrowdState) -> HomeFieldBonus:
        """
        Calculate all home field advantage effects.
        """
        # False start risk for away team
        # Louder crowd = higher risk
        noise_factor = {
            NoiseLevel.QUIET: 0.0,
            NoiseLevel.MODERATE: 0.02,
            NoiseLevel.LOUD: 0.05,
            NoiseLevel.DEAFENING: 0.10,
        }[crowd.noise_level]

        # Snap count difficulty
        snap_mod = noise_factor * 2

        # Altitude effect (Denver)
        altitude_factor = 0.0
        if self.config.altitude > 4000:
            # Physics-based fatigue drain
            # Every 1000 ft above 4000 = 2.5% more fatigue for visitors
            altitude_factor = ((self.config.altitude - 4000) / 1000) * 0.025

        # Crowd energy bonus to home team
        energy_bonus = crowd.energy * 0.05  # Up to 5% performance boost

        return HomeFieldBonus(
            false_start_modifier=noise_factor,
            snap_count_modifier=snap_mod,
            fatigue_modifier=altitude_factor,
            crowd_energy_bonus=energy_bonus,
        )

    def update_crowd_energy(self, current: CrowdState, event: str) -> CrowdState:
        """
        Update crowd energy based on game events.
        """
        energy_changes = {
            "TOUCHDOWN_HOME": 0.25,
            "TOUCHDOWN_AWAY": -0.15,
            "TURNOVER_HOME": 0.20,
            "TURNOVER_AWAY": -0.20,
            "BIG_PLAY_HOME": 0.15,
            "BIG_PLAY_AWAY": -0.10,
            "SACK_HOME": 0.10,
        }

        delta = energy_changes.get(event, 0.0)
        new_energy = max(0.0, min(1.0, current.energy + delta))

        # Update noise level based on new energy
        new_noise = self.calculate_noise_level(current, "NORMAL")

        return CrowdState(
            attendance=current.attendance,
            attendance_pct=current.attendance_pct,
            noise_level=new_noise,
            energy=new_energy,
        )
