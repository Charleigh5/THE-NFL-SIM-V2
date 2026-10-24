import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.data.draft_value_chart import DraftValueChart
from app.models.base import Base
from app.models.draft import DraftPick
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.services.offseason_service import OffseasonService
from app.services.trade_engine.picks import (
    ConditionalPickRule,
    PickValuationInput,
    PickValuationResult,
    assign_draft_order_preserving_trades,
    ensure_future_picks_ledger,
    evaluate_draft_pick_tvp,
    project_team_draft_slot,
)


@pytest.fixture
def sqlite_db():
    """In-memory SQLite session for testing DraftPick ledger and trade preservation."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_draft_value_chart_no_double_counted_top_10_premium():
    """DraftValueChart.get_pick_value should return raw Fitzgerald-Spielberger values by default."""
    assert DraftValueChart.get_pick_value(1) == 3000
    assert DraftValueChart.get_pick_value(1, apply_top_10_premium=True) == 3600
    assert DraftValueChart.get_pick_value(32) == 1244
    assert DraftValueChart.get_pick_value(64) == 895


def test_project_team_draft_slot_monotonicity():
    """Team strength metrics should map monotonically to projected draft slots 1..32."""
    bottom_slot = project_team_draft_slot(
        team_elo=1300.0, wins=1, losses=16, roster_starter_ovr=65.0
    )
    avg_slot = project_team_draft_slot(
        team_elo=1500.0, wins=0, losses=0, roster_starter_ovr=75.0
    )
    contender_slot = project_team_draft_slot(
        team_elo=1680.0, wins=14, losses=3, roster_starter_ovr=84.0
    )

    assert 1 <= bottom_slot <= 4
    assert avg_slot == 16
    assert 27 <= contender_slot <= 32
    assert bottom_slot < avg_slot < contender_slot


def test_evaluate_current_year_known_overall_pick():
    """Known current-year overall pick should return exact chart value without discount."""
    res = evaluate_draft_pick_tvp(
        PickValuationInput(
            round=1,
            year=2025,
            current_year=2025,
            overall_pick=1,
        )
    )
    assert isinstance(res, PickValuationResult)
    assert res.market_tvp == pytest.approx(3000.0)
    assert res.expected_overall_pick == pytest.approx(1.0)
    assert res.years_in_future == 0
    assert res.discount_factor_applied == pytest.approx(1.0)


def test_evaluate_future_first_round_pick_benchmarks():
    """
    Pre-registered benchmark:
    - Average team (slot 16) 1-year-out 1st-round pick must land in [1,100, 1,350] TVP.
    - Bottom-feeder (slot 2) 1-year-out 1st-round pick must exceed average team significantly.
    - Contender (slot 30) 1-year-out 1st-round pick must be lower (~early 2nd round value).
    """
    avg_res = evaluate_draft_pick_tvp(
        PickValuationInput(
            round=1,
            year=2026,
            current_year=2025,
            projected_slot_in_round=16,
        )
    )
    bottom_res = evaluate_draft_pick_tvp(
        PickValuationInput(
            round=1,
            year=2026,
            current_year=2025,
            projected_slot_in_round=2,
        )
    )
    contender_res = evaluate_draft_pick_tvp(
        PickValuationInput(
            round=1,
            year=2026,
            current_year=2025,
            projected_slot_in_round=30,
        )
    )

    assert 1100.0 <= avg_res.market_tvp <= 1350.0
    assert bottom_res.market_tvp >= 1800.0
    assert 950.0 <= contender_res.market_tvp <= 1150.0
    assert bottom_res.market_tvp > avg_res.market_tvp > contender_res.market_tvp
    assert avg_res.years_in_future == 1
    assert avg_res.discount_factor_applied == pytest.approx(0.78)


def test_evaluate_future_pick_horizon_limit_and_multiyear_discount():
    """Picks >3 years out must raise ValueError; 2-year-out picks discount further than 1-year-out."""
    y1 = evaluate_draft_pick_tvp(
        PickValuationInput(round=1, year=2026, current_year=2025, projected_slot_in_round=16)
    )
    y2 = evaluate_draft_pick_tvp(
        PickValuationInput(round=1, year=2027, current_year=2025, projected_slot_in_round=16)
    )
    assert y2.market_tvp < y1.market_tvp
    assert y2.years_in_future == 2
    assert y2.discount_factor_applied == pytest.approx(0.78**2)

    with pytest.raises(ValueError, match="Cannot trade draft picks more than 3 years in the future"):
        evaluate_draft_pick_tvp(
            PickValuationInput(round=1, year=2029, current_year=2025, projected_slot_in_round=16)
        )


def test_compensatory_and_conditional_pick_valuation():
    """Compensatory picks sit at slot 32 of the round; conditional picks blend upgrade EV."""
    comp_r3 = evaluate_draft_pick_tvp(
        PickValuationInput(
            round=3,
            year=2025,
            current_year=2025,
            is_compensatory=True,
        )
    )
    assert comp_r3.expected_overall_pick == pytest.approx(96.0)
    assert comp_r3.market_tvp == pytest.approx(float(DraftValueChart.get_pick_value(96)))

    pure_r3 = evaluate_draft_pick_tvp(
        PickValuationInput(round=3, year=2026, current_year=2025, projected_slot_in_round=16)
    )
    pure_r2 = evaluate_draft_pick_tvp(
        PickValuationInput(round=2, year=2026, current_year=2025, projected_slot_in_round=16)
    )
    cond_r3_to_r2 = evaluate_draft_pick_tvp(
        PickValuationInput(
            round=3,
            year=2026,
            current_year=2025,
            projected_slot_in_round=16,
            conditions=[
                ConditionalPickRule(
                    upgrade_to_round=2,
                    probability=0.50,
                    description="Upgrades to 2nd if player plays >= 65% snaps",
                )
            ],
        )
    )

    expected_blend = 0.50 * pure_r3.market_tvp + 0.50 * pure_r2.market_tvp
    assert cond_r3_to_r2.market_tvp == pytest.approx(expected_blend, rel=1e-4)
    assert pure_r3.market_tvp < cond_r3_to_r2.market_tvp < pure_r2.market_tvp


def test_future_picks_ledger_and_preserving_traded_picks_on_draft_order(sqlite_db):
    """
    Ensure future picks ledger creates multi-year picks with nullable pick_number,
    and generating draft order assigns pick_number WITHOUT overwriting traded team_id.
    """
    season = Season(year=2025, current_week=18, status=SeasonStatus.OFF_SEASON)
    sqlite_db.add(season)
    t1 = Team(city="Alpha", name="Wolves", abbreviation="ALF", conference="AFC", division="East")
    t2 = Team(city="Beta", name="Hawks", abbreviation="BET", conference="NFC", division="West")
    sqlite_db.add_all([t1, t2])
    sqlite_db.commit()

    picks = ensure_future_picks_ledger(
        sqlite_db, current_year=2025, season_id=season.id, horizon=2
    )
    # 2 teams * 7 rounds * 3 years (2025, 2026, 2027) = 42 picks
    assert len(picks) == 42

    # Calling again is idempotent
    picks_again = ensure_future_picks_ledger(
        sqlite_db, current_year=2025, season_id=season.id, horizon=2
    )
    assert len(picks_again) == 42

    # Trade Team 1's 2025 1st-round pick to Team 2 prior to draft order generation
    t1_r1_2025 = sqlite_db.execute(
        select(DraftPick).where(
            DraftPick.original_team_id == t1.id,
            DraftPick.round == 1,
            DraftPick.year == 2025,
        )
    ).scalar_one()
    assert t1_r1_2025.pick_number is None
    t1_r1_2025.team_id = t2.id
    sqlite_db.commit()

    # Now assign draft order with Team 1 picking first, Team 2 picking second
    assign_draft_order_preserving_trades(
        sqlite_db,
        season_id=season.id,
        year=2025,
        ordered_team_ids=[t1.id, t2.id],
    )
    sqlite_db.commit()

    sqlite_db.refresh(t1_r1_2025)
    assert t1_r1_2025.pick_number == 1
    assert t1_r1_2025.original_team_id == t1.id
    assert t1_r1_2025.team_id == t2.id  # Traded owner preserved!
