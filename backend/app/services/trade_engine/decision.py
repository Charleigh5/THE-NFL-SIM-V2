from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from app.models.player import Position
from app.services.trade_engine.cap import TeamCapTradeImpact, evaluate_team_cap_impact
from app.services.trade_engine.class_fit import (
    ProspectBoardEntry,
    evaluate_pick_class_fit,
)
from app.services.trade_engine.context import (
    CompetitiveWindow,
    evaluate_roster_context_multiplier,
)
from app.services.trade_engine.market import (
    PlayerSnapshot,
    calculate_player_market_tvp,
)
from app.services.trade_engine.modifiers import (
    RealismEvaluation,
    TeamContextProfile,
    evaluate_player_realism_modifiers,
    evaluate_trade_relationship_modifiers,
)
from app.services.trade_engine.picks import PickValuationInput, calculate_pick_ev


def ratio_to_letter_grade(ratio: float) -> str:
    """Convert value-in to value-out ratio into a standard football trade letter grade."""
    if ratio >= 1.25:
        return "A+"
    if ratio >= 1.15:
        return "A"
    if ratio >= 1.08:
        return "A-"
    if ratio >= 1.02:
        return "B+"
    if ratio >= 0.96:
        return "B"
    if ratio >= 0.90:
        return "B-"
    if ratio >= 0.84:
        return "C+"
    if ratio >= 0.78:
        return "C"
    if ratio >= 0.72:
        return "D"
    return "F"


@dataclass(frozen=True)
class FactorBreakdown:
    market_tvp: float
    need_fit_delta: float
    cap_impact_delta: float
    window_fit_delta: float
    class_fit_delta: float
    realism_modifiers_delta: float
    gm_threshold: float


@dataclass(frozen=True)
class TeamSideGrade:
    team_id: int
    competitive_window: str
    value_in_tvp: float
    value_out_tvp: float
    ratio: float
    grade: str
    factors: FactorBreakdown


@dataclass(frozen=True)
class CounterOffer:
    add_player_ids: list[int] = field(default_factory=list)
    add_picks: list[PickValuationInput] = field(default_factory=list)
    summary: str = ""


@dataclass(frozen=True)
class TradeDecisionResult:
    is_accepted: bool
    score: float
    reasoning: str
    user_side: TeamSideGrade
    ai_side: TeamSideGrade
    ai_threshold: float
    counter_offer: CounterOffer | None = None
    narrative_notes: list[str] = field(default_factory=list)


