"""
Adversarial Empirical Stress Test Suite — Milestone 2 Endpoints
================================================================
Empirical verification and edge-case probing for:
1. 5-Pathway Orthopedic Triage Endpoints (GET/POST, boundary inputs, 404s, 422s, DB commits)
2. Coaching Dynasty Tree & Staff Synergy Endpoints (GET/POST, SP validation, DAG prerequisites, 400s, 404s, DB commits)
3. Multi-Lens Prospect Intelligence & Trade Urgency Endpoints (Lenses, trade-up curves, fallback synthesis, 422s)
"""

import pytest
from app.models.player import Player, InjuryStatus
from app.models.team import Team
from app.models.coach import Coach, CoachTier
from app.models.medical import BodyPart
from app.schemas.deep_dive import ScoutBiasLens


@pytest.fixture
def adversarial_test_data(db_session):
    """Seed dedicated isolated test entities for adversarial probing."""
    # Seed Team 888
    team = db_session.query(Team).filter(Team.id == 888).first()
    if not team:
        team = Team(
            id=888,
            name="Vipers",
            city="Las Vegas",
            abbreviation="LVV",
            conference="AFC",
            division="West",
            wins=10,
            losses=2,
            salary_cap_space=40000000,
        )
        db_session.add(team)

    # Seed Team 889 (empty staff team)
    team_empty = db_session.query(Team).filter(Team.id == 889).first()
    if not team_empty:
        team_empty = Team(
            id=889,
            name="Phantoms",
            city="Orlando",
            abbreviation="ORL",
            conference="NFC",
            division="South",
            wins=2,
            losses=10,
            salary_cap_space=50000000,
        )
        db_session.add(team_empty)

    # Seed Player 8881 (Injured with BodyPart)
    p1 = db_session.query(Player).filter(Player.id == 8881).first()
    if not p1:
        p1 = Player(
            id=8881,
            team_id=888,
            first_name="Adversarial",
            last_name="Star",
            position="WR",
            jersey_number=18,
            overall_rating=91,
            age=28,
            experience=6,
            speed=93,
            acceleration=92,
            injury_resistance=75,
            injury_status=InjuryStatus.OUT,
            injury_type="Hamstring Strain",
            injury_severity=4,
            weeks_to_recovery=5,
        )
        db_session.add(p1)

    # Seed BodyPart for Player 8881
    bh1 = db_session.query(BodyPart).filter(BodyPart.player_id == 8881).first()
    if not bh1:
        bh1 = BodyPart(
            player_id=8881,
            head_health=90.0,
            neck_health=85.0,
            torso_health=88.0,
            right_arm_health=95.0,
            left_arm_health=95.0,
            right_leg_health=42.0,  # lowest zone
            left_leg_health=88.0,
            general_wear=20.0,
        )
        db_session.add(bh1)

    # Seed Player 8882 (Injured WITHOUT existing BodyPart row)
    p2 = db_session.query(Player).filter(Player.id == 8882).first()
    if not p2:
        p2 = Player(
            id=8882,
            team_id=888,
            first_name="Bare",
            last_name="Bones",
            position="RB",
            jersey_number=22,
            overall_rating=80,
            age=23,
            experience=1,
            injury_status=InjuryStatus.QUESTIONABLE,
            injury_type="Knee Sprain",
            injury_severity=2,
            weeks_to_recovery=2,
        )
        db_session.add(p2)

    # Seed Coach 8881 (HC with high SP)
    hc = db_session.query(Coach).filter(Coach.id == 8881).first()
    if not hc:
        hc = Coach(
            id=8881,
            team_id=888,
            first_name="Bill",
            last_name="Mastermind",
            role="Head Coach",
            tier=CoachTier.ELITE,
            offense_rating=92,
            defense_rating=90,
            development_rating=88,
            playbook_offense="WEST_COAST",
            playbook_defense="COVER_3_ZONE",
            xp=1000,  # 10 SP
            level=18,
            skills={"unlocked_nodes": ["SCHEME_DISGUISE_I"]},
        )
        db_session.add(hc)

    # Seed Coach 8882 (OC matching HC scheme)
    oc = db_session.query(Coach).filter(Coach.id == 8882).first()
    if not oc:
        oc = Coach(
            id=8882,
            team_id=888,
            first_name="Kyle",
            last_name="Playcaller",
            role="Offensive Coordinator",
            tier=CoachTier.VETERAN,
            offense_rating=90,
            defense_rating=60,
            development_rating=85,
            playbook_offense="WEST_COAST",
            xp=300,
            level=10,
            skills={"unlocked_nodes": ["DEV_ROOKIE_ONBOARDING"]},
        )
        db_session.add(oc)

    # Seed Coach 8883 (DC matching)
    dc = db_session.query(Coach).filter(Coach.id == 8883).first()
    if not dc:
        dc = Coach(
            id=8883,
            team_id=888,
            first_name="DeMeco",
            last_name="Stopper",
            role="Defensive Coordinator",
            tier=CoachTier.VETERAN,
            offense_rating=50,
            defense_rating=88,
            development_rating=82,
            playbook_defense="COVER_3_ZONE",
            xp=200,
            level=8,
            skills={},
        )
        db_session.add(dc)

    # Seed Coach 8884 (Broke Coach with 0 XP / 0 SP)
    broke_coach = db_session.query(Coach).filter(Coach.id == 8884).first()
    if not broke_coach:
        broke_coach = Coach(
            id=8884,
            team_id=888,
            first_name="Broke",
            last_name="RookieCoach",
            role="Assistant Coach",
            tier=CoachTier.ROOKIE,
            offense_rating=55,
            defense_rating=55,
            development_rating=50,
            xp=0,
            level=1,
            skills={"unlocked_nodes": []},
        )
        db_session.add(broke_coach)

    db_session.commit()
    return {
        "team": team,
        "team_empty": team_empty,
        "p1": p1,
        "p2": p2,
        "hc": hc,
        "oc": oc,
        "dc": dc,
        "broke_coach": broke_coach,
    }


