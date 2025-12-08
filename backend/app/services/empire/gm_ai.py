#!/usr/bin/env python3
"""
GM AI Module
============
CPU-controlled General Manager with GOAP.

Phase 5: EMPIRE Economic Simulation
- Goal-Oriented Action Planning
- Win Now vs Rebuild modes
- Trade evaluation
- Draft valuations
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
import math


# ============================================================================
# ENUMS
# ============================================================================

class TeamPhilosophy(str, Enum):
    """GM team-building philosophy."""
    WIN_NOW = "WIN_NOW"           # Maximize current roster
    REBUILD = "REBUILD"           # Accumulate assets/youth
    BALANCED = "BALANCED"         # Steady improvement
    DEVELOP = "DEVELOP"           # Focus on draft/development


class TradeAssetType(str, Enum):
    """Types of trade assets."""
    PLAYER = "PLAYER"
    DRAFT_PICK = "DRAFT_PICK"
    CAP_SPACE = "CAP_SPACE"


class NeedPriority(str, Enum):
    """Priority levels for roster needs."""
    CRITICAL = "CRITICAL"    # Must address immediately
    HIGH = "HIGH"            # Address this year
    MODERATE = "MODERATE"    # Nice to have
    LOW = "LOW"              # Future concern


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass(frozen=True)
class GMAIConfig:
    """Configuration for GM AI."""
    # Philosophy thresholds
    playoff_contender_wins: int = 9
    rebuild_trigger_wins: int = 5

    # Draft value decay
    draft_pick_value_decay: float = 0.85  # Per round

    # Trade preferences
    young_player_premium: float = 1.2  # Value boost for <25
    veteran_discount: float = 0.9      # Value drop for >30


@dataclass
class DraftPick:
    """A draft pick asset."""
    year: int
    round: int
    pick_number: Optional[int] = None  # Known after lottery
    original_team: str = ""

    @property
    def approximate_value(self) -> int:
        """Approximate trade value."""
        # Jimmy Johnson chart simplified
        if self.round == 1:
            if self.pick_number:
                base = 3000 - (self.pick_number - 1) * 80
            else:
                base = 2500
        elif self.round == 2:
            base = 600
        elif self.round == 3:
            base = 250
        elif self.round == 4:
            base = 100
        else:
            base = 50

        return max(10, base)


@dataclass
class RosterNeed:
    """A position of team need."""
    position: str
    priority: NeedPriority
    current_starter_rating: int
    depth_count: int


@dataclass
class GMState:
    """GM's current state and goals."""
    team_id: str
    philosophy: TeamPhilosophy = TeamPhilosophy.BALANCED

    # Assets
    cap_space: int = 0
    draft_picks: List[DraftPick] = field(default_factory=list)

    # Needs
    roster_needs: List[RosterNeed] = field(default_factory=list)

    # Performance
    expected_wins: float = 8.0
    playoff_odds: float = 0.5


# ============================================================================
# GOAP PLANNING
# ============================================================================

