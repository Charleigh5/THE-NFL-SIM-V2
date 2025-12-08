"""
EMPIRE Economic Package
=======================
Economic simulation for NFL teams.

Phase 5: EMPIRE Economic Simulation
- Salary cap management
- Contract creation
- GM AI with GOAP
"""

from .salary_cap import (
    SalaryCapEngine,
    SalaryCapConfig,
    Contract,
    ContractYear,
    ContractType,
    TeamCapState,
    CapChargeType,
)

from .gm_ai import (
    GMAI,
    GMAIConfig,
    GMState,
    GOAPAction,
    DraftPick,
    RosterNeed,
    TeamPhilosophy,
    TradeAssetType,
    NeedPriority,
)

__all__ = [
    # Salary Cap
    "SalaryCapEngine", "SalaryCapConfig", "Contract", "ContractYear",
    "ContractType", "TeamCapState", "CapChargeType",
    # GM AI
    "GMAI", "GMAIConfig", "GMState", "GOAPAction", "DraftPick",
    "RosterNeed", "TeamPhilosophy", "TradeAssetType", "NeedPriority",
]
