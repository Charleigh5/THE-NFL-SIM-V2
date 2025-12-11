from app.kernels.core.ecs_manager import Component
from typing import List, Dict, ClassVar
from pydantic import Field

class NemesisSys(Component):
    """
    Nemesis System - Directive 4

    NFL Identity Blueprint Enhancement:
    Games decided by ≤3 points auto-renew rivalries with incremental aggression boost.
    """
    # Directive 4: Nemesis System
    rivalries: Dict[str, List[str]] = {} # TeamID -> List[RivalTeamIDs]
    aggression_modifiers: Dict[str, float] = {} # MatchupKey -> Multiplier
    rivalry_intensities: Dict[str, float] = {} # MatchupKey -> Intensity (0-100)

    # NFL Identity Blueprint: Close game threshold (ClassVar to prevent Pydantic field detection)
    CLOSE_GAME_THRESHOLD: ClassVar[int] = 3  # Points
    INTENSITY_BOOST_PER_THRILLER: ClassVar[float] = 10.0
    MAX_INTENSITY: ClassVar[float] = 100.0
    DECAY_PER_SEASON: ClassVar[float] = 5.0

    def register_rivalry(self, team_a: str, team_b: str):
        if team_a not in self.rivalries: self.rivalries[team_a] = []
        if team_b not in self.rivalries[team_a]:
            self.rivalries[team_a].append(team_b)

        key = self._get_matchup_key(team_a, team_b)
        self.aggression_modifiers[key] = 1.5 # 50% more aggression/penalties
        if key not in self.rivalry_intensities:
            self.rivalry_intensities[key] = 50.0  # Base intensity

    def is_rivalry_game(self, team_a: str, team_b: str) -> bool:
        return team_b in self.rivalries.get(team_a, [])

    def check_rivalry_trigger(self, team_a: str, team_b: str, score_diff: int) -> bool:
        """
        NFL Identity Blueprint: Check if a close game should trigger/renew rivalry.

        Args:
            team_a: First team identifier
            team_b: Second team identifier
            score_diff: Absolute score difference

        Returns:
            True if rivalry was triggered/renewed
        """
        if score_diff <= self.CLOSE_GAME_THRESHOLD:
            self._boost_rivalry(team_a, team_b)
            return True
        return False

    def get_rivalry_intensity(self, team_a: str, team_b: str) -> float:
        """Get cumulative rivalry intensity (0-100)."""
        key = self._get_matchup_key(team_a, team_b)
        return self.rivalry_intensities.get(key, 0.0)

    def get_aggression_modifier(self, team_a: str, team_b: str) -> float:
        """Get aggression modifier for a matchup."""
        key = self._get_matchup_key(team_a, team_b)
        return self.aggression_modifiers.get(key, 1.0)

    def _boost_rivalry(self, team_a: str, team_b: str):
        """Boost rivalry intensity after a close game."""
        key = self._get_matchup_key(team_a, team_b)

        # Initialize if new rivalry
        if key not in self.rivalry_intensities:
            self.rivalry_intensities[key] = 0.0
            self.register_rivalry(team_a, team_b)

        # Boost intensity
        current = self.rivalry_intensities[key]
        self.rivalry_intensities[key] = min(
            self.MAX_INTENSITY,
            current + self.INTENSITY_BOOST_PER_THRILLER
        )

        # Boost aggression modifier slightly
        current_agg = self.aggression_modifiers.get(key, 1.0)
        self.aggression_modifiers[key] = min(2.0, current_agg + 0.1)

    def decay_rivalries(self):
        """Decay all rivalry intensities at end of season."""
        for key in list(self.rivalry_intensities.keys()):
            self.rivalry_intensities[key] = max(
                0.0,
                self.rivalry_intensities[key] - self.DECAY_PER_SEASON
            )
            # Remove dead rivalries
            if self.rivalry_intensities[key] <= 0:
                del self.rivalry_intensities[key]
                if key in self.aggression_modifiers:
                    del self.aggression_modifiers[key]

    def _get_matchup_key(self, team_a: str, team_b: str) -> str:
        """Generate consistent key for team matchup regardless of order."""
        return str(sorted([team_a, team_b]))

class DirectorAI(Component):
    # Directive 5: LLM Narrative Synthesis
    active_storylines: List[str] = Field(default_factory=list)

    # Directive 9: Contextual Decision Veto
    veto_power_active: bool = True

    def generate_headline(self, event_type: str, context: Dict) -> str:
        """
        Placeholder for LLM Hook.
        """
        if event_type == "UPSET_WIN":
            return f"Underdogs {context['winner']} shock the world against {context['loser']}!"
        return "Breaking News"

    def check_veto(self, decision: str, context: Dict) -> bool:
        """
        Directive 9: Vetoes decisions that break immersion or narrative logic.
        e.g. Cutting a star player after a Super Bowl win.
        """
        if decision == "CUT_PLAYER" and context.get("recent_superbowl_mvp", False):
            return True # VETOED
        return False
