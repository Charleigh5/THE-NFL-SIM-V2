from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class HallOfFame(Base):
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"), unique=True, index=True)
    year_inducted = Column(Integer)
    
    # Snapshot of career stats at time of induction
    career_stats_snapshot = Column(JSON, default=dict)
    
    player = relationship("Player")
