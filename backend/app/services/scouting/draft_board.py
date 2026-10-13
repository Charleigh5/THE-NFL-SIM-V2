#!/usr/bin/env python3
"""
Draft Board Module
==================
Manages the list of prospects and team rankings.

Phase 8: Scouting & Draft
- Ranking logic (Best Player Available vs Need)
- Big Board management
- Picking logic
"""

from dataclasses import dataclass

# Import just for typing reference
from .scout import ScoutingReport


@dataclass
class Prospect:
    """An eligible draftee."""

    prospect_id: str
    name: str
    position: str
    college: str
    projected_round: int
    true_rating: int  # Hidden from user usually
    rank: int = 999  # Big Board rank
    scouted_rating: int = 50  # Perceived value


class DraftBoard:
    """
    Manages the draftable player pool and team-specific boards.
    """

    def __init__(self):
        self.prospects: dict[str, Prospect] = {}
        self.team_boards: dict[str, list[str]] = {}  # TeamID -> List[ProspectID] ordered

    def add_prospect(self, prospect: Prospect):
        self.prospects[prospect.prospect_id] = prospect

    def generate_team_board(
        self, team_id: str, needs: list[str], reports: dict[str, ScoutingReport]
    ):
        """
        Create a ranked list for a team based on their needs and scouting info.
        """
        # Score every prospect
        scored_prospects = []

        for pid, p in self.prospects.items():
            # Base score = perceived rating
            score = p.scouted_rating

            # Need multiplier
            if p.position in needs:
                score *= 1.15  # 15% boost for need

            # Scheme fit? (Placeholder)
            # score += scheme_bonus

            scored_prospects.append((score, pid))

        # Sort desc
        scored_prospects.sort(key=lambda x: x[0], reverse=True)

        self.team_boards[team_id] = [pid for _, pid in scored_prospects]

    def make_pick(self, team_id: str) -> Prospect | None:
        """
        Execute a pick for a team (Auto-pick top of board).
        """
        board = self.team_boards.get(team_id, [])

        # Find highest ranked available
        for pid in board:
            if pid in self.prospects:  # Still available?
                # In a real db system, we'd check 'picked' status
                # Here we simulate by popping from a 'remaining' list conceptually
                # But for this class, we just return the object
                return self.prospects[pid]

        return None
