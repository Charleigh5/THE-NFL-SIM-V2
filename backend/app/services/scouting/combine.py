#!/usr/bin/env python3
"""
Combine Module
==============
Simulates the NFL Scouting Combine.

Phase 8: Scouting & Draft
- Physical drill simulation
- Metric conversions (40yd -> Speed Rating)
- Random variance (Good/Bad days)

Phase 2 Enhancement: GENESIS Integration
- Modern metrics (power clean, GPS speed, position agility)
- BiometricProfile reveal at combine
- S2 cognition and medical flags exposure
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import random
import math

from app.engine.genesis.biometrics import BiometricProfile, generate_biometrics_for_position


@dataclass
class CombineResults:
    """
    Raw metric results from combine drills.

    B-037 to B-040: Modernized metrics replacing legacy bench_reps.
    """
    # Speed & Agility Drills
    forty_yard: float           # seconds (e.g. 4.42)
    vertical_jump: float        # inches (e.g. 36.5)
    broad_jump: int             # inches (e.g. 125)
    three_cone: float           # seconds (e.g. 6.95)
    shuttle: float              # seconds (e.g. 4.10)

    # B-038: Modern Strength Metric (replaces bench_reps)
    power_clean_max: int = 0    # lbs (e.g. 315) - functional explosive strength

    # B-039: GPS-Tracked Speed (on-field measurement)
    gps_tracked_speed: float = 0.0   # mph (e.g. 21.5) - max speed during drills

    # B-040: Position-Specific Agility Score
    position_agility_score: float = 0.0  # 0-100 composite score

    # Metadata
    participated: bool = True
    injury_flag: bool = False

    # B-044: Medical Flags (populated by GENESIS reveal)
    medical_flags: List[str] = field(default_factory=list)

    @property
    def bench_reps(self) -> int:
        """Backward compatibility: estimate bench reps from power clean max."""
        if self.power_clean_max > 0:
            return max(0, int((self.power_clean_max - 100) / 7.5))
        return 0


@dataclass
class GenesisRevealData:
    """
    B-041 to B-043: Data revealed from GENESIS biometric system at combine.
    """
    hand_size: float              # inches
    wingspan: float               # inches
    arm_length: float             # inches
    s2_cognition_score: float     # Standard score (mean=100, std=15)
    fast_twitch_percentage: float # 0-100
    reaction_time_ms: float       # milliseconds
    body_fat_percentage: float    # percent
    medical_flags: List[str]      # List of medical concerns

    @classmethod
    def from_biometric_profile(
        cls,
        profile: BiometricProfile,
        include_hidden: bool = True
    ) -> 'GenesisRevealData':
        """Create reveal data from a BiometricProfile."""
        return cls(
            hand_size=profile.hand_size,
            wingspan=profile.wingspan,
            arm_length=profile.arm_length,
            s2_cognition_score=profile.s2_cognition_score if include_hidden else 0.0,
            fast_twitch_percentage=profile.fast_twitch_percentage,
            reaction_time_ms=profile.reaction_time_ms,
            body_fat_percentage=profile.body_fat_percentage,
            medical_flags=[]  # Populated separately by medical screening
        )


class CombineSimulation:
    """
    Simulates combine performance based on true attributes.

    Enhanced with GENESIS biometric integration (B-041 to B-044).
    """

    def __init__(self):
        self._biometric_cache: Dict[int, BiometricProfile] = {}

    def run_combine(self, true_attributes: Dict[str, int], position: str) -> CombineResults:
        """
        Generate mock combine numbers derived from ratings.

        Now includes modern metrics: power clean, GPS speed, position agility.
        """
        # 1. 40 Yard Dash (Speed + Acceleration)
        speed_rating = true_attributes.get("speed", 50)
        base_40 = 5.4 - (speed_rating * 0.012)
        variance_40 = random.uniform(-0.05, 0.05)
        forty = round(base_40 + variance_40, 2)

        # 2. Power Clean Max (B-038) - Replaces bench press
        # More functional strength metric used by modern NFL
        strength = true_attributes.get("strength", 50)
        # 99 Str ~ 365 lbs, 50 Str ~ 250 lbs
        base_power_clean = 200 + (strength * 1.65)
        power_clean = int(base_power_clean + random.uniform(-10, 15))

        # 3. Vertical (Jumping)
        jump = true_attributes.get("jumping", 50)
        base_vert = 20 + (jump * 0.25)
        vert = round(base_vert + random.uniform(-1.5, 1.5), 1)

        # 4. 3-Cone (Agility)
        agility = true_attributes.get("agility", 50)
        base_cone = 8.1 - (agility * 0.016)
        cone = round(base_cone + random.uniform(-0.1, 0.1), 2)

        # 5. Broad Jump (Explosion - mix of Jump/Str)
        base_broad = 100 + (jump * 0.3) + (strength * 0.1)
        broad = int(base_broad + random.uniform(-4, 4))

        # 6. Shuttle (Change of Direction - Agility/Accel)
        accel = true_attributes.get("acceleration", 50)
        base_shuttle = 4.9 - (agility * 0.005) - (accel * 0.005)
        shuttle = round(base_shuttle + random.uniform(-0.05, 0.05), 2)

        # 7. GPS Tracked Speed (B-039)
        # On-field max speed during drills
        # 99 Speed ~ 23 mph, 50 Speed ~ 18 mph
        base_gps = 15 + (speed_rating * 0.08)
        gps_speed = round(base_gps + random.uniform(-0.3, 0.5), 1)

        # 8. Position Agility Score (B-040)
        # Composite of agility, acceleration, and position-specific tests
        base_agility_score = (agility * 0.4) + (accel * 0.3) + (speed_rating * 0.3)
        position_agility = round(base_agility_score + random.uniform(-3, 5), 1)

        return CombineResults(
            forty_yard=forty,
            vertical_jump=vert,
            broad_jump=broad,
            three_cone=cone,
            shuttle=shuttle,
            power_clean_max=max(135, power_clean),  # Min 135 lbs
            gps_tracked_speed=max(14.0, gps_speed),  # Min 14 mph
            position_agility_score=max(0, min(100, position_agility)),  # Clamp 0-100
        )

    def reveal_genesis_data(
        self,
        player_id: int,
        position: str,
        biometric_profile: Optional[BiometricProfile] = None,
        rng: Optional[Any] = None
    ) -> GenesisRevealData:
        """
        B-041: Reveal hidden GENESIS biometric data at combine.

        This exposes the BiometricProfile data that was previously hidden,
        allowing scouts to see hand size, wingspan, S2 cognition, etc.

        Args:
            player_id: Player's ID for caching
            position: Player position for generating defaults
            biometric_profile: Existing profile (or generate new one)
            rng: Random number generator for deterministic generation

        Returns:
            GenesisRevealData with revealed biometric information
        """
        # Use cached or provided profile
        if biometric_profile:
            profile = biometric_profile
        elif player_id in self._biometric_cache:
            profile = self._biometric_cache[player_id]
        else:
            # Generate new profile using GENESIS system
            if rng is None:
                # Create a simple RNG wrapper for compatibility
                class SimpleRNG:
                    def next_float(self) -> float:
                        return random.random()
                rng = SimpleRNG()

            profile = generate_biometrics_for_position(position, rng)
            self._biometric_cache[player_id] = profile

        # B-043: Create reveal data with S2 cognition
        reveal = GenesisRevealData.from_biometric_profile(profile, include_hidden=True)

        # B-044: Medical flags screening
        reveal.medical_flags = self._screen_medical_flags(profile)

        return reveal

    def _screen_medical_flags(self, profile: BiometricProfile) -> List[str]:
        """
        B-044: Generate medical flags based on biometric profile.

        Identifies potential concerns that would be found during combine medical.
        """
        flags = []

        # Body composition concerns
        if profile.body_fat_percentage > 20:
            flags.append("ELEVATED_BODY_FAT")
        if profile.body_fat_percentage < 6:
            flags.append("LOW_BODY_FAT_RISK")

        # Cardiovascular concerns
        if profile.resting_heart_rate > 75:
            flags.append("ELEVATED_RHR")
        if profile.vo2_max < 42:
            flags.append("LOW_AEROBIC_CAPACITY")
        if profile.hrv_score < 55:
            flags.append("LOW_HRV_RECOVERY")

        # Thermal regulation
        if profile.heat_tolerance < 35:
            flags.append("HEAT_SENSITIVITY")
        if profile.sweat_rate > 2.2:
            flags.append("HIGH_SWEAT_RATE")

        # Cognitive (only flagged if significantly low)
        if profile.s2_cognition_score < 85:
            flags.append("COGNITIVE_PROCESSING_CONCERN")
        if profile.reaction_time_ms > 280:
            flags.append("SLOW_REACTION_TIME")

        return flags

