import time

import pytest

from app.models.player import Position
from app.services.trade_engine.class_fit import (
    PickClassFitResult,
    ProspectBoardEntry,
    calculate_class_strength_index,
    calculate_trade_up_run_urgency,
    evaluate_pick_class_fit,
)


def _build_qb_rich_board() -> list[ProspectBoardEntry]:
    """Build a 32-prospect board with 3 elite QBs at the top and solid depth elsewhere."""
    prospects: list[ProspectBoardEntry] = [
        ProspectBoardEntry(prospect_id=1, position=Position.QB, grade=96.0),
        ProspectBoardEntry(prospect_id=2, position=Position.QB, grade=94.0),
        ProspectBoardEntry(prospect_id=3, position=Position.QB, grade=92.0),
    ]
    other_positions = [
        Position.WR,
        Position.OT,
        Position.DE,
        Position.CB,
        Position.DT,
        Position.LB,
        Position.S,
        Position.TE,
    ]
    for i in range(4, 33):
        pos = other_positions[(i - 4) % len(other_positions)]
        grade = max(68.0, 83.0 - (i - 4) * 0.45)
        prospects.append(ProspectBoardEntry(prospect_id=i, position=pos, grade=grade))
    return prospects


def test_qb_rich_top5_boosts_pick_value_for_qb_needy_team() -> None:
    prospects = _build_qb_rich_board()
    qb_needy_tni: dict[Position | str, float] = {
        Position.QB: 0.95,
        Position.WR: 0.30,
        Position.OT: 0.25,
        Position.DE: 0.25,
        Position.CB: 0.25,
    }
    qb_set_tni: dict[Position | str, float] = {
        Position.QB: 0.05,
        Position.WR: 0.40,
        Position.OT: 0.35,
        Position.DE: 0.35,
        Position.CB: 0.35,
    }

    fit_needy = evaluate_pick_class_fit(
        slot=2,
        prospects=prospects,
        evaluating_team_tni=qb_needy_tni,
        num_simulations=60,
        seed=42,
    )
    fit_set = evaluate_pick_class_fit(
        slot=2,
        prospects=prospects,
        evaluating_team_tni=qb_set_tni,
        num_simulations=60,
        seed=42,
    )

    assert fit_needy.class_fit_multiplier > 1.10
    assert fit_needy.class_fit_multiplier > fit_set.class_fit_multiplier + 0.15
    assert fit_needy.expected_best_position == Position.QB
    assert 0.85 <= fit_needy.class_fit_multiplier <= 1.25
    assert 0.85 <= fit_set.class_fit_multiplier <= 1.25


def test_empty_prospects_returns_neutral_multiplier_1_0() -> None:
    tni: dict[Position | str, float] = {Position.QB: 0.90}

    empty_res = evaluate_pick_class_fit(
        slot=5,
        prospects=[],
        evaluating_team_tni=tni,
    )
    assert empty_res == PickClassFitResult(
        slot=5,
        class_fit_multiplier=1.0,
        expected_best_position=None,
        expected_best_grade=0.0,
        positional_run_risk=0.0,
        class_strength_index={},
    )

    prospects = _build_qb_rich_board()
    zero_slot_res = evaluate_pick_class_fit(
        slot=0,
        prospects=prospects,
        evaluating_team_tni=tni,
    )
    assert zero_slot_res.class_fit_multiplier == 1.0
    assert zero_slot_res.expected_best_position is None

    out_of_bounds_res = evaluate_pick_class_fit(
        slot=len(prospects) + 1,
        prospects=prospects,
        evaluating_team_tni=tni,
    )
    assert out_of_bounds_res.class_fit_multiplier == 1.0
    assert out_of_bounds_res.expected_best_position is None


def test_positional_run_risk_increases_at_later_slots_and_drives_trade_up_urgency() -> None:
    prospects: list[ProspectBoardEntry] = [
        ProspectBoardEntry(prospect_id=1, position=Position.OT, grade=92.0),
        ProspectBoardEntry(prospect_id=2, position=Position.OT, grade=89.0),
    ]
    filler_positions = [Position.WR, Position.CB, Position.DE, Position.LB, Position.DT, Position.S]
    for i in range(3, 33):
        pos = filler_positions[(i - 3) % len(filler_positions)]
        grade = max(68.0, 84.0 - (i - 3) * 0.4)
        prospects.append(ProspectBoardEntry(prospect_id=i, position=pos, grade=grade))

    ot_needy_tni: dict[Position | str, float] = {
        Position.OT: 0.95,
        Position.WR: 0.35,
        Position.CB: 0.30,
        Position.DE: 0.30,
    }

    fit_early = evaluate_pick_class_fit(
        slot=2,
        prospects=prospects,
        evaluating_team_tni=ot_needy_tni,
        num_simulations=60,
        seed=42,
    )
    fit_late = evaluate_pick_class_fit(
        slot=12,
        prospects=prospects,
        evaluating_team_tni=ot_needy_tni,
        num_simulations=60,
        seed=42,
    )

    assert 0.0 <= fit_early.positional_run_risk <= 1.0
    assert 0.0 <= fit_late.positional_run_risk <= 1.0
    assert fit_late.positional_run_risk > fit_early.positional_run_risk

    urgency = calculate_trade_up_run_urgency(
        current_slot=12,
        target_slot=2,
        prospects=prospects,
        evaluating_team_tni=ot_needy_tni,
        seed=42,
    )
    assert urgency > 0.50
    assert urgency == pytest.approx(fit_late.positional_run_risk - fit_early.positional_run_risk)


def test_deterministic_seed_reproducibility_and_performance_under_20ms() -> None:
    prospects = _build_qb_rich_board()
    tni: dict[Position | str, float] = {
        Position.QB: 0.85,
        Position.WR: 0.65,
        Position.OT: 0.55,
        Position.DE: 0.40,
    }

    res_a = evaluate_pick_class_fit(
        slot=10,
        prospects=prospects,
        evaluating_team_tni=tni,
        num_simulations=60,
        seed=999,
    )
    res_b = evaluate_pick_class_fit(
        slot=10,
        prospects=prospects,
        evaluating_team_tni=tni,
        num_simulations=60,
        seed=999,
    )
    assert res_a == res_b

    start = time.perf_counter()
    res_perf = evaluate_pick_class_fit(
        slot=15,
        prospects=prospects,
        evaluating_team_tni=tni,
        num_simulations=60,
        seed=77777,
    )
    elapsed_s = time.perf_counter() - start
    assert elapsed_s < 0.020
    assert 0.85 <= res_perf.class_fit_multiplier <= 1.25

    strength_idx = calculate_class_strength_index(prospects)
    assert strength_idx["QB"] > strength_idx["WR"]
    for val in strength_idx.values():
        assert 0.75 <= val <= 1.30
