from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base
import datetime

class BodyPart(Base):
    """
    Detailed health tracking for a player's body parts.
    One-to-One relationship with Player.
    """
    __tablename__ = 'body_health'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"), unique=True, index=True)
    player = relationship("Player", back_populates="body_health")

    # Durability / Integrity (0-100). 100 = Perfect Health.
    # As this drops, injury risk rises and attributes drop.
    head_health = Column(Float, default=100.0)
    neck_health = Column(Float, default=100.0)
    torso_health = Column(Float, default=100.0) # Ribs, Back, Pecs
    right_arm_health = Column(Float, default=100.0) # Shoulder, Elbow, Hand
    left_arm_health = Column(Float, default=100.0)
    right_leg_health = Column(Float, default=100.0) # Hip, Knee, Ankle
    left_leg_health = Column(Float, default=100.0)

    # Wear Accumulation (Temporary fatigue/bruising that recovers weekly)
    general_wear = Column(Float, default=0.0)

    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class InjuryEvent(Base):
    """
    History of specific injury events.
    """
    __tablename__ = 'injury_events'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"), index=True)

    season_id = Column(Integer, ForeignKey("season.id"))
    week = Column(Integer)

    injury_name = Column(String) # e.g. "High Ankle Sprain"
    body_part = Column(String) # e.g. "right_leg"
    severity = Column(Integer) # 1-10 scale

    duration_weeks = Column(Integer)
    is_career_ending = Column(Boolean, default=False)

    # Treatment Choice
    treatment_chosen = Column(String, nullable=True) # "REST", "SURGERY", "PLAY_THROUGH"
