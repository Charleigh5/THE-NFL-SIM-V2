from __future__ import annotations

from dataclasses import dataclass, field

from app.services.trade_engine.market import PlayerSnapshot


@dataclass(frozen=True)
class TeamContextProfile:
    """Team characteristics for contextual trade realism."""

    team_id: int
    conference: str = ""
    division: str = ""
    owner_trust: int = 60
    medical_rating: int = 75
    offensive_scheme: str = "SPREAD"
    defensive_scheme: str = "FOUR_THREE"
    is_trade_deadline: bool = False


@dataclass(frozen=True)
class RealismEvaluation:
    """Output of realism evaluation containing multipliers, floors, taxes, and narratives."""

    injury_risk_mult: float = 1.0           # [0.60, 1.00]
    scheme_fit_mult: float = 1.0            # [0.85, 1.12]
    morale_leverage_mult: float = 1.0       # [0.80, 1.08]
    comp_pick_floor_tvp: float = 0.0        # Reservation price for expiring FAs
    rivalry_threshold_delta: float = 0.0    # +0.12 intra-division, +0.04 intra-conference
    urgency_threshold_delta: float = 0.0    # Negative when deadline/hot-seat active
    narrative_notes: list[str] = field(default_factory=list)


def evaluate_trade_relationship_modifiers(
    offering_team: TeamContextProfile,
    receiving_team: TeamContextProfile,
) -> RealismEvaluation:
    """
    Evaluate inter-team dynamics: division rivalry tax, conference rivalry tax,
    and GM hot-seat desperation.
    """
    notes: list[str] = []
    rivalry_tax = 0.0
    urgency_delta = 0.0

    conf1 = (offering_team.conference or "").strip().upper()
    conf2 = (receiving_team.conference or "").strip().upper()
    div1 = (offering_team.division or "").strip().upper()
    div2 = (receiving_team.division or "").strip().upper()

    if conf1 and conf2 and conf1 == conf2:
        if div1 and div2 and div1 == div2:
            rivalry_tax = 0.12
            notes.append(
                f"Division Rival Tax (+12%): {div1} rivals require a premium to trade assets"
            )
        else:
            rivalry_tax = 0.04
            notes.append(
                f"Intra-Conference Tax (+4%): {conf1} intra-conference trade markup"
            )

    # GM hot-seat pressure: receiving GM on the hot seat is willing to accept slightly less value
    if receiving_team.owner_trust < 35:
        urgency_delta -= 0.05
        notes.append(
            f"GM Hot-Seat Urgency: Low owner trust ({receiving_team.owner_trust}) creates win-now pressure"
        )

    if receiving_team.is_trade_deadline:
        urgency_delta -= 0.03
        notes.append("Trade Deadline Urgency: Buyer paying for stretch-run reinforcement")

    return RealismEvaluation(
        rivalry_threshold_delta=round(rivalry_tax, 3),
        urgency_threshold_delta=round(urgency_delta, 3),
        narrative_notes=notes,
    )


def evaluate_player_realism_modifiers(
    player: PlayerSnapshot,
    acquiring_team: TeamContextProfile,
    selling_team: TeamContextProfile,
    is_acquiring: bool = True,
) -> RealismEvaluation:
    """
    Evaluate player-specific realism factors: injury risk, scheme fit,
    morale/holdout leverage discount, and compensatory pick reservation floor.
    """
    notes: list[str] = []
    injury_mult = 1.0
    scheme_mult = 1.0
    morale_mult = 1.0
    comp_floor = 0.0

    # 1. Injury durability risk
    status = (player.injury_status or "ACTIVE").strip().upper()
    if status in ("IR", "OUT", "INJURED"):
        medical_factor = acquiring_team.medical_rating / 100.0
        injury_mult = max(0.60, min(0.80, 0.65 + 0.15 * medical_factor))
        notes.append(
            f"Medical Flag: Player currently carries injury status ({status}); durability risk applied"
        )
    elif status == "QUESTIONABLE":
        injury_mult = 0.90
        notes.append("Medical Caution: Player listed as Questionable")

    # 2. Scheme & coaching fit
    # (Future scheme mapping can expand, default neutral 1.0)
    scheme_mult = 1.0

    # 3. Locker room morale & holdout leverage discount
    if not is_acquiring:
        if player.morale < 30 or player.tension_score > 75.0:
            morale_mult = 0.82
            notes.append(
                f"Holdout Leverage Discount: Disgruntled player (Morale {player.morale}, Tension {player.tension_score:.0f}) forces seller discount"
            )

    # 4. Compensatory pick reservation floor
    # When selling an elite expiring contract (1 year remaining), the seller
    # will not take less than the projected comp pick they would receive
    if not is_acquiring and (player.contract_years or 1) <= 1:
        if player.overall_rating >= 88 and player.annual_base_salary >= 18_000_000:
            # Projected 3rd round compensatory pick (~650 TVP discounted 1 yr = ~507 TVP)
            comp_floor = 500.0
            notes.append(
                "Compensatory Pick Floor: Team projects a 3rd-round comp pick (~500 TVP) if player walks in free agency"
            )
        elif player.overall_rating >= 82 and player.annual_base_salary >= 10_000_000:
            comp_floor = 250.0
            notes.append(
                "Compensatory Pick Floor: Team projects a 4th/5th round comp pick (~250 TVP) if player walks in free agency"
            )

    return RealismEvaluation(
        injury_risk_mult=round(injury_mult, 3),
        scheme_fit_mult=round(scheme_mult, 3),
        morale_leverage_mult=round(morale_mult, 3),
        comp_pick_floor_tvp=round(comp_floor, 1),
        narrative_notes=notes,
    )
