import pytest
import os
import tempfile
import threading
import time
import random
from sqlalchemy import (
    create_engine,
    event,
    select,
    func,
    and_,
    or_,
    text,
)
from sqlalchemy.orm import sessionmaker, Session, selectinload, joinedload

from app.models import (
    Base,
    Player,
    PlayerAttributes,
    PlayerContract,
    PlayerPhysics,
    PlayerInjury,
    PlayerProgression,
    PlayerGameStarts,
    PlayerGameStart,
    Trait,
    PlayerTrait,
    TraitTier,
    TraitEffectType,
    TraitSource,
    Team,
    Game,
    Season,
)


# ============================================================================
# TEST SUITE 1: COMPLEX SQL QUERIES & HYBRID PROPERTY EXPRESSIONS
# ============================================================================

def test_adversarial_hybrid_multi_column_sorting_and_filtering(db_session):
    """
    Stress test: Multi-column sorting, boolean algebra, and arithmetic in SQL
    using hybrid properties that proxy to satellite models.
    """
    # Create 15 players with diverse attribute profiles
    players_data = [
        ("Tyreek", "Hill", "WR", 99, 99, 65, 98, 92, 4.29, 15, 40.5, 30000000, "ACTIVE", 95, 1),
        ("Derrick", "Henry", "RB", 90, 88, 95, 84, 90, 4.54, 25, 37.0, 16000000, "ACTIVE", 80, 2),
        ("Myles", "Garrett", "DE", 88, 92, 98, 86, 94, 4.64, 33, 41.0, 25000000, "ACTIVE", 70, 3),
        ("Lamar", "Jackson", "QB", 96, 97, 68, 96, 93, 4.34, 12, 36.5, 52000000, "ACTIVE", 100, 1),
        ("Patrick", "Mahomes", "QB", 87, 89, 72, 88, 99, 4.80, 14, 33.5, 45000000, "ACTIVE", 90, 4),
        ("Micah", "Parsons", "LB", 92, 95, 90, 93, 91, 4.39, 23, 38.0, 20000000, "QUESTIONABLE", 60, 2),
        ("Sauce", "Gardner", "CB", 93, 94, 62, 94, 90, 4.41, 10, 38.5, 10000000, "ACTIVE", 75, 1),
        ("Trent", "Williams", "OT", 74, 80, 99, 75, 97, 4.88, 38, 34.5, 23000000, "ACTIVE", 50, 5),
        ("Justin", "Jefferson", "WR", 92, 94, 70, 95, 96, 4.43, 16, 37.5, 35000000, "ACTIVE", 85, 2),
        ("TJ", "Watt", "LB", 86, 90, 94, 88, 95, 4.69, 21, 37.0, 28000000, "ACTIVE", 65, 3),
        ("Christian", "McCaffrey", "RB", 91, 93, 75, 97, 95, 4.48, 18, 37.5, 19000000, "IR", 90, 2),
        ("Travis", "Kelce", "TE", 83, 85, 82, 86, 98, 4.61, 20, 35.0, 15000000, "ACTIVE", 80, 4),
        ("Nick", "Bosa", "DE", 85, 89, 96, 87, 93, 4.79, 29, 33.5, 34000000, "ACTIVE", 70, 3),
        ("Ja'Marr", "Chase", "WR", 94, 95, 71, 93, 91, 4.38, 15, 41.0, 22000000, "ACTIVE", 85, 2),
        ("Fred", "Warner", "LB", 87, 91, 85, 90, 98, 4.64, 18, 38.5, 18000000, "ACTIVE", 75, 3),
    ]

    for row in players_data:
        p = Player(
            first_name=row[0],
            last_name=row[1],
            position=row[2],
            overall_rating=90,
            speed=row[3],
            acceleration=row[4],
            strength=row[5],
            agility=row[6],
            awareness=row[7],
            forty_yard_dash=row[8],
            bench_press=row[9],
            vertical_jump=row[10],
            contract_salary=row[11],
            injury_status=row[12],
            vision_cone_angle=row[13],
            contract_years=row[14],
        )
        db_session.add(p)
    db_session.commit()

    # 1. Complex Multi-Column Ordering (Speed DESC, Strength ASC, Agility DESC)
    stmt_order = select(
        Player.first_name,
        Player.last_name,
        Player.speed,
        Player.strength,
        Player.agility
    ).order_by(
        Player.speed.desc(),
        Player.strength.asc(),
        Player.agility.desc()
    )
    results_order = db_session.execute(stmt_order).all()
    assert len(results_order) == 15
    assert results_order[0][0] == "Tyreek"
    assert results_order[0][2] == 99
    assert results_order[1][0] == "Lamar"
    assert results_order[1][2] == 96

    # 2. Boolean Logic in WHERE clause combining multiple hybrid properties
    stmt_filter = select(Player.first_name, Player.last_name, Player.speed, Player.strength, Player.agility).where(
        and_(
            Player.speed >= 90,
            or_(
                Player.strength >= 90,
                Player.agility >= 95
            )
        )
    ).order_by(Player.speed.desc())

    filtered_players = db_session.execute(stmt_filter).all()
    names = [f"{r[0]} {r[1]}" for r in filtered_players]
    assert "Tyreek Hill" in names
    assert "Lamar Jackson" in names
    assert "Derrick Henry" in names
    assert "Micah Parsons" in names
    assert "Justin Jefferson" in names
    assert "Christian McCaffrey" in names

    # 3. SQL Aggregations & Calculations on Hybrid Properties
    stmt_agg = select(
        func.count(Player.id),
        func.avg(Player.speed),
        func.max(Player.speed),
        func.min(Player.speed),
        func.avg(Player.strength),
        func.avg(Player.forty_yard_dash),
        func.sum(Player.contract_salary)
    )
    agg_res = db_session.execute(stmt_agg).one()
    count, avg_spd, max_spd, min_spd, avg_str, avg_40, total_sal = agg_res
    assert count == 15
    assert max_spd == 99
    assert min_spd == 74
    assert round(float(avg_spd), 1) > 85.0
    assert total_sal > 200000000

    # 4. Hybrid Properties across all satellite models simultaneously
    stmt_all_satellites = select(
        Player.first_name,
        Player.speed,               # PlayerAttributes
        Player.vision_cone_angle,   # PlayerPhysics
        Player.contract_salary,     # PlayerContract
        Player.injury_status,       # PlayerInjury
        Player.xp                   # PlayerProgression
    ).where(Player.first_name == "Lamar")
    lamar_row = db_session.execute(stmt_all_satellites).one()
    assert lamar_row[0] == "Lamar"
    assert lamar_row[1] == 96
    assert lamar_row[2] == 100
    assert lamar_row[3] == 52000000
    assert lamar_row[4] == "ACTIVE"
    assert lamar_row[5] == 0


