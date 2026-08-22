"""
Unit Tests for Simulation Subsystems Deep Dive
==============================================
Tests for:
1. ScoutingLensService
2. CoachingDynastyService
3. OrthopedicTriageService
"""

import pytest
from app.schemas.deep_dive import (
    ScoutBiasLens,
    MedicalProtocolType,
    CoachingBranch,
)
from app.services.draft.scouting_lens_service import scouting_lens_service
from app.services.coaching.coaching_dynasty_service import coaching_dynasty_service
from app.services.medical.orthopedic_triage_service import orthopedic_triage_service


# ============================================================================
# 1. SCOUTING LENS & DRAFT AI TESTS
# ============================================================================

def test_scouting_lens_evaluate_prospect():
    """Verify multi-lens evaluation produces distinct perceived ratings."""
    prospect = scouting_lens_service.evaluate_prospect(
        prospect_id=101,
        name="Caleb Williams",
        position="QB",
        college="USC",
        true_ovr=88,
        s2_score=94,
        gps_speed_max=21.4,
        burst_score=89.0,
        scheme_fit_pct=92,
    )

    assert prospect.id == 101
    assert prospect.name == "Caleb Williams"
    assert prospect.position == "QB"
    assert len(prospect.perceived_ovr) == 4
    assert ScoutBiasLens.CONSENSUS.value in prospect.perceived_ovr
    assert ScoutBiasLens.FILM_TRADITIONALIST.value in prospect.perceived_ovr
    assert ScoutBiasLens.ANALYTICS_METRICS.value in prospect.perceived_ovr
    assert ScoutBiasLens.REGIONAL_SCOUT.value in prospect.perceived_ovr
    assert prospect.draft_projection_round in [1, 2]
    assert 0.0 <= prospect.boom_bust_factor <= 1.0


def test_draft_trade_urgency_calculation():
    """Verify dynamic trade-up urgency scales with positional scarcity."""
    qb_urgency = scouting_lens_service.calculate_trade_urgency(
        team_id="ATL",
        target_position="QB",
        roster_need_score=0.9,
        remaining_in_tier=1,
        current_pick=8,
    )

    g_urgency = scouting_lens_service.calculate_trade_urgency(
        team_id="ATL",
        target_position="OG",
        roster_need_score=0.4,
        remaining_in_tier=5,
        current_pick=8,
    )

    # QB with 1 prospect remaining in tier should have higher urgency than Guard with 5 remaining
    assert qb_urgency.urgency_index > g_urgency.urgency_index
    assert qb_urgency.willing_to_overpay_pct >= g_urgency.willing_to_overpay_pct
    assert qb_urgency.suggested_package_value > 0


# ============================================================================
# 2. COACHING DYNASTY & STAFF CHEMISTRY TESTS
# ============================================================================

def test_coaching_dynasty_profile_and_unlock():
    """Verify 3-branch skill tree prerequisites and SP deduction."""
    profile = coaching_dynasty_service.get_coach_profile(
        coach_id="HC-DAN-CAMPBELL",
        name="Dan Campbell",
        role="Head Coach",
        level=10,
        current_sp=3,
        unlocked_node_ids=["SCHEME_DISGUISE_I"],
    )

    assert "SCHEME_MATCHUP_NIGHTMARE" in profile.tree_nodes
    assert profile.tree_nodes["SCHEME_DISGUISE_I"].unlocked is True
    assert profile.tree_nodes["SCHEME_MATCHUP_NIGHTMARE"].unlocked is False

    # Attempt unlock with sufficient SP and satisfied prerequisite
    success = coaching_dynasty_service.unlock_node(profile, "SCHEME_MATCHUP_NIGHTMARE")
    assert success is True
    assert profile.tree_nodes["SCHEME_MATCHUP_NIGHTMARE"].unlocked is True
    assert profile.current_sp == 1 # 3 - 2 = 1

    # Attempt unlock of Tier 3 without enough SP (requires 3 SP, only 1 left)
    fail_sp = coaching_dynasty_service.unlock_node(profile, "SCHEME_FOURTH_DOWN_ALGO")
    assert fail_sp is False


def test_staff_synergy_breakdown():
    """Verify staff scheme compatibility scores and perks."""
    perfect_staff = coaching_dynasty_service.calculate_staff_synergy(
        hc_scheme="WEST_COAST",
        oc_scheme="WEST_COAST",
        dc_scheme="COVER_3_ZONE",
    )

    clashing_staff = coaching_dynasty_service.calculate_staff_synergy(
        hc_scheme="WEST_COAST",
        oc_scheme="AIR_RAID",
        dc_scheme="COVER_3_ZONE",
    )

    assert perfect_staff.offensive_synergy_score > clashing_staff.offensive_synergy_score
    assert perfect_staff.overall_chemistry_score >= 85
    assert len(perfect_staff.active_synergy_perks) >= 1


# ============================================================================
# 3. ORTHOPEDIC TRAUMA TRIAGE TESTS
# ============================================================================

def test_orthopedic_triage_protocols():
    """Verify 5 medical protocol options and clinical estimates."""
    options = orthopedic_triage_service.get_protocol_options(
        zone_key="leftLeg",
        current_integrity=45.0,
        baseline_weeks=6,
        player_age=24,
        is_x_factor=True,
    )

    assert len(options) == 5
    rest = next(o for o in options if o.protocol == MedicalProtocolType.REST)
    prp = next(o for o in options if o.protocol == MedicalProtocolType.PRP_THERAPY)
    arthro = next(o for o in options if o.protocol == MedicalProtocolType.ARTHROSCOPIC_SURGERY)
    play_through = next(o for o in options if o.protocol == MedicalProtocolType.CORTISONE_STABILIZATION)

    # Rest has 0% complication risk
    assert rest.complication_risk_pct == 0.0
    # PRP is faster than Rest
    assert prp.estimated_recovery_weeks <= rest.estimated_recovery_weeks
    # Arthro is faster than PRP
    assert arthro.estimated_recovery_weeks <= prp.estimated_recovery_weeks
    # Play through has 0 recovery weeks and QUESTIONABLE status
    assert play_through.estimated_recovery_weeks == 0
    assert play_through.game_availability_status == "QUESTIONABLE"


def test_orthopedic_triage_application():
    """Verify triage decision execution and probabilistic forecasting."""
    result = orthopedic_triage_service.apply_triage_protocol(
        player_id=99,
        zone_key="rightArm",
        protocol=MedicalProtocolType.PRP_THERAPY,
        baseline_weeks=4,
        player_age=25,
        toughness=90,
    )

    assert result.player_id == 99
    assert result.zone_key == "rightArm"
    assert result.protocol_applied == MedicalProtocolType.PRP_THERAPY
    assert result.projected_recovery_weeks >= 1
    assert result.final_integrity_forecast > 0.0
    assert result.message is not None
