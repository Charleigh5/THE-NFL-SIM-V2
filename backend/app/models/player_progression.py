from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.player import Player


class DevelopmentTrait(str, enum.Enum):
    NORMAL = "NORMAL"
    STAR = "STAR"
    SUPERSTAR = "SUPERSTAR"
    XFACTOR = "XFACTOR"


class PlayerProgression(Base):
    """
    Player Progression Model (1:1 with Player)
    Contains RPG progression data: XP, levels, abilities, dev traits.
    """

    __tablename__ = "player_progression"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("player.id"), unique=True, index=True
    )

    # Back relation
    player: Mapped[Player] = relationship("Player", back_populates="progression")

    # RPG Stats
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    skill_points: Mapped[int] = mapped_column(Integer, default=0)
    development_trait: Mapped[str] = mapped_column(String, default=DevelopmentTrait.NORMAL)

    # Detailed Tracking
    abilities: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
    attribute_xp: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
