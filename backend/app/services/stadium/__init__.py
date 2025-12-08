"""
STADIUM Package
===============
Stadium and crowd simulation systems.

Phase 10: Stadium Effects
- Stadium Configuration
- Crowd Dynamics
- Home Field Advantage
"""

from .stadium import (
    StadiumEngine,
    StadiumConfig,
    CrowdState,
    HomeFieldBonus,
    StadiumType,
    SurfaceType,
    NoiseLevel,
)

from .crowd import (
    CrowdEngine,
    CrowdDynamics,
    CrowdMood,
)

__all__ = [
    # Stadium
    "StadiumEngine", "StadiumConfig", "CrowdState", "HomeFieldBonus",
    "StadiumType", "SurfaceType", "NoiseLevel",
    # Crowd
    "CrowdEngine", "CrowdDynamics", "CrowdMood",
]
