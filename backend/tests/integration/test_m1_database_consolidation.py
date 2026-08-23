import pytest
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload, joinedload

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
    HallOfFame,
    GM,
    GMDecision,
    Team,
    Game,
    Season,
)
from app.core.database import engine, is_sqlite


def test_f01_player_game_starts_consolidation(db_session):
    """
    F01: PlayerGameStarts table consolidation.
    Verifies canonical model columns, hybrid position_started property,
    and relationships to Player and Game.
    """
    # Create player and game
    season = Season(year=2026)
    db_session.add(season)
    team = Team(name="Tigers", city="Detroit", abbreviation="DET", conference="NFC", division="North")
    db_session.add(team)
    db_session.commit()

    player = Player(
        first_name="Frank",
        last_name="Ragnow",
        position="C",
        team_id=team.id,
        overall_rating=90
    )
    db_session.add(player)

    game = Game(
        season_id=season.id,
        season=2026,
        week=1,
        home_team_id=team.id,
        away_team_id=team.id
    )
    db_session.add(game)
    db_session.commit()

    # Create PlayerGameStarts record
    start = PlayerGameStarts(
        player_id=player.id,
        game_id=game.id,
        team_id=team.id,
        season_id=season.id,
        week=1,
        position="C",
        teammates_hash="abc123olhash"
    )
    db_session.add(start)
    db_session.commit()
    db_session.refresh(start)

    assert start.id is not None
    assert start.player_id == player.id
    assert start.game_id == game.id
    assert start.team_id == team.id
    assert start.season_id == season.id
    assert start.week == 1
    assert start.position == "C"
    assert start.position_started == "C"
    assert start.teammates_hash == "abc123olhash"
    assert start.player.first_name == "Frank"
    assert start.game.week == 1

    # Verify PlayerGameStart alias works identically
    assert PlayerGameStart is PlayerGameStarts

    # Verify query by position_started expression
    query_stmt = select(PlayerGameStarts).where(PlayerGameStarts.position_started == "C")
    res = db_session.execute(query_stmt).scalar_one_or_none()
    assert res is not None
    assert res.id == start.id


def test_f02_alembic_models_registered_in_metadata():
    """
    F02: Alembic model discovery.
    Verifies all models are registered in Base.metadata.tables.
    """
    tables = Base.metadata.tables.keys()

    required_tables = [
        "player",
        "player_attributes",
        "player_contract",
        "player_physics",
        "player_injury",
        "player_progression",
        "player_game_starts",
        "team",
        "game",
        "season",
        "traits",
        "player_traits",
        "gm",
        "gm_decisions",
        "hall_of_fame",
        "playoff_matchup",
        "depthchart",
        "news_items",
        "scouts",
        "gameplans",
    ]

    for table in required_tables:
        assert table in tables, f"Expected table '{table}' in Base.metadata.tables"


def test_f03_player_traits_eager_loading(db_session):
    """
    F03: Player profile trait relationship loading.
    Verifies selectinload(Player.player_traits).joinedload(PlayerTrait.trait) query executes cleanly.
    """
    p = Player(
        first_name="Sauce",
        last_name="Gardner",
        position="CB",
        overall_rating=95
    )
    db_session.add(p)
    db_session.commit()

    trait = Trait(
        name="Island Lockdown",
        description="Elite man coverage ability",
        tier=TraitTier.GOLD,
        effect_type=TraitEffectType.BOOST
    )
    db_session.add(trait)
    db_session.commit()

    pt = PlayerTrait(
        player_id=p.id,
        trait_id=trait.id,
        source=TraitSource.DEVELOPMENT
    )
    db_session.add(pt)
    db_session.commit()

    # Query with selectinload + joinedload
    stmt = (
        select(Player)
        .options(selectinload(Player.player_traits).joinedload(PlayerTrait.trait))
        .where(Player.id == p.id)
    )
    result = db_session.execute(stmt)
    loaded_player = result.scalar_one_or_none()

    assert loaded_player is not None
    assert len(loaded_player.player_traits) == 1
    assert loaded_player.player_traits[0].trait.name == "Island Lockdown"
    assert loaded_player.player_traits[0].trait.tier == TraitTier.GOLD


