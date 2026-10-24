import pytest

from app.models.player import DevelopmentTrait, Position
from app.services.trade_engine.market import (
    POSITION_PROFILES,
    PlayerSnapshot,
    PositionValueProfile,
    calculate_player_market_tvp,
    get_position_profile,
    ovr_to_market_tier,
    project_player_ovr_curve,
)


def test_position_profiles_cover_all_positions():
    """Verify every Position enum member has a calibrated PositionValueProfile and aliases resolve."""
    for pos in Position:
        assert pos in POSITION_PROFILES
        profile = POSITION_PROFILES[pos]
        assert isinstance(profile, PositionValueProfile)
        assert profile.position == pos
        assert 0.0 < profile.top_apy_pct_cap < 0.30
        assert profile.starters_required >= 1
        assert profile.peak_start < profile.peak_end < profile.cliff_age
        assert profile.decline_per_year > 0.0

    # Alias resolution
    assert get_position_profile("EDGE").position == Position.DE
    assert get_position_profile("LT").position == Position.OT
    assert get_position_profile("RT").position == Position.OT
    assert get_position_profile("OL").position == Position.OT
    assert get_position_profile("DL").position == Position.DT
    assert get_position_profile("DB").position == Position.CB
    assert get_position_profile("UNKNOWN_POS").position == Position.LB


def test_rb_ages_faster_than_qb():
    """Verify RB OVR curve declines earlier and steeper than QB OVR curve."""
    rb_curve = project_player_ovr_curve(
        ovr=90,
        age=26,
        position=Position.RB,
        dev_trait=DevelopmentTrait.STAR,
        years=5,
    )
    qb_curve = project_player_ovr_curve(
        ovr=90,
        age=26,
        position=Position.QB,
        dev_trait=DevelopmentTrait.STAR,
        years=5,
    )

    assert len(rb_curve) == 5
    assert len(qb_curve) == 5
    assert rb_curve[0] == 90.0
    assert qb_curve[0] == 90.0
    # At age 30 (year 4), RB is past peak_end (26) and past cliff_age (28), whereas QB is still in peak (26-33)
    assert rb_curve[-1] < qb_curve[-1] - 10.0


def test_preregistered_nfl_trade_benchmarks():
    """
    Validate all 5 pre-registered real-world NFL trade archetypes land within their target TVP bands.
    """
    # 1. Davante Adams (29-yr 95 WR, $35M base, 4 yrs, SUPERSTAR, not rookie): 2,200 <= TVP <= 2,800
    davante = PlayerSnapshot(
        id=1,
        first_name="Davante",
        last_name="Adams",
        position=Position.WR,
        overall_rating=95,
        age=29,
        contract_years=4,
        annual_base_salary=35_000_000,
        is_rookie=False,
        development_trait=DevelopmentTrait.SUPERSTAR,
    )
    davante_val = calculate_player_market_tvp(davante)
    assert 2200.0 <= davante_val.base_market_tvp <= 2800.0, (
        f"Davante Adams TVP {davante_val.base_market_tvp} outside [2200, 2800]"
    )

    # 2. Jalen Ramsey (24-yr 92 CB, $4M base, 2 yrs, is_rookie=True, draft_round=1, XFACTOR): 2,800 <= TVP <= 3,600
    ramsey = PlayerSnapshot(
        id=2,
        first_name="Jalen",
        last_name="Ramsey",
        position=Position.CB,
        overall_rating=92,
        age=24,
        contract_years=2,
        annual_base_salary=4_000_000,
        is_rookie=True,
        draft_round=1,
        development_trait=DevelopmentTrait.XFACTOR,
    )
    ramsey_val = calculate_player_market_tvp(ramsey)
    assert ramsey_val.includes_fifth_year_option is True
    assert 2800.0 <= ramsey_val.base_market_tvp <= 3600.0, (
        f"Jalen Ramsey TVP {ramsey_val.base_market_tvp} outside [2800, 3600]"
    )

    # 3. Christian McCaffrey (26-yr 95 RB, $16M base, 3 yrs, XFACTOR): 1,600 <= TVP <= 2,400
    cmc = PlayerSnapshot(
        id=3,
        first_name="Christian",
        last_name="McCaffrey",
        position=Position.RB,
        overall_rating=95,
        age=26,
        contract_years=3,
        annual_base_salary=16_000_000,
        is_rookie=False,
        development_trait=DevelopmentTrait.XFACTOR,
    )
    cmc_val = calculate_player_market_tvp(cmc)
    assert 1600.0 <= cmc_val.base_market_tvp <= 2400.0, (
        f"CMC TVP {cmc_val.base_market_tvp} outside [1600, 2400]"
    )

    # 4. Stefon Diggs (30-yr 85 WR, $22M base, 2 yrs, STAR): 800 <= TVP <= 1,200
    diggs = PlayerSnapshot(
        id=4,
        first_name="Stefon",
        last_name="Diggs",
        position=Position.WR,
        overall_rating=85,
        age=30,
        contract_years=2,
        annual_base_salary=22_000_000,
        is_rookie=False,
        development_trait=DevelopmentTrait.STAR,
    )
    diggs_val = calculate_player_market_tvp(diggs)
    assert 800.0 <= diggs_val.base_market_tvp <= 1200.0, (
        f"Stefon Diggs TVP {diggs_val.base_market_tvp} outside [800, 1200]"
    )

    # 5. Russell Wilson (33-yr 88 QB, $40M base, 3 yrs, STAR): 3,500 <= TVP <= 4,500
    wilson = PlayerSnapshot(
        id=5,
        first_name="Russell",
        last_name="Wilson",
        position=Position.QB,
        overall_rating=88,
        age=33,
        contract_years=3,
        annual_base_salary=40_000_000,
        is_rookie=False,
        development_trait=DevelopmentTrait.STAR,
    )
    wilson_val = calculate_player_market_tvp(wilson)
    assert 3500.0 <= wilson_val.base_market_tvp <= 4500.0, (
        f"Russell Wilson TVP {wilson_val.base_market_tvp} outside [3500, 4500]"
    )


