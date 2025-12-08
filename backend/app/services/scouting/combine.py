#!/usr/bin/env python3
"""
Combine Module
==============
Simulates the NFL Scouting Combine.

Phase 8: Scouting & Draft
- Physical drill simulation
- Metric conversions (40yd -> Speed Rating)
- Random variance (Good/Bad days)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import random
import math

@dataclass
class CombineResults:
    """Raw metric results from combine drills."""
    forty_yard: float         # seconds (e.g. 4.42)
    bench_reps: int           # reps @ 225 (e.g. 24)
    vertical_jump: float      # inches (e.g. 36.5)
    broad_jump: int           # inches (e.g. 125)
    three_cone: float         # seconds (e.g. 6.95)
    shuttle: float            # seconds (e.g. 4.10)

    # Metadata
    participated: bool = True
    injury_flag: bool = False


class CombineSimulation:
    """
    Simulates combine performance based on true attributes.
    """

    def run_combine(self, true_attributes: Dict[str, int], position: str) -> CombineResults:
        """
        Generate mock combine numbers derived from ratings.
        """
        # 1. 40 Yard Dash (Speed + Acceleration)
        # 99 Speed ~ 4.25, 50 Speed ~ 4.80 (Linear approx for simplicity)
        speed_rating = true_attributes.get("speed", 50)
        # Physics: Inverse relationship. Higher rating = Lower time.
        # Base 5.4 - (Rating * 0.012) -> 99 = 4.21, 50 = 4.8
        base_40 = 5.4 - (speed_rating * 0.012)
        variance_40 = random.uniform(-0.05, 0.05)
        forty = round(base_40 + variance_40, 2)

        # 2. Bench Press (Strength)
        strength = true_attributes.get("strength", 50)
        # 99 Str ~ 40 reps, 50 Str ~ 15 reps
        # Base -5 + (Rating * 0.45) -> 99 = 39.5, 50 = 17.5
        base_bench = max(0, -5 + (strength * 0.45))
        reps = int(base_bench + random.uniform(-2, 3))

        # 3. Vertical (Jumping)
        jump = true_attributes.get("jumping", 50)
        # 99 Jump ~ 45", 50 Jump ~ 30"
        base_vert = 20 + (jump * 0.25)
        vert = round(base_vert + random.uniform(-1.5, 1.5), 1)

        # 4. 3-Cone (Agility)
        agility = true_attributes.get("agility", 50)
        # 99 Agility ~ 6.5, 50 ~ 7.3
        base_cone = 8.1 - (agility * 0.016)
        cone = round(base_cone + random.uniform(-0.1, 0.1), 2)

        # Broad Jump (Explosion - mix of Jump/Str)
        base_broad = 100 + (jump * 0.3) + (strength * 0.1)
        broad = int(base_broad + random.uniform(-4, 4))

        # Shuttle (Change of Direction - Agility/Accel)
        accel = true_attributes.get("acceleration", 50)
        base_shuttle = 4.9 - (agility * 0.005) - (accel * 0.005)
        shuttle = round(base_shuttle + random.uniform(-0.05, 0.05), 2)

        return CombineResults(
            forty_yard=forty,
            bench_reps=max(0, reps),
            vertical_jump=vert,
            broad_jump=broad,
            three_cone=cone,
            shuttle=shuttle
        )
