from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class DraftPick(Base):
    __tablename__ = "draft_pick"
    
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)
    
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False) # Current owner of pick
    original_team_id = Column(Integer, ForeignKey("team.id"), nullable=False) # Original owner
    
    round = Column(Integer, nullable=False)
    pick_number = Column(Integer, nullable=False) # Overall pick number
    
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True) # The player selected
    
    # Relationships
    season = relationship("Season")
    team = relationship("Team", foreign_keys=[team_id])
    original_team = relationship("Team", foreign_keys=[original_team_id])
    player = relationship("Player")