def test_adversarial_hybrid_property_mutation_and_expression_consistency(db_session):
    """
    Stress test: Verify that modifying hybrid properties in Python commits to database
    and subsequent SQL expression queries reflect the modified state identically.
    """
    p = Player(
        first_name="Kyler",
        last_name="Murray",
        position="QB",
        speed=90,
        agility=92,
        injury_status="ACTIVE",
        contract_salary=46000000,
        xp=500,
        level=3
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)

    assert p.speed == 90
    assert p.injury_status == "ACTIVE"
    assert p.contract_salary == 46000000
    assert p.level == 3

    stmt = select(Player.speed, Player.injury_status, Player.contract_salary, Player.level).where(Player.id == p.id)
    row = db_session.execute(stmt).one()
    assert row[0] == 90
    assert row[1] == "ACTIVE"
    assert row[2] == 46000000
    assert row[3] == 3

    # Mutate hybrid properties via setters
    p.speed = 94
    p.agility = 95
    p.injury_status = "OUT"
    p.contract_salary = 50000000
    p.xp = 1200
    p.level = 4
    db_session.commit()

    row_updated = db_session.execute(stmt).one()
    assert row_updated[0] == 94
    assert row_updated[1] == "OUT"
    assert row_updated[2] == 50000000
    assert row_updated[3] == 4


