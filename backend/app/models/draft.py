from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import Base

class DraftPick(Base):
    __tablename__ = "draft_pick"
    __table_args__ = (
        Index("ix_draft_pick_season_round", "season_id", "round"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False, index=True)
    
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False, index=True) # Current owner of pick
    original_team_id = Column(Integer, ForeignKey("team.id"), nullable=False) # Original owner
    
    round = Column(Integer, nullable=False, index=True)
    pick_number = Column(Integer, nullable=False, index=True) # Overall pick number
    
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True) # The player selected
    
    # Relationships
    season = relationship("Season")
    team = relationship("Team", foreign_keys=[team_id])
    original_team = relationship("Team", foreign_keys=[original_team_id])
    player = relationship("Player")
