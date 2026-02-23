#!/usr/bin/env python3
"""
Nemesis System Module
=====================
Tracks deep Rivalries and vendettas.

Phase 6: SOCIETY Locker Room Dynamics
- Player vs Player rivalries
- Team vs Team rivalries
- Escalation mechanics
- "Revenge Game" bonuses
"""

from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================


class RivalryType(str, Enum):
    """Types of nemesis relationships."""

    PERSONAL = "PERSONAL"  # History of conflict
    COMPETITIVE = "COMPETITIVE"  # Fighting for position/award
    DIVISIONAL = "DIVISIONAL"  # Team-based division rival
    LEGACY = "LEGACY"  # Historic rivalry


class NemesisEvent(str, Enum):
    """Events that trigger/escalate rivalries."""

    DIRTY_HIT = "DIRTY_HIT"
    TRASH_TALK = "TRASH_TALK"
    BIG_GAME_LOSS = "BIG_GAME_LOSS"
    MEDIA_INSULT = "MEDIA_INSULT"
    CONTRACT_DISPUTE = "CONTRACT_DISPUTE"


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class Rivalry:
    """A rivalry between two entities."""

    source_id: str
    target_id: str
    type: RivalryType
    intensity: float = 0.0  # 0-100 scale
    history: list[str] = field(default_factory=list)
    active: bool = True

    def escalate(self, amount: float, reason: str) -> None:
        """Increase rivalry intensity."""
        self.intensity = min(100.0, self.intensity + amount)
        self.history.append(reason)

    def cool_down(self, amount: float) -> None:
        """Decrease intensity over time."""
        self.intensity = max(0.0, self.intensity - amount)


@dataclass
class NemesisState:
    """State of all rivalries for a context."""

    rivalries: dict[str, Rivalry] = field(default_factory=dict)

    def get_rivalry(self, id1: str, id2: str) -> Rivalry | None:
        """Get rivalry between two IDs (direction agnostic)."""
        key1 = f"{id1}_{id2}"
        key2 = f"{id2}_{id1}"
        return self.rivalries.get(key1) or self.rivalries.get(key2)


# ============================================================================
# NEMESIS ENGINE
# ============================================================================


class NemesisEngine:
    """
    Manages rivalries and vendettas.

    Features:
    - Tracks rivalry escalation
    - Calculates "Heat" for matchups
    - Applies "Revenge" bonuses
    """

    def __init__(self):
        self.state = NemesisState()

    def register_event(
        self,
        source_id: str,
        target_id: str,
        event: NemesisEvent,
    ) -> Rivalry:
        """
        Record an event that creates or escalates a rivalry.
        """
        rivalry = self.state.get_rivalry(source_id, target_id)

        if not rivalry:
            # Create new rivalry
            rivalry_type = RivalryType.PERSONAL
            if event == NemesisEvent.BIG_GAME_LOSS:
                rivalry_type = RivalryType.COMPETITIVE

            rivalry = Rivalry(
                source_id=source_id, target_id=target_id, type=rivalry_type, intensity=0.0
            )
            key = f"{source_id}_{target_id}"
            self.state.rivalries[key] = rivalry

        # Escalate
        intensity_boost = {
            NemesisEvent.DIRTY_HIT: 40.0,
            NemesisEvent.TRASH_TALK: 10.0,
            NemesisEvent.BIG_GAME_LOSS: 25.0,
            NemesisEvent.MEDIA_INSULT: 15.0,
            NemesisEvent.CONTRACT_DISPUTE: 20.0,
        }.get(event, 5.0)

        rivalry.escalate(intensity_boost, f"Event: {event.value}")
        return rivalry

    def get_matchup_heat(self, team1_ids: list[str], team2_ids: list[str]) -> float:
        """
        Calculate the total "Heat" of a matchup roughly 0-100.

        Based on sum of individual rivalries involved.
        """
        total_intensity = 0.0

        for id1 in team1_ids:
            for id2 in team2_ids:
                rivalry = self.state.get_rivalry(id1, id2)
                if rivalry and rivalry.active:
                    total_intensity += rivalry.intensity

        # Normalize: 100 heat = ~5 intense rivalries
        return min(100.0, total_intensity / 5.0)

    def get_revenge_bonus(self, player_id: str, opponent_id: str) -> float:
        """
        Get attribute bonus multiplier for a player facing a rival.

        High intensity rivalry grants small boost (adrenaline).
        Too high might cause penalties (recklessness).
        """
        rivalry = self.state.get_rivalry(player_id, opponent_id)
        if not rivalry or not rivalry.active:
            return 1.0

        # 50 intensity = 1.05x boost
        # 100 intensity = 1.10x boost
        bonus = 1.0 + (rivalry.intensity / 1000.0)
        return bonus

    def decay_rivalries(self) -> None:
        """Process time decay for all rivalries."""
        for rivalry in self.state.rivalries.values():
            rivalry.cool_down(5.0)  # Cool down 5 points per period (week/season)
            if rivalry.intensity < 10.0:
                rivalry.active = False
