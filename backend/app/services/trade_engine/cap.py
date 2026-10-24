from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.core.nfl_reference_data import SALARY_CAP_CAGR
from app.services.trade_engine.market import PlayerSnapshot


@dataclass(frozen=True)
class CapYearProjection:
    year_offset: int          # 0, 1, 2, 3
    projected_league_cap: int
    space_before: int
    space_after: int
    net_cap_delta: int
    accelerated_dead_money: int
    reserved_extensions: int


@dataclass(frozen=True)
class TeamCapTradeImpact:
    team_id: int
    is_compliant_year0: bool
    dead_money_tvp_cost: float
    cap_stress_tvp_delta: float
    yearly_projections: list[CapYearProjection]
    rejection_reason: str | None = None


def calculate_trade_dead_money(
    player: PlayerSnapshot,
    is_post_june_1: bool = False,
) -> tuple[int, int]:
    """
    Calculate accelerated dead money hitting Year 0 and Year 1 when a player is traded.
    Under NFL CBA Article 13:
    - Pre-June 1 trade: ALL remaining unamortized signing bonus accelerates into Year 0.
    - Post-June 1 trade: Current year's proration remains in Year 0; all remaining
      unamortized bonus across subsequent years accelerates into Year 1.
    """
    signing_bonus_proration = getattr(player, "signing_bonus_proration", 0) or 0
    contract_years = getattr(player, "contract_years", 1) or 1
    void_years = getattr(player, "void_years", 0) or 0

    total_remaining_bonus = signing_bonus_proration * (contract_years + void_years)

    if total_remaining_bonus <= 0:
        return (0, 0)

    if not is_post_june_1:
        return (total_remaining_bonus, 0)
    else:
        dm_y0 = min(signing_bonus_proration, total_remaining_bonus)
        dm_y1 = max(0, total_remaining_bonus - dm_y0)
        return (dm_y0, dm_y1)


def evaluate_team_cap_impact(
    team_id: int,
    current_cap_space: int,
    incoming_players: Sequence[PlayerSnapshot],
    outgoing_players: Sequence[PlayerSnapshot],
    roster: Sequence[PlayerSnapshot],
    is_post_june_1: bool = False,
    current_year: int = 2025,
    base_cap: int = 279_200_000,
) -> TeamCapTradeImpact:
    """
    Evaluate 4-year salary cap impact of a prospective trade for a single team.
    Enforces Year 0 CBA compliance (cap space >= 0 after trade), accounts for
    accelerated dead money on departures, absorbs incoming base salaries,
    and quantifies cap stress in TVP points.
    """
    projections: list[CapYearProjection] = []
    outgoing_ids = {p.id for p in outgoing_players}
    remaining_roster = [p for p in roster if p.id not in outgoing_ids]

    total_dm_y0 = sum(calculate_trade_dead_money(p, is_post_june_1)[0] for p in outgoing_players)
    total_dm_y1 = sum(calculate_trade_dead_money(p, is_post_june_1)[1] for p in outgoing_players)

    cap_stress_tvp = 0.0

    for y in range(4):
        projected_cap = int(base_cap * ((1.0 + SALARY_CAP_CAGR) ** y))
        cap_growth = projected_cap - base_cap

        if y == 0:
            space_before = current_cap_space
            accel_dm = total_dm_y0
        else:
            space_before = max(0, current_cap_space + cap_growth)
            accel_dm = total_dm_y1 if y == 1 else 0

        # Outgoing player cap relief
        # Old cap hit was base salary + signing bonus proration (if under contract in year y)
        out_base_freed = sum(
            p.annual_base_salary for p in outgoing_players
            if (p.contract_years or 1) > y
        )
        out_bonus_freed = sum(
            (getattr(p, "signing_bonus_proration", 0) or 0) for p in outgoing_players
            if (p.contract_years or 1) > y
        )
        outgoing_freed = out_base_freed + out_bonus_freed

        # Incoming player added cap hit (buyer takes ONLY base salary, 0 prior signing bonus)
        incoming_hit = sum(
            p.annual_base_salary for p in incoming_players
            if (p.contract_years or 1) > y
        )

        # Reserved extensions for remaining young core pieces needing extensions by year y
        reserved_ext = 0
        if y > 0:
            for p in remaining_roster:
                if p.age <= 25 and p.overall_rating >= 85 and (p.contract_years or 1) <= y:
                    reserved_ext += 20_000_000

        space_after = space_before + outgoing_freed - incoming_hit - accel_dm - reserved_ext
        net_delta = space_after - space_before

        # Cap stress penalty if space falls below safety buffer ($7.5M)
        safety_buffer = 7_500_000
        if space_after < safety_buffer:
            shortfall = safety_buffer - space_after
            stress_points = (shortfall / 1_000_000.0) * 12.0 * (0.85 ** y)
            cap_stress_tvp += stress_points

        projections.append(
            CapYearProjection(
                year_offset=y,
                projected_league_cap=projected_cap,
                space_before=space_before,
                space_after=space_after,
                net_cap_delta=net_delta,
                accelerated_dead_money=accel_dm,
                reserved_extensions=reserved_ext,
            )
        )

    # Year 0 compliance check
    year0_space = projections[0].space_after
    is_compliant = (year0_space >= 0)
    rejection_reason = None
    if not is_compliant:
        rejection_reason = (
            f"Cannot afford trade: leaves team ${abs(year0_space):,} over the salary cap in Year 0."
        )

    # Dead money TVP cost in Year 0 (drag on roster flexibility)
    dead_money_tvp = (total_dm_y0 / 1_000_000.0) * 8.0

    return TeamCapTradeImpact(
        team_id=team_id,
        is_compliant_year0=is_compliant,
        dead_money_tvp_cost=round(dead_money_tvp, 1),
        cap_stress_tvp_delta=round(cap_stress_tvp, 1),
        yearly_projections=projections,
        rejection_reason=rejection_reason,
    )
