"""
PLAYBOOK Package
================
Play calling and strategy systems.

Phase 9: Playbook & AI
- Playbook Management
- Play Calling AI
- Defensive Coordinator
"""

from .defensive_ai import (
    BlitzPackage,
    CoverageType,
    DefensiveCall,
    DefensiveCoordinatorAI,
    DefensiveGameplan,
)
from .play_caller import (
    AggressionLevel,
    GameScript,
    GameSituation,
    PlayCallerAI,
    PlayCallResult,
)
from .playbook import (
    Concept,
    DefensiveScheme,
    Formation,
    Personnel,
    Play,
    Playbook,
    PlaybookGenerator,
    PlayType,
)

__all__ = [
    # Playbook
    "Playbook",
    "Play",
    "Personnel",
    "PlayType",
    "Formation",
    "Concept",
    "DefensiveScheme",
    "PlaybookGenerator",
    # Play Caller
    "PlayCallerAI",
    "GameSituation",
    "PlayCallResult",
    "AggressionLevel",
    "GameScript",
    # Defensive AI
    "DefensiveCoordinatorAI",
    "DefensiveCall",
    "DefensiveGameplan",
    "CoverageType",
    "BlitzPackage",
]
