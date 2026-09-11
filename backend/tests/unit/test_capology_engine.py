"""
Unit Tests: Capology Engine & Multi-Year Contract Modeling
==========================================================
Verifies:
1. NFL CBA Article 13 5-year maximum signing bonus proration window.
2. Accelerated dead money allocation upon void year triggering.
3. Post-June 1st two-year dead money split calculation.
4. Appendix V Compensatory Free Agent (CFA) qualification tiers & cancellations.
5. FastAPI endpoints /api/capology/simulate-proposal and /five-year-outlook.
6. Execution latency budget (<40ms ceiling).
"""

import time
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.capology import MultiYearContractProposal
from app.services.capology_engine import CapologyEngine, BASE_LEAGUE_YEAR, BASE_SALARY_CAP


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def cap_engine():
    return CapologyEngine()


def test_standard_three_year_no_void(cap_engine):
    """3-year deal with $15M signing bonus and $5M base salary (0 void years)."""
    proposal = MultiYearContractProposal(
        player_id=101,
        team_id=1,
        real_years=3,
        void_years=0,
        annual_base_salary=5_000_000,
        signing_bonus_total=15_000_000,
        guaranteed_total=20_000_000,
        post_june_1_designation=False,
    )
    res = cap_engine.calculate_multi_year_projection(proposal)

    assert res.proration_years_used == 3
    # Proration = 15M / 3 = 5M/year
    # Year 1 (2026): 5M base + 5M bonus = 10M cap hit
    assert res.yearly_schedule[0].proposed_contract_cap_hit == 10_000_000
    assert res.yearly_schedule[0].dead_money == 0

    # Year 2 (2027): 10M cap hit
    assert res.yearly_schedule[1].proposed_contract_cap_hit == 10_000_000
    assert res.yearly_schedule[1].dead_money == 0

    # Year 3 (2028): 10M cap hit
    assert res.yearly_schedule[2].proposed_contract_cap_hit == 10_000_000
    assert res.yearly_schedule[2].dead_money == 0

    # Year 4 (2029): Contract finished, 0 cap hit, 0 dead money
    assert res.yearly_schedule[3].proposed_contract_cap_hit == 0
    assert res.yearly_schedule[3].dead_money == 0


def test_void_years_acceleration(cap_engine):
    """
    3 real years + 2 void years = 5 proration years.
    $20M signing bonus -> $4M/year proration.
    Years 1-3: $6M base + $4M bonus = $10M cap hit.
    Year 4: Contract voids! Remaining unamortized bonus = 2 years * $4M = $8M dead money.
    """
    proposal = MultiYearContractProposal(
        player_id=102,
        team_id=1,
        real_years=3,
        void_years=2,
        annual_base_salary=6_000_000,
        signing_bonus_total=20_000_000,
        guaranteed_total=25_000_000,
        post_june_1_designation=False,
    )
    res = cap_engine.calculate_multi_year_projection(proposal)

    assert res.proration_years_used == 5
    # Year 1-3 cap hit: 6M + 4M = 10M
    for i in range(3):
        assert res.yearly_schedule[i].proposed_contract_cap_hit == 10_000_000
        assert res.yearly_schedule[i].dead_money == 0

    # Year 4 (2029): 8M accelerated dead money
    assert res.yearly_schedule[3].proposed_contract_cap_hit == 0
    assert res.yearly_schedule[3].dead_money == 8_000_000
    assert res.accelerated_dead_money_void_year == 8_000_000

    # Year 5 (2030): Clean slate
    assert res.yearly_schedule[4].proposed_contract_cap_hit == 0
    assert res.yearly_schedule[4].dead_money == 0


def test_post_june_1_void_split(cap_engine):
    """
    Post-June 1st designation splits the $8M accelerated dead money:
    Year 4: $4M (1 year of proration)
    Year 5: $4M (remaining unamortized balance)
    """
    proposal = MultiYearContractProposal(
        player_id=103,
        team_id=1,
        real_years=3,
        void_years=2,
        annual_base_salary=6_000_000,
        signing_bonus_total=20_000_000,
        guaranteed_total=25_000_000,
        post_june_1_designation=True,
    )
    res = cap_engine.calculate_multi_year_projection(proposal)

    assert res.yearly_schedule[3].dead_money == 4_000_000
    assert res.yearly_schedule[4].dead_money == 4_000_000


