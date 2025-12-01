from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class Team(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)
    abbreviation = Column(String, unique=True, index=True)

    # Relationships
    players = relationship("Player", back_populates="team")
    coaches = relationship("Coach", back_populates="team")
    gm = relationship("GM", back_populates="team", uselist=False)
    stadium = relationship("Stadium", back_populates="team", uselist=False)
    depth_chart = relationship("DepthChart", back_populates="team")

    # Division/Conference
    conference = Column(String, index=True) # AFC/NFC
    division = Column(String, index=True) # North/South/East/West

    # Stats/Record
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ties = Column(Integer, default=0)

    # RPG/Franchise
    prestige = Column(Integer, default=50)
    salary_cap_space = Column(Float, default=0.0)
    fan_support = Column(Integer, default=50)

    # Nano Banana
    logo_url = Column(String, nullable=True)
    primary_color = Column(String, default="#000000")
    secondary_color = Column(String, default="#FFFFFF")

    # History
    established_year = Column(Integer, nullable=True)

    # Foreign Keys
    stadium_id = Column(Integer, ForeignKey("stadium.id"), nullable=True)

    # History
    season_history = relationship("TeamSeasonStats", back_populates="team")

