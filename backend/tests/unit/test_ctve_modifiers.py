import pytest

from app.models.player import Position
from app.services.trade_engine.market import PlayerSnapshot
from app.services.trade_engine.modifiers import (
    RealismEvaluation,
    TeamContextProfile,
    evaluate_player_realism_modifiers,
    evaluate_trade_relationship_modifiers,
)


def test_division_rivalry_adds_12_percent_threshold_tax():
    """Trading within the same division adds a +12% acceptance threshold tax."""
    t1 = TeamContextProfile(team_id=1, conference="NFC", division="East", owner_trust=60)
    t2 = TeamContextProfile(team_id=2, conference="NFC", division="East", owner_trust=60)
    rel = evaluate_trade_relationship_modifiers(offering_team=t1, receiving_team=t2)
    assert rel.rivalry_threshold_delta >= 0.12
    assert any("Division" in note for note in rel.narrative_notes)


def test_intra_conference_non_division_tax():
    """Trading within the same conference but different division adds a +4% tax."""
    t1 = TeamContextProfile(team_id=1, conference="AFC", division="North")
    t2 = TeamContextProfile(team_id=2, conference="AFC", division="West")
    rel = evaluate_trade_relationship_modifiers(offering_team=t1, receiving_team=t2)
    assert rel.rivalry_threshold_delta == pytest.approx(0.04, abs=0.01)
    assert any("Conference" in note for note in rel.narrative_notes)


def test_expiring_star_enforces_compensatory_pick_floor():
    """An elite expiring player enforces a compensatory pick reservation floor."""
    expiring_star = PlayerSnapshot(
        id=77,
        position=Position.DE,
        overall_rating=89,
        age=27,
        contract_years=1,
        annual_base_salary=22_000_000,
    )
    seller = TeamContextProfile(team_id=2, conference="AFC", division="North")
    buyer = TeamContextProfile(team_id=1, conference="NFC", division="West")
    mod = evaluate_player_realism_modifiers(
        player=expiring_star, acquiring_team=buyer, selling_team=seller, is_acquiring=False
    )
    # 89 OVR DE commands top-tier FA deal -> 3rd-round comp pick floor (~450+ TVP after 1-yr discount)
    assert mod.comp_pick_floor_tvp >= 450.0
    assert any("Compensatory" in note for note in mod.narrative_notes)


def test_disgruntled_holdout_player_reduces_seller_leverage():
    """Disgruntled stars with low morale and high tension reduce seller trade leverage."""
    holdout_wr = PlayerSnapshot(
        id=88,
        position=Position.WR,
        overall_rating=91,
        age=27,
        contract_years=2,
        annual_base_salary=24_000_000,
        morale=20,
        tension_score=85.0,
    )
    seller = TeamContextProfile(team_id=2, conference="AFC", division="North")
    buyer = TeamContextProfile(team_id=1, conference="NFC", division="West")
    mod = evaluate_player_realism_modifiers(
        player=holdout_wr, acquiring_team=buyer, selling_team=seller, is_acquiring=False
    )
    assert mod.morale_leverage_mult <= 0.85
    assert any("Holdout" in note or "Morale" in note for note in mod.narrative_notes)


def test_injured_player_carries_medical_discount():
    """A player on IR carries an injury discount and medical flag."""
    injured_rb = PlayerSnapshot(
        id=99,
        position=Position.RB,
        overall_rating=85,
        age=25,
        injury_status="IR",
    )
    buyer = TeamContextProfile(team_id=1, medical_rating=70)
    seller = TeamContextProfile(team_id=2)
    mod = evaluate_player_realism_modifiers(
        player=injured_rb, acquiring_team=buyer, selling_team=seller, is_acquiring=True
    )
    assert mod.injury_risk_mult <= 0.80
    assert any("Medical" in note or "Injury" in note for note in mod.narrative_notes)
