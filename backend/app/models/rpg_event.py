from __future__ import annotations
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

from app.models.base import Base

class RPGEvent(Base):
    """
    Persists important events from the EventBus (e.g., SACKS, TRADES, CONFLICTS).
    This serves as the 'memory' for the Living World Engine.
    NarrativeEngine queries this table to generate NewsItems and WeeklyRecaps.
    """
    __tablename__ = "rpg_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    event_type: Mapped[str] = mapped_column(String, nullable=False) # e.g. "SACK_EVENT"

    # Who was involved? Primary subject.
    player_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("player.id"), nullable=True)
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("team.id"), nullable=True)

    # Context
    season_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=False)
    week: Mapped[Optional[int]] = mapped_column(Integer, nullable=False)
    game_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # The full payload from the EventBus
    # We store the raw JSON so we can reconstruct the exact event details later
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Has this event been "consumed" by the narrative engine?
    # False = Needs to be processed into news/storylines
    # True = Already generated content
    processed: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RPGEvent(type='{self.event_type}', player_id={self.player_id}, processed={self.processed})>"
