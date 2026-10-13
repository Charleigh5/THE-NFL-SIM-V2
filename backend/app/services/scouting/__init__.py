"""
SCOUTING Package
================
Draft and Prospect evaluation systems.

Phase 8: Scouting & Draft
- Scout Engine (Fog of War)
- Combine Simulation
- Draft Board & Logic
"""

from .combine import (
    CombineResults,
    CombineSimulation,
)
from .draft_board import (
    DraftBoard,
    Prospect,
)
from .scout import (
    KnowledgeTier,
    ScoutingEngine,
    ScoutingReport,
    ScoutProfile,
    ScoutRegion,
    ScoutSpecialty,
)

__all__ = [
    # Scout
    "ScoutingEngine",
    "ScoutProfile",
    "ScoutingReport",
    "ScoutRegion",
    "ScoutSpecialty",
    "KnowledgeTier",
    # Combine
    "CombineSimulation",
    "CombineResults",
    # Draft
    "DraftBoard",
    "Prospect",
]
