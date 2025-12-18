from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, Float, String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import enum

if TYPE_CHECKING:
    from app.models.player import Player

class InjuryStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    QUESTIONABLE = "QUESTIONABLE"
    DOUBTFUL = "DOUBTFUL"
    OUT = "OUT"
    IR = "IR"

class PlayerInjury(Base):
    """
    Player Injury Model (1:1 with Player)
    Contains current injury status and medical history context.
    """
    __tablename__ = 'player_injury'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("player.id"), unique=True, index=True)

    # Back relation
    player: Mapped["Player"] = relationship("Player", back_populates="injury")

    # Injury State
    injury_status: Mapped[str] = mapped_column(String, default=InjuryStatus.ACTIVE)
    injury_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    weeks_to_recovery: Mapped[int] = mapped_column(Integer, default=0)
    injury_severity: Mapped[int] = mapped_column(Integer, default=0)
    injury_recurrence_risk: Mapped[float] = mapped_column(Float, default=0.0)

    # Medical Profile
    medical_flags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True) # e.g. ["ACL Tear (2022)"]
    genesis_revealed: Mapped[bool] = mapped_column(Boolean, default=False) # Revealed true potential/injury risk
