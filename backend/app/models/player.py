from __future__ import annotations

import enum
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Enum, Boolean, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.trait import PlayerTrait
    from app.models.player_game_starts import PlayerGameStarts
    from app.models.player_attributes import PlayerAttributes
    from app.models.player_contract import PlayerContract
    from app.models.player_physics import PlayerPhysics
    from app.models.player_injury import PlayerInjury
    from app.models.player_progression import PlayerProgression
    from app.models.team import Team
    from app.models.history import PlayerSeasonStats
    from app.models.medical import BodyPart

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
    height: Mapped[int] = mapped_column(Integer, default=72) # in inches
    weight: Mapped[int] = mapped_column(Integer, default=200) # in lbs
    age: Mapped[int] = mapped_column(Integer, default=22)
    experience: Mapped[int] = mapped_column(Integer, default=0) # Years pro
    jersey_number: Mapped[int] = mapped_column(Integer, default=0)
    overall_rating: Mapped[int] = mapped_column(Integer, default=50, index=True)
    depth_chart_rank: Mapped[int] = mapped_column(Integer, default=999) # Lower is better (starter = 1)

    # Team Relationship
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("team.id"), nullable=True, index=True)
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="players")

    # --- Society & Psychological DNA (TASK-009) ---
    psychological_dna: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    backstory: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    tension_score: Mapped[float] = mapped_column(Float, default=0.0)
    trust_in_coach: Mapped[int] = mapped_column(Integer, default=80)
    trust_in_qb: Mapped[int] = mapped_column(Integer, default=80)

    # --- RPG Attributes (Proxied to PlayerAttributes) ---
    @hybrid_property
    def speed(self) -> int:
        return self.attributes.speed if self.attributes else 50
    @speed.setter
    def speed(self, value):
        if self.attributes: self.attributes.speed = value
    @speed.expression
    def speed(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.speed).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def acceleration(self) -> int:
        return self.attributes.acceleration if self.attributes else 50
    @acceleration.setter
    def acceleration(self, value):
        if self.attributes: self.attributes.acceleration = value
    @acceleration.expression
    def acceleration(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.acceleration).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def strength(self) -> int:
        return self.attributes.strength if self.attributes else 50
    @strength.setter
    def strength(self, value):
        if self.attributes: self.attributes.strength = value
    @strength.expression
    def strength(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.strength).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def agility(self) -> int:
        return self.attributes.agility if self.attributes else 50
    @agility.setter
    def agility(self, value):
        if self.attributes: self.attributes.agility = value
    @agility.expression
    def agility(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.agility).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def awareness(self) -> int:
        return self.attributes.awareness if self.attributes else 50
    @awareness.setter
    def awareness(self, value):
        if self.attributes: self.attributes.awareness = value
    @awareness.expression
    def awareness(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.awareness).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def stamina(self) -> int:
        return self.attributes.stamina if self.attributes else 80
    @stamina.setter
    def stamina(self, value):
        if self.attributes: self.attributes.stamina = value
    @stamina.expression
    def stamina(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.stamina).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def injury_resistance(self) -> int:
        return self.attributes.injury_resistance if self.attributes else 80
    @injury_resistance.setter
    def injury_resistance(self, value):
        if self.attributes: self.attributes.injury_resistance = value
    @injury_resistance.expression
    def injury_resistance(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.injury_resistance).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    # --- NFL Combine Metrics (Proxied to PlayerAttributes) ---
    @hybrid_property
    def forty_yard_dash(self) -> Optional[float]:
        return self.attributes.forty_yard_dash if self.attributes else None
    @forty_yard_dash.setter
    def forty_yard_dash(self, value):
        if self.attributes: self.attributes.forty_yard_dash = value
    @forty_yard_dash.expression
    def forty_yard_dash(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.forty_yard_dash).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def bench_press(self) -> Optional[int]:
        return self.attributes.bench_press if self.attributes else None
    @bench_press.setter
    def bench_press(self, value):
        if self.attributes: self.attributes.bench_press = value
    @bench_press.expression
    def bench_press(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.bench_press).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def vertical_jump(self) -> Optional[float]:
        return self.attributes.vertical_jump if self.attributes else None
    @vertical_jump.setter
    def vertical_jump(self, value):
        if self.attributes: self.attributes.vertical_jump = value
    @vertical_jump.expression
    def vertical_jump(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.vertical_jump).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def broad_jump(self) -> Optional[int]:
        return self.attributes.broad_jump if self.attributes else None
    @broad_jump.setter
    def broad_jump(self, value):
        if self.attributes: self.attributes.broad_jump = value
    @broad_jump.expression
    def broad_jump(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.broad_jump).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def three_cone_drill(self) -> Optional[float]:
        return self.attributes.three_cone_drill if self.attributes else None
    @three_cone_drill.setter
    def three_cone_drill(self, value):
        if self.attributes: self.attributes.three_cone_drill = value
    @three_cone_drill.expression
    def three_cone_drill(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.three_cone_drill).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def twenty_yard_shuttle(self) -> Optional[float]:
        return self.attributes.twenty_yard_shuttle if self.attributes else None
    @twenty_yard_shuttle.setter
    def twenty_yard_shuttle(self, value):
        if self.attributes: self.attributes.twenty_yard_shuttle = value
    @twenty_yard_shuttle.expression
    def twenty_yard_shuttle(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.twenty_yard_shuttle).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    # --- Genesis Data (Proxied to PlayerAttributes / PlayerInjury) ---
    @hybrid_property
    def power_clean_max(self) -> Optional[int]:
        return self.attributes.power_clean_max if self.attributes else None
    @power_clean_max.setter
    def power_clean_max(self, value):
        if self.attributes: self.attributes.power_clean_max = value
    @power_clean_max.expression
    def power_clean_max(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.power_clean_max).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def gps_speed_max(self) -> Optional[float]:
        return self.attributes.gps_speed_max if self.attributes else None
    @gps_speed_max.setter
    def gps_speed_max(self, value):
        if self.attributes: self.attributes.gps_speed_max = value
    @gps_speed_max.expression
    def gps_speed_max(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.gps_speed_max).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def s2_cognition_score(self) -> Optional[int]:
        return self.attributes.s2_cognition_score if self.attributes else None
    @s2_cognition_score.setter
    def s2_cognition_score(self, value):
        if self.attributes: self.attributes.s2_cognition_score = value
    @s2_cognition_score.expression
    def s2_cognition_score(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.s2_cognition_score).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def medical_flags(self) -> Optional[dict]:
        return self.injury.medical_flags if self.injury else None
    @medical_flags.setter
    def medical_flags(self, value):
        if self.injury: self.injury.medical_flags = value
    @medical_flags.expression
    def medical_flags(cls):
        from app.models.player_injury import PlayerInjury
        return select(PlayerInjury.medical_flags).where(PlayerInjury.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def genesis_revealed(self) -> bool:
        return self.injury.genesis_revealed if self.injury else False
    @genesis_revealed.setter
    def genesis_revealed(self, value):
        if self.injury: self.injury.genesis_revealed = value
    @genesis_revealed.expression
    def genesis_revealed(cls):
        from app.models.player_injury import PlayerInjury
        return select(PlayerInjury.genesis_revealed).where(PlayerInjury.player_id == cls.id).scalar_subquery()

    # --- Position Specific (Proxied to PlayerAttributes) ---
    @hybrid_property
    def throw_power(self) -> int:
        return self.attributes.throw_power if self.attributes else 50
    @throw_power.setter
    def throw_power(self, value):
        if self.attributes: self.attributes.throw_power = value
    @throw_power.expression
    def throw_power(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.throw_power).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def throw_accuracy_short(self) -> int:
        return self.attributes.throw_accuracy_short if self.attributes else 50
    @throw_accuracy_short.setter
    def throw_accuracy_short(self, value):
        if self.attributes: self.attributes.throw_accuracy_short = value
    @throw_accuracy_short.expression
    def throw_accuracy_short(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.throw_accuracy_short).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def throw_accuracy_mid(self) -> int:
        return self.attributes.throw_accuracy_mid if self.attributes else 50
    @throw_accuracy_mid.setter
    def throw_accuracy_mid(self, value):
        if self.attributes: self.attributes.throw_accuracy_mid = value
    @throw_accuracy_mid.expression
    def throw_accuracy_mid(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.throw_accuracy_mid).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def throw_accuracy_deep(self) -> int:
        return self.attributes.throw_accuracy_deep if self.attributes else 50
    @throw_accuracy_deep.setter
    def throw_accuracy_deep(self, value):
        if self.attributes: self.attributes.throw_accuracy_deep = value
    @throw_accuracy_deep.expression
    def throw_accuracy_deep(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.throw_accuracy_deep).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def catching(self) -> int:
        return self.attributes.catching if self.attributes else 50
    @catching.setter
    def catching(self, value):
        if self.attributes: self.attributes.catching = value
    @catching.expression
    def catching(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.catching).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def route_running(self) -> int:
        return self.attributes.route_running if self.attributes else 50
    @route_running.setter
    def route_running(self, value):
        if self.attributes: self.attributes.route_running = value
    @route_running.expression
    def route_running(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.route_running).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def pass_block(self) -> int:
        return self.attributes.pass_block if self.attributes else 50
    @pass_block.setter
    def pass_block(self, value):
        if self.attributes: self.attributes.pass_block = value
    @pass_block.expression
    def pass_block(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.pass_block).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def run_block(self) -> int:
        return self.attributes.run_block if self.attributes else 50
    @run_block.setter
    def run_block(self, value):
        if self.attributes: self.attributes.run_block = value
    @run_block.expression
    def run_block(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.run_block).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def tackle(self) -> int:
        return self.attributes.tackle if self.attributes else 50
    @tackle.setter
    def tackle(self, value):
        if self.attributes: self.attributes.tackle = value
    @tackle.expression
    def tackle(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.tackle).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def hit_power(self) -> int:
        return self.attributes.hit_power if self.attributes else 50
    @hit_power.setter
    def hit_power(self, value):
        if self.attributes: self.attributes.hit_power = value
    @hit_power.expression
    def hit_power(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.hit_power).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def block_shed(self) -> int:
        return self.attributes.block_shed if self.attributes else 50
    @block_shed.setter
    def block_shed(self, value):
        if self.attributes: self.attributes.block_shed = value
    @block_shed.expression
    def block_shed(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.block_shed).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def man_coverage(self) -> int:
        return self.attributes.man_coverage if self.attributes else 50
    @man_coverage.setter
    def man_coverage(self, value):
        if self.attributes: self.attributes.man_coverage = value
    @man_coverage.expression
    def man_coverage(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.man_coverage).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def zone_coverage(self) -> int:
        return self.attributes.zone_coverage if self.attributes else 50
    @zone_coverage.setter
    def zone_coverage(self, value):
        if self.attributes: self.attributes.zone_coverage = value
    @zone_coverage.expression
    def zone_coverage(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.zone_coverage).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def pass_rush_power(self) -> int:
        return self.attributes.pass_rush_power if self.attributes else 50
    @pass_rush_power.setter
    def pass_rush_power(self, value):
        if self.attributes: self.attributes.pass_rush_power = value
    @pass_rush_power.expression
    def pass_rush_power(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.pass_rush_power).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def pass_rush_finesse(self) -> int:
        return self.attributes.pass_rush_finesse if self.attributes else 50
    @pass_rush_finesse.setter
    def pass_rush_finesse(self, value):
        if self.attributes: self.attributes.pass_rush_finesse = value
    @pass_rush_finesse.expression
    def pass_rush_finesse(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.pass_rush_finesse).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def play_recognition(self) -> int:
        return self.attributes.play_recognition if self.attributes else 50
    @play_recognition.setter
    def play_recognition(self, value):
        if self.attributes: self.attributes.play_recognition = value
    @play_recognition.expression
    def play_recognition(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.play_recognition).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def kick_power(self) -> int:
        return self.attributes.kick_power if self.attributes else 50
    @kick_power.setter
    def kick_power(self, value):
        if self.attributes: self.attributes.kick_power = value
    @kick_power.expression
    def kick_power(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.kick_power).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def kick_accuracy(self) -> int:
        return self.attributes.kick_accuracy if self.attributes else 50
    @kick_accuracy.setter
    def kick_accuracy(self, value):
        if self.attributes: self.attributes.kick_accuracy = value
    @kick_accuracy.expression
    def kick_accuracy(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.kick_accuracy).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    # --- Position Specific Enhancements (Proxied to PlayerAttributes) ---
    @hybrid_property
    def pocket_presence(self) -> int:
        return self.attributes.pocket_presence if self.attributes else 50
    @pocket_presence.setter
    def pocket_presence(self, value):
        if self.attributes: self.attributes.pocket_presence = value
    @pocket_presence.expression
    def pocket_presence(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.pocket_presence).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def quick_release(self) -> int:
        return self.attributes.quick_release if self.attributes else 50
    @quick_release.setter
    def quick_release(self, value):
        if self.attributes: self.attributes.quick_release = value
    @quick_release.expression
    def quick_release(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.quick_release).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def scramble_willingness(self) -> int:
        return self.attributes.scramble_willingness if self.attributes else 50
    @scramble_willingness.setter
    def scramble_willingness(self, value):
        if self.attributes: self.attributes.scramble_willingness = value
    @scramble_willingness.expression
    def scramble_willingness(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.scramble_willingness).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def throw_on_run(self) -> int:
        return self.attributes.throw_on_run if self.attributes else 50
    @throw_on_run.setter
    def throw_on_run(self, value):
        if self.attributes: self.attributes.throw_on_run = value
    @throw_on_run.expression
    def throw_on_run(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.throw_on_run).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def patience(self) -> int:
        return self.attributes.patience if self.attributes else 50
    @patience.setter
    def patience(self, value):
        if self.attributes: self.attributes.patience = value
    @patience.expression
    def patience(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.patience).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def pass_pro_rating(self) -> int:
        return self.attributes.pass_pro_rating if self.attributes else 50
    @pass_pro_rating.setter
    def pass_pro_rating(self, value):
        if self.attributes: self.attributes.pass_pro_rating = value
    @pass_pro_rating.expression
    def pass_pro_rating(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.pass_pro_rating).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def juke_efficiency(self) -> int:
        return self.attributes.juke_efficiency if self.attributes else 50
    @juke_efficiency.setter
    def juke_efficiency(self, value):
        if self.attributes: self.attributes.juke_efficiency = value
    @juke_efficiency.expression
    def juke_efficiency(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.juke_efficiency).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def release(self) -> int:
        return self.attributes.release if self.attributes else 50
    @release.setter
    def release(self, value):
        if self.attributes: self.attributes.release = value
    @release.expression
    def release(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.release).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def blocking_tenacity(self) -> int:
        return self.attributes.blocking_tenacity if self.attributes else 50
    @blocking_tenacity.setter
    def blocking_tenacity(self, value):
        if self.attributes: self.attributes.blocking_tenacity = value
    @blocking_tenacity.expression
    def blocking_tenacity(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.blocking_tenacity).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def pull_speed(self) -> int:
        return self.attributes.pull_speed if self.attributes else 50
    @pull_speed.setter
    def pull_speed(self, value):
        if self.attributes: self.attributes.pull_speed = value
    @pull_speed.expression
    def pull_speed(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.pull_speed).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def anchor(self) -> int:
        return self.attributes.anchor if self.attributes else 50
    @anchor.setter
    def anchor(self, value):
        if self.attributes: self.attributes.anchor = value
    @anchor.expression
    def anchor(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.anchor).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def discipline(self) -> int:
        return self.attributes.discipline if self.attributes else 50
    @discipline.setter
    def discipline(self, value):
        if self.attributes: self.attributes.discipline = value
    @discipline.expression
    def discipline(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.discipline).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def first_step(self) -> int:
        return self.attributes.first_step if self.attributes else 50
    @first_step.setter
    def first_step(self, value):
        if self.attributes: self.attributes.first_step = value
    @first_step.expression
    def first_step(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.first_step).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def gap_integrity(self) -> int:
        return self.attributes.gap_integrity if self.attributes else 50
    @gap_integrity.setter
    def gap_integrity(self, value):
        if self.attributes: self.attributes.gap_integrity = value
    @gap_integrity.expression
    def gap_integrity(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.gap_integrity).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def coverage_disguise(self) -> int:
        return self.attributes.coverage_disguise if self.attributes else 50
    @coverage_disguise.setter
    def coverage_disguise(self, value):
        if self.attributes: self.attributes.coverage_disguise = value
    @coverage_disguise.expression
    def coverage_disguise(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.coverage_disguise).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def blitz_timing(self) -> int:
        return self.attributes.blitz_timing if self.attributes else 50
    @blitz_timing.setter
    def blitz_timing(self, value):
        if self.attributes: self.attributes.blitz_timing = value
    @blitz_timing.expression
    def blitz_timing(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.blitz_timing).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def run_fit(self) -> int:
        return self.attributes.run_fit if self.attributes else 50
    @run_fit.setter
    def run_fit(self, value):
        if self.attributes: self.attributes.run_fit = value
    @run_fit.expression
    def run_fit(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.run_fit).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def press(self) -> int:
        return self.attributes.press if self.attributes else 50
    @press.setter
    def press(self, value):
        if self.attributes: self.attributes.press = value
    @press.expression
    def press(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.press).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def ball_tracking(self) -> int:
        return self.attributes.ball_tracking if self.attributes else 50
    @ball_tracking.setter
    def ball_tracking(self, value):
        if self.attributes: self.attributes.ball_tracking = value
    @ball_tracking.expression
    def ball_tracking(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.ball_tracking).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def run_support(self) -> int:
        return self.attributes.run_support if self.attributes else 50
    @run_support.setter
    def run_support(self, value):
        if self.attributes: self.attributes.run_support = value
    @run_support.expression
    def run_support(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.run_support).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def hang_time(self) -> int:
        return self.attributes.hang_time if self.attributes else 50
    @hang_time.setter
    def hang_time(self, value):
        if self.attributes: self.attributes.hang_time = value
    @hang_time.expression
    def hang_time(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.hang_time).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def coffin_corner(self) -> int:
        return self.attributes.coffin_corner if self.attributes else 50
    @coffin_corner.setter
    def coffin_corner(self, value):
        if self.attributes: self.attributes.coffin_corner = value
    @coffin_corner.expression
    def coffin_corner(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.coffin_corner).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def return_vision(self) -> int:
        return self.attributes.return_vision if self.attributes else 50
    @return_vision.setter
    def return_vision(self, value):
        if self.attributes: self.attributes.return_vision = value
    @return_vision.expression
    def return_vision(cls):
        from app.models.player_attributes import PlayerAttributes
        return select(PlayerAttributes.return_vision).where(PlayerAttributes.player_id == cls.id).scalar_subquery()

    # --- Physics & Simulation Attributes (Proxied to PlayerPhysics) ---
    @hybrid_property
    def arm_slot(self) -> str:
        return self.physics.arm_slot if self.physics else "OverTop"
    @arm_slot.setter
    def arm_slot(self, value):
        if self.physics: self.physics.arm_slot = value
    @arm_slot.expression
    def arm_slot(cls):
        from app.models.player_physics import PlayerPhysics
        return select(PlayerPhysics.arm_slot).where(PlayerPhysics.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def release_point_height(self) -> float:
        return self.physics.release_point_height if self.physics else 6.0
    @release_point_height.setter
    def release_point_height(self, value):
        if self.physics: self.physics.release_point_height = value
    @release_point_height.expression
    def release_point_height(cls):
        from app.models.player_physics import PlayerPhysics
        return select(PlayerPhysics.release_point_height).where(PlayerPhysics.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def vision_cone_angle(self) -> int:
        return self.physics.vision_cone_angle if self.physics else 45
    @vision_cone_angle.setter
    def vision_cone_angle(self, value):
        if self.physics: self.physics.vision_cone_angle = value
    @vision_cone_angle.expression
    def vision_cone_angle(cls):
        from app.models.player_physics import PlayerPhysics
        return select(PlayerPhysics.vision_cone_angle).where(PlayerPhysics.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def break_tackle_threshold(self) -> float:
        return self.physics.break_tackle_threshold if self.physics else 100.0
    @break_tackle_threshold.setter
    def break_tackle_threshold(self, value):
        if self.physics: self.physics.break_tackle_threshold = value
    @break_tackle_threshold.expression
    def break_tackle_threshold(cls):
        from app.models.player_physics import PlayerPhysics
        return select(PlayerPhysics.break_tackle_threshold).where(PlayerPhysics.player_id == cls.id).scalar_subquery()

    # --- RPG Progression (Proxied to PlayerProgression) ---
    @hybrid_property
    def xp(self) -> int:
        return self.progression.xp if self.progression else 0
    @xp.setter
    def xp(self, value):
        if self.progression: self.progression.xp = value
    @xp.expression
    def xp(cls):
        from app.models.player_progression import PlayerProgression
        return select(PlayerProgression.xp).where(PlayerProgression.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def level(self) -> int:
        return self.progression.level if self.progression else 1
    @level.setter
    def level(self, value):
        if self.progression: self.progression.level = value
    @level.expression
    def level(cls):
        from app.models.player_progression import PlayerProgression
        return select(PlayerProgression.level).where(PlayerProgression.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def skill_points(self) -> int:
        return self.progression.skill_points if self.progression else 0
    @skill_points.setter
    def skill_points(self, value):
        if self.progression: self.progression.skill_points = value
    @skill_points.expression
    def skill_points(cls):
        from app.models.player_progression import PlayerProgression
        return select(PlayerProgression.skill_points).where(PlayerProgression.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def development_trait(self) -> str:
        return self.progression.development_trait if self.progression else "NORMAL"
    @development_trait.setter
    def development_trait(self, value):
        if self.progression: self.progression.development_trait = value
    @development_trait.expression
    def development_trait(cls):
        from app.models.player_progression import PlayerProgression
        return select(PlayerProgression.development_trait).where(PlayerProgression.player_id == cls.id).scalar_subquery()

    # Trait Relationship
    player_traits: Mapped[List["PlayerTrait"]] = relationship("PlayerTrait", back_populates="player", cascade="all, delete-orphan")

    # --- RPG Abilities (Phase 11) ---
    @hybrid_property
    def abilities(self) -> Optional[dict]:
        return self.progression.abilities if self.progression else {}
    @abilities.setter
    def abilities(self, value):
        if self.progression: self.progression.abilities = value
    @abilities.expression
    def abilities(cls):
        from app.models.player_progression import PlayerProgression
        return select(PlayerProgression.abilities).where(PlayerProgression.player_id == cls.id).scalar_subquery()

    # --- Use-Based Skill Progression (Skyrim-style) ---
    @hybrid_property
    def attribute_xp(self) -> Optional[dict]:
        return self.progression.attribute_xp if self.progression else {}
    @attribute_xp.setter
    def attribute_xp(self, value):
        if self.progression: self.progression.attribute_xp = value
    @attribute_xp.expression
    def attribute_xp(cls):
        from app.models.player_progression import PlayerProgression
        return select(PlayerProgression.attribute_xp).where(PlayerProgression.player_id == cls.id).scalar_subquery()

    # --- Injury System (Proxied to PlayerInjury) ---
    @hybrid_property
    def injury_status(self) -> str:
        return self.injury.injury_status if self.injury else "ACTIVE"
    @injury_status.setter
    def injury_status(self, value):
        if self.injury: self.injury.injury_status = value
    @injury_status.expression
    def injury_status(cls):
        from app.models.player_injury import PlayerInjury
        return select(PlayerInjury.injury_status).where(PlayerInjury.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def injury_type(self) -> Optional[str]:
        return self.injury.injury_type if self.injury else None
    @injury_type.setter
    def injury_type(self, value):
        if self.injury: self.injury.injury_type = value
    @injury_type.expression
    def injury_type(cls):
        from app.models.player_injury import PlayerInjury
        return select(PlayerInjury.injury_type).where(PlayerInjury.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def weeks_to_recovery(self) -> int:
        return self.injury.weeks_to_recovery if self.injury else 0
    @weeks_to_recovery.setter
    def weeks_to_recovery(self, value):
        if self.injury: self.injury.weeks_to_recovery = value
    @weeks_to_recovery.expression
    def weeks_to_recovery(cls):
        from app.models.player_injury import PlayerInjury
        return select(PlayerInjury.weeks_to_recovery).where(PlayerInjury.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def injury_severity(self) -> int:
        return self.injury.injury_severity if self.injury else 0
    @injury_severity.setter
    def injury_severity(self, value):
        if self.injury: self.injury.injury_severity = value
    @injury_severity.expression
    def injury_severity(cls):
        from app.models.player_injury import PlayerInjury
        return select(PlayerInjury.injury_severity).where(PlayerInjury.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def injury_recurrence_risk(self) -> float:
        return self.injury.injury_recurrence_risk if self.injury else 0.0
    @injury_recurrence_risk.setter
    def injury_recurrence_risk(self, value):
        if self.injury: self.injury.injury_recurrence_risk = value
    @injury_recurrence_risk.expression
    def injury_recurrence_risk(cls):
        from app.models.player_injury import PlayerInjury
        return select(PlayerInjury.injury_recurrence_risk).where(PlayerInjury.player_id == cls.id).scalar_subquery()

    # Nano Banana
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    nano_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # --- Contracts & Offseason (Proxied to PlayerContract) ---
    @hybrid_property
    def contract_years(self) -> int:
        return self.contract.contract_years if self.contract else 1
    @contract_years.setter
    def contract_years(self, value):
        if self.contract: self.contract.contract_years = value
    @contract_years.expression
    def contract_years(cls):
        from app.models.player_contract import PlayerContract
        return select(PlayerContract.contract_years).where(PlayerContract.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def contract_salary(self) -> int:
        return self.contract.contract_salary if self.contract else 1000000
    @contract_salary.setter
    def contract_salary(self, value):
        if self.contract: self.contract.contract_salary = value
    @contract_salary.expression
    def contract_salary(cls):
        from app.models.player_contract import PlayerContract
        return select(PlayerContract.contract_salary).where(PlayerContract.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def is_rookie(self) -> bool:
        return self.contract.is_rookie if self.contract else False
    @is_rookie.setter
    def is_rookie(self, value):
        if self.contract: self.contract.is_rookie = value
    @is_rookie.expression
    def is_rookie(cls):
        from app.models.player_contract import PlayerContract
        return select(PlayerContract.is_rookie).where(PlayerContract.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def is_retired(self) -> bool:
        return self.contract.is_retired if self.contract else False
    @is_retired.setter
    def is_retired(self, value):
        if self.contract: self.contract.is_retired = value
    @is_retired.expression
    def is_retired(cls):
        from app.models.player_contract import PlayerContract
        return select(PlayerContract.is_retired).where(PlayerContract.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def retirement_year(self) -> Optional[int]:
        return self.contract.retirement_year if self.contract else None
    @retirement_year.setter
    def retirement_year(self, value):
        if self.contract: self.contract.retirement_year = value
    @retirement_year.expression
    def retirement_year(cls):
        from app.models.player_contract import PlayerContract
        return select(PlayerContract.retirement_year).where(PlayerContract.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def legacy_score(self) -> int:
        return self.contract.legacy_score if self.contract else 0
    @legacy_score.setter
    def legacy_score(self, value):
        if self.contract: self.contract.legacy_score = value
    @legacy_score.expression
    def legacy_score(cls):
        from app.models.player_contract import PlayerContract
        return select(PlayerContract.legacy_score).where(PlayerContract.player_id == cls.id).scalar_subquery()

    @hybrid_property
    def morale(self) -> int:
        return self.contract.morale if self.contract else 50
    @morale.setter
    def morale(self, value):
        if self.contract: self.contract.morale = value
    @morale.expression
    def morale(cls):
        from app.models.player_contract import PlayerContract
        return select(PlayerContract.morale).where(PlayerContract.player_id == cls.id).scalar_subquery()

    # History
    season_stats: Mapped[List["PlayerSeasonStats"]] = relationship("PlayerSeasonStats", back_populates="player", cascade="all, delete-orphan")

    # New: Game Starts (OL Chemistry)
    game_starts: Mapped[List["PlayerGameStarts"]] = relationship("PlayerGameStarts", back_populates="player", cascade="all, delete-orphan")

    # Hyper-Immersive Relationships
    body_health: Mapped["BodyPart"] = relationship("BodyPart", back_populates="player", uselist=False, cascade="all, delete-orphan")

    # --- Phase 3: Player Decomposition (1:1 Relationships) ---
    attributes: Mapped["PlayerAttributes"] = relationship("PlayerAttributes", back_populates="player", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    contract: Mapped["PlayerContract"] = relationship("PlayerContract", back_populates="player", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    physics: Mapped["PlayerPhysics"] = relationship("PlayerPhysics", back_populates="player", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    injury: Mapped["PlayerInjury"] = relationship("PlayerInjury", back_populates="player", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    progression: Mapped["PlayerProgression"] = relationship("PlayerProgression", back_populates="player", uselist=False, cascade="all, delete-orphan", lazy="selectin")

    def __init__(self, **kwargs):
        from app.models.player_attributes import PlayerAttributes
        from app.models.player_contract import PlayerContract
        from app.models.player_physics import PlayerPhysics
        from app.models.player_injury import PlayerInjury
        from app.models.player_progression import PlayerProgression

        self.height = 72
        self.weight = 200
        self.age = 22
        self.experience = 0
        self.jersey_number = 0
        self.overall_rating = 50
        self.depth_chart_rank = 999
        self.psychological_dna = {}
        self.backstory = {}
        self.tension_score = 0.0
        self.trust_in_coach = 80
        self.trust_in_qb = 80

        # Initialize satellite models so setters work during initialization
        self.attributes = PlayerAttributes()
        self.contract = PlayerContract()
        self.physics = PlayerPhysics()
        self.injury = PlayerInjury()
        self.progression = PlayerProgression()

        # Manually set attributes to support hybrid properties in constructor
        for k, v in kwargs.items():
            if k == "position" and hasattr(v, "value"):
                setattr(self, k, v.value)
            else:
                setattr(self, k, v)

    def __repr__(self):
        return f"<Player(name='{self.first_name} {self.last_name}', position='{self.position}', id={self.id})>"
