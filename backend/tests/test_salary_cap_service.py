
import pytest
from unittest.mock import MagicMock
from app.services.salary_cap_service import SalaryCapService
from app.models.player import Player
from app.models.team import Team

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
    
    # Mock Queries
    mock_db.query.return_value.filter.return_value.first.return_value = mock_team
    mock_db.query.return_value.filter.return_value.all.return_value = [p1, p2, p3]
    
    # Mock League Average Query (second call to query(Team))
    # We need to handle multiple calls to query()
    # 1. query(Team).filter... -> returns mock_team
    # 2. query(Player).filter... -> returns players
    # 3. query(Team).all() -> returns list of teams
    
    # Configure side effects for query calls
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == Team:
            # Handle filter().first() for getting specific team
            mock_query.filter.return_value.first.return_value = mock_team
            # Handle all() for getting all teams
            mock_query.all.return_value = [mock_team]
        elif model == Player:
            mock_query.filter.return_value.all.return_value = [p1, p2, p3]
        return mock_query
        
    mock_db.query.side_effect = query_side_effect
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
    
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(ValueError, match="Team 999 not found"):
        service.get_team_cap_breakdown(999, 2025)
