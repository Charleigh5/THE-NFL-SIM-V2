"""
NFL Reference Data Module
=========================
Contains historical data and analytics parameters for the simulation engine.
Source: NFL Financial Thresholds and Salary Cap Performance Metrics.
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum

# ============================================================================
# SALARY CAP DATA
# ============================================================================

# Historical Salary Cap Maximums (1994-2025)
# Note: 2010 was an uncapped year.
HISTORICAL_SALARY_CAPS: Dict[int, Optional[int]] = {
    2025: 279_200_000,
    2024: 255_400_000,
    2023: 224_800_000,
    2022: 208_200_000,
    2021: 182_500_000,
    2020: 198_200_000,
    2019: 188_200_000,
    2018: 177_200_000,
    2017: 167_000_000,
    2016: 155_270_000,
    2015: 143_280_000,
    2014: 133_000_000,
    2013: 123_000_000,
    2012: 120_600_000,
    2011: 120_400_000,
    2010: None,  # Uncapped Year
    2009: 128_000_000,
    2008: 116_000_000,
    2007: 109_000_000,
    2006: 102_000_000,
    2005: 85_500_000,
    2004: 80_600_000,
    2003: 75_000_000,
    2002: 71_100_000,
    2001: 67_400_000,
    2000: 63_200_000,
    1999: 57_300_000,
    1998: 52_400_000,
    1997: 41_500_000,
    1996: 40_800_000,
    1995: 37_100_000,
    1994: 34_600_000,
}

# Compound Annual Growth Rate (CAGR) for Salary Cap (1994-2025)
SALARY_CAP_CAGR = 0.0697  # 6.97%

# ============================================================================
# SPECIAL PLAYS DATA
# ============================================================================

class RiskLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"

@dataclass(frozen=True)
class PlayReference:
    """Statistical reference for a specific play type."""
    name: str
    success_rate_min: float
    success_rate_max: float
    epa_value: float
    risk_level: RiskLevel
    description: str
    prerequisites: Optional[str] = None
    personnel: Optional[str] = None
    frequency_per_game: Optional[float] = None

    @property
    def success_rate_avg(self) -> float:
        return (self.success_rate_min + self.success_rate_max) / 2.0

SPECIAL_PLAYS: Dict[str, PlayReference] = {
    "TUSH_PUSH": PlayReference(
        name="Tush Push",
        success_rate_min=0.81,
        success_rate_max=0.927,
        epa_value=0.25,
        risk_level=RiskLevel.LOW,
        description="QB Sneak with pushers. Highly efficient in short yardage."
    ),
    "FLEA_FLICKER": PlayReference(
        name="Flea Flicker",
        success_rate_min=0.35,
        success_rate_max=0.55,
        epa_value=0.8,
        risk_level=RiskLevel.MODERATE,
        description="RB flip back to QB for deep shot."
    ),
    "FAKE_PUNT": PlayReference(
        name="Fake Punt",
        success_rate_min=0.60,
        success_rate_max=0.75,
        epa_value=0.4,
        risk_level=RiskLevel.HIGH,
        description="Special teams trick play."
    ),
    "RPO": PlayReference(
        name="RPO",
        success_rate_min=0.55,
        success_rate_max=0.68,
        epa_value=0.35,
        risk_level=RiskLevel.LOW,
        description="Run-Pass Option. Modern offensive staple."
    ),
    "HAIL_MARY": PlayReference(
        name="Hail Mary",
        success_rate_min=0.04,
        success_rate_max=0.12,
        epa_value=-0.5, # Usually low expected value due to incompletion prob
        risk_level=RiskLevel.HIGH,
        description="Desperation deep pass to end zone.",
        prerequisites="End of half/game; long distance"
    )
}

# ============================================================================
# 4TH DOWN ANALYTICS
# ============================================================================

@dataclass(frozen=True)
class FourthDownAnalytics:
    """Parameters for 4th down decision making."""
    always_go_distance: int = 1         # 4th & 1 is 95.2% optimal to go
    consider_go_distance: int = 5       # 4th & 5 or less is often optimal
    go_for_it_zone_start: int = 40      # Own 40
    go_for_it_zone_end: int = 60        # Opponent's 40
    win_prob_penalty_punt_4th_5: float = 0.03 # 3% WP forfeited by punting on 4th & 5
    late_game_trailing_2scores_override: bool = True

FOURTH_DOWN_ANALYTICS = FourthDownAnalytics()

# ============================================================================
# CAREER & PROGRESSION DATA
# ============================================================================

@dataclass(frozen=True)
class PositionCareerData:
    """Career longevity and peak data by position."""
    avg_length_games: int
    peak_age_start: int
    peak_age_end: int
    decline_rate_post_30: float

POSITION_CAREER_DATA: Dict[str, PositionCareerData] = {
    "QB": PositionCareerData(avg_length_games=62, peak_age_start=26, peak_age_end=32, decline_rate_post_30=0.03),
    "RB": PositionCareerData(avg_length_games=30, peak_age_start=22, peak_age_end=27, decline_rate_post_30=0.15),
    "WR": PositionCareerData(avg_length_games=38, peak_age_start=24, peak_age_end=29, decline_rate_post_30=0.08),
    "OT": PositionCareerData(avg_length_games=45, peak_age_start=25, peak_age_end=31, decline_rate_post_30=0.05),
    "DB": PositionCareerData(avg_length_games=38, peak_age_start=23, peak_age_end=28, decline_rate_post_30=0.10),
}

# ============================================================================
# TRICK PLAY CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class TrickPlayConfiguration:
    """Configuration for trick play success and risk."""
    name: str
    base_success_rate: float
    min_success_rate: float  # Against 'Safe' defense
    max_success_rate: float  # Against 'Vulnerable' defense
    turnover_risk_multiplier: float   # Multiplier on base interception/fumble chance
    confusion_duration_s: float  # Reduction in defender reaction time (seconds)

TRICK_PLAY_TABLE: Dict[str, TrickPlayConfiguration] = {
    "FAKE_PUNT_RUN": TrickPlayConfiguration(
        name="Fake Punt Run",
        base_success_rate=0.45,
        min_success_rate=0.05,
        max_success_rate=0.85,
        turnover_risk_multiplier=1.2,
        confusion_duration_s=0.5
    ),
    "FAKE_PUNT_PASS": TrickPlayConfiguration(
        name="Fake Punt Pass",
        base_success_rate=0.38,
        min_success_rate=0.02,
        max_success_rate=0.75,
        turnover_risk_multiplier=2.0,
        confusion_duration_s=0.6
    ),
    "FAKE_FG_RUN": TrickPlayConfiguration(
        name="Fake FG Run",
        base_success_rate=0.42,
        min_success_rate=0.05,
        max_success_rate=0.80,
        turnover_risk_multiplier=1.5,
        confusion_duration_s=0.4
    ),
    "FAKE_FG_PASS": TrickPlayConfiguration(
        name="Fake FG Pass",
        base_success_rate=0.35,
        min_success_rate=0.01,
        max_success_rate=0.70,
        turnover_risk_multiplier=2.2,
        confusion_duration_s=0.5
    ),
    "FLEA_FLICKER": TrickPlayConfiguration(
        name="Flea Flicker",
        base_success_rate=0.30,
        min_success_rate=0.10,
        max_success_rate=0.60,
        turnover_risk_multiplier=2.5,
        confusion_duration_s=1.2
    ),
    "PHILLY_SPECIAL": TrickPlayConfiguration(
        name="Philly Special",
        base_success_rate=0.33,
        min_success_rate=0.05,
        max_success_rate=0.65,
        turnover_risk_multiplier=1.6,
        confusion_duration_s=1.0
    ),
}