@dataclass
class GOAPAction:
    """A potential GM action."""
    name: str
    preconditions: Dict[str, Any]
    effects: Dict[str, Any]
    cost: float  # Lower = more desirable

    def can_execute(self, state: Dict[str, Any]) -> bool:
        """Check if preconditions are met."""
        for key, required in self.preconditions.items():
            if key not in state:
                return False
            if state[key] != required:
                return False
        return True

    def apply(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Apply effects to state."""
        new_state = state.copy()
        new_state.update(self.effects)
        return new_state


# ============================================================================
# GM AI ENGINE
# ============================================================================

class GMAI:
    """
    Goal-Oriented GM AI.

    Uses GOAP for decision-making:
    1. Assess current state
    2. Determine goal state
    3. Plan actions to reach goal
    4. Execute best action
    """

    def __init__(
        self,
        config: Optional[GMAIConfig] = None,
        team_id: str = "",
    ):
        self.config = config or GMAIConfig()
        self.team_id = team_id
        self.state = GMState(team_id=team_id)

    def determine_philosophy(
        self,
        recent_wins: int,
        avg_roster_age: float,
        cap_situation: str,  # "GOOD", "TIGHT", "OVER"
        draft_capital: int,
    ) -> TeamPhilosophy:
        """
        Determine team-building philosophy based on situation.
        """
        # Playoff contender stays in win-now
        if recent_wins >= self.config.playoff_contender_wins:
            return TeamPhilosophy.WIN_NOW

        # Bad team with young roster develops
        if recent_wins <= self.config.rebuild_trigger_wins:
            if avg_roster_age < 26:
                return TeamPhilosophy.DEVELOP
            return TeamPhilosophy.REBUILD

        # Middle teams are balanced
        return TeamPhilosophy.BALANCED

    def evaluate_trade(
        self,
        giving: List[Tuple[TradeAssetType, Any]],
        receiving: List[Tuple[TradeAssetType, Any]],
    ) -> Tuple[bool, float]:
        """
        Evaluate a potential trade.

        Returns:
            Tuple of (should_accept, net_value)
        """
        giving_value = sum(self._value_asset(t, a) for t, a in giving)
        receiving_value = sum(self._value_asset(t, a) for t, a in receiving)

        net = receiving_value - giving_value

        # Philosophy affects threshold
        if self.state.philosophy == TeamPhilosophy.WIN_NOW:
            # Accept slightly losing trades for win-now pieces
            threshold = -50
        elif self.state.philosophy == TeamPhilosophy.REBUILD:
            # Need to clearly win trades
            threshold = 100
        else:
            threshold = 0

        return net >= threshold, net

    def _value_asset(
        self,
        asset_type: TradeAssetType,
        asset: Any,
    ) -> float:
        """Calculate value of a trade asset."""
        if asset_type == TradeAssetType.DRAFT_PICK:
            pick: DraftPick = asset
            return pick.approximate_value

        elif asset_type == TradeAssetType.PLAYER:
            # Simplified player valuation
            player = asset
            age = player.get("age", 26)
            rating = player.get("overall", 75)
            contract_years = player.get("contract_years", 2)

            base_value = (rating - 60) * 30

            # Age modifier
            if age < 25:
                base_value *= self.config.young_player_premium
            elif age > 30:
                base_value *= self.config.veteran_discount

            # Contract value
            if contract_years > 0:
                base_value *= min(1.2, 1 + contract_years * 0.05)

            return max(0, base_value)

        return 0

    def rank_draft_prospects(
        self,
        prospects: List[Dict[str, Any]],
        team_needs: List[RosterNeed],
    ) -> List[Dict[str, Any]]:
        """
        Rank draft prospects based on value and fit.
        """
        need_positions = {n.position: n.priority for n in team_needs}

        def score_prospect(p: Dict) -> float:
            base = p.get("grade", 50)

            # Need bonus
            pos = p.get("position", "")
            if pos in need_positions:
                priority = need_positions[pos]
                if priority == NeedPriority.CRITICAL:
                    base += 15
                elif priority == NeedPriority.HIGH:
                    base += 8
                elif priority == NeedPriority.MODERATE:
                    base += 3

            # Age bonus (younger is better)
            age = p.get("age", 22)
            if age < 22:
                base += 5
            elif age > 23:
                base -= 2

            return base

        return sorted(prospects, key=score_prospect, reverse=True)

    def generate_actions(self) -> List[GOAPAction]:
        """Generate available GOAP actions based on current state."""
        actions = []

        # Sign free agent
        if self.state.cap_space > 5_000_000:
            actions.append(GOAPAction(
                name="sign_free_agent",
                preconditions={"has_cap_space": True},
                effects={"filled_need": True, "has_cap_space": False},
                cost=1.0,
            ))

        # Make trade
        if self.state.draft_picks:
            actions.append(GOAPAction(
                name="trade_for_player",
                preconditions={"has_picks": True},
                effects={"acquired_player": True},
                cost=1.5,
            ))

        # Restructure contract
        actions.append(GOAPAction(
            name="restructure_contract",
            preconditions={"has_veteran": True},
            effects={"has_cap_space": True},
            cost=0.5,
        ))

        # Cut player
        actions.append(GOAPAction(
            name="cut_player",
            preconditions={},
            effects={"has_cap_space": True, "dead_money": True},
            cost=2.0,
        ))

        return actions

    def plan(
        self,
        current_state: Dict[str, Any],
        goal_state: Dict[str, Any],
        max_depth: int = 5,
    ) -> List[GOAPAction]:
        """
        Create action plan to reach goal state.

        Uses A* search through action space.
        """
        actions = self.generate_actions()

        # Simple greedy planning (full A* would be more complex)
        plan = []
        state = current_state.copy()

        for _ in range(max_depth):
            # Check if goal reached
            if all(state.get(k) == v for k, v in goal_state.items()):
                break

            # Find best action
            best_action = None
            best_score = float('inf')

            for action in actions:
                if action.can_execute(state):
                    # Score by how many goals it satisfies + cost
                    new_state = action.apply(state)
                    goals_met = sum(
                        1 for k, v in goal_state.items()
                        if new_state.get(k) == v
                    )
                    score = action.cost - goals_met * 2

                    if score < best_score:
                        best_score = score
                        best_action = action

            if best_action:
                plan.append(best_action)
                state = best_action.apply(state)
            else:
                break

        return plan

    def get_recommendation(self) -> Dict[str, Any]:
        """Get GM's recommended next action."""
        # Build goal state based on philosophy
        if self.state.philosophy == TeamPhilosophy.WIN_NOW:
            goal = {"filled_need": True, "acquired_star": True}
        elif self.state.philosophy == TeamPhilosophy.REBUILD:
            goal = {"has_picks": True, "young_core": True}
        else:
            goal = {"roster_balanced": True}

        # Current state
        current = {
            "has_cap_space": self.state.cap_space > 10_000_000,
            "has_picks": len(self.state.draft_picks) >= 7,
            "filled_need": len([n for n in self.state.roster_needs if n.priority == NeedPriority.CRITICAL]) == 0,
        }

        plan = self.plan(current, goal)

        if plan:
            return {
                "action": plan[0].name,
                "philosophy": self.state.philosophy.value,
                "plan_length": len(plan),
            }

        return {"action": "hold", "philosophy": self.state.philosophy.value}
