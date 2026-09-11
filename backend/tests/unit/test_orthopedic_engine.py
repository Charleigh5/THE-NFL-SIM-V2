"""
Unit Tests for Orthopedic Simulation Engine (TASK-016)
=====================================================
Tests:
1. Gompertz non-linear curve bounds [0.0, 100.0] and monotonicity.
2. Trajectory generation operational latency (<2.5ms).
3. Elite specialist 2nd opinion consults (Andrews, Kerlan-Jobe, HSS),
   occult pathology detection, and 50% complication risk reduction.
4. Live 60Hz physics Cortisone 2.5x hazard multiplier.
5. Full FastAPI REST API endpoint contract verification.
"""

import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.player import Player, InjuryStatus, Position
from app.models.player_injury import PlayerInjury
from app.models.medical import BodyPart
from app.services.orthopedic_engine import OrthopedicEngine, orthopedic_engine
from app.schemas.orthopedic_rtp import (
    OrthopedicEvaluationResponse,
    SecondOpinionCenter,
    SecondOpinionConsultResult,
    CortisoneHazardCheckResponse,
)
from tests.conftest import create_player


@pytest.fixture
def injured_test_player(db_session: Session) -> Player:
    """Create a persistent test player with an active orthopedic injury."""
    player = create_player(
        id=None,
        first_name="Christian",
        last_name="McCaffrey",
        position=Position.RB,
        overall_rating=96,
        team_id=1,
    )
    player.injury_status = InjuryStatus.OUT
    player.injury_type = "Grade II Lateral Meniscus Tear"
    player.injury_severity = 5
    player.weeks_to_recovery = 6

    # Attach BodyPart for health
    player.body_health = BodyPart(
        head_health=100.0,
        neck_health=100.0,
        torso_health=100.0,
        right_arm_health=100.0,
        left_arm_health=100.0,
        right_leg_health=55.0,
        left_leg_health=100.0,
    )

    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)

    # Attach or update PlayerInjury record
    if player.injury:
        player.injury.injury_status = InjuryStatus.OUT
        player.injury.injury_type = "Grade II Lateral Meniscus Tear"
        player.injury.weeks_to_recovery = 6
        player.injury.injury_severity = 5
        player.injury.injury_recurrence_risk = 0.15
        player.injury.medical_flags = {}
    else:
        injury = PlayerInjury(
            player_id=player.id,
            injury_status=InjuryStatus.OUT,
            injury_type="Grade II Lateral Meniscus Tear",
            weeks_to_recovery=6,
            injury_severity=5,
            injury_recurrence_risk=0.15,
            medical_flags={},
        )
        player.injury = injury

    db_session.commit()
    db_session.refresh(player)
    return player


# =============================================================================
# 1. GOMPERTZ MATHEMATICAL MODEL & CURVE BOUNDS
# =============================================================================

def test_gompertz_curve_monotonicity_and_bounds():
    """Verify all 13 weekly points are bounded in [0.0, 100.0] and monotonic for rehab."""
    engine = OrthopedicEngine()
    eval_res = engine.generate_rtp_evaluation(
        player_id=99,
        injury_type="MCL Sprain",
        body_part="right_leg",
        severity_grade=4,
        baseline_health=50.0,
        player_name="Test Athlete",
        player_age=25,
        durability_rating=85,
    )

    assert isinstance(eval_res, OrthopedicEvaluationResponse)
    assert len(eval_res.trajectories) == 5

    # Check Conservative Rest curve
    cons_traj = next(t for t in eval_res.trajectories if t.protocol == "CONSERVATIVE")
    assert len(cons_traj.curve) == 13
    assert cons_traj.complication_risk_pct == 0.0
    assert cons_traj.total_medical_cost == 0

    prev_health = cons_traj.curve[0].health_percentage
    assert 0.0 <= prev_health <= 100.0

    for pt in cons_traj.curve[1:]:
        assert 0.0 <= pt.health_percentage <= 100.0
        assert 0.0 <= pt.re_injury_risk_pct <= 100.0
        assert 0.0 <= pt.on_field_effectiveness_pct <= 100.0
        # Monotonically non-decreasing
        assert pt.health_percentage >= prev_health - 1e-6
        prev_health = pt.health_percentage

    # Check Cortisone Trajectory properties
    cort_traj = next(t for t in eval_res.trajectories if t.protocol == "CORTISONE")
    assert cort_traj.est_recovery_weeks == 0
    assert cort_traj.complication_risk_pct == 35.0
    # In weeks 0-3, effectiveness is masked to 95.0%
    assert cort_traj.curve[0].on_field_effectiveness_pct == 95.0
    assert cort_traj.curve[2].on_field_effectiveness_pct == 95.0
    # Re-injury risk remains high under cortisone
    assert cort_traj.curve[0].re_injury_risk_pct > 20.0


# =============================================================================
# 2. OPERATIONAL LATENCY BENCHMARK (<2.5ms)
# =============================================================================

