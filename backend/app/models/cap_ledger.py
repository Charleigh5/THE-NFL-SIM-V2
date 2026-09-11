"""
Capology Double-Entry Ledger Models
===================================
Authoritative SQLAlchemy models enforcing double-entry financial accounting
for team salary caps, contracts, proration pools, and dead money liabilities.
"""

from typing import Optional, List, TYPE_CHECKING
import enum
from datetime import datetime
from sqlalchemy import Integer, String, BigInteger, ForeignKey, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.player import Player


class CapAccountType(str, enum.Enum):
    """
    Standardized double-entry accounting categories for salary cap management.
    """
    CAP_ROOM = "CAP_ROOM"                           # Available cap space (Credit/Equity)
    ACTIVE_SALARY_LIABILITY = "ACTIVE_SALARY_LIABILITY"   # 53-man roster cash base salaries (Debit)
    UNAMORTIZED_BONUS_POOL = "UNAMORTIZED_BONUS_POOL"     # Future signing bonus balance awaiting proration
    DEAD_MONEY_LIABILITY = "DEAD_MONEY_LIABILITY"         # Accelerated dead money from released/voided players
    ESCROW_GUARANTEE_POOL = "ESCROW_GUARANTEE_POOL"       # Funding pool for guaranteed contracts


class CapTransactionType(str, enum.Enum):
    """
    Business events triggering balanced debit/credit transactions.
    """
    INITIAL_ALLOCATION = "INITIAL_ALLOCATION"       # League-wide hard cap establishment
    CONTRACT_SIGNING = "CONTRACT_SIGNING"           # Free agency or extension signing
    CONTRACT_RESTRUCTURE = "CONTRACT_RESTRUCTURE"   # Converting base salary to signing bonus
    RELEASE_PRE_JUNE_1 = "RELEASE_PRE_JUNE_1"       # Pre-June 1st player release (immediate acceleration)
    RELEASE_POST_JUNE_1 = "RELEASE_POST_JUNE_1"     # Post-June 1st player release (2-year split)
    TRADE_ACQUISITION = "TRADE_ACQUISITION"         # Incoming contract obligations
    TRADE_OUTGOING = "TRADE_OUTGOING"               # Outgoing contract obligations
    VOID_YEAR_ACCELERATION = "VOID_YEAR_ACCELERATION" # Contract void trigger
    CAP_ROLLOVER = "CAP_ROLLOVER"                   # Unused cap rolled into subsequent season


class CapLedgerAccount(Base):
    """
    A financial bucket representing a specific asset/liability category for a team in a league year.
    """
    __tablename__ = "cap_ledger_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), index=True, nullable=False)
    account_type: Mapped[CapAccountType] = mapped_column(SQLEnum(CapAccountType), nullable=False)
    league_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    balance: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False) # In exact integer dollars

    # Relationships
    entries: Mapped[List["CapLedgerEntry"]] = relationship("CapLedgerEntry", back_populates="account")


class CapLedgerTransaction(Base):
    """
    An atomic business event journal header containing one or more balanced entries.
    Invariant: sum(entries.amount) == 0.
    """
    __tablename__ = "cap_ledger_transaction"

    id: Mapped[str] = mapped_column(String(64), primary_key=True) # UUID
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), index=True, nullable=False)
    player_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("player.id"), nullable=True, index=True)
    transaction_type: Mapped[CapTransactionType] = mapped_column(SQLEnum(CapTransactionType), nullable=False)
    league_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    is_committed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    entries: Mapped[List["CapLedgerEntry"]] = relationship("CapLedgerEntry", back_populates="transaction", cascade="all, delete-orphan")


class CapLedgerEntry(Base):
    """
    Individual debit/credit line item associated with an account and transaction.
    Positive (+) = Debit
    Negative (-) = Credit
    """
    __tablename__ = "cap_ledger_entry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(String(64), ForeignKey("cap_ledger_transaction.id"), index=True, nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("cap_ledger_account.id"), index=True, nullable=False)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False) # Positive = Debit, Negative = Credit

    # Relationships
    transaction: Mapped["CapLedgerTransaction"] = relationship("CapLedgerTransaction", back_populates="entries")
    account: Mapped["CapLedgerAccount"] = relationship("CapLedgerAccount", back_populates="entries")
