from __future__ import annotations

import datetime
import random
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import ErrorCategory, get_logger, log_error
from app.models.stadium import Stadium
from app.models.weather import StadiumClimate

logger = get_logger(__name__)

class WeatherService:
    """
    Service for determining weather conditions and their gameplay impact.
    Supports both Simulation Mode (based on historical averages) and Real API Mode.
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
        Legacy synchronous method. Returns neutral modifiers.
        Used if MatchContext is initialized without DB access or async capabilities.
        """
        logger.warning("Using legacy synchronous weather modifiers (Neutral weather).")
        return {
            "passing": 0.0,
            "rushing": 0.0,
            "fumble": 0.0,
            "fg_accuracy": 0.0
        }

    @staticmethod
    async def calculate_simulation_weather(
        db: AsyncSession,
        stadium_id: int,
        game_date: datetime.datetime | str
    ) -> dict[str, Any]:
        """
        Calculates weather conditions for a game based on simulation logic.

        Returns a dictionary containing:
        - modifiers: dict[str, float]
        - conditions: dict[str, Any] (temp, wind, precip, etc.)
        """

        if isinstance(game_date, str):
            try:
                game_date = datetime.datetime.fromisoformat(game_date)
            except ValueError:
                game_date = datetime.datetime.now()

        month = str(game_date.month)

        try:
            # 1. Fetch Stadium Info
            stmt = select(Stadium).where(Stadium.id == stadium_id)
            result = await db.execute(stmt)
            stadium = result.scalar_one_or_none()

            if not stadium:
                logger.warning(f"Stadium {stadium_id} not found, using default weather.")
                return WeatherService._default_weather()

            # 2. Check for Dome
            if stadium.dome:
                return WeatherService._dome_weather()

            # 3. Fetch Climate Data
            stmt_climate = select(StadiumClimate).where(StadiumClimate.stadium_id == stadium_id)
            result_climate = await db.execute(stmt_climate)
            climate = result_climate.scalar_one_or_none()

            if not climate:
                # Seed default climate if missing
                climate = await WeatherService.seed_stadium_climate(db, stadium_id)

            # 4. Calculate Weather based on Monthly Averages + Random Variance

            # Temperature
            avg_temp = climate.avg_temp_by_month.get(month, 70.0)
            # Add variance: Normal distribution with std_dev=10
            temp = random.gauss(avg_temp, 10.0)

            # Wind
            avg_wind = climate.wind_avg_by_month.get(month, 10.0)
            # Log-normal distribution to avoid negative wind, biased towards avg
            # Simplified: avg + random(-5, +15) clipped at 0
            wind_speed = max(0.0, avg_wind + random.uniform(-5, 15))

            # Precipitation
            precip_chance = climate.precip_chance_by_month.get(month, 0.1)
            is_precip = random.random() < precip_chance

            precip_type = "None"
            condition = "Clear"

            if is_precip:
                if temp < 32:
                    precip_type = "Snow"
                    condition = "Snow"
                else:
                    precip_type = "Rain"
                    condition = "Rain"
            elif climate.stadium.city == "London" and random.random() < 0.4: # Easter egg / logic example
                condition = "Fog"
            elif random.random() < 0.2:
                condition = "Cloudy"

            # 5. Calculate Modifiers
            modifiers = WeatherService._calculate_modifiers(temp, wind_speed, condition)

            weather_data = {
                "modifiers": modifiers,
                "conditions": {
                    "temperature": round(temp, 1),
                    "wind_speed": round(wind_speed, 1),
                    "condition": condition,
                    "precipitation_type": precip_type,
                    "is_dome": False
                }
            }

            logger.info("weather_calculated", stadium=stadium.name, data=weather_data)
            return weather_data

        except Exception as e:
            log_error(logger, ErrorCategory.WEATHER_ERROR, "Failed to calculate weather", exc_info=e)
            return WeatherService._default_weather()

    @staticmethod
    def _calculate_modifiers(temp: float, wind_speed: float, condition: str) -> dict[str, float]:
        modifiers = {
            "passing": 0.0,
            "rushing": 0.0,
            "fumble": 0.0,
            "fg_accuracy": 0.0
        }

        if condition == "Rain":
            modifiers["passing"] += WeatherService.MODIFIER_RAIN_PASSING
            modifiers["fumble"] += WeatherService.MODIFIER_RAIN_FUMBLE
        elif condition == "Snow":
            modifiers["passing"] += WeatherService.MODIFIER_SNOW_PASSING
            modifiers["rushing"] += WeatherService.MODIFIER_SNOW_RUSHING

        if wind_speed > 15:
            # Linear penalty: -0.01 per mph over 15?
            # Or simplified tiered
            wind_penalty = (wind_speed - 15) * 0.01
            modifiers["passing"] -= min(0.3, wind_penalty + 0.1) # Base penalty
            modifiers["fg_accuracy"] -= min(0.4, wind_penalty + 0.1)

        if temp < 20:
            modifiers["fumble"] += WeatherService.MODIFIER_COLD_FUMBLE
            modifiers["fg_accuracy"] -= 0.1 # Hard ball

        if temp > 95:
             modifiers["rushing"] -= 0.05 # Fatigue impact implied

        return modifiers

    @staticmethod
    def _default_weather() -> dict[str, Any]:
        return {
            "modifiers": {"passing": 0.0, "rushing": 0.0, "fumble": 0.0, "fg_accuracy": 0.0},
            "conditions": {"temperature": 70, "wind_speed": 0, "condition": "Sunny", "is_dome": False}
        }

    @staticmethod
    def _dome_weather() -> dict[str, Any]:
        return {
            "modifiers": {"passing": 0.0, "rushing": 0.0, "fumble": 0.0, "fg_accuracy": 0.0},
            "conditions": {"temperature": 72, "wind_speed": 0, "condition": "Dome", "is_dome": True}
        }

    @staticmethod
    async def seed_stadium_climate(db: AsyncSession, stadium_id: int) -> StadiumClimate:
        """
        Seeds default climate data for a stadium based on simple ID rules or generics.
        In a real app, this would use real geo-data.
        """
        # Generic "Cold North" vs "Warm South" logic based on ID even/odd for now,
        # or just a standard template.

        # Default Template (Midwest-ish)
        avg_temp = {
            "1": 30.0, "2": 32.0, "3": 45.0, "4": 55.0, "5": 65.0, "6": 75.0,
            "7": 80.0, "8": 78.0, "9": 70.0, "10": 58.0, "11": 45.0, "12": 35.0
        }
        precip = dict.fromkeys(avg_temp, 0.15)
        wind = dict.fromkeys(avg_temp, 12.0)

        # Override for specific known IDs if we knew them, or random variance
        # Adding some randomness to the seed so every stadium isn't identical
        offset = random.uniform(-10, 20)
        avg_temp = {k: v + offset for k, v in avg_temp.items()}

        climate = StadiumClimate(
            stadium_id=stadium_id,
            avg_temp_by_month=avg_temp,
            precip_chance_by_month=precip,
            wind_avg_by_month=wind
        )

        db.add(climate)
        await db.commit()
        await db.refresh(climate)
        return climate

    # -------------------------------------------------------------------------
    # OPTION B: Real Weather API Integration (Notes / Future Toggle)
    # -------------------------------------------------------------------------
    # import httpx
    #
    # @staticmethod
    # async def fetch_live_weather(lat: float, lon: float, api_key: str) -> dict[str, Any]:
    #     """
    #     Fetches real-time weather from OpenWeatherMap (or similar).
    #     To use:
    #     1. Add OPENWEATHER_API_KEY to .env
    #     2. Call this method instead of calculate_simulation_weather if use_live_weather is True.
    #     """
    #     url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    #
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(url)
    #         if response.status_code == 200:
    #             data = response.json()
    #
    #             temp = data["main"]["temp"]
    #             wind_speed = data["wind"]["speed"]
    #             weather_main = data["weather"][0]["main"] # Rain, Snow, Clear
    #
    #             # Map to our conditions
    #             condition = weather_main
    #
    #             modifiers = WeatherService._calculate_modifiers(temp, wind_speed, condition)
    #
    #             return {
    #                 "modifiers": modifiers,
    #                 "conditions": {
    #                     "temperature": temp,
    #                     "wind_speed": wind_speed,
    #                     "condition": condition,
    #                     "source": "LiveAPI"
    #                 }
    #             }
    #         else:
    #             logger.error(f"Weather API Error: {response.status_code}")
    #             return WeatherService._default_weather()
