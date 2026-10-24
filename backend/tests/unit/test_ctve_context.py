import pytest

from app.models.player import DevelopmentTrait, Position
from app.services.trade_engine.context import (
    CompetitiveWindow,
    PositionNeedDetail,
    calculate_position_need,
    calculate_team_need_index,
    classify_competitive_window,
    evaluate_roster_context_multiplier,
)
from app.services.trade_engine.market import PlayerSnapshot


def test_classify_competitive_window_from_elo_and_ovr():
    """Verify team strength maps to the 4 discrete competitive windows."""
    # Contender: high Elo, high starter OVR
    assert classify_competitive_window(elo=1650.0, wins=12, losses=3, starter_avg_ovr=84.5) == CompetitiveWindow.CONTENDER
    # Rebuild: low Elo, low starter OVR
    assert classify_competitive_window(elo=1340.0, wins=2, losses=11, starter_avg_ovr=72.0) == CompetitiveWindow.REBUILD
    # Retool: moderate Elo, older/transitioning team
    assert classify_competitive_window(elo=1460.0, wins=6, losses=8, starter_avg_ovr=77.0, avg_roster_age=28.5) == CompetitiveWindow.RETOOL
    # Bubble: competitive fringe
    assert classify_competitive_window(elo=1510.0, wins=8, losses=7, starter_avg_ovr=79.5, avg_roster_age=26.0) == CompetitiveWindow.BUBBLE


def test_youth_pipeline_reduces_future_need():
    """A young developmental player with STAR+ dev trait reduces future positional need."""
    aging_vet = PlayerSnapshot(
        id=1,
        first_name="Tyron",
        last_name="Smith",
        position=Position.OT,
        overall_rating=83,
        age=32,
        contract_years=1,
        annual_base_salary=18_000_000,
    )
    young_heir = PlayerSnapshot(
        id=2,
        first_name="Amarius",
        last_name="Mims",
        position=Position.OT,
        overall_rating=77,
        age=22,
        contract_years=3,
        annual_base_salary=2_000_000,
        development_trait=DevelopmentTrait.SUPERSTAR,
    )
    need_without_heir = calculate_position_need(
        Position.OT, [aging_vet], window=CompetitiveWindow.RETOOL
    )
    need_with_heir = calculate_position_need(
        Position.OT, [aging_vet, young_heir], window=CompetitiveWindow.RETOOL
    )

    assert isinstance(need_with_heir, PositionNeedDetail)
    assert need_with_heir.youth_pipeline_offset > 0.25
    assert need_with_heir.tni < need_without_heir.tni - 0.10


def test_trading_away_lone_starting_qb_has_high_departure_multiplier():
    """Departing lone starter creates a severe positional deficit and high departure multiplier."""
    qb1 = PlayerSnapshot(
        id=10,
        first_name="Trevor",
        last_name="Lawrence",
        position=Position.QB,
        overall_rating=86,
        age=26,
        contract_years=3,
        annual_base_salary=35_000_000,
    )
    mult = evaluate_roster_context_multiplier(
        player=qb1, roster=[qb1], window=CompetitiveWindow.CONTENDER, is_acquiring=False
    )
    assert mult >= 1.30


def test_acquiring_older_backup_behind_young_stud_is_discounted():
    """Acquiring an older veteran at a position where a young elite starter exists caps multiplier at 0.70."""
    young_stud_cb = PlayerSnapshot(
        id=20,
        first_name="Sauce",
        last_name="Gardner",
        position=Position.CB,
        overall_rating=93,
        age=24,
        contract_years=3,
        annual_base_salary=6_000_000,
        development_trait=DevelopmentTrait.XFACTOR,
    )
    cb2 = PlayerSnapshot(
        id=21, position=Position.CB, overall_rating=82, age=25, contract_years=2, annual_base_salary=4_000_000
    )
    cb3 = PlayerSnapshot(
        id=22, position=Position.CB, overall_rating=78, age=24, contract_years=2, annual_base_salary=2_000_000
    )
    old_vet_cb = PlayerSnapshot(
        id=23,
        first_name="Patrick",
        last_name="Peterson",
        position=Position.CB,
        overall_rating=79,
        age=33,
        contract_years=1,
        annual_base_salary=5_000_000,
    )

    roster = [young_stud_cb, cb2, cb3]
    mult = evaluate_roster_context_multiplier(
        player=old_vet_cb, roster=roster, window=CompetitiveWindow.CONTENDER, is_acquiring=True
    )
    assert mult <= 0.70


def test_empty_position_yields_critical_need():
    """An empty position group produces critical need (TNI == 1.0) and maximum acquisition bonus."""
    need = calculate_position_need(Position.TE, [], window=CompetitiveWindow.BUBBLE)
    assert need.need_now == 1.0
    assert need.tni == 1.0
    starter_te = PlayerSnapshot(id=30, position=Position.TE, overall_rating=82, age=26)
    mult = evaluate_roster_context_multiplier(starter_te, [], window=CompetitiveWindow.BUBBLE, is_acquiring=True)
    assert mult >= 1.35
