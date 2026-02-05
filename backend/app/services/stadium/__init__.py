"""
STADIUM Package
===============
Stadium and crowd simulation systems.

Phase 10: Stadium Effects
- Stadium Configuration
- Crowd Dynamics
- Home Field Advantage
"""

from .crowd import (
    CrowdDynamics,
    CrowdEngine,
    CrowdMood,
)
from .stadium import (
    CrowdState,
    HomeFieldBonus,
    NoiseLevel,
    StadiumConfig,
    StadiumEngine,
    StadiumType,
    SurfaceType,
)

__all__ = [
    # Stadium
    "StadiumEngine", "StadiumConfig", "CrowdState", "HomeFieldBonus",
    "StadiumType", "SurfaceType", "NoiseLevel",
    # Crowd
    "CrowdEngine", "CrowdDynamics", "CrowdMood",
]
