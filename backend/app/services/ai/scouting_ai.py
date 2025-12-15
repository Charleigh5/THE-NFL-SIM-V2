"""
Scouting AI Service
====================
AI-powered scouting report and player backstory generation.

Uses Gemini 2.5 Pro for rich narrative content with structured JSON output.
Provides fallback templates when AI is unavailable.
Includes in-memory caching for performance optimization.
"""

import logging
from typing import Optional, List, Dict, Tuple, Any
from datetime import datetime
from functools import lru_cache

from app.schemas.scouting import ScoutingReportAI, PlayerBackstory  # type: ignore[import-not-found]
from app.services.ai.gemini_client import get_gemini_client  # type: ignore[import-not-found]

logger = logging.getLogger(__name__)


# In-memory cache for reports (cleared on season/game advance)
_report_cache: Dict[Tuple[str, str, int], ScoutingReportAI] = {}
_backstory_cache: Dict[Tuple[str, str], PlayerBackstory] = {}


class ScoutingAIService:
    """
    Generates AI-powered scouting reports and player backstories.

    Features:
    - Structured JSON output via Gemini 2.5 Pro
    - Position-specific evaluation criteria
    - Team need analysis for draft fit
    - Graceful fallback to templates when AI unavailable
    - In-memory caching for performance
    """

    def __init__(self):
        self.client = get_gemini_client()

    async def generate_scouting_report(
        self,
        player_name: str,
        position: str,
        overall_rating: int,
        college: Optional[str] = None,
        attributes: Optional[dict] = None,
        team_needs: Optional[List[str]] = None,
        use_cache: bool = True
    ) -> ScoutingReportAI:
        """
        Generate an AI-powered scouting report for a draft prospect.

        Args:
            player_name: Full name of the player
            position: Position (e.g., "QB", "WR", "CB")
            overall_rating: Player's overall rating (0-99)
            college: College program (optional)
            attributes: Dict of player attributes for analysis
            team_needs: List of team positional needs for fit analysis
            use_cache: Whether to use cached results (default True)

        Returns:
            ScoutingReportAI with AI-generated content
        """
        # Check cache first
        cache_key = (player_name, position, overall_rating)
        if use_cache and cache_key in _report_cache:
            logger.debug(f"Cache hit for scouting report: {player_name}")
            return _report_cache[cache_key]

        # Build prompt with player context
        prompt = self._build_scouting_prompt(
            player_name, position, overall_rating, college, attributes, team_needs
        )

        # Try AI generation
        if self.client.is_available:
            result = await self.client.generate_with_retry(
                prompt=prompt,
                response_schema=ScoutingReportAI,
                max_retries=2,
                temperature=0.8
            )
            if result:
                # Cache the result
                _report_cache[cache_key] = result
                return result

        # Fallback to template
        logger.info(f"Using fallback template for {player_name}")
        report = self._generate_fallback_report(
            player_name, position, overall_rating, team_needs
        )
        # Cache fallback too
        _report_cache[cache_key] = report
        return report

    def _build_scouting_prompt(
        self,
        player_name: str,
        position: str,
        overall_rating: int,
        college: Optional[str],
        attributes: Optional[dict],
        team_needs: Optional[List[str]]
    ) -> str:
        """Build the prompt for scouting report generation."""

        # Position-specific evaluation criteria
        position_criteria = self._get_position_criteria(position)

        # Format attributes if available
        attr_text = ""
        if attributes:
            key_attrs = self._get_key_attributes(position, attributes)
            attr_text = f"Key attributes: {', '.join(f'{k}: {v}' for k, v in key_attrs.items())}\n"

        # Format team needs
        needs_text = ""
        if team_needs:
            needs_text = f"Team positional needs: {', '.join(team_needs)}\n"

        return f"""You are an NFL scout writing a professional scouting report.

Generate a detailed scouting report for this draft prospect:

Player: {player_name}
Position: {position}
Overall Rating: {overall_rating}/99
College: {college or "Unknown"}
{attr_text}{needs_text}

Evaluation criteria for {position}: {position_criteria}

Write a professional NFL-style scouting report. Be specific about:
- What makes this player special or concerning
- Realistic NFL comparisons based on playing style
- How they would fit a team's scheme
- Honest assessment of ceiling/floor

Use vivid language like a real scout would. Include specific plays or tendencies.
"""

    def _get_position_criteria(self, position: str) -> str:
        """Get position-specific evaluation criteria."""
        criteria = {
            "QB": "arm strength, accuracy, pocket presence, decision-making, mobility, leadership",
            "RB": "vision, burst, contact balance, pass protection, receiving ability, durability",
            "WR": "route running, separation, hands, contested catches, YAC ability, blocking",
            "TE": "blocking, receiving, versatility, athleticism, red zone threat",
            "OT": "pass protection, run blocking, footwork, anchor, recovery speed",
            "OG": "run blocking, pass protection, pulling ability, power, technique",
            "C": "snap accuracy, football IQ, communication, blocking, mobility",
            "DE": "pass rush moves, speed to power, run defense, motor, bend",
            "DT": "gap penetration, anchor, power, technique, stamina",
            "LB": "coverage, tackling, blitz ability, instincts, sideline-to-sideline speed",
            "CB": "coverage, ball skills, press technique, tackling, recovery speed",
            "S": "range, tackling, coverage versatility, instincts, communication",
            "K": "leg strength, accuracy, clutch performance, consistency",
            "P": "hangtime, directional kicking, consistency, coverage ability"
        }
        return criteria.get(position, "overall athleticism, technique, football IQ")

    def _get_key_attributes(self, position: str, attributes: dict) -> dict:
        """Get the most relevant attributes for a position."""
        position_attrs = {
            "QB": ["throw_power", "throw_accuracy_mid", "awareness", "speed"],
            "RB": ["speed", "agility", "strength", "catching"],
            "WR": ["speed", "route_running", "catching", "release"],
            "TE": ["catching", "run_block", "speed", "strength"],
            "OT": ["pass_block", "run_block", "strength", "awareness"],
            "OG": ["pass_block", "run_block", "strength", "pull_speed"],
            "C": ["pass_block", "run_block", "awareness", "anchor"],
            "DE": ["pass_rush_power", "pass_rush_finesse", "speed", "strength"],
            "DT": ["block_shed", "strength", "tackle", "gap_integrity"],
            "LB": ["tackle", "man_coverage", "zone_coverage", "speed"],
            "CB": ["man_coverage", "zone_coverage", "speed", "press"],
            "S": ["zone_coverage", "tackle", "speed", "awareness"],
            "K": ["kick_power", "kick_accuracy"],
            "P": ["kick_power", "hang_time", "coffin_corner"]
        }

        keys = position_attrs.get(position, ["overall_rating", "speed", "strength"])
        return {k: attributes.get(k, "N/A") for k in keys if k in attributes}

    def _generate_fallback_report(
        self,
        player_name: str,
        position: str,
        overall_rating: int,
        team_needs: Optional[List[str]]
    ) -> ScoutingReportAI:
        """Generate a template-based fallback when AI is unavailable."""

        # Determine grade based on overall rating
        if overall_rating >= 90:
            grade = "A"
            ceiling = "All-Pro caliber starter"
            floor = "Solid starter with Pro Bowl potential"
        elif overall_rating >= 80:
            grade = "B+"
            ceiling = "Pro Bowl caliber"
            floor = "Quality starter"
        elif overall_rating >= 70:
            grade = "B"
            ceiling = "Quality starter"
            floor = "Rotational player with starter potential"
        elif overall_rating >= 60:
            grade = "C+"
            ceiling = "Rotational contributor"
            floor = "Practice squad candidate"
        else:
            grade = "C"
            ceiling = "Roster depth"
            floor = "Practice squad"

        # Check fit
        fit_text = "Good scheme fit for most teams."
        if team_needs and position in team_needs:
            fit_text = f"Excellent fit - addresses a critical need at {position}."

        return ScoutingReportAI(
            summary=f"{player_name} is a {position} prospect with {overall_rating} overall rating. Shows promise in key areas for the position.",
            strengths=["Solid fundamentals", "Good athletic profile", "Coachable"],
            weaknesses=["Needs more experience", "Technique refinement needed"],
            nfl_comparison=f"Projects as a similar style to typical NFL {position}",
            ceiling_projection=ceiling,
            floor_projection=floor,
            draft_grade=grade,
            fit_analysis=fit_text
        )

    async def generate_backstory(
        self,
        player_name: str,
        position: str,
        college: Optional[str] = None,
        use_cache: bool = True
    ) -> PlayerBackstory:
        """
        Generate an AI-powered biographical backstory for a player.

        Args:
            player_name: Full name of the player
            position: Position (e.g., "QB", "WR")
            college: College program (optional)
            use_cache: Whether to use cached results (default True)

        Returns:
            PlayerBackstory with AI-generated content
        """
        # Check cache first
        cache_key = (player_name, position)
        if use_cache and cache_key in _backstory_cache:
            logger.debug(f"Cache hit for backstory: {player_name}")
            return _backstory_cache[cache_key]

        prompt = f"""You are a sports journalist writing a player profile.

Generate a compelling biographical backstory for this football player:

Player: {player_name}
Position: {position}
College: {college or "Unknown"}

Create a realistic and engaging backstory including:
- Hometown and upbringing
- How they got into football
- Personality and character traits
- What motivates them
- Any adversity or challenges they've overcome
- Notable college moments

Make it feel authentic and human. Avoid clichés.
"""

        if self.client.is_available:
            result = await self.client.generate_with_retry(
                prompt=prompt,
                response_schema=PlayerBackstory,
                max_retries=2,
                temperature=0.9
            )
            if result:
                _backstory_cache[cache_key] = result
                return result

        # Fallback
        backstory = self._generate_fallback_backstory(player_name, position, college)
        _backstory_cache[cache_key] = backstory
        return backstory

    def _generate_fallback_backstory(
        self,
        player_name: str,
        position: str,
        college: Optional[str]
    ) -> PlayerBackstory:
        """Generate template-based backstory when AI unavailable."""

        return PlayerBackstory(
            hometown="Houston, Texas",
            background=f"{player_name} grew up with a passion for football, starting at age 8 in youth leagues. After a standout high school career, they earned a scholarship to {college or 'a D1 program'} where they developed into a pro prospect.",
            personality_traits=["Competitive", "Team player", "Hard worker"],
            motivations="Inspired by family support and a desire to reach the highest level of competition.",
            notable_college_moments=["Conference championship game winner"],
            adversity_overcome=None
        )


# Singleton instance
_service_instance: Optional[ScoutingAIService] = None


def get_scouting_ai_service() -> ScoutingAIService:
    """Get singleton instance of ScoutingAIService."""
    global _service_instance
    if _service_instance is None:
        _service_instance = ScoutingAIService()
    return _service_instance


def clear_scouting_cache() -> Dict[str, int]:
    """
    Clear all cached scouting reports and backstories.

    Should be called when advancing seasons or loading new game.

    Returns:
        Dict with count of cleared items per cache type
    """
    global _report_cache, _backstory_cache

    report_count = len(_report_cache)
    backstory_count = len(_backstory_cache)

    _report_cache.clear()
    _backstory_cache.clear()

    logger.info(f"Cleared scouting cache: {report_count} reports, {backstory_count} backstories")

    return {
        "reports_cleared": report_count,
        "backstories_cleared": backstory_count
    }
