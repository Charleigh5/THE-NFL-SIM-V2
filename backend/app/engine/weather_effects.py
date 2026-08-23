from app.models.weather import GameWeather, PrecipitationType, FieldCondition
from typing import Tuple

class WeatherEffects:
    """
    Calculate weather impact on game outcomes.

    NFL Calibration Data (2020-2024):
    - Wind >10 mph: -5% passing, drops further at 15+ and 20+ mph
    - Rain: -12% passing yards, +20% fumble rate
    - Snow: -15% passing yards, +15% fumble rate
    - Cold (<32°F): -5% passing accuracy
    - FG accuracy: 89% baseline, drops to ~77% at 20+ mph wind
    """

    def __init__(self, weather: GameWeather):
        self.weather = weather

    def get_passing_modifiers(self) -> Tuple[float, float]:
        """
        Returns (accuracy_multiplier, distance_multiplier)

        NFL Data:
        - 10-15 mph wind: -5% accuracy
        - 15-20 mph wind: -12% accuracy
        - Rain: -12% passing yards
        - Snow: -15% passing yards
        """
        accuracy = 1.0
        distance = 1.0

        # Wind (NFL: noticeable effect above 10 mph)
        if self.weather.wind_speed and self.weather.wind_speed > 10:
            wind_over = self.weather.wind_speed - 10
            accuracy -= wind_over * 0.010   # -1.0% per mph over 10
            distance -= wind_over * 0.005   # -0.5% per mph over 10

        # Precipitation (NFL: ~10% reduction in rain, ~15% in snow)
        if self.weather.precipitation_type == PrecipitationType.RAIN.value:
            accuracy *= 0.90  # -10%
        elif self.weather.precipitation_type == PrecipitationType.SNOW.value:
            accuracy *= 0.85  # -15%
            distance *= 0.95

        # Temperature (NFL: Cold hands affect accuracy ~5%)
        if self.weather.temperature and self.weather.temperature < 32:
            accuracy *= 0.95  # -5% for freezing

        return max(0.5, accuracy), max(0.5, distance)

    def get_kicking_modifiers(self) -> Tuple[float, float]:
        """
        Returns (accuracy_multiplier, distance_multiplier)

        NFL Data:
        - 10-15 mph: ~83% FG (vs 89% baseline)
        - 15-20 mph: ~80% FG
        - 20+ mph: ~77% FG
        """
        accuracy = 1.0
        distance = 1.0

        # Wind affects kicking more (NFL: significant above 5 mph)
        if self.weather.wind_speed and self.weather.wind_speed > 5:
            wind_over = self.weather.wind_speed - 5
            accuracy -= wind_over * 0.015   # -1.5% per mph over 5
            distance -= wind_over * 0.008   # -0.8% per mph over 5

        # Temperature (Dense cold air reduces distance)
        if self.weather.temperature and self.weather.temperature < 40:
            distance -= (40 - self.weather.temperature) * 0.004  # -0.4% per degree under 40

        return max(0.5, accuracy), max(0.6, distance)

    def get_fumble_probability_modifier(self) -> float:
        """
        Returns multiplier for fumble probability (1.0 = normal)

        NFL Data:
        - Heavy rain: +20% fumble rate
        - Snow: +15% fumble rate
        - Muddy: +30% fumble rate
        """
        multiplier = 1.0

        if self.weather.field_condition == FieldCondition.WET.value:
            multiplier *= 1.20  # +20%
        elif self.weather.field_condition == FieldCondition.MUDDY.value:
            multiplier *= 1.30  # +30%
        elif self.weather.field_condition == FieldCondition.SNOWY.value:
            multiplier *= 1.15  # +15%

        if self.weather.temperature and self.weather.temperature < 20:
            multiplier *= 1.10  # Hard ball, cold hands

        return multiplier

    def get_fatigue_multiplier(self) -> float:
        """
        Returns multiplier for fatigue accumulation (1.0 = normal)
        """
        multiplier = 1.0

        # Heat
        if self.weather.temperature and self.weather.temperature > 85:
            multiplier += (self.weather.temperature - 85) * 0.02

        # Humidity
        if self.weather.humidity and self.weather.humidity > 0.7:
            multiplier += (self.weather.humidity - 0.7) * 0.5

        # Heavy field
        if self.weather.field_condition in [FieldCondition.MUDDY.value, FieldCondition.SNOWY.value]:
            multiplier *= 1.2

        return multiplier
