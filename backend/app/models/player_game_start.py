"""
Player Game Starts model for tracking OL continuity
"""
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class PlayerGameStart(Base):
    """
    Tracks which players started in which games and at which positions.
    Used primarily for calculating OL unit chemistry bonuses.
    """
    __tablename__ = 'player_game_starts'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False, index=True)
    game_id = Column(Integer, ForeignKey('game.id'), nullable=False, index=True)
    position = Column(Integer, nullable=False, index=True)  # Position they started at (LT, LG, C, RG, RT)
    started = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("Player", backref="game_starts")
    game = relationship("Game", backref="player_starts")

    def __repr__(self):
        return f"<PlayerGameStart(player_id={self.player_id}, game_id={self.game_id}, position={self.position})>"