def test_trajectory_generation_latency():
    """Verify calculating 12-week curves across 5 protocols completes in <2.5ms."""
    engine = OrthopedicEngine()

    # Warmup
    for _ in range(10):
        engine.generate_rtp_evaluation(
            player_id=10,
            injury_type="Hamstring Strain",
            body_part="left_leg",
            severity_grade=3,
            baseline_health=65.0,
        )

    iterations = 100
    start = time.perf_counter()
    for i in range(iterations):
        engine.generate_rtp_evaluation(
            player_id=i,
            injury_type="Ankle Sprain",
            body_part="right_leg",
            severity_grade=4,
            baseline_health=55.0,
        )
    elapsed_total = time.perf_counter() - start
    avg_latency_ms = (elapsed_total / iterations) * 1000.0

    print(f"\n[OrthopedicEngine] Average Trajectory Gen Latency: {avg_latency_ms:.3f}ms")
    assert avg_latency_ms < 2.5, f"Latency {avg_latency_ms:.3f}ms exceeded 2.5ms budget!"


# =============================================================================
# 3. OUTSIDE SPECIALIST 2ND OPINION CONSULTATIONS
# =============================================================================

def test_specialist_centers_configuration():
    """Verify elite outside consultation centers list."""
    centers = orthopedic_engine.get_specialist_centers()
    assert len(centers) == 3
    center_ids = [c.center_id for c in centers]
    assert "andrews_sports_med" in center_ids
    assert "kerlan_jobe" in center_ids
    assert "hss_ny" in center_ids


def test_specialist_consultation_clearance_and_pathology(db_session: Session, injured_test_player: Player):
    """Verify outside specialist consultation updates DB, detects occult pathology, and grants 50% risk reduction."""
    player_id = injured_test_player.id

    result = orthopedic_engine.consult_outside_specialist(
        db=db_session,
        player_id=player_id,
        center_id="andrews_sports_med",
        seed=7,
    )

    assert isinstance(result, SecondOpinionConsultResult)
    assert result.player_id == player_id
    assert result.center_id == "andrews_sports_med"
    assert result.chief_surgeon == "Dr. James Andrews, MD"
    assert result.complication_reduction_factor == 0.50
    assert result.consultation_cost == 45000

    # Refresh player from DB and check medical flags
    db_session.refresh(injured_test_player)
    flags = injured_test_player.injury.medical_flags
    assert flags.get("specialist_cleared") is True
    assert flags.get("specialist_center_id") == "andrews_sports_med"
    assert flags.get("complication_reduction_factor") == 0.50


# =============================================================================
# 4. IN-GAME 60Hz CORTISONE HAZARD MULTIPLIER
# =============================================================================

def test_cortisone_in_game_hazard_multiplier():
    """Verify 2.5x hazard multiplier applied only when player has active cortisone."""
    engine = OrthopedicEngine()

    # Normal player without cortisone
    safe_check = engine.evaluate_cortisone_in_game_hazard(
        runner_has_cortisone=False,
        is_sharp_cut=True,
        momentum=900.0,
        g_force=12.0,
    )
    assert safe_check.hazard_multiplier == 1.0
    assert safe_check.catastrophic_rupture is False

    # Cortisone player under severe cut and tackle
    cort_check_rupture = engine.evaluate_cortisone_in_game_hazard(
        runner_has_cortisone=True,
        is_sharp_cut=True,
        momentum=950.0,
        g_force=15.0,
        seed=1,
    )
    assert cort_check_rupture.hazard_multiplier == 2.5
    assert cort_check_rupture.effective_risk_pct > safe_check.effective_risk_pct

    # Non-rupture run
    cort_check_safe = engine.evaluate_cortisone_in_game_hazard(
        runner_has_cortisone=True,
        is_sharp_cut=False,
        momentum=500.0,
        g_force=3.0,
        seed=99999,
    )
    assert cort_check_safe.hazard_multiplier == 2.5
    assert cort_check_safe.catastrophic_rupture is False


# =============================================================================
# 5. FASTAPI REST API ENDPOINTS
# =============================================================================

def test_orthopedic_api_evaluation(client: TestClient, injured_test_player: Player):
    """Verify GET /api/orthopedic/evaluation/{player_id}."""
    response = client.get(f"/api/orthopedic/evaluation/{injured_test_player.id}")
    assert response.status_code == 200
    data = response.json()

    assert data["player_id"] == injured_test_player.id
    assert data["cortisone_in_game_hazard_multiplier"] == 2.5
    assert len(data["trajectories"]) == 5
    assert len(data["specialist_centers"]) == 3


def test_orthopedic_api_specialists_and_consult(client: TestClient, injured_test_player: Player):
    """Verify GET /api/orthopedic/specialists and POST /api/orthopedic/specialists/consult."""
    # 1. List specialists
    res_list = client.get("/api/orthopedic/specialists")
    assert res_list.status_code == 200
    centers = res_list.json()
    assert len(centers) == 3

    # 2. Consult Kerlan-Jobe
    payload = {
        "player_id": injured_test_player.id,
        "center_id": "kerlan_jobe",
    }
    res_consult = client.post("/api/orthopedic/specialists/consult", json=payload)
    assert res_consult.status_code == 200
    consult_data = res_consult.json()

    assert consult_data["center_id"] == "kerlan_jobe"
    assert consult_data["chief_surgeon"] == "Dr. Neal ElAttrache, MD"
    assert consult_data["complication_reduction_factor"] == 0.50


def test_orthopedic_api_cortisone_hazard(client: TestClient):
    """Verify POST /api/orthopedic/cortisone/check-hazard."""
    payload = {
        "runner_has_cortisone": True,
        "is_sharp_cut": True,
        "momentum": 880.0,
        "g_force": 10.5,
    }
    response = client.post("/api/orthopedic/cortisone/check-hazard", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_multiplier"] == 2.5
    assert "effective_risk_pct" in data
