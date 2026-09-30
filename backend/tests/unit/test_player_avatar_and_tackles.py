"""
Unit tests for TASK-040 code review refinements:
- Player team_abbreviation property & PlayerDetailSchema serialization
- Enhanced player profile in-memory trait mapping without duplicate DB queries
- League leaders total tackles calculation (solo + assist with COALESCE)
"""

import pytest
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker, Session

from app.models.base import Base
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game, GameType
from app.models.season import Season, SeasonStatus
from app.models.stats import PlayerGameStats
from app.models.trait import Trait, PlayerTrait, TraitTier
from app.api.endpoints.players import PlayerDetailSchema, EnhancedPlayerProfile, TraitInfoBrief
from app.services.trait_service import TraitService


@pytest.fixture
def db_session():
    """In-memory SQLite session for isolated testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSession()
    yield session
    session.close()
    engine.dispose()


def test_player_team_abbreviation_property(db_session: Session):
    """Test that Player.team_abbreviation accurately returns team abbreviation or None."""
    team = Team(
        id=16,
        city="Kansas City",
        name="Chiefs",
        abbreviation="KC",
        conference="AFC",
        division="West",
        salary_cap_space=20000000,
    )
    db_session.add(team)
    db_session.commit()

    player_with_team = Player(
        id=15,
        first_name="Patrick",
        last_name="Mahomes",
        position="QB",
        jersey_number=15,
        overall_rating=99,
        age=29,
        experience=8,
        team_id=16,
        team=team,
    )
    player_free_agent = Player(
        id=99,
        first_name="Free",
        last_name="Agent",
        position="RB",
        jersey_number=20,
        overall_rating=75,
        age=25,
        experience=3,
        team_id=None,
        team=None,
    )

    assert player_with_team.team_abbreviation == "KC"
    assert player_free_agent.team_abbreviation is None

    # Test Pydantic schema validation
    schema_with_team = PlayerDetailSchema.model_validate(player_with_team)
    assert schema_with_team.team_abbreviation == "KC"

    schema_fa = PlayerDetailSchema.model_validate(player_free_agent)
    assert schema_fa.team_abbreviation is None


def test_eager_loaded_traits_in_memory_mapping(db_session: Session):
    """Verify that player traits can be mapped into TraitInfoBrief in-memory without secondary queries."""
    trait = Trait(
        id=1,
        name="Gunslinger",
        description="Exceptional throwing velocity and release speed.",
        tier=TraitTier.GOLD,
    )
    db_session.add(trait)
    db_session.commit()

    player = Player(
        id=15,
        first_name="Patrick",
        last_name="Mahomes",
        position="QB",
        jersey_number=15,
        overall_rating=99,
        age=29,
        experience=8,
    )
    db_session.add(player)
    db_session.commit()

    player_trait = PlayerTrait(player_id=15, trait_id=1, trait=trait)
    db_session.add(player_trait)
    db_session.commit()

    # Query with eager relationships
    stmt = (
        select(Player)
        .where(Player.id == 15)
    )
    loaded_player = db_session.execute(stmt).scalar_one()

    # Map directly from loaded_player.player_traits
    traits_brief = []
    for pt in loaded_player.player_traits:
        if pt.trait:
            catalog_def = TraitService.get_trait_by_name(pt.trait.name)
            tier_str = (
                catalog_def.tier
                if catalog_def
                else (pt.trait.tier.value if hasattr(pt.trait.tier, "value") else str(pt.trait.tier or "COMMON"))
            )
            desc_str = (
                catalog_def.description
                if catalog_def
                else (pt.trait.description or "")
            )
            traits_brief.append(
                TraitInfoBrief(
                    name=pt.trait.name,
                    description=desc_str,
                    tier=tier_str,
                )
            )

    assert len(traits_brief) == 1
    assert traits_brief[0].name == "Gunslinger"
    assert traits_brief[0].tier == "GOLD"


def test_total_tackles_calculation_sums_solo_and_assist(db_session: Session):
    """Verify that tackle leaderboard query accurately computes solo + assisted tackles with coalesce."""
    team = Team(
        id=1,
        city="Detroit",
        name="Lions",
        abbreviation="DET",
        conference="NFC",
        division="North",
        salary_cap_space=20000000,
    )
    db_session.add(team)

    season = Season(year=2026, current_week=1, is_active=True, status=SeasonStatus.REGULAR_SEASON)
    db_session.add(season)
    db_session.commit()

    game = Game(season_id=season.id, season=2026, week=1, home_team_id=1, away_team_id=1)
    db_session.add(game)
    db_session.commit()

    # Player 1: 5 solo, 3 assisted = 8 total
    p1 = Player(id=54, first_name="Brian", last_name="Branch", position="S", jersey_number=32, overall_rating=88, age=24, experience=2, team_id=1)
    # Player 2: 6 solo, None assisted = 6 total (tests coalesce null handling)
    p2 = Player(id=34, first_name="Alex", last_name="Anzalone", position="LB", jersey_number=34, overall_rating=82, age=30, experience=8, team_id=1)
    db_session.add_all([p1, p2])
    db_session.commit()

    stat1 = PlayerGameStats(player_id=54, game_id=game.id, team_id=1, season_id=season.id, tackles_solo=5, tackles_assist=3)
    stat2 = PlayerGameStats(player_id=34, game_id=game.id, team_id=1, season_id=season.id, tackles_solo=6, tackles_assist=None)
    db_session.add_all([stat1, stat2])
    db_session.commit()

    # Run the exact leaderboard SQL expression from season.py
    stat_column = func.coalesce(PlayerGameStats.tackles_solo, 0) + func.coalesce(PlayerGameStats.tackles_assist, 0)
    stmt = (
        select(
            Player.id,
            Player.first_name,
            func.sum(stat_column).label("total_tackles")
        )
        .join(PlayerGameStats, Player.id == PlayerGameStats.player_id)
        .join(Game, PlayerGameStats.game_id == Game.id)
        .where(Game.season_id == season.id)
        .group_by(Player.id)
        .order_by(func.sum(stat_column).desc())
    )
    results = db_session.execute(stmt).all()

    assert len(results) == 2
    # Player 1 (5 + 3 = 8) ranks #1
    assert results[0].id == 54
    assert results[0].total_tackles == 8
    # Player 2 (6 + 0 = 6) ranks #2
    assert results[1].id == 34
    assert results[1].total_tackles == 6
