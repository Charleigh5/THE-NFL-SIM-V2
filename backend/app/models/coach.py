from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class Coach(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String) # Head Coach, OC, DC, ST
    
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    team = relationship("Team", back_populates="coaches")
    
    # RPG Attributes
    offense_rating = Column(Integer, default=50)
    defense_rating = Column(Integer, default=50)
    development_rating = Column(Integer, default=50)
    
    # Skill Tree
    # e.g. {"WestCoastOffense": 5, "ZoneBlitz": 3}
    skills = Column(JSON, default=dict)
    
    # Traits
    traits = Column(JSON, default=list)
    
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # Strategy
    playbook_offense = Column(String, nullable=True) # e.g. "West Coast", "Spread"
    playbook_defense = Column(String, nullable=True) # e.g. "4-3", "3-4"
    philosophy = Column(JSON, default=dict) # e.g. {"run_heavy": 70, "blitz_frequency": 40}
