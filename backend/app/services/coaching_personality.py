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
    CEO = "CEO"                    # Leader, Balanced
    GURU_OFF = "GURU_OFF"          # Offensive Scheme
    GURU_DEF = "GURU_DEF"          # Defensive Scheme
    ANALYTICS = "ANALYTICS"        # Aggressive Logic
    OLD_SCHOOL = "OLD_SCHOOL"      # Run heavy, conservative
    RIVERBOAT = "RIVERBOAT"        # Gambler
    ROOKIE = "ROOKIE"              # Basic
    # Deprecated mappings
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    AGGRESSIVE = "AGGRESSIVE"
    GAMBLER = "GAMBLER"


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
    adaptive_score: float = 0.5        # How fast they change plans (New)
    run_clock_urgency: float = 0.5     # Preference for running clock (New)


# ============================================================================
# PERSONALITY DEFINITIONS
# ============================================================================

PERSONALITY_PROFILES: Dict[CoachingPersonality, PersonalityProfile] = {
    CoachingPersonality.CEO: PersonalityProfile(
        name="The CEO",
        aggression=0.40,
        run_pass_ratio=0.50, # Balanced
        fourth_down_threshold=2,
        deep_pass_tendency=1.0,
        two_point_threshold=8,
        timeout_aggression=0.5,
        adaptive_score=0.8,
        run_clock_urgency=0.6
    ),
    CoachingPersonality.GURU_OFF: PersonalityProfile(
        name="Offensive Guru",
        aggression=0.65,
        run_pass_ratio=0.40, # Pass Lean
        fourth_down_threshold=2,
        deep_pass_tendency=1.1,
        two_point_threshold=6,
        timeout_aggression=0.6,
        adaptive_score=0.9,
        run_clock_urgency=0.4
    ),
    CoachingPersonality.GURU_DEF: PersonalityProfile(
        name="Defensive Schemer",
        aggression=0.30,
        run_pass_ratio=0.60, # Run Lean
        fourth_down_threshold=1,
        deep_pass_tendency=0.7,
        two_point_threshold=14,
        timeout_aggression=0.4,
        adaptive_score=0.7,
        run_clock_urgency=0.8
    ),
    CoachingPersonality.ANALYTICS: PersonalityProfile(
        name="Analytics Disciple",
        aggression=0.85,
        run_pass_ratio=0.42,
        fourth_down_threshold=4, # Go for it often
        deep_pass_tendency=1.2,
        two_point_threshold=1, # Chart says go? Go.
        timeout_aggression=0.8,
        adaptive_score=1.0,
        run_clock_urgency=0.3
    ),
    CoachingPersonality.OLD_SCHOOL: PersonalityProfile(
        name="Old School",
        aggression=0.15,
        run_pass_ratio=0.65, # Run Heavy
        fourth_down_threshold=0, # Punt/FG almost always
        deep_pass_tendency=0.5,
        two_point_threshold=16,
        timeout_aggression=0.2,
        adaptive_score=0.3, # Stubborn
        run_clock_urgency=0.9
    ),
    CoachingPersonality.RIVERBOAT: PersonalityProfile(
        name="The Gambler",
        aggression=0.80, # High but random
        run_pass_ratio=0.45,
        fourth_down_threshold=3,
        deep_pass_tendency=1.4,
        two_point_threshold=4,
        timeout_aggression=0.7,
        adaptive_score=0.5,
        run_clock_urgency=0.5
    ),
    CoachingPersonality.ROOKIE: PersonalityProfile(
        name="The Clipboard",
        aggression=0.50,
        run_pass_ratio=0.50,
        fourth_down_threshold=2,
        deep_pass_tendency=1.0,
        two_point_threshold=8,
        timeout_aggression=0.5,
        adaptive_score=0.2, # Slow to adjust
        run_clock_urgency=0.5
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
    risk_tolerance: Optional[int] = None
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

    # Expanded 7-Archetype Logic
    if score >= 90: return CoachingPersonality.ANALYTICS
    elif score >= 80: return CoachingPersonality.GAMBLER
    elif score >= 70: return CoachingPersonality.GURU_OFF
    elif score >= 50: return CoachingPersonality.CEO
    elif score >= 40: return CoachingPersonality.BALANCED
    elif score >= 30: return CoachingPersonality.GURU_DEF
    elif score >= 20: return CoachingPersonality.OLD_SCHOOL
    else: return CoachingPersonality.ROOKIE


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
