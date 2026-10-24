from __future__ import annotations

import math
from dataclasses import dataclass

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.trade_config import trade_config
from app.data.draft_value_chart import DraftValueChart
from app.models.draft import DraftPick
from app.models.team import Team


@dataclass(frozen=True)
class ConditionalPickRule:
    upgrade_to_round: int
    probability: float
    description: str = ""


@dataclass(frozen=True)
class PickValuationInput:
    round: int
    year: int
    current_year: int = 2025
    overall_pick: int | None = None
    projected_slot_in_round: int = 16
    original_team_id: int | None = None
    is_compensatory: bool = False
    conditions: list[ConditionalPickRule] | None = None


@dataclass(frozen=True)
class PickValuationResult:
    market_tvp: float
    expected_overall_pick: float
    years_in_future: int
    discount_factor_applied: float


def _clamp_int(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _clamp_float(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def project_team_draft_slot(
    team_elo: float = 1500.0,
    wins: int = 0,
    losses: int = 0,
    roster_starter_ovr: float = 75.0,
) -> int:
    """
    Map a team's competitive strength (Elo, record, and starter OVR)
    to an expected draft slot in [1..32] (1 = weakest team picking 1st, 32 = strongest).
    """
    elo_norm = _clamp_float((team_elo - 1300.0) / 400.0, 0.0, 1.0)
    ovr_norm = _clamp_float((roster_starter_ovr - 65.0) / 20.0, 0.0, 1.0)
    prior_strength = 0.60 * elo_norm + 0.40 * ovr_norm

    games_played = max(0, wins + losses)
    if games_played > 0:
        win_pct = _clamp_float(wins / games_played, 0.0, 1.0)
        record_weight = min(0.70, 0.70 * (games_played / 17.0))
        composite_strength = (record_weight * win_pct) + ((1.0 - record_weight) * prior_strength)
    else:
        composite_strength = prior_strength

    projected_slot = int(1 + composite_strength * 31.0)
    return _clamp_int(projected_slot, 1, 32)


def _compute_single_round_ev(
    round_num: int,
    years_out: int,
    overall_pick: int | None,
    projected_slot_in_round: int,
    is_compensatory: bool,
) -> tuple[float, float]:
    round_clamped = _clamp_int(round_num, 1, 7)
    mu = _clamp_int(projected_slot_in_round, 1, 32)

    if years_out == 0 and overall_pick is not None:
        clamped_overall = _clamp_int(overall_pick, 1, 256)
        return float(DraftValueChart.get_pick_value(clamped_overall)), float(clamped_overall)

    if is_compensatory:
        overall_comp = (round_clamped - 1) * 32 + 32
        return float(DraftValueChart.get_pick_value(overall_comp)), float(overall_comp)

    sigma = 4.0 if years_out == 0 else (7.5 if years_out == 1 else 10.0)
    weighted_sum = 0.0
    total_weight = 0.0

    for slot in range(1, 33):
        weight = math.exp(-0.5 * ((slot - mu) / sigma) ** 2)
        overall_slot = (round_clamped - 1) * 32 + slot
        val = float(DraftValueChart.get_pick_value(overall_slot))
        weighted_sum += weight * val
        total_weight += weight

    base_ev = weighted_sum / total_weight if total_weight > 0.0 else 0.0

    # Top-5 projected 1st-round future picks retain lottery upside
    # to compensate for left-tail boundary truncation at Pick #1.
    if round_clamped == 1 and years_out >= 1 and mu <= 5:
        lottery_upside = 1.0 + 0.14 * ((6 - mu) / 5.0)
        base_ev *= lottery_upside

    expected_overall = float((round_clamped - 1) * 32 + mu)
    return base_ev, expected_overall


def evaluate_draft_pick_tvp(
    pick: PickValuationInput,
    future_discount_rate: float = 0.78,
) -> PickValuationResult:
    """
    Evaluate a current or future draft pick in Fitzgerald-Spielberger TVP units,
    accounting for projected draft slot uncertainty, temporal discounting,
    compensatory placement, and conditional round upgrades.
    """
    raw_years_out = pick.year - pick.current_year
    if raw_years_out > trade_config.MAX_FUTURE_PICK_YEARS:
        raise ValueError("Cannot trade draft picks more than 3 years in the future.")

    years_out = max(0, raw_years_out)

    base_ev, expected_overall = _compute_single_round_ev(
        round_num=pick.round,
        years_out=years_out,
        overall_pick=pick.overall_pick,
        projected_slot_in_round=pick.projected_slot_in_round,
        is_compensatory=pick.is_compensatory,
    )

    if pick.conditions:
        valid_rules = [
            (
                _clamp_int(rule.upgrade_to_round, 1, 7),
                _clamp_float(rule.probability, 0.0, 1.0),
            )
            for rule in pick.conditions
            if rule.probability > 0.0
        ]
        if valid_rules:
            raw_prob_sum = sum(prob for _, prob in valid_rules)
            scale = (1.0 / raw_prob_sum) if raw_prob_sum > 1.0 else 1.0
            base_prob = max(0.0, 1.0 - min(1.0, raw_prob_sum))

            blended_ev = base_prob * base_ev
            blended_overall = base_prob * expected_overall

            for upg_round, prob in valid_rules:
                w = prob * scale
                upg_ev, upg_overall = _compute_single_round_ev(
                    round_num=upg_round,
                    years_out=years_out,
                    overall_pick=None,
                    projected_slot_in_round=pick.projected_slot_in_round,
                    is_compensatory=pick.is_compensatory,
                )
                blended_ev += w * upg_ev
                blended_overall += w * upg_overall

            base_ev = blended_ev
            expected_overall = blended_overall

    discount_factor = float(future_discount_rate**years_out)
    market_tvp = round(base_ev * discount_factor, 2)

    return PickValuationResult(
        market_tvp=market_tvp,
        expected_overall_pick=round(expected_overall, 2),
        years_in_future=years_out,
        discount_factor_applied=round(discount_factor, 6),
    )


def calculate_pick_ev(
    pick: PickValuationInput,
    future_discount_rate: float = 0.78,
) -> float:
    """Return the expected Fitzgerald-Spielberger TVP of a draft pick."""
    return evaluate_draft_pick_tvp(pick, future_discount_rate).market_tvp


def ensure_future_picks_ledger(
    db: Session,
    current_year: int,
    season_id: int | None = None,
    horizon: int = 2,
) -> list[DraftPick]:
    """
    Idempotently ensure that all teams have their 7-round draft picks initialized
    across [current_year .. current_year + horizon].
    """
    teams = list(db.execute(select(Team)).scalars().all())
    ledger_picks: list[DraftPick] = []

    for yr in range(current_year, current_year + horizon + 1):
        for rnd in range(1, 8):
            for team in teams:
                if yr == current_year and season_id is not None:
                    year_filter = or_(DraftPick.year == yr, DraftPick.season_id == season_id)
                else:
                    year_filter = DraftPick.year == yr

                stmt = select(DraftPick).where(
                    DraftPick.original_team_id == team.id,
                    DraftPick.round == rnd,
                    DraftPick.is_compensatory.is_(False),
                    year_filter,
                )
                existing = db.execute(stmt).scalar_one_or_none()
                if isinstance(existing, DraftPick):
                    existing.year = yr
                    if yr == current_year and season_id is not None and existing.season_id is None:
                        existing.season_id = season_id
                    ledger_picks.append(existing)
                else:
                    new_pick = DraftPick(
                        season_id=season_id if yr == current_year else None,
                        year=yr,
                        team_id=team.id,
                        original_team_id=team.id,
                        round=rnd,
                        pick_number=None,
                        is_compensatory=False,
                    )
                    db.add(new_pick)
                    ledger_picks.append(new_pick)

    db.commit()
    return ledger_picks


def assign_draft_order_preserving_trades(
    db: Session,
    season_id: int,
    year: int,
    ordered_team_ids: list[int],
) -> None:
    """
    Assign overall pick numbers for a completed season's 7-round draft order
    while preserving any prior trades (never overwriting DraftPick.team_id).
    """
    for round_num in range(1, 8):
        for i, orig_team_id in enumerate(ordered_team_ids):
            pick_num = (round_num - 1) * 32 + (i + 1)
            stmt = select(DraftPick).where(
                DraftPick.original_team_id == orig_team_id,
                DraftPick.round == round_num,
                DraftPick.is_compensatory.is_(False),
                or_(DraftPick.season_id == season_id, DraftPick.year == year),
            )
            existing_pick = db.execute(stmt).scalar_one_or_none()
            if isinstance(existing_pick, DraftPick):
                existing_pick.pick_number = pick_num
                existing_pick.season_id = season_id
                existing_pick.year = year
            else:
                pick = DraftPick(
                    season_id=season_id,
                    year=year,
                    team_id=orig_team_id,
                    original_team_id=orig_team_id,
                    round=round_num,
                    pick_number=pick_num,
                    is_compensatory=False,
                    player_id=None,
                )
                db.add(pick)