def test_monotonicity_ovr_and_contract_efficiency():
    """Verify TVP increases strictly with OVR and decreases strictly with salary ceteris paribus."""
    p75 = PlayerSnapshot(
        id=10, position=Position.WR, overall_rating=75, age=26, contract_years=3, annual_base_salary=10_000_000
    )
    p85 = PlayerSnapshot(
        id=11, position=Position.WR, overall_rating=85, age=26, contract_years=3, annual_base_salary=10_000_000
    )
    p90 = PlayerSnapshot(
        id=12, position=Position.WR, overall_rating=90, age=26, contract_years=3, annual_base_salary=10_000_000
    )

    tvp_75 = calculate_player_market_tvp(p75).base_market_tvp
    tvp_85 = calculate_player_market_tvp(p85).base_market_tvp
    tvp_90 = calculate_player_market_tvp(p90).base_market_tvp

    assert tvp_90 > tvp_85 > tvp_75

    # Cheap control ($2M) vs Expensive ($20M)
    cheap = PlayerSnapshot(
        id=13, position=Position.DE, overall_rating=86, age=25, contract_years=3, annual_base_salary=2_000_000
    )
    expensive = PlayerSnapshot(
        id=14, position=Position.DE, overall_rating=86, age=25, contract_years=3, annual_base_salary=20_000_000
    )
    assert calculate_player_market_tvp(cheap).base_market_tvp > calculate_player_market_tvp(expensive).base_market_tvp


def test_rb_age_cliff_vs_qb_longevity_ratio():
    """
    Verify:
    - An RB at age 29 has < 60% of the TVP of an identical RB at age 24.
    - A QB at age 33 has > 75% of the TVP of an identical QB at age 28.
    """
    rb_24 = PlayerSnapshot(
        id=20,
        position=Position.RB,
        overall_rating=88,
        age=24,
        contract_years=3,
        annual_base_salary=8_000_000,
        development_trait=DevelopmentTrait.STAR,
    )
    rb_29 = PlayerSnapshot(
        id=21,
        position=Position.RB,
        overall_rating=88,
        age=29,
        contract_years=3,
        annual_base_salary=8_000_000,
        development_trait=DevelopmentTrait.STAR,
    )
    rb_24_tvp = calculate_player_market_tvp(rb_24).base_market_tvp
    rb_29_tvp = calculate_player_market_tvp(rb_29).base_market_tvp
    assert rb_29_tvp < 0.60 * rb_24_tvp, f"RB 29 TVP ({rb_29_tvp}) not < 60% of RB 24 TVP ({rb_24_tvp})"

    qb_28 = PlayerSnapshot(
        id=22,
        position=Position.QB,
        overall_rating=88,
        age=28,
        contract_years=3,
        annual_base_salary=35_000_000,
        development_trait=DevelopmentTrait.STAR,
    )
    qb_33 = PlayerSnapshot(
        id=23,
        position=Position.QB,
        overall_rating=88,
        age=33,
        contract_years=3,
        annual_base_salary=35_000_000,
        development_trait=DevelopmentTrait.STAR,
    )
    qb_28_tvp = calculate_player_market_tvp(qb_28).base_market_tvp
    qb_33_tvp = calculate_player_market_tvp(qb_33).base_market_tvp
    assert qb_33_tvp > 0.75 * qb_28_tvp, f"QB 33 TVP ({qb_33_tvp}) not > 75% of QB 28 TVP ({qb_28_tvp})"


def test_overpaid_sub_starter_has_negative_tvp_salary_dump():
    """Overpaid sub-starter (68 OVR on $18M salary) yields negative base_market_tvp < 0."""
    albatross = PlayerSnapshot(
        id=30,
        position=Position.WR,
        overall_rating=68,
        age=29,
        contract_years=2,
        annual_base_salary=18_000_000,
    )
    breakdown = calculate_player_market_tvp(albatross)
    assert breakdown.base_market_tvp < 0.0
