from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.player import Player

class PlayerContract(Base):
    """
    Player Contract Model (1:1 with Player)
    Contains contract details, rookie status, and retirement info.
    """
    __tablename__ = 'player_contract'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("player.id"), unique=True, index=True)

    # Back relation
    player: Mapped["Player"] = relationship("Player", back_populates="contract")

    # Contract Details
    contract_years: Mapped[int] = mapped_column(Integer, default=1)
    contract_salary: Mapped[int] = mapped_column(Integer, default=1000000)
    is_rookie: Mapped[bool] = mapped_column(Boolean, default=False)

    # Retirement & Legacy
    is_retired: Mapped[bool] = mapped_column(Boolean, default=False)
    retirement_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    legacy_score: Mapped[int] = mapped_column(Integer, default=0)

    # Morale
    morale: Mapped[int] = mapped_column(Integer, default=50)
