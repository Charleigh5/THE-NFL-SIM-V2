"""
SCOUTING Package
================
Draft and Prospect evaluation systems.

Phase 8: Scouting & Draft
- Scout Engine (Fog of War)
- Combine Simulation
- Draft Board & Logic
"""

from .scout import (
    ScoutingEngine,
    ScoutProfile,
    ScoutingReport,
    ScoutRegion,
    ScoutSpecialty,
    KnowledgeTier,
)

from .combine import (
    CombineSimulation,
    CombineResults,
)

from .draft_board import (
    DraftBoard,
    Prospect,
)

__all__ = [
    # Scout
    "ScoutingEngine", "ScoutProfile", "ScoutingReport",
    "ScoutRegion", "ScoutSpecialty", "KnowledgeTier",
    # Combine
    "CombineSimulation", "CombineResults",
    # Draft
    "DraftBoard", "Prospect",
]