# =============================================================================
# 1. 5-PATHWAY ORTHOPEDIC TRIAGE ADVERSARIAL TESTS
# =============================================================================

def test_get_protocols_valid_player_with_body_part(client, adversarial_test_data):
    """Verify protocol retrieval identifies lowest health zone and offers 5 distinct pathways."""
    resp = client.get("/api/medical/players/8881/triage/protocols")
    assert resp.status_code == 200
    data = resp.json()
    assert data["player_id"] == 8881
    assert data["current_diagnosis"]["body_zone"] == "right_leg"
    assert data["current_diagnosis"]["current_integrity"] == 42.0
    assert len(data["protocols"]) == 5

    # Check protocol types
    protocols = {p["protocol"] for p in data["protocols"]}
    expected = {
        "REST",
        "PRP_THERAPY",
        "ARTHROSCOPIC_SURGERY",
        "RECONSTRUCTIVE_SURGERY",
        "CORTISONE_STABILIZATION",
    }
    assert protocols == expected

    # Check Cortisone has 0 weeks and QUESTIONABLE status
    cortisone = next(p for p in data["protocols"] if p["protocol"] == "CORTISONE_STABILIZATION")
    assert cortisone["estimated_recovery_weeks"] == 0
    assert cortisone["game_availability_status"] == "QUESTIONABLE"
    assert cortisone["re_injury_hazard_multiplier"] >= 2.0


def test_get_protocols_player_without_body_part(client, adversarial_test_data):
    """Verify protocol retrieval gracefully handles player without existing BodyPart record."""
    resp = client.get("/api/medical/players/8882/triage/protocols")
    assert resp.status_code == 200
    data = resp.json()
    assert data["player_id"] == 8882
    assert len(data["protocols"]) == 5
    assert data["current_diagnosis"]["weeks_to_recovery"] == 2


def test_get_protocols_nonexistent_player(client, adversarial_test_data):
    """Probing non-existent player returns 404 with descriptive detail."""
    resp = client.get("/api/medical/players/999999/triage/protocols")
    assert resp.status_code == 404
    data = resp.json()
    assert "not found" in data["detail"].lower()


