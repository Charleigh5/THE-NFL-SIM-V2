from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.player import Player
    from app.models.game import Game


class PlayerGameStarts(Base):
    """
    Consolidated Player Game Starts model.
    Tracks player starts, positions, and OL chemistry lineup hashes.
    """
    __tablename__ = 'player_game_starts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey('player.id'), nullable=False, index=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('game.id'), nullable=False, index=True)
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('team.id'), nullable=True, index=True)
    season_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('season.id'), nullable=True, index=True)
    week: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    position: Mapped[str] = mapped_column(String(10), nullable=False)
    teammates_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    player: Mapped["Player"] = relationship("Player", back_populates="game_starts")
    game: Mapped["Game"] = relationship("Game", back_populates="player_starts")

    @hybrid_property
    def position_started(self) -> str:
        return self.position

    @position_started.setter
    def position_started(self, value: str) -> None:
        self.position = value

    @position_started.expression
    def position_started(cls):
        return cls.position

    __table_args__ = (
        Index('idx_player_game_start', 'player_id', 'game_id', unique=False),
        {'extend_existing': True}
    )

    def __repr__(self) -> str:
        return f"<PlayerGameStarts(player_id={self.player_id}, game_id={self.game_id}, position='{self.position}')>"


# Alias for backward compatibility
PlayerGameStart = PlayerGameStarts