def test_adversarial_team_roster_group_by_hybrid_expressions(db_session):
    """
    Stress test: Grouping by Team and aggregating on hybrid properties with HAVING filters.
    """
    team_det = Team(name="Lions", city="Detroit", abbreviation="DET", conference="NFC", division="North")
    team_kc = Team(name="Chiefs", city="Kansas City", abbreviation="KC", conference="AFC", division="West")
    db_session.add_all([team_det, team_kc])
    db_session.commit()

    p_det1 = Player(first_name="Amon-Ra", last_name="St. Brown", position="WR", team_id=team_det.id, speed=93)
    p_det2 = Player(first_name="Jameson", last_name="Williams", position="WR", team_id=team_det.id, speed=98)
    p_det3 = Player(first_name="Jahmyr", last_name="Gibbs", position="RB", team_id=team_det.id, speed=95)

    p_kc1 = Player(first_name="Creed", last_name="Humphrey", position="C", team_id=team_kc.id, speed=72)
    p_kc2 = Player(first_name="Chris", last_name="Jones", position="DT", team_id=team_kc.id, speed=80)
    p_kc3 = Player(first_name="Travis", last_name="Kelce", position="TE", team_id=team_kc.id, speed=84)

    db_session.add_all([p_det1, p_det2, p_det3, p_kc1, p_kc2, p_kc3])
    db_session.commit()

    stmt = (
        select(
            Team.abbreviation,
            func.avg(Player.speed).label("avg_speed")
        )
        .join(Player, Player.team_id == Team.id)
        .group_by(Team.id, Team.abbreviation)
        .having(func.avg(Player.speed) > 90)
    )

    rows = db_session.execute(stmt).all()
    assert len(rows) == 1
    assert rows[0][0] == "DET"
    assert rows[0][1] > 90


# ============================================================================
# TEST SUITE 2: CASCADE DELETION & ZERO ORPHAN AUDIT
# ============================================================================

def test_adversarial_cascade_delete_decomposition_satellites_only(db_session):
    """
    Stress test: Bulk create 20 players with 1:1 decomposition satellite records only.
    Delete players and verify that all 5 satellite tables have zero orphans.
    """
    created_players = []
    satellite_ids = {
        "attr": [],
        "contract": [],
        "physics": [],
        "injury": [],
        "progression": [],
    }

    for i in range(20):
        p = Player(
            first_name=f"Player_{i}",
            last_name=f"Sat_{i}",
            position="WR",
            speed=80 + i,
            contract_salary=1000000 * (i + 1),
            injury_status="ACTIVE",
            xp=100 * i
        )
        db_session.add(p)
        created_players.append(p)

    db_session.commit()

    for p in created_players:
        db_session.refresh(p)
        satellite_ids["attr"].append(p.attributes.id)
        satellite_ids["contract"].append(p.contract.id)
        satellite_ids["physics"].append(p.physics.id)
        satellite_ids["injury"].append(p.injury.id)
        satellite_ids["progression"].append(p.progression.id)

    # Delete players
    for p in created_players:
        db_session.delete(p)
    db_session.commit()

    # Verify ALL 20 satellite records in all 5 tables are deleted
    for aid in satellite_ids["attr"]:
        assert db_session.execute(select(PlayerAttributes).where(PlayerAttributes.id == aid)).scalar_one_or_none() is None
    for cid in satellite_ids["contract"]:
        assert db_session.execute(select(PlayerContract).where(PlayerContract.id == cid)).scalar_one_or_none() is None
    for pid in satellite_ids["physics"]:
        assert db_session.execute(select(PlayerPhysics).where(PlayerPhysics.id == pid)).scalar_one_or_none() is None
    for iid in satellite_ids["injury"]:
        assert db_session.execute(select(PlayerInjury).where(PlayerInjury.id == iid)).scalar_one_or_none() is None
    for prid in satellite_ids["progression"]:
        assert db_session.execute(select(PlayerProgression).where(PlayerProgression.id == prid)).scalar_one_or_none() is None


