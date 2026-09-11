"""
Unit Tests for Medical Backend Repairs & In-Game Play-Calling HUD (TASK-012 & TASK-013)
======================================================================================
Tests:
1. Ben Baldwin 4th-down decision modeling accuracy, win probabilities, and <10ms latency.
2. Medical player status enum fix (InjuryStatus.ACTIVE not marked as injured).
3. Medical scalar BodyPart subscript fix in MedicalService (no TypeError on scalar object).
4. Orthopedic triage persistence: final_integrity_forecast saved to body_health and InjuryEvent inserted.
5. In-game play-calling and timeout REST endpoints.
"""

import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import SessionLocal
from app.models.player import Player, InjuryStatus, Position
from app.models.player_attributes import PlayerAttributes
from app.models.player_injury import PlayerInjury
from app.models.medical import BodyPart, InjuryEvent
from app.services.medical_service import MedicalService
from app.engine.fourth_down_calculator import FourthDownCalculator, FourthDownRecommendation
from app.schemas.deep_dive import MedicalProtocolType
from tests.conftest import create_player


# =============================================================================
# 1. BEN BALDWIN 4TH-DOWN MODEL & LATENCY TESTS (TASK-013)
# =============================================================================

def test_baldwin_fourth_down_short_yardage_optimal_go():
    """Verify 4th & 1 in plus territory recommends GO with high win probability."""
    # 4th & 1 at opponent's 40-yard line (yardline = 60 from own endzone)
    rec = FourthDownCalculator.evaluate(
        down=4,
        distance=1,
        yardline=60,
        score_diff=0,
        time_remaining=1200,
        timeouts=3,
    )

    assert isinstance(rec, FourthDownRecommendation)
    assert rec.recommendation == "GO"
    assert rec.conversion_prob >= 0.70  # ~76% on 4th & 1
    assert rec.wp_go > rec.wp_punt
    assert rec.wp_go > rec.wp_fg
    assert rec.ep_go > rec.ep_punt
    assert "STRONG_GO" in rec.recommendation_strength or "LEAN_GO" in rec.recommendation_strength
    assert "Go for it" in rec.summary


def test_baldwin_fourth_down_long_distance_own_territory_punt():
    """Verify 4th & 12 backed up in own territory recommends PUNT."""
    # 4th & 12 at own 15-yard line
    rec = FourthDownCalculator.evaluate(
        down=4,
        distance=12,
        yardline=15,
        score_diff=0,
        time_remaining=1800,
        timeouts=3,
    )

    assert rec.recommendation == "PUNT"
    assert rec.conversion_prob < 0.25
    assert rec.wp_punt > rec.wp_go
    assert rec.ep_punt > rec.ep_go
    assert "PUNT" in rec.recommendation_strength
    assert "Punt" in rec.summary


def test_baldwin_fourth_down_red_zone_field_goal():
    """Verify 4th & 8 at opponent 15 recommends FIELD GOAL."""
    # 4th & 8 at opponent 15 (yardline = 85 from own endzone)
    rec = FourthDownCalculator.evaluate(
        down=4,
        distance=8,
        yardline=85,
        score_diff=0,
        time_remaining=1800,
        timeouts=3,
    )

    assert rec.recommendation == "FIELD_GOAL"
    assert rec.fg_distance == 32  # 15 + 17
    assert rec.fg_make_prob >= 0.85
    assert rec.wp_fg > rec.wp_go
    assert rec.wp_fg > rec.wp_punt


def test_baldwin_fourth_down_late_game_trailing_urgency():
    """Verify trailing by 5 late in 4th quarter penalizes punting and favors going for it."""
    # Trailing by 5, 4th & 4 at midfield, 120 seconds left
    rec = FourthDownCalculator.evaluate(
        down=4,
        distance=4,
        yardline=50,
        score_diff=-5,
        time_remaining=120,
        timeouts=1,
    )

    assert rec.recommendation == "GO"
    # Punting when trailing with 2 mins remaining should have abysmal WP
    assert rec.wp_punt < 0.20
    assert rec.wp_go > rec.wp_punt


