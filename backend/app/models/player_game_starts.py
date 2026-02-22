from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PlayerGameStarts(Base):
    __tablename__ = "player_game_starts"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=False)
    # game_id will be added later when we have a Game model, for now just Integer or create Game stub if needed?
    # For now, linking to game_id assuming it exists or will exist.
    # Actually, Game model exists in task description "Task B2-BE-B: game_id: ForeignKey to Game"
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False)

    position_started: Mapped[str] = mapped_column(String(10), nullable=False)  # e.g. "LT", "RB"
    teammates_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True
    )  # Hash of OL unit IDs

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    player: Mapped[Player] = relationship(back_populates="game_starts")
    game: Mapped[Game] = relationship(back_populates="player_starts")

    __table_args__ = (
        Index("idx_player_game", "player_id", "game_id", unique=True),
        {"extend_existing": True},
    )

    def __repr__(self) -> str:
        return f"<PlayerGameStarts(player_id={self.player_id}, game_id={self.game_id}, pos='{self.position_started}')>"
