"""
Manual test script for Draft Assistant recommendation quality.
Tests the draft recommendation system with various scenarios.
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.services.draft_assistant import DraftAssistant
from app.models.player import Player
from app.models.team import Team
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_draft_recommendation_quality():
    """Test draft recommendation quality with realistic scenarios."""

    logger.info("=" * 80)
    logger.info("DRAFT ASSISTANT RECOMMENDATION QUALITY TEST")
    logger.info("=" * 80)

    assistant = DraftAssistant()

    async with AsyncSessionLocal() as db:
        # Scenario 1: Team with critical QB need
        logger.info("\n📋 Scenario 1: Team with critical QB need")
        logger.info("-" * 80)

        # Find a team
        team_stmt = select(Team).limit(1)
        result = await db.execute(team_stmt)
        team = result.scalar_one_or_none()

        if not team:
            logger.error("No teams found in database")
            return

        # Get available QB prospects
        players_stmt = select(Player).where(
            Player.team_id.is_(None),
            Player.position == "QB"
        ).order_by(Player.overall_rating.desc()).limit(5)

        result = await db.execute(players_stmt)
        qb_prospects = result.scalars().all()

        if not qb_prospects:
            logger.warning("No QB prospects found")
            return

        available_ids = [p.id for p in qb_prospects]

        try:
            suggestion = await assistant.suggest_pick(
                team_id=team.id,
                pick_number=1,
                available_players=available_ids,
                db=db,
                include_historical_data=True
            )

            logger.info(f"✅ Recommendation: {suggestion.player_name} ({suggestion.position})")
            logger.info(f"   Overall Rating: {suggestion.overall_rating}")
            logger.info(f"   Confidence: {suggestion.confidence_score:.2%}")
            logger.info(f"   Draft Value Score: {suggestion.draft_value_score}/10")
            logger.info(f"   Reasoning: {suggestion.reasoning}")
            logger.info(f"   MCP Data Used: {'Yes' if suggestion.mcp_data_used else 'No'}")

            if suggestion.historical_comparison:
                logger.info(f"   Historical Comp: {suggestion.historical_comparison.comparable_player_name}")
                logger.info(f"   Similarity: {suggestion.historical_comparison.similarity_score:.0%}")

            logger.info(f"\n📊 Team Needs Analysis:")
            top_needs = sorted(suggestion.team_needs.items(), key=lambda x: x[1], reverse=True)[:5]
            for pos, need in top_needs:
                logger.info(f"   {pos}: {need:.1%} priority")

            if suggestion.roster_gap_analysis:
                logger.info(f"\n🎯 Critical Roster Gaps:")
                critical_gaps = [g for g in suggestion.roster_gap_analysis if g.priority_level in ["CRITICAL", "HIGH"]]
                for gap in critical_gaps[:5]:
                    logger.info(f"   {gap.position}: {gap.current_count}/{gap.target_count} ({gap.priority_level})")

            logger.info(f"\n🔄 Alternative Picks:")
            for i, alt in enumerate(suggestion.alternative_picks, 1):
                logger.info(f"   {i}. {alt.player_name} ({alt.position}) - {alt.overall_rating} OVR")
                logger.info(f"      {alt.reasoning}")

        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}", exc_info=True)
            return

        # Scenario 2: Late round pick
        logger.info("\n" + "=" * 80)
        logger.info("📋 Scenario 2: Late round value pick (Pick #200)")
        logger.info("-" * 80)

        # Get lower-rated prospects
        late_stmt = select(Player).where(
            Player.team_id.is_(None),
            Player.overall_rating < 75
        ).order_by(Player.overall_rating.desc()).limit(10)

        result = await db.execute(late_stmt)
        late_prospects = result.scalars().all()

        if late_prospects:
            late_ids = [p.id for p in late_prospects]

            try:
                late_suggestion = await assistant.suggest_pick(
                    team_id=team.id,
                    pick_number=200,
                    available_players=late_ids,
                    db=db,
                    include_historical_data=False
                )

                logger.info(f"✅ Late Round Gem: {late_suggestion.player_name}")
                logger.info(f"   Overall Rating: {late_suggestion.overall_rating}")
                logger.info(f"   Draft Value Score: {late_suggestion.draft_value_score}/10")
                logger.info(f"   {late_suggestion.reasoning}")

                if late_suggestion.draft_value_score and late_suggestion.draft_value_score >= 7.0:
                    logger.info("   💎 EXCELLENT VALUE - Potential steal!")

            except Exception as e:
                logger.error(f"❌ Late round test failed: {str(e)}")

        # Scenario 3: Compare first round vs later rounds
        logger.info("\n" + "=" * 80)
        logger.info("📊 Value Comparison: Same Players at Different Picks")
        logger.info("-" * 80)

        # Get a high-quality player
        comp_stmt = select(Player).where(
            Player.team_id.is_(None),
            Player.overall_rating >= 80
        ).limit(1)

        result = await db.execute(comp_stmt)
        comp_player = result.scalar_one_or_none()

        if comp_player:
            logger.info(f"\nPlayer: {comp_player.first_name} {comp_player.last_name} ({comp_player.overall_rating} OVR)")

            for pick_num in [1, 32, 100, 224]:
                try:
                    comp_suggestion = await assistant.suggest_pick(
                        team_id=team.id,
                        pick_number=pick_num,
                        available_players=[comp_player.id],
                        db=db,
                        include_historical_data=False
                    )

                    logger.info(f"   Pick #{pick_num:3d}: Value Score = {comp_suggestion.draft_value_score:.1f}/10")

                except Exception as e:
                    logger.error(f"   Pick #{pick_num}: Error - {str(e)}")

        logger.info("\n" + "=" * 80)
        logger.info("✅ Draft Assistant Quality Test Complete!")
        logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_draft_recommendation_quality())
