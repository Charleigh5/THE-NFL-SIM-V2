"""
Unit Tests for Milestone 2: Live FastAPI Endpoints
==================================================
Verifies the newly added REST endpoints for:
1. 5-Pathway Orthopedic Triage (/api/medical/players/{id}/triage/...)
2. Body health neck_health field (/api/medical/player/{id})
3. Coaching Dynasty Tree & Staff Synergy (/api/coaches/{id}/tree, /unlock-node, /staff/synergy/{team_id})
4. Multi-Lens Scouting Intelligence & Draft Trade Urgency (/api/scouts/prospects/{id}/intelligence, /trade-urgency/{team_id})
5. Player Narrative Backstory (/api/players/{id}/backstory)
"""

import pytest
from app.models.player import Player, InjuryStatus
from app.models.team import Team
from app.models.coach import Coach, CoachTier
from app.models.medical import BodyPart

@pytest.fixture
def setup_test_data(db_session):
    # Create test team
    team = db_session.query(Team).filter(Team.id == 999).first()
    if not team:
        team = Team(
            id=999,
            name="Titans",
            city="Tennessee",
            abbreviation="TEN",
            conference="AFC",
            division="South",
            wins=8,
            losses=4,
            salary_cap_space=30000000,
        )
        db_session.add(team)

    # Create test player
    player = db_session.query(Player).filter(Player.id == 9991).first()
    if not player:
        player = Player(
            id=9991,
            team_id=999,
            first_name="Jordan",
            last_name="Love",
            position="QB",
            jersey_number=10,
            overall_rating=86,
            age=25,
            experience=4,
            speed=84,
            acceleration=86,
            strength=72,
            agility=82,
            awareness=88,
            stamina=92,
            injury_resistance=85,
            injury_status=InjuryStatus.QUESTIONABLE,
            injury_type="High Ankle Sprain",
            injury_severity=3,
            weeks_to_recovery=4,
            contract_years=3,
            contract_salary=45000000,
            is_rookie=False,
        )
        db_session.add(player)

    # Create body health
    bh = db_session.query(BodyPart).filter(BodyPart.player_id == 9991).first()
    if not bh:
        bh = BodyPart(
            player_id=9991,
            head_health=95.0,
            neck_health=98.0,
            torso_health=90.0,
            right_arm_health=92.0,
            left_arm_health=94.0,
            right_leg_health=55.0,
            left_leg_health=90.0,
            general_wear=15.0,
        )
        db_session.add(bh)

    # Create coaches
    hc = db_session.query(Coach).filter(Coach.id == 9991).first()
    if not hc:
        hc = Coach(
            id=9991,
            team_id=999,
            first_name="Matt",
            last_name="LaFleur",
            role="Head Coach",
            tier=CoachTier.ELITE,
            offense_rating=88,
            defense_rating=80,
            development_rating=85,
            playbook_offense="WEST_COAST",
            playbook_defense="COVER_3_ZONE",
            xp=400,
            level=14,
            skills={"unlocked_nodes": ["SCHEME_DISGUISE_I"]},
        )
        db_session.add(hc)

    oc = db_session.query(Coach).filter(Coach.id == 9992).first()
    if not oc:
        oc = Coach(
            id=9992,
            team_id=999,
            first_name="Adam",
            last_name="Stenavich",
            role="Offensive Coordinator",
            tier=CoachTier.VETERAN,
            offense_rating=82,
            defense_rating=65,
            development_rating=80,
            playbook_offense="WEST_COAST",
        )
        db_session.add(oc)

    dc = db_session.query(Coach).filter(Coach.id == 9993).first()
    if not dc:
        dc = Coach(
            id=9993,
            team_id=999,
            first_name="Jeff",
            last_name="Hafley",
            role="Defensive Coordinator",
            tier=CoachTier.DEVELOPING,
            offense_rating=60,
            defense_rating=84,
            development_rating=75,
            playbook_defense="COVER_3_ZONE",
        )
        db_session.add(dc)

    db_session.commit()
    return {"team": team, "player": player, "hc": hc}


