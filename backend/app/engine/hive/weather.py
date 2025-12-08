#!/usr/bin/env python3
"""
Weather Integration Module
==========================
Enhanced weather effects on gameplay.

Phase 4: HIVE Environment Physics
- Wind effects on passing/kicking
- Temperature on stamina
- Precipitation on ball handling
- Combined environment calculations
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import math

from .turf_grid import WeatherEffect


# ============================================================================
# ENUMS
# ============================================================================

class WindDirection(str, Enum):
    """Wind direction relative to play direction."""
    HEADWIND = "HEADWIND"       # Against play direction
    TAILWIND = "TAILWIND"       # With play direction
    CROSSWIND_LEFT = "CROSSWIND_LEFT"
    CROSSWIND_RIGHT = "CROSSWIND_RIGHT"
    NONE = "NONE"


class PrecipitationType(str, Enum):
    """Type of precipitation."""
    NONE = "NONE"
    LIGHT_RAIN = "LIGHT_RAIN"
    HEAVY_RAIN = "HEAVY_RAIN"
    LIGHT_SNOW = "LIGHT_SNOW"
    HEAVY_SNOW = "HEAVY_SNOW"
    SLEET = "SLEET"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass(frozen=True)
class WeatherConfig:
    """Configuration for weather physics."""
    # Wind effects on passes (yards adjustment per 10mph)
    wind_pass_distance_factor: float = 1.5
    wind_pass_accuracy_penalty: float = 0.3

    # Wind effects on kicks
    wind_kick_distance_factor: float = 2.0
    wind_kick_accuracy_penalty: float = 0.5

    # Temperature effects
    cold_threshold_f: float = 32.0
    hot_threshold_f: float = 85.0
    stamina_drain_cold_bonus: float = 0.1
    stamina_drain_hot_penalty: float = 0.2
    cramp_risk_hot: float = 0.05

    # Precipitation effects
    ball_handling_rain_penalty: float = 0.15
    ball_handling_snow_penalty: float = 0.1
    visibility_rain_penalty: float = 0.05
    visibility_snow_penalty: float = 0.15


@dataclass
class GameWeather:
    """Complete weather state for a game."""
    temperature_f: float = 70.0
    wind_speed_mph: float = 0.0
    wind_direction: WindDirection = WindDirection.NONE
    precipitation: PrecipitationType = PrecipitationType.NONE
    humidity_pct: float = 50.0

    # Derived
    is_dome: bool = False

    @property
    def effect(self) -> WeatherEffect:
        """Convert to turf weather effect."""
        if self.is_dome:
            return WeatherEffect.DRY

        if self.precipitation == PrecipitationType.HEAVY_RAIN:
            return WeatherEffect.MUDDY
        elif self.precipitation in [PrecipitationType.LIGHT_RAIN, PrecipitationType.SLEET]:
            return WeatherEffect.WET
        elif self.precipitation in [PrecipitationType.LIGHT_SNOW, PrecipitationType.HEAVY_SNOW]:
            return WeatherEffect.SNOW_COVERED
        elif self.temperature_f < 32:
            return WeatherEffect.FROZEN

        return WeatherEffect.DRY


# ============================================================================
# WEATHER PHYSICS ENGINE
# ============================================================================

class WeatherPhysics:
    """
    Calculate weather effects on gameplay.

    Integrates:
    - Wind trajectory physics
    - Temperature stamina effects
    - Precipitation ball handling
    - Combined modifiers for equipment
    """

    def __init__(self, config: Optional[WeatherConfig] = None):
        self.config = config or WeatherConfig()

    def calculate_pass_wind_effect(
        self,
        weather: GameWeather,
        throw_direction: float,  # Degrees, 0 = upfield/north
        throw_distance: float,   # Yards intended
    ) -> Tuple[float, float]:
        """
        Calculate wind effect on pass.

        Returns:
            Tuple of (distance_adjustment, accuracy_penalty)
        """
        if weather.is_dome or weather.wind_speed_mph < 5:
            return 0.0, 0.0

        # Calculate wind component in throw direction
        wind_mph = weather.wind_speed_mph
        wind_factor = wind_mph / 10.0 * self.config.wind_pass_distance_factor

        # Direction effect
        if weather.wind_direction == WindDirection.HEADWIND:
            distance_adj = -wind_factor * (throw_distance / 40)  # Longer throws more affected
        elif weather.wind_direction == WindDirection.TAILWIND:
            distance_adj = wind_factor * (throw_distance / 40) * 0.7  # Less boost than penalty
        elif weather.wind_direction in [WindDirection.CROSSWIND_LEFT, WindDirection.CROSSWIND_RIGHT]:
            distance_adj = 0  # Crosswind affects accuracy, not distance
        else:
            distance_adj = 0

        # Accuracy penalty from any significant wind
        accuracy_penalty = wind_mph / 10.0 * self.config.wind_pass_accuracy_penalty

        # Crosswind is worst for accuracy
        if weather.wind_direction in [WindDirection.CROSSWIND_LEFT, WindDirection.CROSSWIND_RIGHT]:
            accuracy_penalty *= 1.5

        return distance_adj, accuracy_penalty

    def calculate_kick_wind_effect(
        self,
        weather: GameWeather,
        kick_distance: float,
        is_field_goal: bool = True,
    ) -> Tuple[float, float]:
        """
        Calculate wind effect on kicks.

        Returns:
            Tuple of (distance_adjustment, accuracy_penalty)
        """
        if weather.is_dome or weather.wind_speed_mph < 5:
            return 0.0, 0.0

        wind_mph = weather.wind_speed_mph
        wind_factor = wind_mph / 10.0 * self.config.wind_kick_distance_factor

        # Direction effect
        if weather.wind_direction == WindDirection.HEADWIND:
            distance_adj = -wind_factor * (kick_distance / 50)
        elif weather.wind_direction == WindDirection.TAILWIND:
            distance_adj = wind_factor * (kick_distance / 50) * 0.8
        else:
            distance_adj = 0

        # Accuracy penalty
        accuracy_penalty = wind_mph / 10.0 * self.config.wind_kick_accuracy_penalty

        if weather.wind_direction in [WindDirection.CROSSWIND_LEFT, WindDirection.CROSSWIND_RIGHT]:
            accuracy_penalty *= 2.0  # Crosswind very bad for kicking

        return distance_adj, accuracy_penalty

    def calculate_stamina_modifier(
        self,
        weather: GameWeather,
        is_outdoor_stadium: bool = True,
    ) -> float:
        """
        Calculate stamina drain modifier.

        Returns modifier to stamina drain (>1 = faster drain).
        """
        if not is_outdoor_stadium or weather.is_dome:
            return 1.0

        temp = weather.temperature_f

        if temp > self.config.hot_threshold_f:
            # Hot weather increases drain
            excess = (temp - self.config.hot_threshold_f) / 20.0
            return 1.0 + self.config.stamina_drain_hot_penalty * excess
        elif temp < self.config.cold_threshold_f:
            # Cold weather can actually help (less overheating)
            return 1.0 - self.config.stamina_drain_cold_bonus

        return 1.0

    def calculate_cramp_risk(
        self,
        weather: GameWeather,
        player_fatigue: float,
        player_hydration: float = 100.0,
    ) -> float:
        """
        Calculate risk of cramping.

        Returns probability 0-1.
        """
        if weather.temperature_f < self.config.hot_threshold_f:
            return 0.0

        # Base risk from heat
        heat_excess = (weather.temperature_f - self.config.hot_threshold_f) / 20.0
        base_risk = self.config.cramp_risk_hot * heat_excess

        # Fatigue increases risk
        fatigue_factor = player_fatigue / 100.0

        # Low hydration increases risk
        hydration_factor = (100 - player_hydration) / 100.0

        # Humidity makes it worse
        humidity_factor = 1.0 + (weather.humidity_pct / 100.0) * 0.5

        return min(0.5, base_risk * (1 + fatigue_factor + hydration_factor) * humidity_factor)

    def calculate_ball_handling_modifier(
        self,
        weather: GameWeather,
    ) -> float:
        """
        Calculate ball handling modifier from precipitation.

        Returns modifier (1.0 = normal, lower = worse).
        """
        if weather.is_dome:
            return 1.0

        modifiers = {
            PrecipitationType.NONE: 1.0,
            PrecipitationType.LIGHT_RAIN: 1.0 - self.config.ball_handling_rain_penalty * 0.5,
            PrecipitationType.HEAVY_RAIN: 1.0 - self.config.ball_handling_rain_penalty,
            PrecipitationType.LIGHT_SNOW: 1.0 - self.config.ball_handling_snow_penalty * 0.5,
            PrecipitationType.HEAVY_SNOW: 1.0 - self.config.ball_handling_snow_penalty,
            PrecipitationType.SLEET: 1.0 - self.config.ball_handling_rain_penalty * 0.8,
        }

        return modifiers.get(weather.precipitation, 1.0)

    def calculate_visibility_modifier(
        self,
        weather: GameWeather,
    ) -> float:
        """
        Calculate visibility modifier.

        Affects QB reads, WR tracking, punt returns.
        Returns modifier (1.0 = normal, lower = worse).
        """
        if weather.is_dome:
            return 1.0

        base = 1.0

        # Precipitation effects
        if weather.precipitation == PrecipitationType.HEAVY_RAIN:
            base -= self.config.visibility_rain_penalty
        elif weather.precipitation == PrecipitationType.HEAVY_SNOW:
            base -= self.config.visibility_snow_penalty
        elif weather.precipitation == PrecipitationType.LIGHT_SNOW:
            base -= self.config.visibility_snow_penalty * 0.5
        elif weather.precipitation == PrecipitationType.LIGHT_RAIN:
            base -= self.config.visibility_rain_penalty * 0.3

        # Strong wind can affect visibility (debris, snow blown)
        if weather.wind_speed_mph > 20:
            base -= 0.05

        return max(0.7, base)

    def get_combined_modifiers(
        self,
        weather: GameWeather,
    ) -> Dict[str, float]:
        """
        Get all weather modifiers in one call.

        Convenience method for game engine.
        """
        return {
            "stamina_drain": self.calculate_stamina_modifier(weather),
            "ball_handling": self.calculate_ball_handling_modifier(weather),
            "visibility": self.calculate_visibility_modifier(weather),
            "pass_accuracy_penalty": self.calculate_pass_wind_effect(weather, 0, 30)[1],
            "kick_accuracy_penalty": self.calculate_kick_wind_effect(weather, 40)[1],
        }

    def to_dict(self, weather: GameWeather) -> Dict[str, Any]:
        """Serialize weather state with modifiers."""
        return {
            "temperature_f": weather.temperature_f,
            "wind_speed_mph": weather.wind_speed_mph,
            "wind_direction": weather.wind_direction.value,
            "precipitation": weather.precipitation.value,
            "humidity_pct": weather.humidity_pct,
            "is_dome": weather.is_dome,
            "modifiers": self.get_combined_modifiers(weather),
        }
