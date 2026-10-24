from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.models.player import DevelopmentTrait, Position

SALARY_CAP_CAGR: float = 0.0697
DEFAULT_NFL_SALARY_CAP: int = 279_200_000


@dataclass(frozen=True)
class PositionValueProfile:
    """Market APY ceiling and biological aging profile for an NFL position."""

    position: Position
    top_apy_pct_cap: float
    starters_required: int
    peak_start: int
    peak_end: int
    decline_per_year: float
    cliff_age: int


POSITION_PROFILES: dict[Position, PositionValueProfile] = {
    Position.QB: PositionValueProfile(
        position=Position.QB,
        top_apy_pct_cap=0.215,
        starters_required=1,
        peak_start=26,
        peak_end=33,
        decline_per_year=0.8,
        cliff_age=37,
    ),
    Position.DE: PositionValueProfile(
        position=Position.DE,
        top_apy_pct_cap=0.143,
        starters_required=2,
        peak_start=25,
        peak_end=29,
        decline_per_year=1.6,
        cliff_age=32,
    ),
    Position.WR: PositionValueProfile(
        position=Position.WR,
        top_apy_pct_cap=0.140,
        starters_required=3,
        peak_start=24,
        peak_end=29,
        decline_per_year=1.8,
        cliff_age=32,
    ),
    Position.DT: PositionValueProfile(
        position=Position.DT,
        top_apy_pct_cap=0.130,
        starters_required=2,
        peak_start=25,
        peak_end=30,
        decline_per_year=1.5,
        cliff_age=33,
    ),
    Position.OT: PositionValueProfile(
        position=Position.OT,
        top_apy_pct_cap=0.105,
        starters_required=2,
        peak_start=25,
        peak_end=31,
        decline_per_year=1.2,
        cliff_age=34,
    ),
    Position.CB: PositionValueProfile(
        position=Position.CB,
        top_apy_pct_cap=0.095,
        starters_required=3,
        peak_start=23,
        peak_end=28,
        decline_per_year=2.2,
        cliff_age=30,
    ),
    Position.C: PositionValueProfile(
        position=Position.C,
        top_apy_pct_cap=0.092,
        starters_required=1,
        peak_start=25,
        peak_end=31,
        decline_per_year=1.2,
        cliff_age=34,
    ),
    Position.LB: PositionValueProfile(
        position=Position.LB,
        top_apy_pct_cap=0.090,
        starters_required=2,
        peak_start=24,
        peak_end=29,
        decline_per_year=1.8,
        cliff_age=31,
    ),
    Position.OG: PositionValueProfile(
        position=Position.OG,
        top_apy_pct_cap=0.089,
        starters_required=2,
        peak_start=25,
        peak_end=31,
        decline_per_year=1.2,
        cliff_age=34,
    ),
    Position.S: PositionValueProfile(
        position=Position.S,
        top_apy_pct_cap=0.082,
        starters_required=2,
        peak_start=24,
        peak_end=29,
        decline_per_year=1.8,
        cliff_age=31,
    ),
    Position.RB: PositionValueProfile(
        position=Position.RB,
        top_apy_pct_cap=0.078,
        starters_required=1,
        peak_start=22,
        peak_end=26,
        decline_per_year=2.8,
        cliff_age=28,
    ),
    Position.TE: PositionValueProfile(
        position=Position.TE,
        top_apy_pct_cap=0.070,
        starters_required=1,
        peak_start=25,
        peak_end=30,
        decline_per_year=1.5,
        cliff_age=32,
    ),
    Position.K: PositionValueProfile(
        position=Position.K,
        top_apy_pct_cap=0.025,
        starters_required=1,
        peak_start=24,
        peak_end=36,
        decline_per_year=0.6,
        cliff_age=40,
    ),
    Position.P: PositionValueProfile(
        position=Position.P,
        top_apy_pct_cap=0.025,
        starters_required=1,
        peak_start=24,
        peak_end=36,
        decline_per_year=0.6,
        cliff_age=40,
    ),
}

_POSITION_ALIASES: dict[str, Position] = {
    "EDGE": Position.DE,
    "LT": Position.OT,
    "RT": Position.OT,
    "OL": Position.OT,
    "DL": Position.DT,
    "DB": Position.CB,
}

_DEV_TRAIT_GROWTH: dict[str, float] = {
    DevelopmentTrait.NORMAL.value: 1.0,
    DevelopmentTrait.STAR.value: 1.8,
    DevelopmentTrait.SUPERSTAR.value: 2.6,
    DevelopmentTrait.XFACTOR.value: 3.4,
}


def get_position_profile(position: Position | str) -> PositionValueProfile:
    """Resolve a Position enum or string (including common NFL aliases) to its profile."""
    if isinstance(position, Position):
        return POSITION_PROFILES[position]

    normalized = str(position).strip().upper()
    if normalized in _POSITION_ALIASES:
        return POSITION_PROFILES[_POSITION_ALIASES[normalized]]

    try:
        pos_enum = Position(normalized)
        return POSITION_PROFILES[pos_enum]
    except ValueError:
        return POSITION_PROFILES[Position.LB]


