from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class Position(str, enum.Enum):
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"
    OT = "OT"
    OG = "OG"
    C = "C"
    DE = "DE"
    DT = "DT"
    LB = "LB"
    CB = "CB"
    S = "S"
    K = "K"
    P = "P"

class Player(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    position = Column(String, index=True) # Using String for flexibility, or Enum
    height = Column(Integer) # in inches
    weight = Column(Integer) # in lbs
    age = Column(Integer)
    experience = Column(Integer, default=0) # Years pro
    jersey_number = Column(Integer, default=0)
    overall_rating = Column(Integer, default=50, index=True)
    
    # Team Relationship
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True, index=True)
    team = relationship("Team", back_populates="players")

    # --- RPG Attributes (0-100 Scale) ---
    # General
    speed = Column(Integer, default=50)
    acceleration = Column(Integer, default=50)
    strength = Column(Integer, default=50)
    agility = Column(Integer, default=50)
    awareness = Column(Integer, default=50)
    
    # Offensive Specific
    throw_power = Column(Integer, default=50)
    throw_accuracy_short = Column(Integer, default=50)
    throw_accuracy_mid = Column(Integer, default=50)
    throw_accuracy_deep = Column(Integer, default=50)
    catching = Column(Integer, default=50)
    route_running = Column(Integer, default=50)
    pass_block = Column(Integer, default=50)
    run_block = Column(Integer, default=50)
    
    # Defensive Specific
    tackle = Column(Integer, default=50)
    hit_power = Column(Integer, default=50)
    block_shed = Column(Integer, default=50)
    man_coverage = Column(Integer, default=50)
    zone_coverage = Column(Integer, default=50)
    pass_rush_power = Column(Integer, default=50)
    pass_rush_finesse = Column(Integer, default=50)
    
    # Special Teams
    kick_power = Column(Integer, default=50)
    kick_accuracy = Column(Integer, default=50)

    # --- Physics & Simulation Attributes ---
    # QB
    arm_slot = Column(String, default="OverTop") # OverTop, ThreeQuarter, Sidearm
    release_point_height = Column(Float, default=6.0) # in feet
    
    # RB/Ball Carrier
    vision_cone_angle = Column(Integer, default=45) # Degrees
    break_tackle_threshold = Column(Float, default=100.0) # Force needed to tackle
    
    # --- RPG Progression ---
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    skill_points = Column(Integer, default=0)
    traits = Column(JSON, default=list) # List of trait strings e.g. ["DeepBall", "Clutch"]
    
    # Nano Banana
    image_url = Column(String, nullable=True)
    nano_id = Column(String, nullable=True) # Reference to Nano Banana processed asset

    # --- Contracts & Offseason ---
    contract_years = Column(Integer, default=1)
    contract_salary = Column(Integer, default=1000000) # In dollars
    is_rookie = Column(Boolean, default=False, index=True)
