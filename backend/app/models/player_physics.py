from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.player import Player


class PlayerPhysics(Base):
    """
    Player Physics Model (1:1 with Player)
    Contains physical simulation parameters.
    """

    __tablename__ = "player_physics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("player.id"), unique=True, index=True
    )

    # Back relation
    player: Mapped[Player] = relationship("Player", back_populates="physics")

    # Physics Attributes
    arm_slot: Mapped[str] = mapped_column(String, default="OverTop")
    release_point_height: Mapped[float] = mapped_column(Float, default=6.0)
    vision_cone_angle: Mapped[int] = mapped_column(Integer, default=45)
    break_tackle_threshold: Mapped[float] = mapped_column(Float, default=100.0)