@dataclass(frozen=True)
class PlayerSnapshot:
    """Immutable value snapshot of a player for deterministic trade valuation."""

    id: int
    position: Position | str
    overall_rating: int
    age: int
    contract_years: int = 1
    annual_base_salary: int = 1_000_000
    signing_bonus_proration: int = 0
    void_years: int = 0
    guaranteed_total: int = 0
    is_rookie: bool = False
    draft_round: int | None = None
    development_trait: DevelopmentTrait | str = DevelopmentTrait.NORMAL
    potential: int | None = None
    morale: int = 50
    tension_score: float = 0.0
    injury_status: str = "ACTIVE"
    first_name: str = ""
    last_name: str = ""

    @classmethod
    def from_orm_player(cls, player: Any) -> PlayerSnapshot:
        """Safely construct a PlayerSnapshot from an ORM Player instance."""
        contract = getattr(player, "contract", None)
        progression = getattr(player, "progression", None)
        injury = getattr(player, "injury", None)

        contract_years = (
            getattr(contract, "contract_years", None)
            if contract is not None
            else getattr(player, "contract_years", 1)
        )
        if contract_years is None:
            contract_years = getattr(player, "contract_years", 1) or 1

        annual_base_salary = None
        if contract is not None:
            annual_base_salary = getattr(contract, "annual_base_salary", None)
            if not annual_base_salary:
                annual_base_salary = getattr(contract, "contract_salary", None)
        if not annual_base_salary:
            annual_base_salary = getattr(player, "contract_salary", 1_000_000) or 1_000_000

        signing_bonus_proration = (
            getattr(contract, "signing_bonus_proration", 0)
            if contract is not None
            else getattr(player, "signing_bonus_proration", 0)
        ) or 0
        void_years = (
            getattr(contract, "void_years", 0)
            if contract is not None
            else getattr(player, "void_years", 0)
        ) or 0
        guaranteed_total = (
            getattr(contract, "guaranteed_total", 0)
            if contract is not None
            else getattr(player, "guaranteed_total", 0)
        ) or 0
        is_rookie = bool(
            getattr(contract, "is_rookie", False)
            if contract is not None
            else getattr(player, "is_rookie", False)
        )
        morale = (
            getattr(contract, "morale", None)
            if contract is not None
            else getattr(player, "morale", 50)
        )
        if morale is None:
            morale = 50

        dev_trait = (
            getattr(progression, "development_trait", None)
            if progression is not None
            else getattr(player, "development_trait", DevelopmentTrait.NORMAL)
        ) or DevelopmentTrait.NORMAL

        potential = (
            getattr(progression, "potential", None)
            if progression is not None
            else getattr(player, "potential", None)
        )

        injury_status = (
            getattr(injury, "injury_status", None)
            if injury is not None
            else getattr(player, "injury_status", "ACTIVE")
        ) or "ACTIVE"

        return cls(
            id=int(getattr(player, "id", 0) or 0),
            position=getattr(player, "position", Position.LB),
            overall_rating=int(getattr(player, "overall_rating", 50) or 50),
            age=int(getattr(player, "age", 22) or 22),
            contract_years=int(contract_years),
            annual_base_salary=int(annual_base_salary),
            signing_bonus_proration=int(signing_bonus_proration),
            void_years=int(void_years),
            guaranteed_total=int(guaranteed_total),
            is_rookie=is_rookie,
            draft_round=getattr(player, "draft_round", None),
            development_trait=dev_trait,
            potential=int(potential) if potential is not None else None,
            morale=int(morale),
            tension_score=float(getattr(player, "tension_score", 0.0) or 0.0),
            injury_status=str(injury_status),
            first_name=str(getattr(player, "first_name", "") or ""),
            last_name=str(getattr(player, "last_name", "") or ""),
        )


@dataclass(frozen=True)
class PlayerValuationBreakdown:
    """Multi-year surplus and market valuation breakdown on the unified TVP scale."""

    player_id: int
    base_market_tvp: float
    projected_ovrs: list[float]
    annual_market_values: list[int]
    annual_cap_hits: list[int]
    years_of_control: int
    includes_fifth_year_option: bool
    includes_franchise_tag_window: bool


def project_player_ovr_curve(
    ovr: int,
    age: int,
    position: Position | str,
    dev_trait: DevelopmentTrait | str = DevelopmentTrait.NORMAL,
    years: int = 4,
    potential: int | None = None,
) -> list[float]:
    """
    Project a player's OVR trajectory across `years` seasons using position-specific
    peak windows, development traits, and age cliffs.
    """
    if years <= 0:
        return []

    profile = get_position_profile(position)
    dev_key = dev_trait.value if isinstance(dev_trait, DevelopmentTrait) else str(dev_trait).upper()
    annual_growth = _DEV_TRAIT_GROWTH.get(dev_key, 1.0)
    ceiling = float(potential) if potential is not None else 99.0

    initial_ovr = max(40.0, min(99.0, float(ovr)))
    curve: list[float] = [initial_ovr]

    for y in range(1, years):
        current_age = age + y
        prev_ovr = curve[-1]

        if current_age <= profile.peak_start:
            taper = 0.5 if current_age == profile.peak_start else 1.0
            next_ovr = min(ceiling, prev_ovr + annual_growth * taper)
        elif current_age <= profile.peak_end:
            if dev_key in (
                DevelopmentTrait.SUPERSTAR.value,
                DevelopmentTrait.XFACTOR.value,
            ) and current_age < profile.peak_start + 2:
                next_ovr = min(ceiling, prev_ovr + 0.5)
            else:
                next_ovr = prev_ovr
        else:
            decline = (
                profile.decline_per_year
                if current_age < profile.cliff_age
                else profile.decline_per_year * 2.0
            )
            next_ovr = prev_ovr - decline

        clamped_ovr = round(max(40.0, min(99.0, next_ovr)), 2)
        curve.append(clamped_ovr)

    return curve


