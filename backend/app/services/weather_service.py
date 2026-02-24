from __future__ import annotations

from app.core.logging_config import get_logger, ErrorCategory, log_error

logger = get_logger(__name__)

class WeatherService:
    """
    Service for determining weather conditions and their gameplay impact.
    """

    # Modifier constants
    MODIFIER_RAIN_PASSING = -0.15
    MODIFIER_RAIN_FUMBLE = 0.10
    MODIFIER_SNOW_PASSING = -0.25
    MODIFIER_SNOW_RUSHING = 0.05 # easier to run in snow? or just relative to pass
    MODIFIER_WIND_PASSING = -0.20 # > 15mph
    MODIFIER_WIND_FG = -0.10
    MODIFIER_COLD_FUMBLE = 0.15 # < 20F

    @staticmethod
    def get_weather_modifiers(stadium_id: int, game_datetime: str) -> dict[str, float]:
        """
        Get gameplay modifiers based on weather conditions.

        Args:
            stadium_id: ID of the stadium (to check for dome, location)
            game_datetime: ISO string of game time

        Returns:
            Dictionary of modifiers, e.g. {"passing": -0.15, "fumble": 0.10}
        """
        modifiers = {
            "passing": 0.0,
            "rushing": 0.0,
            "fumble": 0.0,
            "fg_accuracy": 0.0
        }

        try:
            # TODO: Integrate with real weather API or Simulation Weather Engine
            # For now, simplistic random weather based on "month" if we parsed date,
            # but here we'll just mock it or assume inputs provided context.

            # Mock Condition
            # 10% chance of Rain, 5% Snow, 10% High Wind in "Simulation"

            # Determine conditions (Mock)
            condition = "CLEAR"
            temp = 70
            wind_speed = 5

            # Logic to determining condition would go here (or be passed in)
            # For this service, we assume we might determine it here.

            # Calculate impact
            if condition == "RAIN":
                modifiers["passing"] += WeatherService.MODIFIER_RAIN_PASSING
                modifiers["fumble"] += WeatherService.MODIFIER_RAIN_FUMBLE

            elif condition == "SNOW":
                modifiers["passing"] += WeatherService.MODIFIER_SNOW_PASSING
                modifiers["rushing"] += WeatherService.MODIFIER_SNOW_RUSHING

            if wind_speed > 15:
                modifiers["passing"] += WeatherService.MODIFIER_WIND_PASSING
                modifiers["fg_accuracy"] += WeatherService.MODIFIER_WIND_FG

            if temp < 20:
                modifiers["fumble"] += WeatherService.MODIFIER_COLD_FUMBLE

            logger.info("weather_modifiers_calculated", stadium_id=stadium_id, modifiers=modifiers)
            return modifiers

        except Exception as e:
            log_error(logger, ErrorCategory.WEATHER_ERROR, "Failed to calculate weather modifiers", exc_info=e)
            return modifiers
