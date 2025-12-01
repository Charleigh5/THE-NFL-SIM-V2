from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class GM(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    team = relationship("Team", back_populates="gm")
    
    # RPG Attributes
    scouting = Column(Integer, default=50)
    negotiation = Column(Integer, default=50)
    cap_management = Column(Integer, default=50)
    
    # Reputation
    owner_trust = Column(Integer, default=50)
    league_reputation = Column(Integer, default=50)
    
    # Skill Tree
    skills = Column(JSON, default=dict)
    
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # Philosophy & Strategy
    philosophy = Column(String, default="BALANCED") # WIN_NOW, REBUILD, etc.
    aggression = Column(Integer, default=50) # 0-100, trade frequency
    patience = Column(Integer, default=50) # 0-100, tolerance for losing
    
    # Traits
    traits = Column(JSON, default=list) # e.g. ["ScoutingGuru", "CapWizard"]

