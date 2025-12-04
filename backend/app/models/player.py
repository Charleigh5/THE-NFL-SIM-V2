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

class InjuryStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    QUESTIONABLE = "QUESTIONABLE"
    DOUBTFUL = "DOUBTFUL"
    OUT = "OUT"
    IR = "IR"

class DevelopmentTrait(str, enum.Enum):
    NORMAL = "NORMAL"
    STAR = "STAR"
    SUPERSTAR = "SUPERSTAR"
    XFACTOR = "XFACTOR"

class Player(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    position = Column(String, index=True) # Using String for flexibility, or Enum
    college = Column(String, index=True, nullable=True)
    height = Column(Integer) # in inches
    weight = Column(Integer) # in lbs
    age = Column(Integer)
    experience = Column(Integer, default=0) # Years pro
    jersey_number = Column(Integer, default=0)
    overall_rating = Column(Integer, default=50, index=True)
    depth_chart_rank = Column(Integer, default=999) # Lower is better (starter = 1)

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
    stamina = Column(Integer, default=80) # New for Phase 7
    injury_resistance = Column(Integer, default=80) # New for Phase 7

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
    play_recognition = Column(Integer, default=50) # New for Phase 7

    # Special Teams
    kick_power = Column(Integer, default=50)
    kick_accuracy = Column(Integer, default=50)

    # --- Proposed QB Enhancements ---
    pocket_presence = Column(Integer, default=50, nullable=False)
    quick_release = Column(Integer, default=50, nullable=False)
    scramble_willingness = Column(Integer, default=50, nullable=False)
    throw_on_run = Column(Integer, default=50, nullable=False)

    # --- Proposed RB Enhancements ---
    patience = Column(Integer, default=50, nullable=False)
    pass_pro_rating = Column(Integer, default=50, nullable=False)
    juke_efficiency = Column(Integer, default=50, nullable=False)

    # --- Proposed WR/TE Enhancements ---
    release = Column(Integer, default=50, nullable=False)
    blocking_tenacity = Column(Integer, default=50, nullable=False)

    # --- Proposed OL Enhancements ---
    pull_speed = Column(Integer, default=50, nullable=False)
    anchor = Column(Integer, default=50, nullable=False)
    discipline = Column(Integer, default=50, nullable=False)

    # --- Proposed DL Enhancements ---
    first_step = Column(Integer, default=50, nullable=False)
    gap_integrity = Column(Integer, default=50, nullable=False)

    # --- Proposed LB Enhancements ---
    coverage_disguise = Column(Integer, default=50, nullable=False)
    blitz_timing = Column(Integer, default=50, nullable=False)
    run_fit = Column(Integer, default=50, nullable=False)

    # --- Proposed DB Enhancements ---
    press = Column(Integer, default=50, nullable=False)
    ball_tracking = Column(Integer, default=50, nullable=False)
    run_support = Column(Integer, default=50, nullable=False)

    # --- Proposed K/P Enhancements ---
    hang_time = Column(Integer, default=50, nullable=False)
    coffin_corner = Column(Integer, default=50, nullable=False)
    return_vision = Column(Integer, default=50, nullable=False)

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
    traits = relationship("Trait", secondary="player_traits")
    development_trait = Column(String, default=DevelopmentTrait.NORMAL) # Using String to store Enum value

    # --- Morale & Chemistry ---
    morale = Column(Integer, default=50) # 0-100

    # --- Injury System ---
    injury_status = Column(String, default=InjuryStatus.ACTIVE)
    injury_type = Column(String, nullable=True) # e.g. "ACL Tear", "Sprained Ankle"
    weeks_to_recovery = Column(Integer, default=0)
    injury_severity = Column(Integer, default=0) # 1-10 scale
    injury_recurrence_risk = Column(Float, default=0.0)

    # Nano Banana
    image_url = Column(String, nullable=True)
    nano_id = Column(String, nullable=True) # Reference to Nano Banana processed asset

    # --- Contracts & Offseason ---
    contract_years = Column(Integer, default=1)
    contract_salary = Column(Integer, default=1000000) # In dollars
    is_rookie = Column(Boolean, default=False, index=True)

    # --- Retirement & Legacy ---
    is_retired = Column(Boolean, default=False, index=True)
    retirement_year = Column(Integer, nullable=True)
    legacy_score = Column(Integer, default=0) # For Hall of Fame tracking

    # History
    season_stats = relationship("PlayerSeasonStats", back_populates="player")

class Trait(Base):
    __tablename__ = 'traits'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

class PlayerTrait(Base):
    __tablename__ = 'player_traits'
    player_id = Column(Integer, ForeignKey('player.id'), primary_key=True)
    trait_id = Column(Integer, ForeignKey('traits.id'), primary_key=True)
