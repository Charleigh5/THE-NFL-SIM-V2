#!/usr/bin/env python3
"""
Coaching Personality System
===========================
Game-day coaching personalities that affect play-calling decisions.

Personalities affect:
- Aggression level (4th down decisions, deep passes)
- Run/Pass ratio tendencies
- In-game adjustments
- Risk tolerance
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum


class CoachingPersonality(str, Enum):
    """Game-day coaching personality types."""
    CONSERVATIVE = "CONSERVATIVE"  # Ball control, limit turnovers
    BALANCED = "BALANCED"          # Situational, adaptable
    AGGRESSIVE = "AGGRESSIVE"      # Push tempo, take chances
    GAMBLER = "GAMBLER"            # High risk, high reward


@dataclass
class PersonalityProfile:
    """
    Configuration for a coaching personality.

    Attributes:
        name: Display name
        aggression: 0.0 (very conservative) to 1.0 (very aggressive)
        run_pass_ratio: 0.0 (all pass) to 1.0 (all run)
        fourth_down_threshold: Distance willing to go for on 4th
        deep_pass_tendency: Multiplier for deep pass selection
        two_point_threshold: Score difference to attempt 2-pt conversion
        timeout_aggression: How aggressively to use timeouts
    """
    name: str
    aggression: float
    run_pass_ratio: float
    fourth_down_threshold: int  # Max yards to go for it
    deep_pass_tendency: float
    two_point_threshold: int
    timeout_aggression: float


# ============================================================================
# PERSONALITY DEFINITIONS
# ============================================================================

PERSONALITY_PROFILES: Dict[CoachingPersonality, PersonalityProfile] = {
    CoachingPersonality.CONSERVATIVE: PersonalityProfile(
        name="Conservative",
        aggression=0.20,
        run_pass_ratio=0.55,  # Run-heavy
        fourth_down_threshold=1,  # Only go for it on 4th and 1
        deep_pass_tendency=0.6,  # 40% less deep passes
        two_point_threshold=15,  # Only when way behind
        timeout_aggression=0.3,
    ),
    CoachingPersonality.BALANCED: PersonalityProfile(
        name="Balanced",
        aggression=0.50,
        run_pass_ratio=0.45,
        fourth_down_threshold=2,
        deep_pass_tendency=1.0,  # Baseline
        two_point_threshold=8,
        timeout_aggression=0.5,
    ),
    CoachingPersonality.AGGRESSIVE: PersonalityProfile(
        name="Aggressive",
        aggression=0.75,
        run_pass_ratio=0.38,  # Pass-heavy
        fourth_down_threshold=3,
        deep_pass_tendency=1.3,  # 30% more deep passes
        two_point_threshold=4,
        timeout_aggression=0.7,
    ),
    CoachingPersonality.GAMBLER: PersonalityProfile(
        name="Gambler",
        aggression=0.90,
        run_pass_ratio=0.30,  # Very pass-heavy
        fourth_down_threshold=5,  # Go for it on 4th and 5
        deep_pass_tendency=1.5,  # 50% more deep passes
        two_point_threshold=0,  # Always consider it
        timeout_aggression=0.9,
    ),
}


# ============================================================================
# SITUATIONAL MODIFIERS
# ============================================================================

def get_situational_modifiers(
    score_diff: int,
    time_remaining_seconds: int,
    is_home: bool,
    quarter: int
) -> Dict[str, float]:
    """
    Calculate situational modifiers to coaching behavior.

    Args:
        score_diff: Positive = winning, negative = losing
        time_remaining_seconds: Time left in game
        is_home: Playing at home
        quarter: Current quarter (1-4)

    Returns:
        Dict with modifiers for aggression, run_ratio, etc.
    """
    modifiers = {
        "aggression": 0.0,
        "run_ratio": 0.0,
        "deep_tendency": 0.0,
    }

    # Home field confidence
    if is_home:
        modifiers["aggression"] += 0.05

    # Trailing adjustments
    if score_diff < -14:
        modifiers["aggression"] += 0.20
        modifiers["run_ratio"] -= 0.15  # More passing
        modifiers["deep_tendency"] += 0.2
    elif score_diff < -7:
        modifiers["aggression"] += 0.10
        modifiers["run_ratio"] -= 0.08

    # Leading adjustments (protect the lead)
    if score_diff > 14:
        modifiers["aggression"] -= 0.15
        modifiers["run_ratio"] += 0.20  # More running
        modifiers["deep_tendency"] -= 0.3
    elif score_diff > 7:
        modifiers["aggression"] -= 0.08
        modifiers["run_ratio"] += 0.10

    # Late game adjustments
    if quarter == 4 and time_remaining_seconds < 300:  # Final 5 minutes
        if score_diff < 0:
            # Trailing: become more aggressive
            modifiers["aggression"] += 0.15
            modifiers["run_ratio"] -= 0.15
        elif score_diff > 0:
            # Leading: become conservative, run clock
            modifiers["aggression"] -= 0.20
            modifiers["run_ratio"] += 0.25

    return modifiers


def apply_personality_modifiers(
    profile: PersonalityProfile,
    score_diff: int,
    time_remaining: int,
    is_home: bool,
    quarter: int
) -> Dict[str, float]:
    """
    Get final play-calling parameters with situational adjustments.

    Returns:
        Dict with final aggression, run_pass_ratio, etc.
    """
    situational = get_situational_modifiers(
        score_diff, time_remaining, is_home, quarter
    )

    # Apply modifiers with clamping
    return {
        "aggression": max(0.0, min(1.0,
            profile.aggression + situational["aggression"]
        )),
        "run_pass_ratio": max(0.10, min(0.90,
            profile.run_pass_ratio + situational["run_ratio"]
        )),
        "deep_pass_tendency": max(0.3, min(2.0,
            profile.deep_pass_tendency + situational["deep_tendency"]
        )),
        "fourth_down_threshold": profile.fourth_down_threshold,
        "two_point_threshold": profile.two_point_threshold,
    }


def get_personality_for_coach(
    aggression_rating: int,
    risk_tolerance: int = None
) -> CoachingPersonality:
    """
    Determine personality based on coach attributes.

    Args:
        aggression_rating: Coach's aggression stat (0-100)
        risk_tolerance: Optional override

    Returns:
        Matching CoachingPersonality
    """
    score = risk_tolerance if risk_tolerance is not None else aggression_rating

    if score >= 80:
        return CoachingPersonality.GAMBLER
    elif score >= 60:
        return CoachingPersonality.AGGRESSIVE
    elif score >= 40:
        return CoachingPersonality.BALANCED
    else:
        return CoachingPersonality.CONSERVATIVE


# ============================================================================
# PLAYCALLER INTEGRATION
# ============================================================================

def create_playcaller_config(
    personality: CoachingPersonality,
    score_diff: int = 0,
    time_remaining: int = 3600,
    is_home: bool = True,
    quarter: int = 1
) -> Dict[str, float]:
    """
    Generate PlayCaller initialization parameters from personality.

    This is designed to integrate with PlayCaller.__init__():
        PlayCaller(rng, aggression=config["aggression"],
                   run_pass_ratio=config["run_pass_ratio"])
    """
    profile = PERSONALITY_PROFILES[personality]

    return apply_personality_modifiers(
        profile, score_diff, time_remaining, is_home, quarter
    )
