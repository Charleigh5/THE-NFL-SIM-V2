from enum import Enum

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import Base


class CoachTier(str, Enum):
    """Coach tier based on combined ratings and experience."""

    LEGEND = "LEGEND"  # 270+ combined, 1.50x development
    ELITE = "ELITE"  # 230-269, 1.30x development
    VETERAN = "VETERAN"  # 180-229, 1.10x development
    DEVELOPING = "DEVELOPING"  # 140-179, 1.00x development
    ROOKIE = "ROOKIE"  # <140, 0.90x development


class Coach(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)  # Head Coach, OC, DC, ST

    # Tier system
    tier = Column(SQLEnum(CoachTier), default=CoachTier.DEVELOPING, nullable=False)

    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    team = relationship("Team", back_populates="coaches")

    # RPG Attributes
    offense_rating = Column(Integer, default=50)
    defense_rating = Column(Integer, default=50)
    development_rating = Column(Integer, default=50)
    intelligence = Column(Integer, default=70)  # NFL Identity Blueprint: Coordinator IQ

    # --- Defensive Disguise (Phase 11) ---
    # Used for DC vs QB pre-snap read battles
    # Higher rating = better at disguising coverages
    defensive_disguise = Column(Integer, default=50)

    # Skill Tree
    # e.g. {"WestCoastOffense": 5, "ZoneBlitz": 3}
    skills = Column(JSON, default=dict)

    # Traits
    traits = Column(JSON, default=list)

    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # Strategy
    playbook_offense = Column(String, nullable=True)  # e.g. "West Coast", "Spread"
    playbook_defense = Column(String, nullable=True)  # e.g. "4-3", "3-4"
    philosophy = Column(JSON, default=dict)  # e.g. {"run_heavy": 70, "blitz_frequency": 40}

    # Hyper-Immersive
    coaching_tree = relationship("CoachingTree", backref="coach", uselist=False)