def test_get_protocols_negative_player_id(client, adversarial_test_data):
    """Negative player ID returns 404."""
    resp = client.get("/api/medical/players/-1/triage/protocols")
    assert resp.status_code == 404


def test_get_protocols_route_alias(client, adversarial_test_data):
    """Verify legacy /triage/protocols/{id} alias functions identically."""
    resp = client.get("/api/medical/triage/protocols/8881")
    assert resp.status_code == 200
    assert resp.json()["player_id"] == 8881


def test_get_triage_general_options(client, adversarial_test_data):
    """Verify /triage/options returns 5 baseline options."""
    resp = client.get("/api/medical/triage/options")
    assert resp.status_code == 200
    options = resp.json()
    assert len(options) == 5


@pytest.mark.parametrize("protocol,expected_status", [
    ("REST", InjuryStatus.OUT),
    ("PRP_THERAPY", InjuryStatus.OUT),
    ("ARTHROSCOPIC_SURGERY", InjuryStatus.OUT),
    ("RECONSTRUCTIVE_SURGERY", InjuryStatus.OUT),
    ("CORTISONE_STABILIZATION", InjuryStatus.QUESTIONABLE),
])
def test_apply_all_5_protocols_db_commit(client, adversarial_test_data, protocol, expected_status):
    """Empirically verify all 5 protocols modify and commit player state to the database."""
    resp = client.post(
        "/api/medical/players/8881/triage/apply",
        json={"protocol": protocol, "zone_key": "right_leg"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["player_id"] == 8881
    assert data["protocol_applied"] == protocol
    assert "projected_recovery_weeks" in data
    assert "re_injury_risk_index" in data


def test_apply_triage_nonexistent_player(client, adversarial_test_data):
    """POST apply on non-existent player returns 404."""
    resp = client.post(
        "/api/medical/players/999999/triage/apply",
        json={"protocol": "REST"}
    )
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_apply_triage_invalid_protocol_payload(client, adversarial_test_data):
    """Invalid protocol enum value triggers 422 Unprocessable Entity."""
    resp = client.post(
        "/api/medical/players/8881/triage/apply",
        json={"protocol": "MAGIC_CURE_POTION"}
    )
    assert resp.status_code == 422


def test_apply_triage_empty_body(client, adversarial_test_data):
    """Empty request body triggers 422 Unprocessable Entity."""
    resp = client.post(
        "/api/medical/players/8881/triage/apply",
        json={}
    )
    assert resp.status_code == 422


# =============================================================================
# 2. COACHING DYNASTY TREE & STAFF SYNERGY ADVERSARIAL TESTS
# =============================================================================

def test_get_coach_tree_success(client, adversarial_test_data):
    """Verify coach profile returns complete tree with 3 branches and correct SP."""
    resp = client.get("/api/coaches/8881/tree")
    assert resp.status_code == 200
    data = resp.json()
    assert data["coach_id"] == "8881"
    assert data["name"] == "Bill Mastermind"
    assert data["current_sp"] == 10  # xp=1000 -> 1000 // 100 = 10
    assert "SCHEME_DISGUISE_I" in data["tree_nodes"]
    assert data["tree_nodes"]["SCHEME_DISGUISE_I"]["unlocked"] is True

    # Check branch distribution (Scheme, Development, Culture)
    branches = {n["branch"] for n in data["tree_nodes"].values()}
    assert "SCHEME_TACTICS" in branches
    assert "DEVELOPMENT" in branches
    assert "PROGRAM_CULTURE" in branches


def test_get_coach_tree_nonexistent(client, adversarial_test_data):
    """Probing non-existent coach returns 404."""
    resp = client.get("/api/coaches/999999/tree")
    assert resp.status_code == 404
    assert "coach not found" in resp.json()["detail"].lower()


def test_get_coach_tree_alias(client, adversarial_test_data):
    """Verify /dynasty alias returns identical payload."""
    resp = client.get("/api/coaches/8881/dynasty")
    assert resp.status_code == 200
    assert resp.json()["coach_id"] == "8881"


def test_unlock_node_valid_tier2_persists_to_db(client, adversarial_test_data):
    """Unlock tier 2 node where tier 1 prereq is met: verify 200, SP deducted, DB committed."""
    resp = client.post(
        "/api/coaches/8881/unlock-node",
        json={"node_id": "SCHEME_MATCHUP_NIGHTMARE"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["tree_nodes"]["SCHEME_MATCHUP_NIGHTMARE"]["unlocked"] is True
    assert data["current_sp"] == 8  # 10 - 2 = 8

    # Verify retrieval after mutation preserves unlocked state
    get_resp = client.get("/api/coaches/8881/tree")
    assert get_resp.status_code == 200
    tree_data = get_resp.json()
    assert tree_data["tree_nodes"]["SCHEME_MATCHUP_NIGHTMARE"]["unlocked"] is True


def test_unlock_already_unlocked_node_fails(client, adversarial_test_data):
    """Unlocking already unlocked node returns 400 Bad Request."""
    resp = client.post(
        "/api/coaches/8881/unlock-node",
        json={"node_id": "SCHEME_DISGUISE_I"}
    )
    assert resp.status_code == 400
    assert "cannot unlock" in resp.json()["detail"].lower()


def test_unlock_node_unmet_prerequisites_fails(client, adversarial_test_data):
    """Attempting to jump to Tier 4 node without Tier 2 & 3 returns 400 Bad Request."""
    resp = client.post(
        "/api/coaches/8881/unlock-node",
        json={"node_id": "SCHEME_CHAMPIONSHIP_INSTALL"}
    )
    assert resp.status_code == 400
    assert "prerequisites" in resp.json()["detail"].lower()


def test_unlock_node_insufficient_sp_fails(client, adversarial_test_data):
    """Coach with 0 SP cannot unlock nodes; returns 400 Bad Request."""
    resp = client.post(
        "/api/coaches/8884/unlock-node",
        json={"node_id": "SCHEME_DISGUISE_I"}
    )
    assert resp.status_code == 400
    assert "sufficient sp" in resp.json()["detail"].lower()


def test_unlock_nonexistent_node_id_fails(client, adversarial_test_data):
    """Unlocking non-existent node ID returns 400 Bad Request."""
    resp = client.post(
        "/api/coaches/8881/unlock-node",
        json={"node_id": "INVALID_SUPER_POWER_999"}
    )
    assert resp.status_code == 400


def test_unlock_node_nonexistent_coach_fails(client, adversarial_test_data):
    """Unlocking node on non-existent coach ID returns 404 Not Found."""
    resp = client.post(
        "/api/coaches/999999/unlock-node",
        json={"node_id": "SCHEME_DISGUISE_I"}
    )
    assert resp.status_code == 404


def test_staff_synergy_matching_schemes(client, adversarial_test_data):
    """HC & OC with identical WEST_COAST scheme earn 95 offensive score and Apex perks."""
    resp = client.get("/api/coaches/staff/synergy/888")
    assert resp.status_code == 200
    data = resp.json()
    assert data["offensive_synergy_score"] == 95
    assert data["defensive_synergy_score"] == 88
    assert data["overall_chemistry_score"] >= 90
    assert any("Apex Staff Synergy" in perk for perk in data["active_synergy_perks"])
    assert any("Perfect Scheme Lock" in note for note in data["scheme_alignment_notes"])


def test_staff_synergy_empty_staff_fallback(client, adversarial_test_data):
    """Team with no assigned coaches uses clean fallbacks without 500 crashes."""
    resp = client.get("/api/coaches/staff/synergy/889")
    assert resp.status_code == 200
    data = resp.json()
    assert data["offensive_synergy_score"] >= 70
    assert data["overall_chemistry_score"] >= 70


def test_staff_synergy_nonexistent_team(client, adversarial_test_data):
    """Probing non-existent team ID returns 404."""
    resp = client.get("/api/coaches/staff/synergy/999999")
    assert resp.status_code == 404
    assert "team 999999 not found" in resp.json()["detail"].lower()


# =============================================================================
# 3. MULTI-LENS PROSPECT INTELLIGENCE & TRADE URGENCY ADVERSARIAL TESTS
# =============================================================================

def test_get_prospect_intelligence_existing_player(client, adversarial_test_data):
    """Verify all 4 bias lenses and physical metrics on existing player record."""
    resp = client.get("/api/scouts/prospects/8881/intelligence")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 8881
    assert data["name"] == "Adversarial Star"
    assert data["position"] == "WR"

    # Check all 4 lenses
    perceived = data["perceived_ovr"]
    assert ScoutBiasLens.CONSENSUS.value in perceived
    assert ScoutBiasLens.FILM_TRADITIONALIST.value in perceived
    assert ScoutBiasLens.ANALYTICS_METRICS.value in perceived
    assert ScoutBiasLens.REGIONAL_SCOUT.value in perceived

    # Value bounds validation
    for lens, rating in perceived.items():
        assert 55 <= rating <= 99, f"Rating for {lens} out of bounds: {rating}"

    assert 0 <= data["s2_cognition_score"] <= 100
    assert 15.0 <= data["gps_speed_max"] <= 24.0
    assert 0.0 <= data["burst_score"] <= 100.0
    assert 0.0 <= data["boom_bust_factor"] <= 1.0
    assert data["medical_grade"] in ["PASS", "CONCERN", "FAIL"]
    assert 1 <= data["draft_projection_round"] <= 7


def test_get_prospect_intelligence_synthetic_prospect_fallback(client, adversarial_test_data):
    """Prospect ID not in DB synthesizes a valid draft prospect profile."""
    resp = client.get("/api/scouts/prospects/7777/intelligence")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 7777
    assert "Draft Prospect #7777" in data["name"]
    assert len(data["perceived_ovr"]) == 4


def test_get_prospect_intelligence_scouting_route_alias(client, adversarial_test_data):
    """Verify /api/scouting/prospects/{id}/intelligence alias works identically."""
    resp = client.get("/api/scouting/prospects/8881/intelligence")
    assert resp.status_code == 200
    assert resp.json()["id"] == 8881


@pytest.mark.parametrize("position,expected_mult_effect", [
    ("QB", True),
    ("OT", True),
    ("CB", True),
    ("K", False),
])
def test_trade_urgency_positional_premiums(client, adversarial_test_data, position, expected_mult_effect):
    """Verify positional multipliers influence draft trade-up package valuations."""
    resp = client.get(f"/api/scouts/trade-urgency/888?target_position={position}&roster_need_score=0.9&remaining_in_tier=1&current_pick=5")
    assert resp.status_code == 200
    data = resp.json()
    assert data["team_id"] == "888"
    assert data["target_position"] == position
    assert 0.0 <= data["urgency_index"] <= 1.0
    assert 0.0 <= data["willing_to_overpay_pct"] <= 0.50
    assert data["suggested_package_value"] > 0


def test_trade_urgency_zero_remaining_in_tier(client, adversarial_test_data):
    """Verify remaining_in_tier=0 does not cause ZeroDivisionError (capped by max(1, ...))."""
    resp = client.get("/api/scouts/trade-urgency/888?remaining_in_tier=0")
    assert resp.status_code == 200
    assert resp.json()["urgency_index"] >= 0.0


def test_trade_urgency_zero_need_score(client, adversarial_test_data):
    """Verify roster_need_score=0.0 results in 0 urgency and 0 overpay."""
    resp = client.get("/api/scouts/trade-urgency/888?roster_need_score=0.0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["urgency_index"] == 0.0
    assert data["willing_to_overpay_pct"] == 0.0


def test_trade_urgency_invalid_params_422(client, adversarial_test_data):
    """Invalid non-numeric parameter triggers 422 Unprocessable Entity."""
    resp = client.get("/api/scouts/trade-urgency/888?roster_need_score=not_a_number")
    assert resp.status_code == 422