def evaluate_trade_package(
    offered_players: Sequence[PlayerSnapshot] = (),
    requested_players: Sequence[PlayerSnapshot] = (),
    offered_picks: Sequence[PickValuationInput] = (),
    requested_picks: Sequence[PickValuationInput] = (),
    offering_team_id: int = 1,
    receiving_team_id: int = 2,
    offering_roster: Sequence[PlayerSnapshot] = (),
    receiving_roster: Sequence[PlayerSnapshot] = (),
    offering_cap_space: int = 25_000_000,
    receiving_cap_space: int = 25_000_000,
    offering_team_profile: TeamContextProfile | None = None,
    receiving_team_profile: TeamContextProfile | None = None,
    offering_window: CompetitiveWindow = CompetitiveWindow.BUBBLE,
    receiving_window: CompetitiveWindow = CompetitiveWindow.BUBBLE,
    prospects: Sequence[ProspectBoardEntry] = (),
    available_counter_picks: Sequence[PickValuationInput] = (),
    available_counter_players: Sequence[PlayerSnapshot] = (),
    gm_archetype: str = "BALANCED",
    gm_trade_aggression: int = 50,
) -> TradeDecisionResult:
    """
    Orchestrate full evaluation across Market, Picks, Context, Cap, Fit, and Realism layers.
    Produces dual-side letter grades, explainable reasoning, and minimal knapsack counter-offers.
    """
    if offering_team_profile is None:
        offering_team_profile = TeamContextProfile(team_id=offering_team_id)
    if receiving_team_profile is None:
        receiving_team_profile = TeamContextProfile(team_id=receiving_team_id)

    notes: list[str] = []

    # 1. Relationship Modifiers
    rel = evaluate_trade_relationship_modifiers(offering_team_profile, receiving_team_profile)
    notes.extend(rel.narrative_notes)

    # Effective roster post-departures (outgoing assets do not block incoming assets)
    ai_requested_ids = {r.id for r in requested_players}
    ai_roster_post_departures = [p for p in receiving_roster if p.id not in ai_requested_ids]

    user_offered_ids = {o.id for o in offered_players}
    user_roster_post_departures = [p for p in offering_roster if p.id not in user_offered_ids]

    # 2. AI Side Value In (what AI receives: offered players + offered picks)
    ai_in_player_tvp = 0.0
    for p in offered_players:
        base_tvp = calculate_player_market_tvp(p).base_market_tvp
        ctx_mult = evaluate_roster_context_multiplier(
            p, ai_roster_post_departures, receiving_window, is_acquiring=True
        )
        realism = evaluate_player_realism_modifiers(
            p, receiving_team_profile, offering_team_profile, is_acquiring=True
        )
        notes.extend(realism.narrative_notes)
        effective = base_tvp * ctx_mult * realism.injury_risk_mult * realism.scheme_fit_mult * realism.morale_leverage_mult
        ai_in_player_tvp += effective

    ai_in_pick_tvp = 0.0
    receiving_tni_map = {
        pos: calculate_position_need(pos, receiving_roster, receiving_window).tni
        for pos in Position
    } if receiving_roster else {}
    for pick in offered_picks:
        ev = calculate_pick_ev(pick)
        if prospects and pick.projected_slot_in_round:
            slot = (pick.round - 1) * 32 + pick.projected_slot_in_round
            fit = evaluate_pick_class_fit(slot, list(prospects), evaluating_team_tni=receiving_tni_map)
            ev *= fit.class_fit_multiplier
        ai_in_pick_tvp += ev

    ai_total_value_in = max(0.0, ai_in_player_tvp + ai_in_pick_tvp)

    # 3. AI Side Value Out (what AI gives up: requested players + requested picks)
    ai_out_player_tvp = 0.0
    for p in requested_players:
        base_tvp = calculate_player_market_tvp(p).base_market_tvp
        ctx_mult = evaluate_roster_context_multiplier(
            p, receiving_roster, receiving_window, is_acquiring=False
        )
        realism = evaluate_player_realism_modifiers(
            p, offering_team_profile, receiving_team_profile, is_acquiring=False
        )
        notes.extend(realism.narrative_notes)
        val = base_tvp * ctx_mult * realism.morale_leverage_mult
        val = max(val, realism.comp_pick_floor_tvp)
        ai_out_player_tvp += val

    ai_out_pick_tvp = 0.0
    offering_tni_map = {
        pos: calculate_position_need(pos, offering_roster, offering_window).tni
        for pos in Position
    } if offering_roster else {}
    for pick in requested_picks:
        ev = calculate_pick_ev(pick)
        if prospects and pick.projected_slot_in_round:
            slot = (pick.round - 1) * 32 + pick.projected_slot_in_round
            fit = evaluate_pick_class_fit(slot, list(prospects), evaluating_team_tni=offering_tni_map)
            ev *= fit.class_fit_multiplier
        ai_out_pick_tvp += ev

    ai_base_value_out = max(0.0, ai_out_player_tvp + ai_out_pick_tvp)

    # 4. Cap Impact for AI Team
    ai_cap = evaluate_team_cap_impact(
        team_id=receiving_team_id,
        current_cap_space=receiving_cap_space,
        incoming_players=offered_players,
        outgoing_players=requested_players,
        roster=receiving_roster,
    )

    # 5. Acceptance Threshold
    base_tau = 1.00
    arch_upper = gm_archetype.upper()
    arch_adjustments = {
        "WIN_NOW": -0.04,
        "REBUILDER": 0.05,
        "DRAFT_HOARDER": 0.03,
        "TALENT_MAXIMIZER": -0.02,
        "ANALYTICS_FIRST": 0.02,
    }
    arch_delta = arch_adjustments.get(arch_upper, 0.0)
    aggr_delta = -(gm_trade_aggression - 50) * 0.002
    ai_threshold = max(0.85, min(1.30, base_tau + arch_delta + aggr_delta + rel.rivalry_threshold_delta + rel.urgency_threshold_delta))

    # 6. AI Ratio & Decision
    ai_effective_cost = max(50.0, ai_base_value_out + ai_cap.dead_money_tvp_cost + ai_cap.cap_stress_tvp_delta)
    ai_ratio = ai_total_value_in / ai_effective_cost

    # Hard rejection if salary cap is breached in Year 0
    if not ai_cap.is_compliant_year0:
        is_accepted = False
        reasoning = ai_cap.rejection_reason or "Trade rejected due to salary cap non-compliance."
    elif ai_ratio >= ai_threshold:
        is_accepted = True
        surplus_pct = round((ai_ratio - 1.0) * 100.0, 1)
        reasoning = f"Offer accepted. Net package value meets organizational criteria (+{surplus_pct}% surplus)."
    else:
        is_accepted = False
        deficit_pct = round((ai_threshold - ai_ratio) * 100.0, 1)
        reasoning = f"Offer declined. Package falls {deficit_pct}% short of required value threshold."

    # Normalized score: relative percentage surplus or deficit compared to acceptance threshold
    score = round((ai_ratio - ai_threshold) * 100.0, 1)

    # 7. Knapsack Counter-Offer Generator
    counter_offer: CounterOffer | None = None
    if not is_accepted and ai_cap.is_compliant_year0 and (ai_ratio >= 0.70):
        needed_tvp = (ai_threshold * ai_effective_cost) - ai_total_value_in
        if needed_tvp > 0 and available_counter_picks:
            # Sort picks by EV ascending to find the minimal sufficient sweetener
            sorted_picks = sorted(
                available_counter_picks, key=lambda pk: calculate_pick_ev(pk)
            )
            # Find the best single pick
            best_pick = None
            for pk in sorted_picks:
                if calculate_pick_ev(pk) >= needed_tvp * 0.85:
                    best_pick = pk
                    break
            if best_pick is None and sorted_picks:
                best_pick = sorted_picks[-1]

            if best_pick:
                counter_offer = CounterOffer(
                    add_picks=[best_pick],
                    summary=f"Add Round {best_pick.round} pick ({best_pick.year}) to bridge value gap (~{calculate_pick_ev(best_pick):.0f} TVP)",
                )

    # 8. User Side Grading
    user_cap = evaluate_team_cap_impact(
        team_id=offering_team_id,
        current_cap_space=offering_cap_space,
        incoming_players=requested_players,
        outgoing_players=offered_players,
        roster=offering_roster,
    )
    user_value_in = ai_base_value_out
    user_effective_cost = max(50.0, ai_total_value_in + user_cap.dead_money_tvp_cost + user_cap.cap_stress_tvp_delta)
    user_ratio = user_value_in / user_effective_cost

    user_grade = ratio_to_letter_grade(user_ratio)
    ai_grade = ratio_to_letter_grade(ai_ratio)

    user_side = TeamSideGrade(
        team_id=offering_team_id,
        competitive_window=offering_window.value,
        value_in_tvp=round(user_value_in, 1),
        value_out_tvp=round(ai_total_value_in, 1),
        ratio=round(user_ratio, 3),
        grade=user_grade,
        factors=FactorBreakdown(
            market_tvp=round(user_value_in, 1),
            need_fit_delta=0.0,
            cap_impact_delta=round(-user_cap.dead_money_tvp_cost, 1),
            window_fit_delta=0.0,
            class_fit_delta=0.0,
            realism_modifiers_delta=0.0,
            gm_threshold=1.00,
        ),
    )

    ai_side = TeamSideGrade(
        team_id=receiving_team_id,
        competitive_window=receiving_window.value,
        value_in_tvp=round(ai_total_value_in, 1),
        value_out_tvp=round(ai_base_value_out, 1),
        ratio=round(ai_ratio, 3),
        grade=ai_grade,
        factors=FactorBreakdown(
            market_tvp=round(ai_base_value_out, 1),
            need_fit_delta=round(ai_in_player_tvp - sum(calculate_player_market_tvp(p).base_market_tvp for p in offered_players), 1),
            cap_impact_delta=round(-ai_cap.dead_money_tvp_cost - ai_cap.cap_stress_tvp_delta, 1),
            window_fit_delta=0.0,
            class_fit_delta=0.0,
            realism_modifiers_delta=round((rel.rivalry_threshold_delta + rel.urgency_threshold_delta) * 100.0, 1),
            gm_threshold=round(ai_threshold, 3),
        ),
    )

    return TradeDecisionResult(
        is_accepted=is_accepted,
        score=score,
        reasoning=reasoning,
        user_side=user_side,
        ai_side=ai_side,
        ai_threshold=round(ai_threshold, 3),
        counter_offer=counter_offer,
        narrative_notes=notes,
    )