def test_adversarial_cascade_delete_with_traits_and_game_starts(db_session):
    """
    Stress test: Create players with PlayerTrait and PlayerGameStarts relationships.
    Verify whether deleting Player cascades cleanly to child records or raises dependency errors.
    """
    season = Season(year=2026)
    team = Team(name="Ravens", city="Baltimore", abbreviation="BAL", conference="AFC", division="North")
    db_session.add_all([season, team])
    db_session.commit()

    game = Game(season_id=season.id, season=2026, week=1, home_team_id=team.id, away_team_id=team.id)
    trait = Trait(name="Clutch Performer", description="Boost in 4th quarter", tier=TraitTier.GOLD, effect_type=TraitEffectType.BOOST)
    db_session.add_all([game, trait])
    db_session.commit()

    p = Player(first_name="Lamar", last_name="Jackson", position="QB", team_id=team.id)
    db_session.add(p)
    db_session.commit()

    pt = PlayerTrait(player_id=p.id, trait_id=trait.id, source=TraitSource.DEVELOPMENT)
    gs = PlayerGameStarts(player_id=p.id, game_id=game.id, team_id=team.id, season_id=season.id, week=1, position="QB")
    db_session.add_all([pt, gs])
    db_session.commit()

    # Attempt to delete player
    db_session.delete(p)
    db_session.commit()

    # If cascade works, child rows should be deleted
    assert db_session.execute(select(PlayerTrait).where(PlayerTrait.player_id == p.id)).all() == []
    assert db_session.execute(select(PlayerGameStarts).where(PlayerGameStarts.player_id == p.id)).all() == []


# ============================================================================
# TEST SUITE 3: CONCURRENT INSERT/QUERY UNDER SQLITE WAL MODE
# ============================================================================

def test_adversarial_sqlite_wal_concurrent_inserts_and_queries():
    """
    Stress test: Multi-threaded concurrent reads and writes on a file-based SQLite database
    configured with WAL mode and busy_timeout=5000.
    Ensures zero 'database is locked' errors under concurrent load.
    """
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "wal_stress_test.db")
    db_url = f"sqlite:///{db_path}"

    stress_engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20
    )

    @event.listens_for(stress_engine, "connect")
    def set_sqlite_wal_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()

    Base.metadata.create_all(bind=stress_engine)

    with stress_engine.connect() as conn:
        wal_mode = conn.execute(text("PRAGMA journal_mode;")).scalar()
        assert wal_mode.lower() == "wal"

    SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=stress_engine)

    with SessionFactory() as session:
        team = Team(name="49ers", city="San Francisco", abbreviation="SF", conference="NFC", division="West")
        session.add(team)
        session.commit()
        team_id = team.id

    errors = []
    success_counts = {"inserts": 0, "queries": 0, "updates": 0}
    lock = threading.Lock()

    def worker_task(thread_id: int):
        local_session = SessionFactory()
        try:
            for op_idx in range(20):
                op_type = op_idx % 3
                if op_type == 0:
                    # INSERT: Create a new player with satellite models
                    p = Player(
                        first_name=f"T{thread_id}",
                        last_name=f"P{op_idx}",
                        position="CB",
                        team_id=team_id,
                        speed=random.randint(60, 99),
                        strength=random.randint(50, 95),
                        agility=random.randint(60, 99),
                        contract_salary=random.randint(1000000, 30000000)
                    )
                    local_session.add(p)
                    local_session.commit()
                    with lock:
                        success_counts["inserts"] += 1

                elif op_type == 1:
                    # QUERY: Complex hybrid property aggregation and sort
                    stmt = select(
                        Player.first_name,
                        Player.speed,
                        Player.strength,
                        Player.contract_salary
                    ).where(Player.speed > 70).order_by(Player.speed.desc()).limit(10)
                    res = local_session.execute(stmt).all()
                    with lock:
                        success_counts["queries"] += 1

                elif op_type == 2:
                    # UPDATE: Update hybrid properties on an existing player
                    stmt = select(Player).where(Player.team_id == team_id).order_by(func.random()).limit(1)
                    p = local_session.execute(stmt).scalars().first()
                    if p:
                        p.speed = min(99, p.speed + 1)
                        p.injury_status = "QUESTIONABLE"
                        local_session.commit()
                    with lock:
                        success_counts["updates"] += 1

                time.sleep(0.005)
        except Exception as e:
            with lock:
                errors.append(f"Thread {thread_id} error at op {op_idx}: {type(e).__name__}: {str(e)}")
        finally:
            local_session.close()

    # Launch 8 concurrent worker threads
    num_threads = 8
    threads = []
    for t_id in range(num_threads):
        t = threading.Thread(target=worker_task, args=(t_id,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=30)

    stress_engine.dispose()

    try:
        for fname in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, fname))
        os.rmdir(temp_dir)
    except OSError:
        pass

    assert len(errors) == 0, f"Encountered concurrency errors: {errors}"
    assert success_counts["inserts"] > 0
    assert success_counts["queries"] > 0
    assert success_counts["updates"] > 0
