"""
HIVE Environment Package
========================
Environmental physics affecting gameplay.

Phase 4: HIVE Environment Physics
- Turf grid (10x10 zones)
- Equipment physics
- Weather integration
"""

from .turf_grid import (
    TurfGrid,
    TurfGridState,
    TurfZone,
    TurfGridConfig,
    TurfType,
    TurfCondition,
    WeatherEffect,
)

from .equipment import (
    EquipmentPhysics,
    PlayerEquipment,
    EquipmentConfig,
    CleatType,
    GloveType,
    HelmetType,
)

from .weather import (
    WeatherPhysics,
    GameWeather,
    WeatherConfig,
    WindDirection,
    PrecipitationType,
)

__all__ = [
    # Turf
    "TurfGrid", "TurfGridState", "TurfZone", "TurfGridConfig",
    "TurfType", "TurfCondition", "WeatherEffect",
    # Equipment
    "EquipmentPhysics", "PlayerEquipment", "EquipmentConfig",
    "CleatType", "GloveType", "HelmetType",
    # Weather
    "WeatherPhysics", "GameWeather", "WeatherConfig",
    "WindDirection", "PrecipitationType",
]
