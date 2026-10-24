import pytest

from app.models.player import Position
from app.services.trade_engine.cap import (
    CapYearProjection,
    TeamCapTradeImpact,
    calculate_trade_dead_money,
    evaluate_team_cap_impact,
)
from app.services.trade_engine.market import PlayerSnapshot


def test_calculate_trade_dead_money_pre_and_post_june_1():
    """Verify remaining signing bonus accelerates to current year pre-June 1, or splits post-June 1."""
    # Player with 3 remaining years, $5M/yr signing bonus proration ($15M total unamortized)
    star = PlayerSnapshot(
        id=1,
        position=Position.WR,
        overall_rating=90,
        age=28,
        contract_years=3,
        annual_base_salary=15_000_000,
        signing_bonus_proration=5_000_000,
        void_years=0,
    )
    pre_june1_dm = calculate_trade_dead_money(star, is_post_june_1=False)
    # Pre-June 1: all 3 years accelerate into current year (Year 0 = $15M, Year 1 = $0)
    assert pre_june1_dm == (15_000_000, 0)

    post_june1_dm = calculate_trade_dead_money(star, is_post_june_1=True)
    # Post-June 1: Year 0 keeps current year ($5M), remaining $10M hits Year 1
    assert post_june1_dm == (5_000_000, 10_000_000)


def test_seller_and_buyer_cap_trade_impact():
    """Verify seller absorbs accelerated dead money while buyer absorbs only base salary."""
    traded_star = PlayerSnapshot(
        id=50,
        position=Position.WR,
        overall_rating=90,
        age=27,
        contract_years=3,
        annual_base_salary=10_000_000,
        signing_bonus_proration=6_000_000,
        void_years=0,
    )
    seller_impact = evaluate_team_cap_impact(
        team_id=1,
        current_cap_space=20_000_000,
        incoming_players=[],
        outgoing_players=[traded_star],
        roster=[traded_star],
    )
    buyer_impact = evaluate_team_cap_impact(
        team_id=2,
        current_cap_space=20_000_000,
        incoming_players=[traded_star],
        outgoing_players=[],
        roster=[],
    )

    assert isinstance(seller_impact, TeamCapTradeImpact)
    assert isinstance(buyer_impact, TeamCapTradeImpact)
    assert seller_impact.is_compliant_year0 is True
    assert buyer_impact.is_compliant_year0 is True

    # Seller Year 0: had 20M cap space. Traded player frees 10M base, but accelerates 12M extra bonus -> net 18M
    assert seller_impact.yearly_projections[0].accelerated_dead_money == 18_000_000
    assert seller_impact.yearly_projections[0].space_after == 18_000_000

    # Buyer Year 0: had 20M cap space. Takes 10M base salary -> 10M cap space remaining
    assert buyer_impact.yearly_projections[0].space_after == 10_000_000


def test_trade_rejected_if_year0_cap_space_exceeded():
    """Verify non-compliance flag and explicit rejection reason when Year 0 cap space is insufficient."""
    expensive_qb = PlayerSnapshot(
        id=99,
        position=Position.QB,
        overall_rating=88,
        age=29,
        contract_years=3,
        annual_base_salary=30_000_000,
    )
    impact = evaluate_team_cap_impact(
        team_id=5,
        current_cap_space=15_000_000,
        incoming_players=[expensive_qb],
        outgoing_players=[],
        roster=[],
    )
    assert impact.is_compliant_year0 is False
    assert impact.rejection_reason is not None
    assert "Cannot afford" in impact.rejection_reason or "cap" in impact.rejection_reason.lower()