def test_f04_hybrid_property_subqueries_in_select_and_where(db_session):
    """
    F04: Hybrid property expressions.
    Verifies that Player.speed, Player.strength, Player.agility, etc.,
    can be used directly in SQL select() and .where() expressions without Comparator exceptions.
    """
    p1 = Player(
        first_name="Tyreek",
        last_name="Hill",
        position="WR",
        overall_rating=98,
        speed=99,
        acceleration=99,
        strength=65,
        agility=98,
        awareness=92,
        forty_yard_dash=4.29
    )
    p2 = Player(
        first_name="Derrick",
        last_name="Henry",
        position="RB",
        overall_rating=95,
        speed=90,
        acceleration=88,
        strength=95,
        agility=84,
        awareness=90,
        bench_press=25
    )
    db_session.add_all([p1, p2])
    db_session.commit()

    # Query columns directly in select()
    stmt = select(
        Player.id,
        Player.first_name,
        Player.speed,
        Player.strength,
        Player.agility,
        Player.acceleration,
        Player.awareness,
        Player.forty_yard_dash
    ).where(Player.id.in_([p1.id, p2.id])).order_by(Player.speed.desc())

    rows = db_session.execute(stmt).all()
    assert len(rows) == 2
    assert rows[0][1] == "Tyreek"
    assert rows[0][2] == 99  # speed
    assert rows[0][3] == 65  # strength
    assert rows[0][7] == 4.29  # forty_yard_dash

    assert rows[1][1] == "Derrick"
    assert rows[1][2] == 90  # speed
    assert rows[1][3] == 95  # strength

    # Query in where() clause
    speed_stmt = select(Player).where(Player.speed > 92)
    fast_players = db_session.execute(speed_stmt).scalars().all()
    assert len(fast_players) == 1
    assert fast_players[0].first_name == "Tyreek"


def test_f05_player_decomposition_cascade_delete(db_session):
    """
    F05: 1:1 decomposition relationships cascade delete.
    Verifies that deleting a Player cascades to delete-orphan on
    PlayerAttributes, PlayerContract, PlayerPhysics, PlayerInjury, and PlayerProgression.
    """
    p = Player(
        first_name="Cascade",
        last_name="Test",
        position="DE",
        overall_rating=80,
        speed=82,
        contract_salary=3000000
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)

    player_id = p.id
    attr_id = p.attributes.id
    contract_id = p.contract.id
    physics_id = p.physics.id
    injury_id = p.injury.id
    prog_id = p.progression.id

    assert attr_id is not None
    assert contract_id is not None

    # Delete player
    db_session.delete(p)
    db_session.commit()

    # Check satellites are deleted
    assert db_session.execute(select(PlayerAttributes).where(PlayerAttributes.id == attr_id)).scalar_one_or_none() is None
    assert db_session.execute(select(PlayerContract).where(PlayerContract.id == contract_id)).scalar_one_or_none() is None
    assert db_session.execute(select(PlayerPhysics).where(PlayerPhysics.id == physics_id)).scalar_one_or_none() is None
    assert db_session.execute(select(PlayerInjury).where(PlayerInjury.id == injury_id)).scalar_one_or_none() is None
    assert db_session.execute(select(PlayerProgression).where(PlayerProgression.id == prog_id)).scalar_one_or_none() is None


def test_f06_sqlite_wal_and_pragmas():
    """
    F06: SQLite WAL mode and busy timeout pragmas.
    Verifies event listener pragmas on app.core.database.engine.
    """
    if is_sqlite:
        with engine.connect() as conn:
            journal_mode = conn.execute(text("PRAGMA journal_mode;")).scalar()
            busy_timeout = conn.execute(text("PRAGMA busy_timeout;")).scalar()
            foreign_keys = conn.execute(text("PRAGMA foreign_keys;")).scalar()

            assert journal_mode.lower() in ["wal", "memory"]
            assert busy_timeout is not None
            assert int(busy_timeout) == 5000
            assert int(foreign_keys) == 1
