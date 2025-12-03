import pytest
from unittest.mock import MagicMock, AsyncMock
from app.services.gm_agent import GMAgent
from app.models.player import Player
from app.models.team import Team
from app.models.gm import GM, GMDecision

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_team():
    team = MagicMock(spec=Team)
    team.id = 1
    team.salary_cap_space = 50000000.0
    team.players = []
    team.gm = MagicMock(spec=GM)
    team.gm.id = 1
    team.gm.philosophy = "BALANCED"
    team.gm.aggression = 50
    team.gm.patience = 50
    team.gm.negotiation = 50
    team.gm.scouting = 50
    return team

@pytest.fixture
def gm_agent(mock_db, mock_team):
    mock_db.get.return_value = mock_team
    return GMAgent(mock_db, 1)

@pytest.mark.asyncio
async def test_evaluate_trade_accept(gm_agent, mock_db):
    # Setup players
    p1 = MagicMock(spec=Player)
    p1.id = 101
    p1.overall = 85
    p1.age = 26
    p1.salary = 10000000
    p1.position = "WR"
    p1.last_name = "StarReceiver"

    p2 = MagicMock(spec=Player)
    p2.id = 201
    p2.overall = 80
    p2.age = 28
    p2.salary = 8000000
    p2.position = "CB"
    p2.last_name = "SolidCorner"

    mock_db.get.side_effect = lambda model, id: p1 if id == 101 else (p2 if id == 201 else None)

    # Mock LLM response
    gm_agent._get_llm_trade_opinion = AsyncMock(return_value={"score_modifier": 0, "reasoning": "Neutral"})

    result = await gm_agent.evaluate_trade(
        offered_players_ids=[101],
        requested_players_ids=[201]
    )

    assert result["decision"] == "ACCEPT"
    assert result["score"] > 0

    # Verify decision logging
    mock_db.add.assert_called()
    call_args = mock_db.add.call_args[0][0]
    assert isinstance(call_args, GMDecision)
    assert call_args.decision_type == "TRADE_EVALUATION"
    assert call_args.outcome == "ACCEPT"

@pytest.mark.asyncio
async def test_evaluate_trade_reject_financial(gm_agent, mock_db, mock_team):
    mock_team.salary_cap_space = 1000000 # Low cap space

    p1 = MagicMock(spec=Player)
    p1.id = 101
    p1.salary = 20000000 # Expensive

    p2 = MagicMock(spec=Player)
    p2.id = 201
    p2.salary = 5000000 # Cheap

    mock_db.get.side_effect = lambda model, id: p1 if id == 101 else (p2 if id == 201 else None)

    result = await gm_agent.evaluate_trade(
        offered_players_ids=[101],
        requested_players_ids=[201]
    )

    assert result["decision"] == "REJECT"
    assert "Cannot afford trade" in result["reasoning"]

    # Verify decision logging
    mock_db.add.assert_called()
    call_args = mock_db.add.call_args[0][0]
    assert isinstance(call_args, GMDecision)
    assert call_args.outcome == "REJECT"

def test_negotiate_contract(gm_agent, mock_db):
    player = MagicMock(spec=Player)
    demand = 10000000

    result = gm_agent.negotiate_contract(player, demand)

    assert 9000000 <= result["counter_offer"] <= 11000000

    # Verify decision logging
    mock_db.add.assert_called()
    call_args = mock_db.add.call_args[0][0]
    assert isinstance(call_args, GMDecision)
    assert call_args.decision_type == "CONTRACT_NEGOTIATION"

def test_generate_trade_proposal(gm_agent, mock_db):
    # Mock finding a player
    target_player = MagicMock(spec=Player)
    target_player.id = 301
    target_player.team_id = 2
    target_player.position = "QB"
    target_player.overall = 75
    target_player.age = 25
    target_player.salary = 5000000

    # Mock DB execute result
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [target_player]
    mock_db.execute.return_value = mock_result

    # Force need for QB
    gm_agent.team.players = [] # No players means high need for everything

    proposal = gm_agent.generate_trade_proposal(target_position="QB")

    assert proposal["target_team_id"] == 2
    assert proposal["requested_players"] == [301]

    # Verify decision logging
    mock_db.add.assert_called()
    call_args = mock_db.add.call_args[0][0]
    assert isinstance(call_args, GMDecision)
    assert call_args.decision_type == "TRADE_PROPOSAL"
