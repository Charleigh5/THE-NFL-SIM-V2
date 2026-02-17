"""
Crowd Noise System
==================
Models stadium atmosphere and its effects on gameplay.

CITATION: ENHANCEMENT_REFERENCE.md - Crowd Noise Impact
- Affects audible execution for away team
- Increases false start probability
- Momentum swings affect crowd intensity
"""

from dataclasses import dataclass
from enum import Enum


class NoiseLevel(str, Enum):
    """Stadium noise levels in decibels (approximate)."""
    QUIET = "QUIET"           # ~50 dB - Empty/low attendance
    MODERATE = "MODERATE"     # ~70 dB - Normal crowd
    LOUD = "LOUD"             # ~90 dB - Big moment
    DEAFENING = "DEAFENING"   # ~110+ dB - CenturyLink/Arrowhead level


# Noise level thresholds in decibels
NOISE_DB_THRESHOLDS: dict[NoiseLevel, int] = {
    NoiseLevel.QUIET: 50,
    NoiseLevel.MODERATE: 70,
    NoiseLevel.LOUD: 90,
    NoiseLevel.DEAFENING: 110,
}


@dataclass
class CrowdNoiseState:
    """
    Current state of crowd noise and its effects.
    """
    current_db: float = 70.0           # Current decibel level
    base_db: float = 70.0              # Stadium baseline
    momentum_bonus: float = 0.0        # Bonus from momentum (-10 to +20 dB)
    is_home_team_on_offense: bool = False

    @property
    def noise_level(self) -> NoiseLevel:
        """Categorize current noise level."""
        total_db = self.current_db + self.momentum_bonus

        if self.is_home_team_on_offense:
            # Crowd quiets for home offense
            total_db -= 15

        if total_db >= NOISE_DB_THRESHOLDS[NoiseLevel.DEAFENING]:
            return NoiseLevel.DEAFENING
        elif total_db >= NOISE_DB_THRESHOLDS[NoiseLevel.LOUD]:
            return NoiseLevel.LOUD
        elif total_db >= NOISE_DB_THRESHOLDS[NoiseLevel.MODERATE]:
            return NoiseLevel.MODERATE
        else:
            return NoiseLevel.QUIET

    def get_effective_db(self) -> float:
        """Get effective decibel level including all modifiers."""
        total = self.current_db + self.momentum_bonus
        if self.is_home_team_on_offense:
            total -= 15  # Crowd quiets for home team
        return max(40, min(130, total))  # Clamp to realistic range


@dataclass
class CrowdNoiseEffects:
    """
    Gameplay effects caused by crowd noise on the AWAY team.
    """
    audible_success_rate: float = 1.0      # Multiplier for audible success
    false_start_probability: float = 0.0   # Added probability (0-0.15)
    communication_drop_rate: float = 0.0   # % of verbal signals missed
    awareness_penalty: int = 0             # Penalty to Awareness rating


def calculate_crowd_noise_effects(
    noise_state: CrowdNoiseState,
    player_awareness: int = 80,
    is_away_team: bool = True,
) -> CrowdNoiseEffects:
    """
    Calculate gameplay effects of crowd noise.

    Args:
        noise_state: Current crowd noise state
        player_awareness: Player's awareness rating (used for resistance)
        is_away_team: Whether the affected team is the away team

    Returns:
        CrowdNoiseEffects with all calculated penalties
    """
    effects = CrowdNoiseEffects()

    # Home team is not affected by their own crowd
    if not is_away_team:
        return effects

    effective_db = noise_state.get_effective_db()
    noise_level = noise_state.noise_level

    # Awareness provides resistance (higher = less affected)
    awareness_resistance = player_awareness / 100.0  # 0.0 - 1.0

    # Calculate effects based on noise level
    if noise_level == NoiseLevel.DEAFENING:
        # Stadium is ROARING - significant penalties
        base_audible_penalty = 0.40           # -40% audible success
        base_false_start = 0.12               # +12% false start risk
        base_comm_drop = 0.30                 # 30% signals dropped
        base_awareness_penalty = 8            # -8 awareness

    elif noise_level == NoiseLevel.LOUD:
        # Big moment - moderate penalties
        base_audible_penalty = 0.25
        base_false_start = 0.06
        base_comm_drop = 0.15
        base_awareness_penalty = 4

    elif noise_level == NoiseLevel.MODERATE:
        # Normal crowd - minor penalties
        base_audible_penalty = 0.10
        base_false_start = 0.02
        base_comm_drop = 0.05
        base_awareness_penalty = 0

    else:  # QUIET
        # Minimal effect
        return effects

    # Apply awareness resistance
    resistance_factor = 1.0 - (awareness_resistance * 0.5)  # 50% mitigation at 100 AWR

    effects.audible_success_rate = 1.0 - (base_audible_penalty * resistance_factor)
    effects.false_start_probability = base_false_start * resistance_factor
    effects.communication_drop_rate = base_comm_drop * resistance_factor
    effects.awareness_penalty = int(base_awareness_penalty * resistance_factor)

    return effects


def update_crowd_noise_from_momentum(
    noise_state: CrowdNoiseState,
    home_momentum: int,
    turnover_just_occurred: bool = False,
    touchdown_just_occurred: bool = False,
    big_play_just_occurred: bool = False,
) -> CrowdNoiseState:
    """
    Update crowd noise based on game momentum and events.

    Args:
        noise_state: Current noise state
        home_momentum: Home team momentum (-10 to +10)
        turnover_just_occurred: If home team just forced turnover
        touchdown_just_occurred: If home team just scored
        big_play_just_occurred: If home team just had 20+ yard play

    Returns:
        Updated CrowdNoiseState
    """
    # Base momentum effect: -10 to +10 momentum -> -5 to +15 dB
    momentum_db = (home_momentum + 10) * 0.75  # 0 to 15 dB swing

    # Spike events add temporary boost
    event_bonus = 0.0
    if turnover_just_occurred:
        event_bonus += 10.0  # +10 dB spike
    if touchdown_just_occurred:
        event_bonus += 15.0  # +15 dB spike
    if big_play_just_occurred:
        event_bonus += 8.0   # +8 dB spike

    # Event bonus decays over time (handled elsewhere)
    noise_state.momentum_bonus = momentum_db + event_bonus

    return noise_state


def get_stadium_base_noise(stadium_name: str | None = None) -> float:
    """
    Get baseline noise level for a stadium.

    Some stadiums are known for exceptional crowd noise.
    """
    LOUD_STADIUMS = {
        "Arrowhead Stadium": 85,      # Chiefs - famously loud
        "CenturyLink Field": 85,      # Seahawks - 12th Man
        "Mercedes-Benz Superdome": 82, # Saints - indoor
        "NRG Stadium": 78,            # Texans - retractable roof
        "U.S. Bank Stadium": 80,      # Vikings - indoor
        "SoFi Stadium": 75,           # Chargers/Rams - newer design
    }

    if stadium_name and stadium_name in LOUD_STADIUMS:
        return LOUD_STADIUMS[stadium_name]

    # Default baseline
    return 72.0
