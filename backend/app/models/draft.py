from sqlalchemy import JSON, Boolean, Column, ForeignKey, Index, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base


class DraftPick(Base):
    __tablename__ = "draft_pick"
    __table_args__ = (Index("ix_draft_pick_season_round", "season_id", "round"),)

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=True, index=True)
    year = Column(Integer, nullable=False, default=2025, index=True)

    team_id = Column(
        Integer, ForeignKey("team.id"), nullable=False, index=True
    )  # Current owner of pick
    original_team_id = Column(Integer, ForeignKey("team.id"), nullable=False)  # Original owner

    round = Column(Integer, nullable=False, index=True)
    pick_number = Column(Integer, nullable=True, index=True)  # Overall pick number
    is_compensatory = Column(Boolean, default=False, nullable=False)
    conditions = Column(JSON, nullable=True)

    player_id = Column(Integer, ForeignKey("player.id"), nullable=True)  # The player selected

    # Relationships
    season = relationship("Season")
    team = relationship("Team", foreign_keys=[team_id])
    original_team = relationship("Team", foreign_keys=[original_team_id])
    player = relationship("Player")