def test_get_player_health_with_neck(client, setup_test_data):
    """Verify BodyHealthResponse includes neck_health."""
    response = client.get("/api/medical/player/9991")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == 9991
    assert "neck_health" in data
    assert data["neck_health"] == 98.0
    assert data["head_health"] == 95.0
    assert data["right_leg_health"] == 55.0


def test_get_player_triage_protocols(client, setup_test_data):
    """Verify 5-pathway orthopedic triage protocols response."""
    response = client.get("/api/medical/players/9991/triage/protocols")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == 9991
    assert "current_diagnosis" in data
    assert len(data["protocols"]) == 5
    protocols = [p["protocol"] for p in data["protocols"]]
    assert "REST" in protocols
    assert "PRP_THERAPY" in protocols
    assert "ARTHROSCOPIC_SURGERY" in protocols
    assert "RECONSTRUCTIVE_SURGERY" in protocols
    assert "CORTISONE_STABILIZATION" in protocols


def test_apply_player_triage_protocol(client, setup_test_data):
    """Verify applying a triage protocol updates player recovery state."""
    response = client.post(
        "/api/medical/players/9991/triage/apply",
        json={"protocol": "PRP_THERAPY", "zone_key": "right_leg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == 9991
    assert data["protocol_applied"] == "PRP_THERAPY"
    assert data["projected_recovery_weeks"] >= 1
    assert data["final_integrity_forecast"] > 0
    assert data["message"] != ""


def test_get_coach_tree(client, setup_test_data):
    """Verify coaching dynasty tree profile retrieval."""
    response = client.get("/api/coaches/9991/tree")
    assert response.status_code == 200
    data = response.json()
    assert data["coach_id"] == "9991"
    assert data["name"] == "Matt LaFleur"
    assert data["level"] >= 1
    assert "tree_nodes" in data
    assert "SCHEME_DISGUISE_I" in data["tree_nodes"]
    assert data["tree_nodes"]["SCHEME_DISGUISE_I"]["unlocked"] is True


def test_unlock_coach_node(client, setup_test_data):
    """Verify unlocking a valid skill node."""
    response = client.post(
        "/api/coaches/9991/unlock-node",
        json={"node_id": "SCHEME_MATCHUP_NIGHTMARE"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tree_nodes"]["SCHEME_MATCHUP_NIGHTMARE"]["unlocked"] is True


def test_get_staff_synergy(client, setup_test_data):
    """Verify staff synergy and organizational chemistry."""
    response = client.get("/api/coaches/staff/synergy/999")
    assert response.status_code == 200
    data = response.json()
    assert data["offensive_synergy_score"] >= 70
    assert data["defensive_synergy_score"] >= 70
    assert data["overall_chemistry_score"] >= 70
    assert len(data["scheme_alignment_notes"]) >= 1


def test_get_prospect_intelligence(client, setup_test_data):
    """Verify multi-lens scouting intelligence evaluation."""
    response = client.get("/api/scouts/prospects/9991/intelligence")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 9991
    assert data["name"] == "Jordan Love"
    assert "perceived_ovr" in data
    assert "CONSENSUS" in data["perceived_ovr"]
    assert "FILM_TRADITIONALIST" in data["perceived_ovr"]
    assert "ANALYTICS_METRICS" in data["perceived_ovr"]
    assert "REGIONAL_SCOUT" in data["perceived_ovr"]
    assert data["s2_cognition_score"] >= 0
    assert data["gps_speed_max"] >= 15.0


def test_get_trade_urgency(client, setup_test_data):
    """Verify draft trade-up urgency calculation."""
    response = client.get("/api/scouts/trade-urgency/999?target_position=QB")
    assert response.status_code == 200
    data = response.json()
    assert data["team_id"] == "999"
    assert data["target_position"] == "QB"
    assert 0.0 <= data["urgency_index"] <= 1.0
    assert data["suggested_package_value"] > 0


def test_get_player_backstory(client, setup_test_data):
    """Verify player narrative backstory generation."""
    response = client.get("/api/players/9991/backstory")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == 9991
    assert len(data["hometown"]) > 0
    assert len(data["background"]) > 0
    assert len(data["personality_traits"]) >= 2
    assert "motivations" in data
    assert "college_career" in data
