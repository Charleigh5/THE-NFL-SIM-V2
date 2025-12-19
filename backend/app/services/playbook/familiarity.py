"""
Playbook Familiarity Module
===========================
Tracks player knowledge of plays and applies execution penalties.

Phase 3: Playbook Familiarity System
- Tracks play_knowledge per player/play combination
- Calculates execution penalties based on familiarity
- Implements learning with veteran bonuses
- Handles scheme change penalties

NFL Reality:
- New players take 6-8 weeks to learn a playbook
- Veterans learn faster due to pattern recognition
- Scheme changes (e.g., West Coast to Air Raid) cause regression
- Execution degrades with unfamiliar plays
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Learning rates (per play executed)
BASE_LEARNING_RATE = 0.05  # 5% per execution
VETERAN_LEARNING_MULTIPLIER = 1.5  # Veterans learn 50% faster
ROOKIE_LEARNING_MULTIPLIER = 0.8  # Rookies learn 20% slower

# Execution penalty bounds
MIN_EXECUTION_PENALTY = 0.70  # Minimum 70% effectiveness for unknown plays
MAX_EXECUTION_PENALTY = 1.00  # Full effectiveness for mastered plays

# Familiarity thresholds
FAMILIARITY_THRESHOLD_BASIC = 0.25  # Basic understanding
FAMILIARITY_THRESHOLD_COMPETENT = 0.50  # Competent execution
FAMILIARITY_THRESHOLD_PROFICIENT = 0.75  # Proficient execution
FAMILIARITY_THRESHOLD_MASTERY = 0.95  # Mastery

# Scheme change penalty
SCHEME_CHANGE_PENALTY = 0.30  # Lose 30% familiarity on scheme change

# Initial familiarity for new plays
INITIAL_FAMILIARITY = 0.10  # 10% base familiarity


class FamiliarityTier(str, Enum):
    """Familiarity tier for display purposes."""
    UNKNOWN = "UNKNOWN"
    BASIC = "BASIC"
    COMPETENT = "COMPETENT"
    PROFICIENT = "PROFICIENT"
    MASTERY = "MASTERY"


@dataclass
class PlayFamiliarity:
    """Familiarity data for a single play."""
    play_id: str
    familiarity: float = INITIAL_FAMILIARITY
    times_executed: int = 0
    times_successful: int = 0

    @property
    def success_rate(self) -> float:
        if self.times_executed == 0:
            return 0.0
        return self.times_successful / self.times_executed

    @property
    def tier(self) -> FamiliarityTier:
        if self.familiarity >= FAMILIARITY_THRESHOLD_MASTERY:
            return FamiliarityTier.MASTERY
        elif self.familiarity >= FAMILIARITY_THRESHOLD_PROFICIENT:
            return FamiliarityTier.PROFICIENT
        elif self.familiarity >= FAMILIARITY_THRESHOLD_COMPETENT:
            return FamiliarityTier.COMPETENT
        elif self.familiarity >= FAMILIARITY_THRESHOLD_BASIC:
            return FamiliarityTier.BASIC
        return FamiliarityTier.UNKNOWN


@dataclass
class PlaybookFamiliarity:
    """
    Tracks a player's familiarity with plays in a playbook.

    This component models the cognitive aspect of NFL players learning
    offensive/defensive schemes. Key mechanics:

    1. **Execution Penalty**: Unknown plays are harder to execute
    2. **Learning**: Familiarity increases with each execution
    3. **Veteran Bonus**: Experienced players learn faster
    4. **Scheme Changes**: Switching systems penalizes familiarity
    """

    player_id: int
    play_knowledge: Dict[str, PlayFamiliarity] = field(default_factory=dict)
    current_scheme: Optional[str] = None
    experience_years: int = 0

    # --- Core Methods ---

    def get_familiarity(self, play_id: str) -> float:
        """Get familiarity level for a specific play (0.0 to 1.0)."""
        if play_id not in self.play_knowledge:
            return INITIAL_FAMILIARITY
        return self.play_knowledge[play_id].familiarity

    def calculate_execution_penalty(self, play_id: str) -> float:
        """
        Calculate execution penalty based on play familiarity.

        Returns a multiplier between 0.7 (unfamiliar) and 1.0 (mastered).
        This multiplier affects player ratings during play execution.

        The curve is non-linear to model realistic learning:
        - Early learning has diminishing returns
        - Mid-range learning accelerates
        - Late mastery requires extensive practice
        """
        familiarity = self.get_familiarity(play_id)

        # Sigmoid-like curve for natural learning feel
        # Low familiarity = steep penalty, high familiarity = near 1.0
        penalty_range = MAX_EXECUTION_PENALTY - MIN_EXECUTION_PENALTY

        # Use smooth step for natural curve
        t = familiarity
        smooth_t = t * t * (3 - 2 * t)  # Smoothstep function

        penalty = MIN_EXECUTION_PENALTY + (penalty_range * smooth_t)

        return min(MAX_EXECUTION_PENALTY, max(MIN_EXECUTION_PENALTY, penalty))

    def learn_play(
        self,
        play_id: str,
        success: bool = True,
        practice_bonus: float = 1.0
    ) -> float:
        """
        Increase familiarity with a play after execution.

        Args:
            play_id: The play that was executed
            success: Whether the play was successful (affects learning rate)
            practice_bonus: Additional multiplier for practice sessions (1.0-2.0)

        Returns:
            New familiarity level
        """
        # Initialize if first time seeing this play
        if play_id not in self.play_knowledge:
            self.play_knowledge[play_id] = PlayFamiliarity(play_id=play_id)

        play_data = self.play_knowledge[play_id]

        # Calculate learning rate with modifiers
        learning_rate = BASE_LEARNING_RATE * practice_bonus

        # Apply experience modifier
        if self.experience_years >= 5:
            learning_rate *= VETERAN_LEARNING_MULTIPLIER
        elif self.experience_years == 0:
            learning_rate *= ROOKIE_LEARNING_MULTIPLIER

        # Success/failure affects learning
        if success:
            learning_rate *= 1.2  # 20% bonus for successful execution
        else:
            learning_rate *= 0.8  # 20% penalty for failed execution

        # Diminishing returns at high familiarity (harder to master)
        current = play_data.familiarity
        diminishing_factor = 1.0 - (current * 0.5)  # 50% reduction at 100%
        learning_rate *= diminishing_factor

        # Apply learning
        new_familiarity = min(1.0, current + learning_rate)
        play_data.familiarity = new_familiarity

        # Track execution stats
        play_data.times_executed += 1
        if success:
            play_data.times_successful += 1

        logger.debug(
            f"Player {self.player_id} learned play {play_id}: "
            f"{current:.2f} -> {new_familiarity:.2f}"
        )

        return new_familiarity

    def apply_scheme_change_penalty(self, new_scheme: str) -> None:
        """
        Apply penalty when team changes offensive/defensive scheme.

        Real NFL examples:
        - QB going from West Coast to Air Raid
        - LB switching from 4-3 to 3-4

        This causes a regression in all play familiarity.
        """
        if self.current_scheme is None:
            self.current_scheme = new_scheme
            return

        if new_scheme == self.current_scheme:
            return

        logger.info(
            f"Player {self.player_id} scheme change: "
            f"{self.current_scheme} -> {new_scheme}"
        )

        # Apply penalty to all plays
        for play_data in self.play_knowledge.values():
            old_familiarity = play_data.familiarity
            play_data.familiarity = max(
                INITIAL_FAMILIARITY,
                old_familiarity * (1.0 - SCHEME_CHANGE_PENALTY)
            )

        self.current_scheme = new_scheme

    # --- Bulk Operations ---

    def get_total_plays_known(self) -> int:
        """Count plays with at least basic familiarity."""
        return sum(
            1 for p in self.play_knowledge.values()
            if p.familiarity >= FAMILIARITY_THRESHOLD_BASIC
        )

    def get_mastered_plays(self) -> list[str]:
        """Get list of mastered play IDs."""
        return [
            play_id for play_id, data in self.play_knowledge.items()
            if data.familiarity >= FAMILIARITY_THRESHOLD_MASTERY
        ]

    def get_average_familiarity(self) -> float:
        """Get average familiarity across all known plays."""
        if not self.play_knowledge:
            return INITIAL_FAMILIARITY
        total = sum(p.familiarity for p in self.play_knowledge.values())
        return total / len(self.play_knowledge)

    def to_dict(self) -> dict:
        """Serialize to dictionary for API responses."""
        return {
            "player_id": self.player_id,
            "experience_years": self.experience_years,
            "current_scheme": self.current_scheme,
            "total_plays_known": self.get_total_plays_known(),
            "mastered_plays_count": len(self.get_mastered_plays()),
            "average_familiarity": self.get_average_familiarity(),
            "plays": {
                play_id: {
                    "familiarity": data.familiarity,
                    "tier": data.tier.value,
                    "times_executed": data.times_executed,
                    "success_rate": data.success_rate,
                }
                for play_id, data in self.play_knowledge.items()
            }
        }


class FamiliarityManager:
    """
    Service to manage familiarity across multiple players.

    Typically instantiated once per simulation and passed to play_resolver.
    """

    def __init__(self):
        self._players: Dict[int, PlaybookFamiliarity] = {}

    def get_or_create(
        self,
        player_id: int,
        experience_years: int = 0
    ) -> PlaybookFamiliarity:
        """Get existing familiarity or create new instance."""
        if player_id not in self._players:
            self._players[player_id] = PlaybookFamiliarity(
                player_id=player_id,
                experience_years=experience_years
            )
        return self._players[player_id]

    def calculate_team_execution_modifier(
        self,
        player_ids: list[int],
        play_id: str
    ) -> float:
        """
        Calculate average execution modifier for a group of players.

        Used when multiple players need to execute the same play
        (e.g., entire offensive line on a blocking scheme).
        """
        if not player_ids:
            return 1.0

        total = sum(
            self._players.get(pid, PlaybookFamiliarity(player_id=pid))
            .calculate_execution_penalty(play_id)
            for pid in player_ids
        )
        return total / len(player_ids)

    def apply_learning_batch(
        self,
        player_ids: list[int],
        play_id: str,
        success: bool
    ) -> None:
        """Apply learning to multiple players after a play."""
        for pid in player_ids:
            if pid in self._players:
                self._players[pid].learn_play(play_id, success)
