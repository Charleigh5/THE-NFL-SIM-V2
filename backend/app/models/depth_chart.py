from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class DepthChart(Base):
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True)
    player_id = Column(Integer, ForeignKey("player.id"), index=True)
    position = Column(String, index=True) # e.g. "QB", "WR", "LWR", "RWR", "SLOT"
    depth_order = Column(Integer, default=1) # 1 = Starter, 2 = Backup, etc.

    # Relationships
    team = relationship("Team", back_populates="depth_chart")
    player = relationship("Player")
