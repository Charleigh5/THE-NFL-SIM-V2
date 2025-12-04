from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class PrecipitationType(enum.Enum):
    NONE = "None"
    RAIN = "Rain"
    SNOW = "Snow"
    SLEET = "Sleet"

class FieldCondition(enum.Enum):
    DRY = "Dry"
    WET = "Wet"
    SNOWY = "Snowy"
    MUDDY = "Muddy"
    FROZEN = "Frozen"

class GameWeather(Base):
    __tablename__ = "game_weather"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game.id"), unique=True, nullable=False)

    temperature = Column(Float) # Fahrenheit
    wind_speed = Column(Float) # MPH
    wind_direction = Column(String) # e.g., "NW", "S"

    precipitation_type = Column(String, default="None") # None, Rain, Snow, Sleet
    precipitation_intensity = Column(Float, default=0.0) # 0.0 to 1.0

    cloud_cover = Column(Float, default=0.0) # 0.0 to 1.0
    humidity = Column(Float, default=0.0) # 0.0 to 1.0
    pressure = Column(Float, default=29.92) # inHg

    field_condition = Column(String, default="Dry") # Dry, Wet, Snowy, Muddy, Frozen

    # Relationship
    game = relationship("Game", back_populates="weather_info")

class StadiumClimate(Base):
    __tablename__ = "stadium_climate"

    id = Column(Integer, primary_key=True, index=True)
    stadium_id = Column(Integer, ForeignKey("stadium.id"), unique=True)

    # Monthly averages: {"9": 75.0, ...}
    avg_temp_by_month = Column(JSON, default={})
    precip_chance_by_month = Column(JSON, default={})
    wind_avg_by_month = Column(JSON, default={})

    stadium = relationship("Stadium", back_populates="climate")
