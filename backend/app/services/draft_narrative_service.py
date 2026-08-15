"""
Draft & Free Agency Narrative Engine (2025 Architecture)
=========================================================
Generates dynamic media reactions, steal/reach analyses, team draft grades,
and free agency storyline articles for the NFL Sim Living League news wire.
"""

from typing import List, Optional, Dict, Any, Tuple
import random
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from datetime import datetime

from app.models.news_item import NewsItem, NewsCategory
from app.models.player import Player
from app.models.team import Team
from app.models.draft import DraftPick
from app.schemas.offseason import FreeAgentSigning


class DraftNarrativeService:
    """
    Analyzes draft picks and free agent transactions to generate immersive,
    dynamic news feed articles and media reactions.
    """

    def __init__(self, db: Session):
        self.db = db

    # =========================================================================
    # DRAFT PICK STORYLINE GENERATION
    # =========================================================================

    def generate_pick_narrative(
        self,
        season_id: int,
        round_num: int,
        pick_number: int,
        team_id: int,
        player_id: int
    ) -> Optional[NewsItem]:
        """
        Evaluate a single draft selection and generate a contextual media reaction.
        """
        player = self.db.get(Player, player_id)
        team = self.db.get(Team, team_id)

        if not player or not team:
            return None

        ovr = player.overall_rating
        pos = player.position if isinstance(player.position, str) else player.position.value
        player_name = f"{player.first_name} {player.last_name}"
        team_name = f"{team.city} {team.name}"

        # Projected slot based on OVR rating (90+ = top 5, 85+ = top 15, 80+ = top 32, 75+ = rd 2-3, etc.)
        projected_slot = self._estimate_consensus_edp(ovr)
        slot_diff = pick_number - projected_slot  # Positive means fell late (Steal), Negative means reached early

        headline: str
        content: str
        importance: float
        is_breaking: bool = False

        if pick_number <= 5:
            importance = 1.0
            is_breaking = True
            headline = f"Cornerstone Selected: {team_name} drafts {player_name} at #{pick_number}"
            content = (
                f"With the #{pick_number} overall pick in the NFL Draft, the {team_name} have secured "
                f"{player_name}, a elite {pos} ({ovr} OVR). Team brass erupted into celebration as the pick was submitted. "
                f"Scouts project {player_name} to be a day-one starter and potential franchise pillar."
            )
        elif slot_diff >= 22 and ovr >= 78:
            # Massive Steal
            importance = 0.85
            headline = f"Draft Steal Alert: {team_name} nabs falling star {player_name} at #{pick_number}"
            content = (
                f"In what analysts are already hailing as one of the best value selections of the draft, "
                f"the {team_name} stopped {player_name}'s slide at pick #{pick_number}. "
                f"The {ovr} OVR {pos} was projected as a consensus top-{projected_slot} prospect and brings immediate elite talent."
            )
        elif slot_diff <= -25 and round_num <= 2:
            # High-profile Reach
            importance = 0.80
            headline = f"War Room Surprise: {team_name} reaches for {player_name} at pick #{pick_number}"
            content = (
                f"The {team_name} raised eyebrows across the league by drafting {player_name} ({pos}, {ovr} OVR) "
                f"early in Round {round_num}. While draft boards rated {player_name} as a developmental project, "
                f"the coaching staff believes his unique physical upside fits their scheme perfectly."
            )
        elif round_num >= 5 and ovr >= 74:
            # Late-round Gem
            importance = 0.70
            headline = f"Day 3 Gem: {team_name} finds intriguing talent in {player_name} (Round {round_num})"
            content = (
                f"Late-round scouting paid off for {team_name} as they scooped up {player_name} ({pos}) in Round {round_num}. "
                f"With a {ovr} overall rating, {player_name} could push for significant rotational snaps this autumn."
            )
        else:
            importance = 0.50
            headline = f"Draft Board: {team_name} selects {player_name} ({pos}) with pick #{pick_number}"
            content = (
                f"The {team_name} addressed their roster depth by choosing {player_name} at pick #{pick_number} (Round {round_num}). "
                f"The {pos} brings steady fundamental grading ({ovr} OVR) to the locker room."
            )

        news = NewsItem(
            season_id=season_id,
            week=0,
            team_id=team.id,
            player_id=player.id,
            category=NewsCategory.DRAFT_NEWS,
            headline=headline,
            content=content,
            importance_score=importance,
            created_at=datetime.utcnow()
        )
        self.db.add(news)
        self.db.commit()
        return news

    def _estimate_consensus_edp(self, ovr: int) -> int:
        """Estimate consensus Expected Draft Position based on OVR."""
        if ovr >= 90:
            return random.randint(1, 5)
        elif ovr >= 85:
            return random.randint(6, 16)
        elif ovr >= 80:
            return random.randint(17, 36)
        elif ovr >= 76:
            return random.randint(37, 70)
        elif ovr >= 72:
            return random.randint(71, 120)
        elif ovr >= 68:
            return random.randint(121, 180)
        return random.randint(181, 224)

    # =========================================================================
    # FREE AGENCY STORYLINE GENERATION
    # =========================================================================

    def generate_free_agency_narratives(
        self,
        season_id: int,
        signings: List[FreeAgentSigning]
    ) -> List[NewsItem]:
        """
        Generate breaking news articles for standout free agency signings.
        """
        news_items: List[NewsItem] = []

        # Sort signings to highlight top deals
        top_signings = sorted(signings, key=lambda s: (s.overall_rating, s.annual_avg), reverse=True)[:10]

        for s in top_signings:
            millions_total = round(s.total_value / 1_000_000, 1)
            millions_aav = round(s.annual_avg / 1_000_000, 1)
            millions_gtd = round(s.guaranteed / 1_000_000, 1)

            if s.overall_rating >= 88 or s.annual_avg >= 20_000_000:
                headline = f"BLOCKBUSTER: {s.team_name} signs superstar {s.player_name} to ${millions_total}M deal"
                content = (
                    f"Free agency kicked off with a massive splash as the {s.team_name} agreed to terms with "
                    f"premier {s.position} {s.player_name} on a {s.contract_years}-year contract worth ${millions_total}M "
                    f"(${millions_aav}M AAV with ${millions_gtd}M guaranteed). "
                    f"{s.player_name} ({s.overall_rating} OVR) chose {s.team_name} over {s.bidding_teams_count - 1} other competing offers."
                )
                importance = 0.95
            elif s.bidding_teams_count >= 5:
                headline = f"Bidding War Won: {s.team_name} lands coveted free agent {s.player_name}"
                content = (
                    f"After an intense multi-team bidding contest involving {s.bidding_teams_count} franchises, "
                    f"the {s.team_name} have officially signed {s.player_name} ({s.position}, {s.overall_rating} OVR) "
                    f"to a {s.contract_years}-year, ${millions_total}M agreement."
                )
                importance = 0.85
            elif s.signing_grade.startswith("A"):
                headline = f"Market Steal: {s.team_name} secures high-value signing in {s.player_name}"
                content = (
                    f"Front office analysts are praising the {s.team_name} for signing {s.player_name} ({s.position}, {s.overall_rating} OVR) "
                    f"to an exceptionally cap-friendly {s.contract_years}-year deal. The signing earned an instant '{s.signing_grade}' grade."
                )
                importance = 0.75
            else:
                headline = f"Roster Wire: {s.team_name} adds veteran {s.position} {s.player_name}"
                content = (
                    f"The {s.team_name} addressed veteran depth by adding {s.player_name} ({s.overall_rating} OVR) "
                    f"on a {s.contract_years}-year, ${millions_total}M contract."
                )
                importance = 0.60

            item = NewsItem(
                season_id=season_id,
                week=0,
                team_id=s.team_id,
                player_id=s.player_id,
                category=NewsCategory.TRANSACTION,
                headline=headline,
                content=content,
                importance_score=importance,
                created_at=datetime.utcnow()
            )
            self.db.add(item)
            news_items.append(item)

        self.db.commit()
        return news_items
