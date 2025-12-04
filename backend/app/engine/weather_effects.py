from app.models.weather import GameWeather, PrecipitationType, FieldCondition
from typing import Tuple

class WeatherEffects:
    def __init__(self, weather: GameWeather):
        self.weather = weather

    def get_passing_modifiers(self) -> Tuple[float, float]:
        """
        Returns (accuracy_multiplier, distance_multiplier)
        """
        accuracy = 1.0
        distance = 1.0

        # Wind
        # Assuming wind_speed is in mph
        if self.weather.wind_speed and self.weather.wind_speed > 10:
            accuracy -= (self.weather.wind_speed - 10) * 0.01 # -1% per mph over 10
            distance -= (self.weather.wind_speed - 10) * 0.005 # -0.5% per mph over 10

        # Precipitation
        if self.weather.precipitation_type == PrecipitationType.RAIN.value:
            accuracy *= 0.9
        elif self.weather.precipitation_type == PrecipitationType.SNOW.value:
            accuracy *= 0.85
            distance *= 0.95

        # Temperature (Cold hands)
        if self.weather.temperature and self.weather.temperature < 32:
            accuracy *= 0.95

        return max(0.5, accuracy), max(0.5, distance)

    def get_kicking_modifiers(self) -> Tuple[float, float]:
        """
        Returns (accuracy_multiplier, distance_multiplier)
        """
        accuracy = 1.0
        distance = 1.0

        # Wind affects kicking more
        if self.weather.wind_speed and self.weather.wind_speed > 5:
            accuracy -= (self.weather.wind_speed - 5) * 0.02
            distance -= (self.weather.wind_speed - 5) * 0.01

        # Temperature (Dense air in cold)
        if self.weather.temperature and self.weather.temperature < 40:
            distance -= (40 - self.weather.temperature) * 0.005 # -0.5% per degree under 40

        return max(0.4, accuracy), max(0.6, distance)

    def get_fumble_probability_modifier(self) -> float:
        """
        Returns multiplier for fumble probability (1.0 = normal)
        """
        multiplier = 1.0

        if self.weather.field_condition == FieldCondition.WET.value:
            multiplier *= 1.2
        elif self.weather.field_condition == FieldCondition.MUDDY.value:
            multiplier *= 1.3
        elif self.weather.field_condition == FieldCondition.SNOWY.value:
            multiplier *= 1.15

        if self.weather.temperature and self.weather.temperature < 20:
            multiplier *= 1.1 # Hard ball, cold hands

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
