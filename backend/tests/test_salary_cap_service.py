
import pytest
from unittest.mock import MagicMock
from app.services.salary_cap_service import SalaryCapService
from app.models.player import Player
from app.models.team import Team
from sqlalchemy import select

def test_get_team_cap_breakdown():
    # Setup
    mock_db = MagicMock()
    service = SalaryCapService(mock_db)

    # Mock Team
    mock_team = MagicMock(spec=Team)
    mock_team.id = 1
    mock_team.name = "Test Team"
    mock_team.salary_cap_total = 200000000
    mock_team.salary_cap_space = 50000000

    # Mock Players
    p1 = MagicMock(spec=Player)
    p1.id = 101
    p1.first_name = "Joe"
    p1.last_name = "Burrow"
    p1.position = "QB"
    p1.contract_salary = 50000000
    p1.contract_years = 5
    p1.team_id = 1

    p2 = MagicMock(spec=Player)
    p2.id = 102
    p2.first_name = "Ja'Marr"
    p2.last_name = "Chase"
    p2.position = "WR"
    p2.contract_salary = 30000000
    p2.contract_years = 4
    p2.team_id = 1

    p3 = MagicMock(spec=Player)
    p3.id = 103
    p3.first_name = "Trey"
    p3.last_name = "Hendrickson"
    p3.position = "DE"
    p3.contract_salary = 20000000
    p3.contract_years = 2
    p3.team_id = 1

    # Configure side effects for execute calls
    def execute_side_effect(stmt):
        mock_result = MagicMock()
        stmt_str = str(stmt).lower()

        if "from team" in stmt_str:
            if "where team.id" in stmt_str:
                mock_result.scalar_one_or_none.return_value = mock_team
            else:
                mock_result.scalars.return_value.all.return_value = [mock_team]
        elif "from player" in stmt_str:
            mock_result.scalars.return_value.all.return_value = [p1, p2, p3]

        return mock_result

    mock_db.execute.side_effect = execute_side_effect

    result = service.get_team_cap_breakdown(1, 2025)

    # Verify
    assert result["team_id"] == 1
    assert result["team_name"] == "Test Team"
    assert result["total_cap"] == 200000000
    assert result["used_cap"] == 100000000 # 50+30+20
    assert result["cap_percentage"] == 50.0

    # Verify Top Contracts
    assert len(result["top_contracts"]) == 3
    assert result["top_contracts"][0]["name"] == "Joe Burrow"
    assert result["top_contracts"][0]["salary"] == 50000000

    # Verify Position Breakdown
    # QB: 50M, WR/TE: 30M, DL: 20M
    breakdown = result["position_breakdown"]
    assert len(breakdown) == 8 # All groups present

    qb_group = next(g for g in breakdown if g["group"] == "QB")
    assert qb_group["total_salary"] == 50000000
    assert qb_group["percentage"] == 50.0 # 50/100

    wr_group = next(g for g in breakdown if g["group"] == "WR/TE")
    assert wr_group["total_salary"] == 30000000
    assert wr_group["percentage"] == 30.0 # 30/100

def test_get_team_cap_breakdown_team_not_found():
    mock_db = MagicMock()
    service = SalaryCapService(mock_db)

    def execute_side_effect(stmt):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        return mock_result

    mock_db.execute.side_effect = execute_side_effect

    with pytest.raises(ValueError, match="Team 999 not found"):
        service.get_team_cap_breakdown(999, 2025)
