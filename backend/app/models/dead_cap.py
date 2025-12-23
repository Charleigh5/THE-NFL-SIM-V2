from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class DeadCapReason(str, enum.Enum):
    CUT = "CUT"
    TRADE = "TRADE"
    RETIREMENT = "RETIREMENT"

class DeadCapCharge(Base):
    __tablename__ = "dead_cap_charges"  # type: ignore[assignment]

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True) # Nullable in case player record is deleted, though usually we keep it
    amount = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    reason = Column(String, nullable=False) # Store as string for flexibility, or use Enum

    # Relationships
    team = relationship("Team", backref="dead_cap_charges")
    player = relationship("Player", backref="dead_cap_charges")
