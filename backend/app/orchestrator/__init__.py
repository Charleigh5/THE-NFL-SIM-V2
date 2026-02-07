"""
Game Orchestrator Package
-------------------------
Agent 2: Senior Game Simulation Engineer

Coordinates all 6 backend kernels:
- Genesis (Player Biology)
- Empire (Team Management)
- Hive (Environmental Physics)
- Society (Media & Narrative)
- Core (Simulation Engine)
- RPG (Progression System)
"""

# from .game_orchestrator import GameOrchestrator
from .play_resolver import PlayResolver
from .state_machine import GameState, GameStateMachine

__all__ = ["GameStateMachine", "GameState", "PlayResolver"] # "GameOrchestrator" removed temporarily