def test_baldwin_fourth_down_latency_budget_strictly_under_10ms():
    """Benchmark 200 consecutive evaluations to prove lookup latency is strictly < 10ms."""
    scenarios = [
        (4, 1, 60, 0, 1200, 3),
        (4, 2, 75, -3, 300, 2),
        (4, 10, 25, 7, 1800, 3),
        (4, 5, 55, -4, 90, 1),
        (4, 3, 90, 3, 45, 0),
    ]

    durations = []
    for _ in range(40):
        for down, dist, ydl, diff, time_rem, to in scenarios:
            t0 = time.perf_counter()
            rec = FourthDownCalculator.evaluate(
                down=down,
                distance=dist,
                yardline=ydl,
                score_diff=diff,
                time_remaining=time_rem,
                timeouts=to,
            )
            t1 = time.perf_counter()
            elapsed_ms = (t1 - t0) * 1000.0
            durations.append(elapsed_ms)
            assert rec.recommendation in ("GO", "FIELD_GOAL", "PUNT")

    max_ms = max(durations)
    avg_ms = sum(durations) / len(durations)

    # Mandatory requirement: strictly < 10.0 ms
    assert max_ms < 10.0, f"Max latency was {max_ms:.3f}ms, exceeding 10ms budget"
    # Analytical math runs in sub-millisecond range
    assert avg_ms < 1.0, f"Average latency was {avg_ms:.3f}ms, exceeding 1ms"


# =============================================================================
# 2. MEDICAL STATUS ENUM FIX TESTS (TASK-012)
# =============================================================================

