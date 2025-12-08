"""
PLAYBOOK Package
================
Play calling and strategy systems.

Phase 9: Playbook & AI
- Playbook Management
- Play Calling AI
- Defensive Coordinator
"""

from .playbook import (
    Playbook,
    Play,
    Personnel,
    PlayType,
    Formation,
    Concept,
    DefensiveScheme,
    PlaybookGenerator,
)

from .play_caller import (
    PlayCallerAI,
    GameSituation,
    PlayCallResult,
    AggressionLevel,
    GameScript,
)

from .defensive_ai import (
    DefensiveCoordinatorAI,
    DefensiveCall,
    DefensiveGameplan,
    CoverageType,
    BlitzPackage,
)

__all__ = [
    # Playbook
    "Playbook", "Play", "Personnel",
    "PlayType", "Formation", "Concept", "DefensiveScheme",
    "PlaybookGenerator",
    # Play Caller
    "PlayCallerAI", "GameSituation", "PlayCallResult",
    "AggressionLevel", "GameScript",
    # Defensive AI
    "DefensiveCoordinatorAI", "DefensiveCall", "DefensiveGameplan",
    "CoverageType", "BlitzPackage",
]
