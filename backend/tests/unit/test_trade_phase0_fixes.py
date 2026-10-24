"""Unit and API tests for TASK-CTVE-000 (Phase 0: Foundational Bug Fixes & Contract Alignment)."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import select

from app.core.trade_config import trade_config
from app.models.draft import DraftPick
from app.models.gm import GM
from app.models.player import Player, Position
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.trade_offer import TradeOffer
from app.schemas.trade import DraftPickInfo, TradeEvaluationRequest, TradeOfferRequest
from app.services.gm_agent import GMAgent


def test_all_position_enum_members_have_explicit_tier():
    """Every Position enum member must map explicitly to its proper tier and multiplier."""
    all_configured_positions = {
        pos
        for tier_data in trade_config.POSITION_VALUE_TIERS.values()
        for pos in tier_data["positions"]
    }

    for pos in Position:
        assert pos.value in all_configured_positions, (
            f"Position {pos.value} missing from POSITION_VALUE_TIERS"
        )
        # Ensure enum object itself resolves identically to string value
        assert trade_config.get_position_tier(pos) == trade_config.get_position_tier(pos.value)

    # Verify specific tier and multiplier assignments
    assert trade_config.get_position_tier("QB") == "ELITE"
    assert trade_config.get_position_multiplier("QB") == 1.45

    assert trade_config.get_position_tier("DE") == "PREMIUM"
    assert trade_config.get_position_multiplier("DE") == 1.25
    assert trade_config.get_position_tier(Position.DE) == "PREMIUM"

    assert trade_config.get_position_tier("OT") == "PREMIUM"
    assert trade_config.get_position_multiplier("OT") == 1.25
    assert trade_config.get_position_tier(Position.OT) == "PREMIUM"

    assert trade_config.get_position_tier("DT") == "HIGH"
    assert trade_config.get_position_multiplier("DT") == 1.15

    # Verify legacy aliases remain supported
    assert trade_config.get_position_tier("EDGE") == "PREMIUM"
    assert trade_config.get_position_tier("LT") == "PREMIUM"
    assert trade_config.get_position_tier("RT") == "HIGH"
    assert trade_config.get_position_tier("FB") == "DEPTH"
    assert trade_config.get_position_tier("LS") == "DEPTH"


@pytest.mark.asyncio
async def test_gm_agent_evaluate_trade_rounds_score_and_respects_log_decision_flag():
    """evaluate_trade must round score to 1 decimal place and skip DB logging when log_decision=False."""
    mock_db = MagicMock()
    mock_team = MagicMock(spec=Team)
    mock_team.id = 1
    mock_team.salary_cap_space = 50_000_000.0
    mock_team.players = []
    mock_team.gm = MagicMock(spec=GM)
    mock_team.gm.id = 1
    mock_team.gm.philosophy = "BALANCED"
    mock_team.gm.aggression = 50
    mock_team.gm.patience = 50
    mock_team.gm.negotiation = 50
    mock_team.gm.scouting = 50

    p1 = MagicMock(spec=Player)
    p1.id = 101
    p1.overall_rating = 87
    p1.age = 25
    p1.contract_salary = 9_000_000
    p1.contract_years = 3
    p1.position = "DE"
    p1.last_name = "PassRusher"

    p2 = MagicMock(spec=Player)
    p2.id = 201
    p2.overall_rating = 79
    p2.age = 29
    p2.contract_salary = 8_000_000
    p2.contract_years = 2
    p2.position = "OG"
    p2.last_name = "Guard"

    def get_side_effect(model, obj_id):
        if model is Team and obj_id == 1:
            return mock_team
        if model is Player and obj_id == 101:
            return p1
        if model is Player and obj_id == 201:
            return p2
        return None

    mock_db.get.side_effect = get_side_effect
    gm_agent = GMAgent(mock_db, 1, seed=42)
    gm_agent._get_llm_trade_opinion = AsyncMock(
        return_value={"score_modifier": 0.123456, "reasoning": "Slight boost"}
    )

    result_no_log = await gm_agent.evaluate_trade(
        offered_players_ids=[101],
        requested_players_ids=[201],
        log_decision=False,
    )

    assert result_no_log["score"] == round(result_no_log["score"], 1)
    # Check that precision does not have unrounded float tail like .123456
    assert len(str(result_no_log["score"]).split(".")[-1]) <= 1
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()

    # Now with default log_decision=True
    result_logged = await gm_agent.evaluate_trade(
        offered_players_ids=[101],
        requested_players_ids=[201],
    )
    assert result_logged["score"] == round(result_logged["score"], 1)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_submit_pick_only_trade_offer_with_offering_team_id(
    async_client, async_db_session, sample_teams
):
    """Pick-only trade offers using offering_team_id must succeed and preserve pick metadata."""
    # Schema validation checks
    pick_info = DraftPickInfo(id=42, round=1, year=2035, original_team_id=1)
    assert pick_info.id == 42
    assert pick_info.year == 2035

    eval_req = TradeEvaluationRequest(
        offering_team_id=1,
        target_team_id=2,
        offered_picks=[pick_info],
        requested_picks=[DraftPickInfo(round=2, year=2026)],
    )
    assert eval_req.offering_team_id == 1

    offer_req = TradeOfferRequest(
        offering_team_id=1,
        target_team_id=2,
        offered_picks=[pick_info],
        requested_picks=[DraftPickInfo(round=2, year=2026)],
    )
    assert offer_req.offering_team_id == 1

    response = await async_client.post(
        "/api/trades/offer",
        json={
            "offering_team_id": 1,
            "target_team_id": 2,
            "offered_player_ids": [],
            "requested_player_ids": [],
            "offered_picks": [{"id": 10, "round": 1, "year": 2026, "original_team_id": 1}],
            "requested_picks": [{"id": 20, "round": 2, "year": 2026, "original_team_id": 2}],
            "message": "Pick swap proposal",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING"
    offer_id = data["offer_id"]

    stmt = select(TradeOffer).where(TradeOffer.id == offer_id)
    offer = (await async_db_session.execute(stmt)).scalar_one()
    assert offer.offering_team_id == 1
    assert offer.receiving_team_id == 2
    assert offer.offered_picks[0]["id"] == 10
    assert offer.offered_picks[0]["original_team_id"] == 1
    assert offer.requested_picks[0]["id"] == 20
    assert offer.requested_picks[0]["original_team_id"] == 2


@pytest.mark.asyncio
async def test_accept_offer_transfers_draft_pick_ownership_by_id(
    async_client, async_db_session, sample_teams
):
    """Accepting a trade offer must transfer DraftPick.team_id ownership for offered and requested picks."""
    season = Season(id=1, year=2026, current_week=1, is_active=True, status=SeasonStatus.REGULAR_SEASON)
    async_db_session.add(season)

    pick_team1 = DraftPick(
        id=501,
        season_id=1,
        team_id=1,
        original_team_id=1,
        round=1,
        pick_number=10,
    )
    pick_team2 = DraftPick(
        id=502,
        season_id=1,
        team_id=2,
        original_team_id=2,
        round=2,
        pick_number=42,
    )
    async_db_session.add_all([pick_team1, pick_team2])
    await async_db_session.commit()

    # Submit pick-only trade offer from team 1 to team 2
    offer_resp = await async_client.post(
        "/api/trades/offer",
        json={
            "offering_team_id": 1,
            "target_team_id": 2,
            "offered_player_ids": [],
            "requested_player_ids": [],
            "offered_picks": [{"id": 501, "round": 1, "year": 2026, "original_team_id": 1}],
            "requested_picks": [{"id": 502, "round": 2, "year": 2026, "original_team_id": 2}],
        },
    )
    assert offer_resp.status_code == 200
    offer_id = offer_resp.json()["offer_id"]

    # Accept the trade offer
    respond_resp = await async_client.post(
        f"/api/trades/respond/{offer_id}",
        json={"action": "accept", "message": "Deal!"},
    )
    assert respond_resp.status_code == 200
    assert respond_resp.json()["success"] is True

    # Refresh picks and verify ownership swapped
    await async_db_session.refresh(pick_team1)
    await async_db_session.refresh(pick_team2)
    assert pick_team1.team_id == 2
    assert pick_team1.original_team_id == 1
    assert pick_team2.team_id == 1
    assert pick_team2.original_team_id == 2
