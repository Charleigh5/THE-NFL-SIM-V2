from app.kernels.core.ecs_manager import Component
from typing import Tuple
from pydantic import Field
import math
import random

class WeatherSys(Component):
    # Directive 5: Dynamic Weather
    temperature_f: float = 72.0
    wind_speed_mph: float = 0.0
    wind_direction_deg: float = 0.0 # 0 = North
    precipitation_intensity: float = 0.0 # 0.0 - 1.0 (Rain/Snow)
    is_snowing: bool = False
    
    # Directive 14: Altitude
    altitude_ft: float = 0.0 # Sea level default

    def get_ballistic_modifiers(self) -> Tuple[float, float]:
        """
        Directive 6: Ballistics Trajectory.
        Returns (DistanceMultiplier, DriftMultiplier).
        """
        # Altitude: +1% distance per 1000ft
        altitude_boost = 1.0 + (self.altitude_ft / 1000.0) * 0.01
        
        # Wind: Headwind/Tailwind calculation would go here, simplified for now
        return (altitude_boost, self.wind_speed_mph * 0.5)

    def get_visibility_penalty(self) -> float:
        """
        Directive 12: Snowfall Obscuration.
        """
        if self.is_snowing:
            return self.precipitation_intensity * 0.4 # Max 40% vision loss
        return 0.0

    def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
        """
        Directive 5: Sun Glare.
        Simplified: Returns glare intensity 0.0 - 1.0.
        """
    # Directive 5: Dynamic Weather Generation
    forecast: str = "Clear" # "Rain", "Snow", "Heavy Snow"
    fog_density: float = 0.0 # 0.0 - 1.0

    def generate_forecast(self, month: int, location_climate: str):
        """
        Generates a forecast based on season and location.
        """
        if location_climate == "Cold" and month > 10:
            self.forecast = "Snow" if random.random() > 0.5 else "Clear"
            self.temperature_f = 25.0
            self.is_snowing = True
        elif location_climate == "Warm":
            self.forecast = "Rain" if random.random() > 0.7 else "Clear"
            self.temperature_f = 75.0

    def get_ballistic_modifiers(self) -> Tuple[float, float, float]:
        """
        Directive 6: Ballistics Trajectory.
        Returns (DistanceMultiplier, DriftMultiplier, WeightMultiplier).
        """
        # Altitude: +1% distance per 1000ft
        altitude_boost = 1.0 + (self.altitude_ft / 1000.0) * 0.01
        
        # Snow Weight: Heavy snow weighs down the ball
        weight_multiplier = 1.0
        if self.is_snowing and self.precipitation_intensity > 0.5:
            weight_multiplier = 0.9 # 10% range reduction
        
        return (altitude_boost, self.wind_speed_mph * 0.5, weight_multiplier)

    def get_visibility_penalty(self) -> float:
        """
        Directive 12: Snowfall & Fog Obscuration.
        """
        penalty = 0.0
        if self.is_snowing:
            penalty += self.precipitation_intensity * 0.4
        
        if self.fog_density > 0.0:
            penalty += self.fog_density * 0.5 # Fog is dense
            
        return min(0.9, penalty)

    def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
        """
        Directive 5: Sun Glare.
        Simplified: Returns glare intensity 0.0 - 1.0.
        """
        if time_of_day == "Late Afternoon":
            return 0.8
        return 0.0

    def get_weather_report(self) -> str:
        """
        Directive: Weekly Weather Forecast Top Story.
        """
        if self.forecast == "Clear":
            return f"Clear skies expected, perfect for passing."
        elif self.forecast == "Snow":
            return f"Snow forecast! Expect reduced visibility and slippery conditions."
        return f"Weather Alert: {self.forecast} conditions may impact game strategy."