def test_five_year_proration_ceiling(cap_engine):
    """Even if proposal attempts more years, proration cannot exceed 5 years."""
    proposal = MultiYearContractProposal(
        player_id=104,
        team_id=1,
        real_years=5,
        void_years=4,  # Sum = 9, must clamp to 5
        annual_base_salary=10_000_000,
        signing_bonus_total=50_000_000,
        guaranteed_total=50_000_000,
    )
    res = cap_engine.calculate_multi_year_projection(proposal)
    assert res.proration_years_used == 5


def test_compensatory_free_agent_qualification(cap_engine):
    """Test CFA qualification thresholds under CBA Appendix V."""
    # Under $3.0M APY: Does not qualify
    low_deal = MultiYearContractProposal(
        player_id=105,
        team_id=1,
        real_years=2,
        annual_base_salary=1_200_000,
        signing_bonus_total=500_000,
    )
    cfa_low = cap_engine.evaluate_comp_pick_formula(low_deal, 1)
    assert cfa_low.qualifies_as_cfa is False
    assert cfa_low.cfa_tier is None
    assert cfa_low.cancelled_pick_round is None

    # $16.0M APY: Round 4 Tier
    mid_deal = MultiYearContractProposal(
        player_id=106,
        team_id=1,
        real_years=3,
        annual_base_salary=12_000_000,
        signing_bonus_total=12_000_000,  # APY = (36M + 12M)/3 = 16M
    )
    cfa_mid = cap_engine.evaluate_comp_pick_formula(mid_deal, 1)
    assert cfa_mid.qualifies_as_cfa is True
    assert cfa_mid.cfa_tier == 4
    assert cfa_mid.cancelled_pick_round == 4
    assert "Round 4 Compensatory Pick" in cfa_mid.projected_comp_picks_lost[0]

    # $25.0M APY: Round 3 Tier
    elite_deal = MultiYearContractProposal(
        player_id=107,
        team_id=1,
        real_years=4,
        annual_base_salary=20_000_000,
        signing_bonus_total=20_000_000,  # APY = (80M + 20M)/4 = 25M
    )
    cfa_elite = cap_engine.evaluate_comp_pick_formula(elite_deal, 1)
    assert cfa_elite.qualifies_as_cfa is True
    assert cfa_elite.cfa_tier == 3
    assert cfa_elite.cancelled_pick_round == 3


def test_api_simulate_proposal_endpoint(client):
    """Verify POST /api/capology/simulate-proposal responds with 200 and correct schema."""
    payload = {
        "player_id": 99,
        "team_id": 1,
        "real_years": 3,
        "void_years": 2,
        "annual_base_salary": 8000000,
        "signing_bonus_total": 15000000,
        "guaranteed_total": 20000000,
        "post_june_1_designation": False,
    }
    response = client.post("/api/capology/simulate-proposal", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["player_id"] == 99
    assert data["proration_years_used"] == 5
    assert len(data["yearly_schedule"]) == 5
    assert data["accelerated_dead_money_void_year"] == 6000000  # 2 years * 3M
    assert "comp_pick_impact" in data
    assert data["comp_pick_impact"]["qualifies_as_cfa"] is True


def test_api_five_year_outlook_endpoint(client):
    """Verify GET /api/capology/teams/1/five-year-outlook responds with 200 and 5 years."""
    response = client.get("/api/capology/teams/1/five-year-outlook")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 5
    for i, item in enumerate(data):
        assert item["year"] == BASE_LEAGUE_YEAR + i
        assert item["projected_cap"] > 0
        assert "net_cap_space" in item


def test_capology_latency_budget(cap_engine):
    """Verify calculate_multi_year_projection executes in under 40ms."""
    proposal = MultiYearContractProposal(
        player_id=1,
        team_id=1,
        real_years=4,
        void_years=1,
        annual_base_salary=15_000_000,
        signing_bonus_total=25_000_000,
        guaranteed_total=30_000_000,
    )
    start_time = time.perf_counter()
    for _ in range(20):
        cap_engine.calculate_multi_year_projection(proposal)
    elapsed = (time.perf_counter() - start_time) / 20.0

    # Strict latency verification: <40ms budget
    assert elapsed < 0.040, f"Capology execution too slow: {elapsed*1000:.2f}ms"
