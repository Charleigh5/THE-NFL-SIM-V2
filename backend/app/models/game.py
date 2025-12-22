from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime
from enum import Enum

class GameType(str, Enum):
    """Type of game for special scheduling and presentation."""
    REGULAR = "REGULAR"
    THANKSGIVING = "THANKSGIVING"
    PRIMETIME = "PRIMETIME"
    PLAYOFF = "PLAYOFF"
    SUPER_BOWL = "SUPER_BOWL"

class Game(Base):
    __tablename__ = "game"  # type: ignore[assignment]
    __table_args__ = (
        Index("ix_game_season_week", "season_id", "week"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # Season Link
    season_id = Column(Integer, ForeignKey("season.id"), nullable=True, index=True)
    season_obj = relationship("Season", backref="games")

    # Schedule Info (keeping legacy 'season' field for year)
    season = Column(Integer, index=True)  # Year (e.g., 2024)
    week = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    is_playoff = Column(Boolean, default=False)
    is_preseason = Column(Boolean, default=False)  # Flag for preseason games
    game_type = Column(SQLEnum(GameType), default=GameType.REGULAR, nullable=False)

    # Teams
    home_team_id = Column(Integer, ForeignKey("team.id"))
    away_team_id = Column(Integer, ForeignKey("team.id"))

    home_team = relationship("Team", foreign_keys="[Game.home_team_id]")
    away_team = relationship("Team", foreign_keys="[Game.away_team_id]")

    # Result
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    is_played = Column(Boolean, default=False)

    # Live Game State (for resumability)
    current_quarter = Column(Integer, default=1)
    time_left = Column(String, default="15:00")

    # Detailed Game Data (Play-by-play summary or reference)
    game_data = Column(JSON, nullable=True)

    # Weather
    weather_temperature = Column(Integer)
    weather_condition = Column(String)  # Sunny, Rain, Snow
    wind_speed = Column(Integer)

    weather_info = relationship("GameWeather", uselist=False, back_populates="game")

    # Player game starts tracking for chemistry calculations
    player_starts = relationship("PlayerGameStarts", back_populates="game")
