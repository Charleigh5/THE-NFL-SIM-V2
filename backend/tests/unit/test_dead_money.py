
import pytest
from unittest.mock import MagicMock, Mock
from sqlalchemy.orm import Session
from app.services.salary_cap_service import SalaryCapService
from app.models.dead_cap import DeadCapCharge, DeadCapReason
from app.models.player import Player
from app.models.team import Team
from app.models.season import Season
from app.models.player_contract import PlayerContract

def test_calculate_potential_dead_money():
    # Setup
    mock_db = MagicMock(spec=Session)
    service = SalaryCapService(mock_db)

    player = Player()
    contract = PlayerContract(contract_salary=10000000, contract_years=3)
    player.contract = contract
    player.contract_salary = 10000000 # Helper setter

    # Execute
    dead_money = service.calculate_potential_dead_money(player)

    # Verify - Heuristic is 50% of current salary
    assert dead_money == 5000000

def test_process_dead_money_charge():
    # Setup
    mock_db = MagicMock(spec=Session)
    service = SalaryCapService(mock_db)

    # Execute
    charge = service.process_dead_money_charge(
        team_id=1,
        player_id=101,
        amount=5000000,
        year=2025,
        reason=DeadCapReason.CUT
    )

    # Verify - Check that the charge was created with correct values
    # We inspect the object passed to db.add()
    added_obj = mock_db.add.call_args[0][0]
    assert added_obj.amount == 5000000
    assert added_obj.reason == "CUT"
    mock_db.commit.assert_called_once()

def test_get_team_cap_breakdown_includes_dead_money():
    # Setup
    mock_db = MagicMock(spec=Session)
    service = SalaryCapService(mock_db)

    # Mock Models
    mock_team = Team(id=1, name="Test Team", salary_cap_space=100000000)
    mock_season = Season(id=1, year=2025)

    mock_player = Player(id=10, first_name="Active", last_name="Player", position="QB", team_id=1)
    mock_player.contract = PlayerContract(contract_salary=10000000)

    # Mock Query Returns
    # 1. Team query
    mock_db.execute.return_value.scalar_one_or_none.side_effect = [mock_team, mock_season]

    # 2. Players query
    players_result = MagicMock()
    players_result.scalars.return_value.all.return_value = [mock_player]

    # 3. Dead Money query
    # We need to be careful with side_effects because execute is called multiple times
    # Sequence: Team -> Season -> Players -> Dead Money -> Teams (league avg)

    # Let's rebuild the side_effect chain more robustly
    def mock_execute(stmt):
        s = str(stmt)
        result = MagicMock()
        if "FROM team" in s and "WHERE team.id" in s:
            result.scalar_one_or_none.return_value = mock_team
        elif "FROM season" in s:
            result.scalar_one_or_none.return_value = mock_season
        elif "FROM player" in s:
            result.scalars.return_value.all.return_value = [mock_player]
        elif "FROM dead_cap_charges" in s:
            # Assume query for dead money returns 5M
            result.scalar.return_value = 5000000
        elif "FROM team" in s: # All teams
             result.scalars.return_value.all.return_value = [mock_team]
        return result

    mock_db.execute.side_effect = mock_execute

    # Execute
    breakdown = service.get_team_cap_breakdown(team_id=1, season_id=1)

    # Verify
    assert breakdown["active_cap"] == 10000000
    assert breakdown["dead_money"] == 5000000
    assert breakdown["used_cap"] == 15000000 # 10M active + 5M dead
    # 279,200,000 (2025 Cap) - 15,000,000 = 264,200,000
    assert breakdown["available_cap"] == 264200000
