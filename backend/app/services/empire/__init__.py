"""
EMPIRE Economic Package
=======================
Economic simulation for NFL teams.

Phase 5: EMPIRE Economic Simulation
- Salary cap management
- Contract creation
- GM AI with GOAP
"""

from .gm_ai import (
    GMAI,
    DraftPick,
    GMAIConfig,
    GMState,
    GOAPAction,
    NeedPriority,
    RosterNeed,
    TeamPhilosophy,
    TradeAssetType,
)
from .salary_cap import (
    CapChargeType,
    Contract,
    ContractType,
    ContractYear,
    SalaryCapConfig,
    SalaryCapEngine,
    TeamCapState,
)

__all__ = [
    # Salary Cap
    "SalaryCapEngine",
    "SalaryCapConfig",
    "Contract",
    "ContractYear",
    "ContractType",
    "TeamCapState",
    "CapChargeType",
    # GM AI
    "GMAI",
    "GMAIConfig",
    "GMState",
    "GOAPAction",
    "DraftPick",
    "RosterNeed",
    "TeamPhilosophy",
    "TradeAssetType",
    "NeedPriority",
]
