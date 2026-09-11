"""
Capology Double-Entry Ledger Pydantic Schemas
============================================
Strict Pydantic V2 schemas for double-entry financial transactions,
account balances, and institutional audit statements.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.cap_ledger import CapAccountType, CapTransactionType


class CapLedgerEntryDTO(BaseModel):
    """
    Line-item debit/credit entry.
    """
    id: Optional[int] = None
    account_id: int
    account_type: CapAccountType
    amount: int = Field(description="Positive (+) for Debit, Negative (-) for Credit")
    model_config = ConfigDict(from_attributes=True)


class CapLedgerTransactionDTO(BaseModel):
    """
    Journaled business transaction with balanced entries.
    """
    id: str
    team_id: int
    player_id: Optional[int] = None
    player_name: Optional[str] = None
    transaction_type: CapTransactionType
    league_year: int
    timestamp: datetime
    description: str
    is_committed: bool = True
    entries: List[CapLedgerEntryDTO] = []
    net_cap_delta: int = 0
    model_config = ConfigDict(from_attributes=True)


class TeamLedgerStatementDTO(BaseModel):
    """
    Authoritative 5-year or single-year ledger statement for a team.
    """
    team_id: int
    team_name: str
    league_year: int
    total_salary_cap: int
    available_cap_room: int
    active_salary_liability: int
    dead_money_liability: int
    unamortized_bonus_pool: int
    is_balanced: bool = True
    proof_of_balance_delta: int = 0
    transactions: List[CapLedgerTransactionDTO] = []
    model_config = ConfigDict(from_attributes=True)


class MultiYearLedgerStatementResponse(BaseModel):
    """
    Consolidated 5-year multi-year outlook derived from ledger state.
    """
    team_id: int
    team_name: str
    base_league_year: int
    yearly_statements: List[TeamLedgerStatementDTO]
    is_fully_compliant: bool = True
    model_config = ConfigDict(from_attributes=True)


class LedgerSimulateRequest(BaseModel):
    """
    Request payload to simulate a contract transaction dry-run.
    """
    team_id: int
    player_id: Optional[int] = None
    transaction_type: CapTransactionType
    annual_base_salary: int = Field(default=1_000_000, ge=0)
    signing_bonus_total: int = Field(default=0, ge=0)
    real_years: int = Field(default=1, ge=1, le=5)
    void_years: int = Field(default=0, ge=0, le=4)
    post_june_1_designation: bool = False
    description: Optional[str] = None


class LedgerSimulateResponse(BaseModel):
    """
    Result of a dry-run ledger simulation with invariant checks.
    """
    team_id: int
    is_compliant: bool
    current_cap_room: int
    projected_cap_room: int
    net_cap_delta: int
    is_balanced: bool
    proof_of_balance_delta: int
    staged_entries: List[CapLedgerEntryDTO]
    compliance_message: str
    model_config = ConfigDict(from_attributes=True)
