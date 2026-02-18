
from unittest.mock import patch

import polars as pl

from app.services.nflverse_service import NflverseService, calculate_age

# Mock data
MOCK_ROSTERS = pl.DataFrame({
    "gsis_id": ["00-12345", "00-67890"],
    "first_name": ["John", "Jane"],
    "last_name": ["Doe", "Smith"],
    "position": ["QB", "WR"],
    "team": ["KC", "BUF"],
    "birth_date": ["1995-01-01", "1998-05-15"],
    "height": [74, 70],
    "weight": [225, 190],
    "years_exp": [5, 2],
    "jersey_number": [15, 14],
    "college": ["Texas Tech", "Maryland"]
})

MOCK_CONTRACTS = pl.DataFrame({
    "gsis_id": ["00-12345"],
    "apy": [45000000.0],
    "years": [10],
    "year_signed": [2020]
})

MOCK_NGS = pl.DataFrame({
    "player_gsis_id": ["00-12345", "00-67890"],
    "season": [2024, 2024],
    "week": [1, 1],
    "avg_time_to_throw": [2.5, None],
    "avg_separation": [None, 3.5]
})

MOCK_STATS = pl.DataFrame({
    "player_id": ["00-12345", "00-67890"],
    "passing_yards": [300, 0],
    "receiving_yards": [0, 100]
})

def test_calculate_age():
    assert calculate_age("1995-01-01") >= 29
    assert calculate_age(None) == 25
    assert calculate_age("invalid") == 25

@patch("app.services.nflverse_service.nfl")
def test_import_rosters(mock_nfl):
    mock_nfl.load_rosters.return_value = MOCK_ROSTERS
    service = NflverseService()
    df = service.import_rosters()
    assert isinstance(df, pl.DataFrame)
    assert len(df) == 2
    mock_nfl.load_rosters.assert_called_once()

@patch("app.services.nflverse_service.nfl")
def test_enrichment_logic(mock_nfl):
    # Setup mocks
    mock_nfl.load_rosters.return_value = MOCK_ROSTERS
    mock_nfl.load_contracts.return_value = MOCK_CONTRACTS
    mock_nfl.load_combine.return_value = pl.DataFrame() # Empty combine
    mock_nfl.load_nextgen_stats.return_value = MOCK_NGS
    mock_nfl.load_player_stats.return_value = MOCK_STATS

    service = NflverseService()
    players = service.get_all_active_players()

    assert len(players) == 2

    # Check QB Enrichment (John Doe)
    qb = next(p for p in players if p["gsis_id"] == "00-12345")
    assert qb["contract_years"] == 10
    assert qb["contract_salary"] == 45000000
    assert qb["ngs"]["avg_time_to_throw"] == 2.5
    assert qb["stats"]["passing_yards"] == 300

    # Check WR Enrichment (Jane Smith) - No contract
    wr = next(p for p in players if p["gsis_id"] == "00-67890")
    assert "contract_years" not in wr or wr.get("contract_years") == 1 # Depending on implementation default
    assert wr["ngs"]["avg_separation"] == 3.5
