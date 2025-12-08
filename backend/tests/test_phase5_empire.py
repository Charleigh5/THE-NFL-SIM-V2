#!/usr/bin/env python3
"""
Phase 5: EMPIRE Economic Tests
===============================
Unit tests for economic simulation modules.

Context7 Best Practices:
- pytest fixtures
- Edge case coverage
"""

import pytest
from typing import List

from app.services.empire import (
    # Salary Cap
    SalaryCapEngine, Contract, ContractType, TeamCapState,
    # GM AI
    GMAI, GMState, DraftPick, RosterNeed, TeamPhilosophy,
    TradeAssetType, NeedPriority, GOAPAction,
)


# ============================================================================
# SALARY CAP TESTS
# ============================================================================

class TestSalaryCapEngine:
    """Tests for SalaryCapEngine."""

    @pytest.fixture
    def engine(self):
        return SalaryCapEngine()

    def test_create_contract(self, engine):
        """Contract creation works correctly."""
        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=20_000_000,
            signing_bonus=10_000_000,
        )

        assert contract.player_id == "P001"
        assert len(contract.years) == 4
        assert contract.total_value == 40_000_000

    def test_signing_bonus_prorate(self, engine):
        """Signing bonus is prorated correctly."""
        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=50_000_000,
            years=5,
            guaranteed=25_000_000,
            signing_bonus=25_000_000,
        )

        # Signing bonus prorated over all 5 years
        prorate_per_year = 25_000_000 // 5
        for year in contract.years:
            assert year.signing_bonus_prorate == prorate_per_year

    def test_rookie_contract(self, engine):
        """Rookie contracts scale by draft position."""
        first_pick = engine.create_rookie_contract("R001", 1)
        late_pick = engine.create_rookie_contract("R002", 100)

        assert first_pick.total_value > late_pick.total_value
        assert len(first_pick.years) == 4  # Standard rookie deal

    def test_back_loaded_contract(self, engine):
        """Back-loaded contracts have higher later salaries."""
        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=10_000_000,
            signing_bonus=0,
            back_loaded=True,
        )

        assert contract.years[3].base_salary > contract.years[0].base_salary

    def test_front_loaded_contract(self, engine):
        """Front-loaded contracts have higher early salaries."""
        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=10_000_000,
            signing_bonus=0,
            front_loaded=True,
        )

        assert contract.years[0].base_salary > contract.years[3].base_salary

    def test_dead_money_calculation(self, engine):
        """Dead money calculated correctly on release."""
        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=20_000_000,
            signing_bonus=16_000_000,
        )

        # Cut after year 1 = 3 years of bonus remaining
        dead = engine.calculate_dead_money(contract, 1)
        assert dead == 16_000_000 // 4 * 3  # 3 years of prorate

    def test_franchise_tag(self, engine):
        """Franchise tag calculates correctly."""
        tag_value = engine.calculate_franchise_tag("QB", 250_000_000)

        # QB is 8% of cap
        expected = int(250_000_000 * 0.08)
        assert tag_value == expected

    def test_cap_savings(self, engine):
        """Cap savings calculated correctly."""
        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=10_000_000,
            signing_bonus=8_000_000,
        )

        savings = engine.calculate_cap_savings(contract, 1)
        # Should save next year's cap hit minus dead money
        assert savings >= 0

    def test_restructure_contract(self, engine):
        """Contract restructure converts base to bonus."""
        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=10_000_000,
            signing_bonus=0,
        )

        original_base = contract.years[0].base_salary
        restructured = engine.restructure_contract(contract, 5_000_000, 1)

        assert restructured.years[0].base_salary < original_base
        assert restructured.years[0].signing_bonus_prorate > 0

    def test_cap_projection(self, engine):
        """Cap projects with growth rate."""
        projections = engine.project_cap(250_000_000, 3)

        assert len(projections) == 3
        assert projections[0] > 250_000_000
        assert projections[2] > projections[1]

    def test_cap_summary(self, engine):
        """Cap summary returns correct data."""
        state = TeamCapState(
            team_id="NE",
            season_year=2024,
            salary_cap=250_000_000,
            active_cap=200_000_000,
            dead_money=10_000_000,
        )

        summary = engine.get_cap_summary(state)

        assert summary["cap_space"] == 40_000_000


# ============================================================================
# GM AI TESTS
# ============================================================================

