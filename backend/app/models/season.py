import enum

from sqlalchemy import Boolean, Column, Integer
from sqlalchemy import Enum as SQLEnum

from app.models.base import Base


class SeasonStatus(str, enum.Enum):
    """Enum for season status."""

    PRE_SEASON = "PRE_SEASON"
    REGULAR_SEASON = "REGULAR_SEASON"
    POST_SEASON = "POST_SEASON"
    OFF_SEASON = "OFF_SEASON"


class Season(Base):
    """
    Represents an NFL season.

    A season contains multiple weeks of games, tracks the current week,
    and manages the overall state of the season (preseason, regular, playoffs, offseason).
    """

    __tablename__ = "season"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True, index=True, nullable=False)
    current_week = Column(Integer, default=1)
    is_active = Column(Boolean, default=False, index=True)
    status = Column(SQLEnum(SeasonStatus), default=SeasonStatus.REGULAR_SEASON, nullable=False)

    # Configuration
    total_weeks = Column(Integer, default=18)  # NFL has 18 weeks in regular season
    playoff_weeks = Column(Integer, default=4)  # Wild Card, Divisional, Conference, Super Bowl
    preseason_weeks = Column(Integer, default=3)  # NFL preseason is 3 weeks

    def __repr__(self):
        return f"<Season(year={self.year}, week={self.current_week}, status={self.status})>"
