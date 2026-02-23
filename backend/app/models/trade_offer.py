"""Trade Offer Model for persisting trade proposals between teams."""

from datetime import datetime, timedelta
from enum import Enum as PyEnum

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class TradeOfferStatus(PyEnum):
    """Status of a trade offer."""

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COUNTERED = "COUNTERED"
    EXPIRED = "EXPIRED"
    WITHDRAWN = "WITHDRAWN"


class TradeOffer(Base):
    """
    Trade Offer Model - Tracks trade proposals between teams.

    Supports the full trade offer lifecycle:
    - Initial offer creation
    - AI GM evaluation and response
    - Accept/Reject/Counter actions
    - Offer expiration
    """

    __tablename__ = "trade_offer"

    id = Column(Integer, primary_key=True, index=True)

    # Teams involved
    offering_team_id = Column(Integer, ForeignKey("team.id"), nullable=False, index=True)
    receiving_team_id = Column(Integer, ForeignKey("team.id"), nullable=False, index=True)

    # Assets (stored as JSON arrays of IDs)
    offered_player_ids = Column(JSON, default=list)
    requested_player_ids = Column(JSON, default=list)
    offered_picks = Column(JSON, nullable=True)  # [{round: 1, year: 2025}, ...]
    requested_picks = Column(JSON, nullable=True)

    # Status
    status = Column(
        Enum(TradeOfferStatus), default=TradeOfferStatus.PENDING, nullable=False, index=True
    )

    # Messages
    message = Column(Text, nullable=True)  # Message from offering team
    gm_response = Column(Text, nullable=True)  # Response from AI GM

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    # Counter-offer tracking
    parent_offer_id = Column(Integer, ForeignKey("trade_offer.id"), nullable=True)

    # Relationships
    offering_team = relationship("Team", foreign_keys=[offering_team_id])
    receiving_team = relationship("Team", foreign_keys=[receiving_team_id])
    parent_offer = relationship("TradeOffer", remote_side=[id], backref="counter_offers")

    def __repr__(self):
        return f"<TradeOffer {self.id}: Team {self.offering_team_id} -> Team {self.receiving_team_id} ({self.status.value})>"

    @classmethod
    def create_with_expiration(cls, days: int = 3, **kwargs):
        """Create an offer with automatic expiration."""
        expires_at = datetime.utcnow() + timedelta(days=days)
        return cls(expires_at=expires_at, **kwargs)

    @property
    def is_expired(self) -> bool:
        """Check if the offer has expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