class TestGMAI:
    """Tests for GMAI."""

    @pytest.fixture
    def gm(self):
        return GMAI(team_id="KC")

    def test_philosophy_win_now(self, gm):
        """Good team gets WIN_NOW philosophy."""
        philosophy = gm.determine_philosophy(
            recent_wins=12,
            avg_roster_age=27,
            cap_situation="GOOD",
            draft_capital=7,
        )

        assert philosophy == TeamPhilosophy.WIN_NOW

    def test_philosophy_rebuild(self, gm):
        """Bad team gets REBUILD philosophy."""
        philosophy = gm.determine_philosophy(
            recent_wins=3,
            avg_roster_age=29,
            cap_situation="OVER",
            draft_capital=5,
        )

        assert philosophy == TeamPhilosophy.REBUILD

    def test_philosophy_develop(self, gm):
        """Young bad team gets DEVELOP philosophy."""
        philosophy = gm.determine_philosophy(
            recent_wins=4,
            avg_roster_age=24,
            cap_situation="GOOD",
            draft_capital=10,
        )

        assert philosophy == TeamPhilosophy.DEVELOP

    def test_draft_pick_value(self):
        """Draft picks have correct approximate value."""
        first_round = DraftPick(year=2024, round=1, pick_number=1)
        seventh_round = DraftPick(year=2024, round=7)

        assert first_round.approximate_value > seventh_round.approximate_value

    def test_trade_evaluation_accept(self, gm):
        """GM accepts winning trade."""
        gm.state.philosophy = TeamPhilosophy.BALANCED

        giving = [(TradeAssetType.DRAFT_PICK, DraftPick(year=2024, round=3))]
        receiving = [(TradeAssetType.DRAFT_PICK, DraftPick(year=2024, round=2))]

        accept, net = gm.evaluate_trade(giving, receiving)

        assert accept is True
        assert net > 0

    def test_trade_evaluation_reject(self, gm):
        """GM rejects losing trade."""
        gm.state.philosophy = TeamPhilosophy.REBUILD

        giving = [(TradeAssetType.DRAFT_PICK, DraftPick(year=2024, round=1, pick_number=5))]
        receiving = [(TradeAssetType.DRAFT_PICK, DraftPick(year=2024, round=4))]

        accept, net = gm.evaluate_trade(giving, receiving)

        assert accept is False

    def test_player_valuation(self, gm):
        """Players are valued correctly."""
        young_star = {"age": 24, "overall": 90, "contract_years": 3}
        old_vet = {"age": 33, "overall": 80, "contract_years": 1}

        young_value = gm._value_asset(TradeAssetType.PLAYER, young_star)
        old_value = gm._value_asset(TradeAssetType.PLAYER, old_vet)

        assert young_value > old_value

    def test_prospect_ranking(self, gm):
        """Prospects ranked by grade and need."""
        gm.state.roster_needs = [
            RosterNeed("QB", NeedPriority.CRITICAL, 65, 1),
        ]

        prospects = [
            {"name": "QB1", "position": "QB", "grade": 85, "age": 22},
            {"name": "WR1", "position": "WR", "grade": 90, "age": 21},
        ]

        ranked = gm.rank_draft_prospects(prospects, gm.state.roster_needs)

        # QB should rank higher due to critical need bonus
        assert ranked[0]["position"] == "QB"

    def test_goap_action_execution(self):
        """GOAP actions check preconditions correctly."""
        action = GOAPAction(
            name="test",
            preconditions={"has_cap": True},
            effects={"signed": True},
            cost=1.0,
        )

        assert action.can_execute({"has_cap": True})
        assert not action.can_execute({"has_cap": False})

    def test_goap_action_apply(self):
        """GOAP actions apply effects correctly."""
        action = GOAPAction(
            name="test",
            preconditions={},
            effects={"signed": True},
            cost=1.0,
        )

        new_state = action.apply({"cap": 100})

        assert new_state["signed"] is True
        assert new_state["cap"] == 100

    def test_generate_actions(self, gm):
        """GM generates available actions."""
        gm.state.cap_space = 50_000_000
        gm.state.draft_picks = [DraftPick(2024, 1)]

        actions = gm.generate_actions()

        assert len(actions) > 0

    def test_get_recommendation(self, gm):
        """GM provides action recommendation."""
        gm.state.philosophy = TeamPhilosophy.WIN_NOW
        gm.state.cap_space = 30_000_000

        rec = gm.get_recommendation()

        assert "action" in rec
        assert "philosophy" in rec


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestEmpireIntegration:
    """Integration tests for EMPIRE."""

    def test_contract_and_cap_state(self):
        """Contracts integrate with cap state."""
        engine = SalaryCapEngine()

        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=20_000_000,
            signing_bonus=10_000_000,
        )

        state = TeamCapState(
            team_id="KC",
            season_year=2024,
            salary_cap=250_000_000,
            contracts={"P001": contract},
        )

        # Calculate cap used from contracts
        cap_used = sum(c.years[0].cap_hit for c in state.contracts.values())
        state.active_cap = cap_used

        assert state.cap_space == state.total_cap - cap_used

    def test_gm_evaluates_contract_player(self):
        """GM can evaluate player with contract."""
        engine = SalaryCapEngine()
        gm = GMAI(team_id="KC")

        contract = engine.create_contract(
            player_id="P001",
            contract_type=ContractType.VETERAN,
            total_value=40_000_000,
            years=4,
            guaranteed=20_000_000,
            signing_bonus=10_000_000,
        )

        player = {"age": 26, "overall": 85, "contract_years": 4}

        value = gm._value_asset(TradeAssetType.PLAYER, player)
        assert value > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
