from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.player import Player

class PlayerAttributes(Base):
    """
    Player Attributes Model (1:1 with Player)
    Contains all skill ratings and combine metrics.
    """
    __tablename__ = 'player_attributes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("player.id"), unique=True, index=True)

    # Back relation
    player: Mapped[Player] = relationship("Player", back_populates="attributes")

    # --- RPG Attributes (0-100 Scale) ---
    # General
    speed: Mapped[int] = mapped_column(Integer, default=50)
    acceleration: Mapped[int] = mapped_column(Integer, default=50)
    strength: Mapped[int] = mapped_column(Integer, default=50)
    agility: Mapped[int] = mapped_column(Integer, default=50)
    awareness: Mapped[int] = mapped_column(Integer, default=50)
    stamina: Mapped[int] = mapped_column(Integer, default=80)
    injury_resistance: Mapped[int] = mapped_column(Integer, default=80)

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

    # --- Position Specific Enhancements ---
    # QB
    pocket_presence: Mapped[int] = mapped_column(Integer, default=50)
    quick_release: Mapped[int] = mapped_column(Integer, default=50)
    scramble_willingness: Mapped[int] = mapped_column(Integer, default=50)
    throw_on_run: Mapped[int] = mapped_column(Integer, default=50)

    # RB
    patience: Mapped[int] = mapped_column(Integer, default=50)
    pass_pro_rating: Mapped[int] = mapped_column(Integer, default=50)
    juke_efficiency: Mapped[int] = mapped_column(Integer, default=50)

    # WR/TE
    release: Mapped[int] = mapped_column(Integer, default=50)
    blocking_tenacity: Mapped[int] = mapped_column(Integer, default=50)

    # OL
    pull_speed: Mapped[int] = mapped_column(Integer, default=50)
    anchor: Mapped[int] = mapped_column(Integer, default=50)
    discipline: Mapped[int] = mapped_column(Integer, default=50)

    # DL
    first_step: Mapped[int] = mapped_column(Integer, default=50)
    gap_integrity: Mapped[int] = mapped_column(Integer, default=50)

    # LB
    coverage_disguise: Mapped[int] = mapped_column(Integer, default=50)
    blitz_timing: Mapped[int] = mapped_column(Integer, default=50)
    run_fit: Mapped[int] = mapped_column(Integer, default=50)

    # DB
    press: Mapped[int] = mapped_column(Integer, default=50)
    ball_tracking: Mapped[int] = mapped_column(Integer, default=50)
    run_support: Mapped[int] = mapped_column(Integer, default=50)

    # K/P
    hang_time: Mapped[int] = mapped_column(Integer, default=50)
    coffin_corner: Mapped[int] = mapped_column(Integer, default=50)
    return_vision: Mapped[int] = mapped_column(Integer, default=50)

    # --- NFL Combine Metrics ---
    forty_yard_dash: Mapped[float | None] = mapped_column(Float, nullable=True)
    bench_press: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vertical_jump: Mapped[float | None] = mapped_column(Float, nullable=True)
    broad_jump: Mapped[int | None] = mapped_column(Integer, nullable=True)
    three_cone_drill: Mapped[float | None] = mapped_column(Float, nullable=True)
    twenty_yard_shuttle: Mapped[float | None] = mapped_column(Float, nullable=True)

    # --- Genesis Data ---
    power_clean_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gps_speed_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    s2_cognition_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
