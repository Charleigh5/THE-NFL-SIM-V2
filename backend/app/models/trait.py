from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class TraitEffectType(str, Enum):
    BOOST = "BOOST"
    SITUATIONAL = "SITUATIONAL"
    PASSIVE = "PASSIVE"


class TraitTier(str, Enum):
    """APF 2K8-style trait tiers for player differentiation."""
    GOLD = "GOLD"       # Elite, game-breaking abilities (max 1 per player)
    SILVER = "SILVER"   # Strong role-player traits (max 2 per player)
    BRONZE = "BRONZE"   # Solid supporting abilities (max 3 per player)
    COMMON = "COMMON"   # No cap, baseline traits


class TraitSource(str, Enum):
    DRAFT = "DRAFT"
    DEVELOPMENT = "DEVELOPMENT"
    MILESTONE = "MILESTONE"


class Trait(Base):
    __tablename__ = 'traits'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    effect_type: Mapped[TraitEffectType] = mapped_column(default=TraitEffectType.PASSIVE)
    effect_value: Mapped[float] = mapped_column(default=0.0)
    position_groups = mapped_column(JSON, nullable=True)  # JSON list of positions

    # APF 2K8-style tiered badge system
    tier: Mapped[TraitTier] = mapped_column(default=TraitTier.COMMON, nullable=True)
    is_badge: Mapped[bool] = mapped_column(default=True, nullable=True)  # Visible badge vs backend-only
    icon_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    players: Mapped[List["PlayerTrait"]] = relationship(back_populates="trait")

    def __repr__(self) -> str:
        return f"<Trait(name='{self.name}', type='{self.effect_type}')>"

class PlayerTrait(Base):
    __tablename__ = 'player_traits'

    player_id: Mapped[int] = mapped_column(ForeignKey('player.id'), primary_key=True)
    trait_id: Mapped[int] = mapped_column(ForeignKey('traits.id'), primary_key=True)

    acquired_date: Mapped[date] = mapped_column(default=date.today)
    source: Mapped[TraitSource] = mapped_column(default=TraitSource.DRAFT)

    # Relationships
    player: Mapped["Player"] = relationship(back_populates="player_traits")
    trait: Mapped["Trait"] = relationship(back_populates="players")

    def __repr__(self) -> str:
        return f"<PlayerTrait(player_id={self.player_id}, trait_id={self.trait_id})>"