def test_medical_active_player_is_not_injured(client: TestClient, db_session: Session):
    """Verify player with InjuryStatus.ACTIVE has is_injured=False on /api/medical/player/{id}."""
    # Create healthy player using factory
    player = create_player(
        id=None,
        first_name="Healthy",
        last_name="Athlete",
        position="QB",
        team_id=1,
    )
    player.injury_status = InjuryStatus.ACTIVE
    player.weeks_to_recovery = 0
    player.body_health = BodyPart(
        head_health=100.0,
        neck_health=100.0,
        torso_health=100.0,
        right_arm_health=100.0,
        left_arm_health=100.0,
        right_leg_health=100.0,
        left_leg_health=100.0,
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)

    response = client.get(f"/api/medical/player/{player.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == player.id
    # Critical test: was previously True because player.injury_status != "HEALTHY"
    assert data["is_injured"] is False


def test_medical_out_player_is_injured(client: TestClient, db_session: Session):
    """Verify player with InjuryStatus.OUT has is_injured=True."""
    player = create_player(
        id=None,
        first_name="Injured",
        last_name="Star",
        position="WR",
        team_id=1,
    )
    player.injury_status = InjuryStatus.OUT
    player.injury_type = "Hamstring Strain"
    player.weeks_to_recovery = 3
    player.body_health = BodyPart(
        right_leg_health=55.0,
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)

    response = client.get(f"/api/medical/player/{player.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_injured"] is True


# =============================================================================
# 3. MEDICAL SCALAR SUBSCRIPT FIX TESTS (TASK-012)
# =============================================================================

def test_medical_service_scalar_body_health_no_subscript_typeerror(db_session: Session):
    """Verify MedicalService operates on 1:1 scalar player.body_health without TypeError."""
    player = create_player(
        id=None,
        first_name="Tough",
        last_name="Lineman",
        position="OG",
        team_id=1,
    )
    # Assign single scalar BodyPart instance (uselist=False in Player model)
    player.body_health = BodyPart(
        head_health=95.0,
        torso_health=92.0,
        right_leg_health=90.0,
        left_leg_health=90.0,
        general_wear=5.0,
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)

    # Verify relationship is a scalar BodyPart object, NOT a list
    assert not isinstance(player.body_health, list)
    assert isinstance(player.body_health, BodyPart)

    service = MedicalService(db_session)

    # Should execute without TypeError: 'BodyPart' object is not subscriptable
    service.apply_game_wear(player, snaps_played=60, position="OG")
    assert player.body_health.general_wear > 5.0

    # Test weekly recovery on scalar object
    service.process_weekly_recovery(player.id)
    db_session.refresh(player)
    assert player.body_health is not None


# =============================================================================
# 4. TRIAGE PERSISTENCE & INJURY EVENT TESTS (TASK-012)
# =============================================================================

def test_apply_player_triage_protocol_persists_forecast_and_injury_event(
    client: TestClient, db_session: Session
):
    """Verify /api/medical/players/{id}/triage/apply persists final_integrity_forecast and inserts InjuryEvent."""
    player = create_player(
        id=None,
        first_name="Christian",
        last_name="McCaffrey",
        position="RB",
        team_id=1,
    )
    player.injury_status = InjuryStatus.OUT
    player.injury_type = "Right Knee Meniscus Tear"
    player.injury_severity = 3
    player.weeks_to_recovery = 4
    player.body_health = BodyPart(
        right_leg_health=45.0,
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)

    # Apply accelerated arthroscopic repair protocol
    payload = {
        "protocol": MedicalProtocolType.ARTHROSCOPIC_SURGERY.value,
        "zone_key": "right_leg",
    }
    response = client.post(
        f"/api/medical/players/{player.id}/triage/apply",
        json=payload,
    )
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["player_id"] == player.id
    assert res_data["protocol_applied"] == MedicalProtocolType.ARTHROSCOPIC_SURGERY.value
    assert res_data["final_integrity_forecast"] > 0

    # Check persistence in database
    db_session.expire_all()
    updated_player = db_session.query(Player).filter(Player.id == player.id).first()
    assert updated_player is not None
    # 1. Verify player recovery timetable updated
    assert updated_player.weeks_to_recovery == res_data["projected_recovery_weeks"]
    # 2. Verify zone integrity forecast was saved to body_health
    assert updated_player.body_health.right_leg_health == res_data["final_integrity_forecast"]
    # 3. Verify InjuryEvent record was inserted
    events = db_session.query(InjuryEvent).filter(InjuryEvent.player_id == player.id).all()
    assert len(events) >= 1
    event = events[-1]
    assert event.player_id == player.id
    assert event.body_part == "right_leg"
    assert event.treatment_chosen == MedicalProtocolType.ARTHROSCOPIC_SURGERY.value
    assert event.duration_weeks == res_data["projected_recovery_weeks"]


# =============================================================================
# 5. PLAYCALLING & 4TH-DOWN API ENDPOINT TESTS (TASK-013)
# =============================================================================

def test_api_fourth_down_recommendation_endpoint(client: TestClient):
    """Verify POST /api/playcalling/fourth-down-recommendation returns complete analytics."""
    payload = {
        "down": 4,
        "distance": 1,
        "yardline": 65,
        "score_diff": -3,
        "time_remaining": 600,
        "timeouts": 2,
    }
    response = client.post("/api/playcalling/fourth-down-recommendation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommendation"] == "GO"
    assert "wp_go" in data
    assert "wp_fg" in data
    assert "wp_punt" in data
    assert "conversion_prob" in data
    assert "fg_make_prob" in data
    assert "recommendation_strength" in data
    assert "summary" in data


def test_api_call_play_endpoint(client: TestClient):
    """Verify POST /api/playcalling/call-play queues play call."""
    payload = {
        "game_id": 1,
        "team_id": 1,
        "play_type": "PASS",
        "concept_id": "mesh",
        "tempo": "NORMAL",
    }
    response = client.post("/api/playcalling/call-play", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["play_type"] == "PASS"
    assert data["concept_id"] == "mesh"


def test_api_timeout_endpoint(client: TestClient):
    """Verify POST /api/playcalling/timeout processes sideline timeout."""
    payload = {"game_id": 1, "team_id": 1}
    response = client.post("/api/playcalling/timeout", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["team_id"] == 1
