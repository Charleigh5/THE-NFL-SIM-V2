from __future__ import annotations

import enum
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.trait import PlayerTrait
    from app.models.player_game_starts import PlayerGameStarts
    # from app.models.team import Team # Circular import handling if needed, or string reference
    # from app.models.stats import PlayerSeasonStats

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
    """
    Player Model - 2025 Refactor
    Uses SQLAlchemy 2.0 Mapped syntax for type safety.
    """
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    position: Mapped[str] = mapped_column(String, index=True) # Using String for flexibility, validation in schema
    college: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    height: Mapped[int] = mapped_column(Integer) # in inches
    weight: Mapped[int] = mapped_column(Integer) # in lbs
    age: Mapped[int] = mapped_column(Integer)
    experience: Mapped[int] = mapped_column(Integer, default=0) # Years pro
    jersey_number: Mapped[int] = mapped_column(Integer, default=0)
    overall_rating: Mapped[int] = mapped_column(Integer, default=50, index=True)
    depth_chart_rank: Mapped[int] = mapped_column(Integer, default=999) # Lower is better (starter = 1)

    # Team Relationship
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("team.id"), nullable=True, index=True)
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="players")

    # --- RPG Attributes (0-100 Scale) ---
    # General
    speed: Mapped[int] = mapped_column(Integer, default=50)
    acceleration: Mapped[int] = mapped_column(Integer, default=50)
    strength: Mapped[int] = mapped_column(Integer, default=50)
    agility: Mapped[int] = mapped_column(Integer, default=50)
    awareness: Mapped[int] = mapped_column(Integer, default=50)
    stamina: Mapped[int] = mapped_column(Integer, default=80)
    injury_resistance: Mapped[int] = mapped_column(Integer, default=80)

    # --- NFL Combine Metrics ---
    # Standard Combine Events
    forty_yard_dash: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bench_press: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    vertical_jump: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    broad_jump: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    three_cone_drill: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    twenty_yard_shuttle: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # --- Genesis Data (Advanced Biometrics) ---
    power_clean_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gps_speed_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    s2_cognition_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    medical_flags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True) # e.g. ["ACL Tear (2022)"]
    genesis_revealed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Offensive Specific
    throw_power: Mapped[int] = mapped_column(Integer, default=50)
    throw_accuracy_short: Mapped[int] = mapped_column(Integer, default=50)
    throw_accuracy_mid: Mapped[int] = mapped_column(Integer, default=50)
    throw_accuracy_deep: Mapped[int] = mapped_column(Integer, default=50)
    catching: Mapped[int] = mapped_column(Integer, default=50)
    route_running: Mapped[int] = mapped_column(Integer, default=50)
    pass_block: Mapped[int] = mapped_column(Integer, default=50)
    run_block: Mapped[int] = mapped_column(Integer, default=50)

    # Defensive Specific
    tackle: Mapped[int] = mapped_column(Integer, default=50)
    hit_power: Mapped[int] = mapped_column(Integer, default=50)
    block_shed: Mapped[int] = mapped_column(Integer, default=50)
    man_coverage: Mapped[int] = mapped_column(Integer, default=50)
    zone_coverage: Mapped[int] = mapped_column(Integer, default=50)
    pass_rush_power: Mapped[int] = mapped_column(Integer, default=50)
    pass_rush_finesse: Mapped[int] = mapped_column(Integer, default=50)
    play_recognition: Mapped[int] = mapped_column(Integer, default=50)

    # Special Teams
    kick_power: Mapped[int] = mapped_column(Integer, default=50)
    kick_accuracy: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed QB Enhancements ---
    pocket_presence: Mapped[int] = mapped_column(Integer, default=50)
    quick_release: Mapped[int] = mapped_column(Integer, default=50)
    scramble_willingness: Mapped[int] = mapped_column(Integer, default=50)
    throw_on_run: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed RB Enhancements ---
    patience: Mapped[int] = mapped_column(Integer, default=50)
    pass_pro_rating: Mapped[int] = mapped_column(Integer, default=50)
    juke_efficiency: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed WR/TE Enhancements ---
    release: Mapped[int] = mapped_column(Integer, default=50)
    blocking_tenacity: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed OL Enhancements ---
    pull_speed: Mapped[int] = mapped_column(Integer, default=50)
    anchor: Mapped[int] = mapped_column(Integer, default=50)
    discipline: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed DL Enhancements ---
    first_step: Mapped[int] = mapped_column(Integer, default=50)
    gap_integrity: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed LB Enhancements ---
    coverage_disguise: Mapped[int] = mapped_column(Integer, default=50)
    blitz_timing: Mapped[int] = mapped_column(Integer, default=50)
    run_fit: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed DB Enhancements ---
    press: Mapped[int] = mapped_column(Integer, default=50)
    ball_tracking: Mapped[int] = mapped_column(Integer, default=50)
    run_support: Mapped[int] = mapped_column(Integer, default=50)

    # --- Proposed K/P Enhancements ---
    hang_time: Mapped[int] = mapped_column(Integer, default=50)
    coffin_corner: Mapped[int] = mapped_column(Integer, default=50)
    return_vision: Mapped[int] = mapped_column(Integer, default=50)

    # --- Physics & Simulation Attributes ---
    # QB
    arm_slot: Mapped[str] = mapped_column(String, default="OverTop")
    release_point_height: Mapped[float] = mapped_column(Float, default=6.0)

    # RB/Ball Carrier
    vision_cone_angle: Mapped[int] = mapped_column(Integer, default=45)
    break_tackle_threshold: Mapped[float] = mapped_column(Float, default=100.0)

    # --- RPG Progression ---
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    skill_points: Mapped[int] = mapped_column(Integer, default=0)
    development_trait: Mapped[str] = mapped_column(String, default=DevelopmentTrait.NORMAL)

    # Trait Relationship - Refactored for new setup
    player_traits: Mapped[List["PlayerTrait"]] = relationship("PlayerTrait", back_populates="player")

    # --- RPG Abilities (Phase 11) ---
    # JSON dict of unlocked abilities: {"pre_snap_diagnostician": True, "audible_master": True}
    abilities: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)

    # --- Morale & Chemistry ---
    morale: Mapped[int] = mapped_column(Integer, default=50)

    # --- Injury System ---
    injury_status: Mapped[str] = mapped_column(String, default=InjuryStatus.ACTIVE)
    injury_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    weeks_to_recovery: Mapped[int] = mapped_column(Integer, default=0)
    injury_severity: Mapped[int] = mapped_column(Integer, default=0)
    injury_recurrence_risk: Mapped[float] = mapped_column(Float, default=0.0)

    # Nano Banana
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    nano_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # --- Contracts & Offseason ---
    contract_years: Mapped[int] = mapped_column(Integer, default=1)
    contract_salary: Mapped[int] = mapped_column(Integer, default=1000000)
    is_rookie: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    # --- Retirement & Legacy ---
    is_retired: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    retirement_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    legacy_score: Mapped[int] = mapped_column(Integer, default=0)

    # History
    season_stats: Mapped[List["PlayerSeasonStats"]] = relationship("PlayerSeasonStats", back_populates="player")

    # New: Game Starts (OL Chemistry)
    game_starts: Mapped[List["PlayerGameStarts"]] = relationship("PlayerGameStarts", back_populates="player")

    # Hyper-Immersive Relationships
    body_health: Mapped["BodyPart"] = relationship("BodyPart", back_populates="player", uselist=False)

    def __repr__(self):
        return f"<Player(name='{self.first_name} {self.last_name}', position='{self.position}', id={self.id})>"
