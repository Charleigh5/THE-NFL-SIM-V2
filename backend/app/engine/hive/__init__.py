"""
HIVE Environment Package
========================
Environmental physics affecting gameplay.

Phase 4: HIVE Environment Physics
- Turf grid (10x10 zones)
- Equipment physics
- Weather integration
"""

from .equipment import (
    CleatType,
    EquipmentConfig,
    EquipmentPhysics,
    GloveType,
    HelmetType,
    PlayerEquipment,
)
from .turf_grid import (
    TurfCondition,
    TurfGrid,
    TurfGridConfig,
    TurfGridState,
    TurfType,
    TurfZone,
    WeatherEffect,
)
from .weather import (
    GameWeather,
    PrecipitationType,
    WeatherConfig,
    WeatherPhysics,
    WindDirection,
)

__all__ = [
    # Turf
    "TurfGrid",
    "TurfGridState",
    "TurfZone",
    "TurfGridConfig",
    "TurfType",
    "TurfCondition",
    "WeatherEffect",
    # Equipment
    "EquipmentPhysics",
    "PlayerEquipment",
    "EquipmentConfig",
    "CleatType",
    "GloveType",
    "HelmetType",
    # Weather
    "WeatherPhysics",
    "GameWeather",
    "WeatherConfig",
    "WindDirection",
    "PrecipitationType",
]
