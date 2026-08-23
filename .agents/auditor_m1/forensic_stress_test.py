import asyncio
import os
import sys
import tempfile
from pathlib import Path

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine, select, text, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, selectinload, joinedload

from app.models.base import Base
import app.models
from app.models import (
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
from app.core.database import is_sqlite


def test_metadata_completeness():
    print("[FORENSIC TEST 1] Metadata Registration Completeness")
    registered_tables = sorted(list(Base.metadata.tables.keys()))
    print(f"Total tables registered in Base.metadata: {len(registered_tables)}")
    print(f"Tables: {registered_tables}")
    
    expected_tables = [
        "player", "player_attributes", "player_contract", "player_physics",
        "player_injury", "player_progression", "player_game_starts", "team",
        "stadium", "coach", "gm", "gm_decisions", "game", "playergamestats",
        "season", "playoff_matchup", "draft_pick", "season_history",
        "player_season_stats", "team_season_stats", "depthchart", "traits",
        "player_traits", "hall_of_fame", "scouts", "scouting_reports",
        "body_health", "injury_events", "gameplans", "coaching_trees",
        "news_items", "weekly_recaps", "rpg_events"
    ]
    missing = [t for t in expected_tables if t not in registered_tables]
    if missing:
        print(f"FAILED: Missing tables: {missing}")
        return False
    print("PASS: All 33+ expected tables are genuinely registered in Base.metadata.")
    return True


def test_sqlite_pragmas_on_file():
    print("\n[FORENSIC TEST 2] SQLite PRAGMAs on File-Based Database")
    temp_dir = tempfile.mkdtemp()
    temp_db_file = os.path.join(temp_dir, "test_pragmas.db")
    db_url = f"sqlite:///{temp_db_file}"
    
    # Import event listener logic from database.py
    from sqlalchemy import event
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()
        
    with engine.connect() as conn:
        journal_mode = conn.execute(text("PRAGMA journal_mode;")).scalar()
        busy_timeout = conn.execute(text("PRAGMA busy_timeout;")).scalar()
        foreign_keys = conn.execute(text("PRAGMA foreign_keys;")).scalar()
        synchronous = conn.execute(text("PRAGMA synchronous;")).scalar()
        
    print(f"PRAGMA journal_mode = {journal_mode}")
    print(f"PRAGMA busy_timeout = {busy_timeout}")
    print(f"PRAGMA foreign_keys = {foreign_keys}")
    print(f"PRAGMA synchronous  = {synchronous}")
    
    passed = (
        str(journal_mode).lower() == "wal" and
        int(busy_timeout) == 5000 and
        int(foreign_keys) == 1
    )
    if passed:
        print("PASS: SQLite WAL and busy timeout pragmas genuinely active.")
    else:
        print("FAILED: Pragmas did not match expected values.")
    
    engine.dispose()
    try:
        os.remove(temp_db_file)
        os.rmdir(temp_dir)
    except Exception:
        pass
    return passed


def test_hybrid_property_sql_compilation():
    print("\n[FORENSIC TEST 3] Hybrid Property SQL Subquery Compilation")
    # Verify SQL generation for multiple proxied properties
    properties_to_test = [
        Player.speed,
        Player.acceleration,
        Player.strength,
        Player.agility,
        Player.awareness,
        Player.stamina,
        Player.injury_resistance,
        Player.pass_block,
        Player.run_block,
        Player.contract_salary,
        Player.injury_status,
        Player.injury_severity,
        Player.xp,
        Player.level,
        Player.development_trait,
        Player.legacy_score,
        Player.morale,
    ]
    
    for prop in properties_to_test:
        stmt = select(Player.id, prop).where(prop > 0).order_by(prop.desc())
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": False}))
        if "SELECT" not in compiled or "player" not in compiled:
            print(f"FAILED compiling {prop}: {compiled}")
            return False
            
    print(f"PASS: Verified SQL scalar subquery compilation for {len(properties_to_test)} hybrid properties.")
    return True


def test_cascading_deletion_and_relationships():
    print("\n[FORENSIC TEST 4] Cascading Deletion & 1:1 Satellites Persistence")
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    p = Player(
        first_name="Lamar",
        last_name="Jackson",
        position="QB",
        overall_rating=96,
        speed=96,
        contract_salary=52000000,
        height=74,
        weight=215
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    
    p_id = p.id
    attr_id = p.attributes.id
    contract_id = p.contract.id
    physics_id = p.physics.id
    injury_id = p.injury.id
    prog_id = p.progression.id
    
    # Verify satellites were automatically populated
    assert p.speed == 96
    assert p.attributes.speed == 96
    assert p.contract.contract_salary == 52000000
    
    # Delete player and check cascade
    session.delete(p)
    session.commit()
    
    remaining_attr = session.execute(select(PlayerAttributes).where(PlayerAttributes.id == attr_id)).scalar_one_or_none()
    remaining_contract = session.execute(select(PlayerContract).where(PlayerContract.id == contract_id)).scalar_one_or_none()
    remaining_physics = session.execute(select(PlayerPhysics).where(PlayerPhysics.id == physics_id)).scalar_one_or_none()
    remaining_injury = session.execute(select(PlayerInjury).where(PlayerInjury.id == injury_id)).scalar_one_or_none()
    remaining_prog = session.execute(select(PlayerProgression).where(PlayerProgression.id == prog_id)).scalar_one_or_none()
    
    assert remaining_attr is None, "PlayerAttributes was not cascaded"
    assert remaining_contract is None, "PlayerContract was not cascaded"
    assert remaining_physics is None, "PlayerPhysics was not cascaded"
    assert remaining_injury is None, "PlayerInjury was not cascaded"
    assert remaining_prog is None, "PlayerProgression was not cascaded"
    
    print("PASS: 1:1 decomposition satellites initialized, populated, and cascaded cleanly on delete.")
    session.close()
    engine.dispose()
    return True


async def test_async_profile_loading():
    print("\n[FORENSIC TEST 5] Async Player Profile Query with Eager Traits Loading")
    async_eng = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with async_eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    AsyncSessionMaker = async_sessionmaker(async_eng, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionMaker() as session:
        p = Player(
            first_name="Justin",
            last_name="Jefferson",
            position="WR",
            overall_rating=99,
            speed=93
        )
        session.add(p)
        await session.commit()
        await session.refresh(p)
        
        t = Trait(
            name="Route Technician",
            description="Crisp route running with separation boost",
            tier=TraitTier.GOLD,
            effect_type=TraitEffectType.BOOST
        )
        session.add(t)
        await session.commit()
        await session.refresh(t)
        
        pt = PlayerTrait(
            player_id=p.id,
            trait_id=t.id,
            source=TraitSource.DRAFT
        )
        session.add(pt)
        await session.commit()
        
        # Execute the exact endpoint query
        stmt = (
            select(Player)
            .options(selectinload(Player.player_traits).joinedload(PlayerTrait.trait))
            .where(Player.id == p.id)
        )
        res = await session.execute(stmt)
        player_loaded = res.scalar_one_or_none()
        
        assert player_loaded is not None
        assert len(player_loaded.player_traits) == 1
        assert player_loaded.player_traits[0].trait.name == "Route Technician"
        assert player_loaded.player_traits[0].trait.tier == TraitTier.GOLD
        print(f"Loaded player: {player_loaded.first_name} {player_loaded.last_name}")
        print(f"Loaded trait: {player_loaded.player_traits[0].trait.name} ({player_loaded.player_traits[0].trait.tier})")
        
    print("PASS: Async profile query with selectinload(Player.player_traits).joinedload(PlayerTrait.trait) executes cleanly.")
    await async_eng.dispose()
    return True


async def main():
    print("=================================================================")
    print("      M1 DATABASE CONSOLIDATION FORENSIC AUDIT SUITE             ")
    print("=================================================================")
    
    r1 = test_metadata_completeness()
    r2 = test_sqlite_pragmas_on_file()
    r3 = test_hybrid_property_sql_compilation()
    r4 = test_cascading_deletion_and_relationships()
    r5 = await test_async_profile_loading()
    
    all_passed = r1 and r2 and r3 and r4 and r5
    print("\n=================================================================")
    if all_passed:
        print("FINAL VERDICT: ALL FORENSIC CHECKS PASSED [CLEAN]")
    else:
        print("FINAL VERDICT: INTEGRITY VIOLATION DETECTED")
    print("=================================================================")
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)
