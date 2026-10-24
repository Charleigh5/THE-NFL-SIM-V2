import pytest

from app.models.player import Position
from app.services.trade_engine.decision import (
    evaluate_trade_package,
    ratio_to_letter_grade,
)
from app.services.trade_engine.market import PlayerSnapshot
from app.services.trade_engine.picks import PickValuationInput


def test_ratio_to_letter_grade_scale():
    """Verify ratio converts accurately to letter grades."""
    assert ratio_to_letter_grade(1.30) == "A+"
    assert ratio_to_letter_grade(1.00) == "B"
    assert ratio_to_letter_grade(0.70) == "F"


def test_close_trade_generates_knapsack_counter_offer():
    """When a trade offer is close (within bargaining range), generate a minimal counter-offer."""
    offered = [
        PlayerSnapshot(
            id=1,
            position=Position.WR,
            overall_rating=83,
            age=26,
            contract_years=2,
            annual_base_salary=10_000_000,
        )
    ]
    requested = [
        PlayerSnapshot(
            id=2,
            position=Position.WR,
            overall_rating=86,
            age=26,
            contract_years=2,
            annual_base_salary=12_000_000,
        )
    ]
    available_user_picks = [
        PickValuationInput(round=3, year=2025, current_year=2025, projected_slot_in_round=16),
        PickValuationInput(round=5, year=2025, current_year=2025, projected_slot_in_round=16),
    ]
    res = evaluate_trade_package(
        offered_players=offered,
        requested_players=requested,
        offered_picks=[],
        requested_picks=[],
        available_counter_picks=available_user_picks,
    )
    assert res.ai_side.ratio < res.ai_threshold
    assert res.counter_offer is not None
    assert len(res.counter_offer.add_picks) >= 1