def ovr_to_market_tier(ovr: float) -> float:
    """
    Map player OVR to a fraction of top-of-market positional APY.
    - Below 65 OVR: 0.03 (veteran minimum floor)
    - 65-75 OVR: convex sub-starter ramp
    - 75-99 OVR: starter market curve + star scarcity boost for elite 88-99 players
    """
    if ovr < 65.0:
        return 0.03

    clamped = min(ovr, 99.0)
    if clamped < 75.0:
        return 0.03 + 0.15 * (((clamped - 65.0) / 10.0) ** 1.6)

    norm = (clamped - 75.0) / 24.0
    starter_tier = 0.18 + 0.84 * (norm**0.55)
    star_scarcity = 0.08 * (max(0.0, (clamped - 88.0) / 11.0) ** 1.2)
    return starter_tier + star_scarcity


def _positional_scarcity_multiplier(profile: PositionValueProfile) -> float:
    """Compute positional scarcity multiplier for TVP conversion."""
    if profile.position == Position.QB:
        return 1.42
    if profile.position == Position.WR:
        return 0.86
    if profile.position == Position.CB:
        return 1.12
    return (0.11 / max(profile.top_apy_pct_cap, 0.025)) ** 0.42


def calculate_player_market_tvp(
    player: PlayerSnapshot,
    current_cap: int = DEFAULT_NFL_SALARY_CAP,
    discount_factor: float = 0.85,
    cap_weight_lambda: float = 0.60,
) -> PlayerValuationBreakdown:
    """
    Compute a player's multi-year surplus and scarcity valuation on the unified
    Fitzgerald-Spielberger Trade Value Point (TVP) scale (#1 overall pick = 3,000 TVP).
    """
    profile = get_position_profile(player.position)

    includes_fifth_year_option = bool(
        player.is_rookie and player.draft_round == 1 and player.age <= 25
    )
    includes_franchise_tag_window = bool(
        player.overall_rating >= 88 and player.age <= profile.peak_end
    )

    base_years = max(1, player.contract_years)
    years_of_control = (
        base_years
        + (1 if includes_fifth_year_option else 0)
        + (1 if includes_franchise_tag_window else 0)
    )

    projected_ovrs = project_player_ovr_curve(
        ovr=player.overall_rating,
        age=player.age,
        position=profile.position,
        dev_trait=player.development_trait,
        years=years_of_control,
        potential=player.potential,
    )

    scarcity_mult = _positional_scarcity_multiplier(profile)
    annual_market_values: list[int] = []
    annual_cap_hits: list[int] = []
    total_tvp = 0.0

    for y, ovr_y in enumerate(projected_ovrs):
        projected_cap_y = current_cap * ((1.0 + SALARY_CAP_CAGR) ** y)
        mv_y_float = projected_cap_y * profile.top_apy_pct_cap * ovr_to_market_tier(ovr_y)
        mv_y = int(round(mv_y_float))
        annual_market_values.append(mv_y)

        if y < base_years:
            cap_hit_y = int(player.annual_base_salary)
            option_weight = 1.0
        elif includes_fifth_year_option and y == base_years:
            cap_hit_y = int(round(0.55 * mv_y_float))
            option_weight = 1.0
        else:
            cap_hit_y = int(round(0.85 * mv_y_float))
            option_weight = 0.5

        annual_cap_hits.append(cap_hit_y)

        surplus_dollars_y = mv_y_float - cap_weight_lambda * float(cap_hit_y)
        surplus_tvp_y = (surplus_dollars_y / 1_000_000.0) * 32.0 * scarcity_mult

        star_scarcity_floor_y = 0.0
        if ovr_y >= 82.0:
            star_scarcity_floor_y = ((ovr_y - 80.0) ** 1.18) * 18.5 * scarcity_mult

        year_tvp = (surplus_tvp_y + star_scarcity_floor_y) * (discount_factor**y) * option_weight
        total_tvp += year_tvp

    return PlayerValuationBreakdown(
        player_id=player.id,
        base_market_tvp=round(total_tvp, 2),
        projected_ovrs=projected_ovrs,
        annual_market_values=annual_market_values,
        annual_cap_hits=annual_cap_hits,
        years_of_control=years_of_control,
        includes_fifth_year_option=includes_fifth_year_option,
        includes_franchise_tag_window=includes_franchise_tag_window,
    )
