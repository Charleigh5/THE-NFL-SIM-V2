"""
Opponent Film Study & Gameplan Counter-Scheming AI (2026 Production Architecture)
================================================================================
Tier 2 Strategic Reasoning Service for NFL Coaches & Coordinators.
Analyzes opponent tendencies across key downs and formulates synthetic schematic adjustments.

Features:
- Opponent film tendency extraction (Run/Pass ratios on 1st & 10, 3rd & short, 3rd & long)
- Defensive coverage counters (Cover 1 Man, Cover 2 Zone, Cover 3 Match, Cover 4 Quarters, Zero Blitz)
- Offensive tempo & personnel package counters (11 personnel spread, 12 heavy, 21 power)
- Seamless offline deterministic coaching heuristic fallback
"""

import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from app.services.ai.ai_provider import get_ai_registry, AIProviderType

logger = logging.getLogger(__name__)


class OpponentFilmTendency(BaseModel):
    """Statistical tendencies extracted from opponent's recent game tape."""
    opponent_team_name: str
    run_pass_ratio_1st_down: float = Field(0.50, description="Percentage of run plays on 1st & 10 (0.0 - 1.0)")
    blitz_rate_3rd_down: float = Field(0.35, description="Opponent defensive blitz frequency on 3rd down")
    deep_pass_rate: float = Field(0.20, description="Rate of 20+ yard air throw attempts")
    redzone_run_rate: float = Field(0.55, description="Run frequency inside the 20-yard line")
    star_offensive_threat: str = "WR1"
    vulnerable_defensive_zone: str = "Middle Hook / Seam"


class DefensiveSchemeCounter(BaseModel):
    """Defensive schematic counter-measures."""
    primary_coverage: str = "Cover 3 Match"
    blitz_rate_recommended: float = 0.28
    front_alignment: str = "4-3 Over"
    bracket_target: Optional[str] = None
    tactic_rationale: str = "Contain outside zone rush and funnel passes into loaded middle coverage."


class OffensiveGameplanCounter(BaseModel):
    """Offensive schematic counter-measures."""
    primary_concept: str = "West Coast Quick Slants & Mesh"
    run_scheme_focus: str = "Inside Zone / Duo"
    tempo: str = "Balanced No-Huddle"
    target_matchup_advantage: str = "Isolate RB/TE against slow middle linebackers."


class GameplanCounterProposal(BaseModel):
    """Full strategic gameplan proposal for the upcoming game."""
    opponent_team_name: str
    scouting_executive_summary: str
    defensive_counter: DefensiveSchemeCounter
    offensive_counter: OffensiveGameplanCounter
    key_victory_keys: List[str] = Field(default_factory=list)
    confidence_rating: int = Field(85, ge=50, le=99)


class GameplanAIService:
    """
    Tier 2 AI Service providing opponent tape analysis and gameplan counter-scheming.
    """

    def __init__(self):
        self.registry = get_ai_registry()

    async def formulate_gameplan(
        self,
        opponent_name: str,
        tendencies: Optional[OpponentFilmTendency] = None
    ) -> GameplanCounterProposal:
        """
        Synthesizes a tactical gameplan tailored to exploit the opponent's schematic weaknesses.
        """
        if tendencies is None:
            tendencies = OpponentFilmTendency(opponent_team_name=opponent_name)

        provider = self.registry.get_provider()

        prompt = (
            f"You are an elite NFL Defensive and Offensive Coordinator preparing a gameplan against {opponent_name}.\n"
            f"Tape Analytics:\n"
            f"- 1st Down Run Ratio: {tendencies.run_pass_ratio_1st_down * 100:.1f}%\n"
            f"- 3rd Down Blitz Rate: {tendencies.blitz_rate_3rd_down * 100:.1f}%\n"
            f"- Deep Pass Threat Rate: {tendencies.deep_pass_rate * 100:.1f}%\n"
            f"- Star Threat: {tendencies.star_offensive_threat}\n"
            f"- Vulnerability: {tendencies.vulnerable_defensive_zone}\n"
            f"Formulate a complete gameplan with defensive coverage counters, offensive attack concepts, and 3 keys to victory."
        )

        if provider.provider_type != AIProviderType.DETERMINISTIC_FALLBACK and provider.is_available:
            result = await provider.generate_structured(prompt, GameplanCounterProposal)
            if result:
                return result

        # Deterministic Strategic Fallback
        return self._generate_deterministic_gameplan(opponent_name, tendencies)

    def _generate_deterministic_gameplan(
        self,
        opponent_name: str,
        tendencies: OpponentFilmTendency
    ) -> GameplanCounterProposal:
        """Rule-based tactical coaching engine for offline execution."""
        # Determine defensive coverage based on deep pass rate and blitz tendencies
        if tendencies.deep_pass_rate > 0.25:
            coverage = "Cover 4 Quarters"
            def_rationale = f"Opponent attacks deep at {tendencies.deep_pass_rate*100:.0f}%. Two-high safety shell prevents explosive over-the-top touchdowns."
        elif tendencies.run_pass_ratio_1st_down > 0.60:
            coverage = "Cover 1 Robber"
            def_rationale = f"Opponent heavily runs on 1st down ({tendencies.run_pass_ratio_1st_down*100:.0f}%). 8-man box with robber safety stops early-down ground game."
        else:
            coverage = "Cover 3 Match"
            def_rationale = "Balanced zone scheme matching deep verticals while keeping eyes on the backfield."

        # Determine offensive concept based on opponent blitz rate
        if tendencies.blitz_rate_3rd_down > 0.30:
            off_concept = "Quick Hot-Reads, WR Screens & Shallow Cross"
            target_matchup = "Attack vacated hot zones behind blitzing linebackers."
        else:
            off_concept = "Play-Action Bootlegs & Intermediate Digs"
            target_matchup = "Exploit soft zone coverage intermediate hashes."

        return GameplanCounterProposal(
            opponent_team_name=opponent_name,
            scouting_executive_summary=(
                f"Film analysis against {opponent_name} indicates high reliance on {tendencies.star_offensive_threat}. "
                f"Defensively, their soft spot remains {tendencies.vulnerable_defensive_zone}."
            ),
            defensive_counter=DefensiveSchemeCounter(
                primary_coverage=coverage,
                blitz_rate_recommended=0.25 if tendencies.deep_pass_rate > 0.25 else 0.35,
                front_alignment="4-2-5 Nickel",
                bracket_target=tendencies.star_offensive_threat,
                tactic_rationale=def_rationale
            ),
            offensive_counter=OffensiveGameplanCounter(
                primary_concept=off_concept,
                run_scheme_focus="Outside Zone Stretch" if "Middle" in tendencies.vulnerable_defensive_zone else "Duo / Power",
                tempo="Up-Tempo Sugar Huddle",
                target_matchup_advantage=target_matchup
            ),
            key_victory_keys=[
                f"Neutralize {tendencies.star_offensive_threat} with safety bracket leverage on 3rd down.",
                "Win time of possession by sustaining 8+ play drives on early-down runs.",
                f"Target {tendencies.vulnerable_defensive_zone} in 2-minute and redzone situations."
            ],
            confidence_rating=88
        )


gameplan_ai_service = GameplanAIService()
