"""
Integration tests for TraitEvolutionService and StorylineEventService.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.player import Player
from app.models.rpg_event import RPGEvent
from app.models.trait import Trait, PlayerTrait, TraitTier
from app.engine.event_bus import EventType
from app.services.trait_evolution_service import TraitEvolutionService, TRAIT_TRIGGERS
from app.services.storyline_service import StorylineEventService, StorylineType


@pytest.fixture
def test_db():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_player(test_db):
    """Create a sample player for testing."""
    player = Player(
        id=1,
        first_name="Test",
        last_name="Player",
        position="QB",
        age=25,
        height=75,
        weight=220
    )
    test_db.add(player)
    test_db.commit()
    return player


class TestTraitEvolutionService:
    """Test suite for TraitEvolutionService."""

    def test_gunslinger_trait_awarded_on_4_tds(self, test_db, sample_player):
        """Verify that throwing 4+ TDs in a game awards the Gunslinger trait."""
        service = TraitEvolutionService()

        # Create 4 TD events for this player in the same game
        for i in range(4):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                player_id=sample_player.id,
                season_id=2025,
                week=5,
                game_id="GAME_123",
                payload={"yards": 20 + i * 10}
            )
            test_db.add(event)
        test_db.commit()

        # Check triggers for this game
        triggered = service.check_trait_triggers(
            test_db, sample_player.id, season_id=2025, game_id="GAME_123"
        )

        assert len(triggered) == 1
        assert triggered[0]["trait_name"] == "Gunslinger"
        assert triggered[0]["action"] == "EARNED"
        assert triggered[0]["tier"] == TraitTier.GOLD.value

        # Verify trait is in database
        player_trait = test_db.query(PlayerTrait).filter_by(player_id=sample_player.id).first()
        assert player_trait is not None

    def test_no_trait_if_below_threshold(self, test_db, sample_player):
        """Verify that traits are not awarded if threshold isn't met."""
        service = TraitEvolutionService()

        # Create only 2 TD events (threshold is 4)
        for i in range(2):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                player_id=sample_player.id,
                season_id=2025,
                week=5,
                game_id="GAME_123",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        triggered = service.check_trait_triggers(
            test_db, sample_player.id, season_id=2025, game_id="GAME_123"
        )

        assert len(triggered) == 0

    def test_trait_not_awarded_twice(self, test_db, sample_player):
        """Verify that a player can't earn the same trait twice."""
        service = TraitEvolutionService()

        # Create 4 TD events
        for i in range(4):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                player_id=sample_player.id,
                season_id=2025,
                week=5,
                game_id="GAME_123",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        # First check - should award
        triggered1 = service.check_trait_triggers(
            test_db, sample_player.id, season_id=2025, game_id="GAME_123"
        )
        assert len(triggered1) == 1

        # Second check - should not award again
        triggered2 = service.check_trait_triggers(
            test_db, sample_player.id, season_id=2025, game_id="GAME_123"
        )
        assert len(triggered2) == 0

    def test_remove_trait(self, test_db, sample_player):
        """Verify that traits can be removed."""
        service = TraitEvolutionService()

        # First award a trait
        for i in range(4):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                player_id=sample_player.id,
                season_id=2025,
                week=5,
                game_id="GAME_123",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        service.check_trait_triggers(test_db, sample_player.id, season_id=2025, game_id="GAME_123")

        # Now remove it
        result = service.remove_trait(test_db, sample_player.id, "Gunslinger")

        assert result is not None
        assert result["action"] == "LOST"

        # Verify trait is removed from database
        player_trait = test_db.query(PlayerTrait).filter_by(player_id=sample_player.id).first()
        assert player_trait is None


class TestStorylineEventService:
    """Test suite for StorylineEventService."""

    def test_hot_streak_detection(self, test_db):
        """Verify that a hot streak storyline is detected."""
        service = StorylineEventService()

        # Create many TD events for a team
        for i in range(10):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                team_id=1,
                season_id=2025,
                week=5,
                game_id=f"GAME_{i}",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        storylines = service.check_for_storyline_triggers(test_db, team_id=1, season_id=2025, week=5)

        assert len(storylines) >= 1
        hot_streak = [s for s in storylines if s.storyline_type == StorylineType.HOT_STREAK]
        assert len(hot_streak) == 1

    def test_cold_streak_detection(self, test_db):
        """Verify that a cold streak storyline is detected."""
        service = StorylineEventService()

        # Create many turnover events for a team
        for i in range(8):
            event = RPGEvent(
                event_type=EventType.TURNOVER_EVENT,
                team_id=2,
                season_id=2025,
                week=5,
                game_id=f"GAME_{i}",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        storylines = service.check_for_storyline_triggers(test_db, team_id=2, season_id=2025, week=5)

        assert len(storylines) >= 1
        cold_streak = [s for s in storylines if s.storyline_type == StorylineType.COLD_STREAK]
        assert len(cold_streak) == 1

    def test_storyline_intensity_increases(self, test_db):
        """Verify that storyline intensity increases over time."""
        service = StorylineEventService()

        # Create initial TD events
        for i in range(10):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                team_id=3,
                season_id=2025,
                week=5,
                game_id=f"GAME_{i}",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        # First check
        storylines1 = service.check_for_storyline_triggers(test_db, team_id=3, season_id=2025, week=5)
        initial_intensity = storylines1[0].intensity

        # Add more events and check again
        for i in range(10, 15):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                team_id=3,
                season_id=2025,
                week=6,
                game_id=f"GAME_{i}",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        storylines2 = service.check_for_storyline_triggers(test_db, team_id=3, season_id=2025, week=6)
        new_intensity = storylines2[0].intensity

        assert new_intensity > initial_intensity

    def test_breakout_player_detection(self, test_db, sample_player):
        """Verify that a breakout player storyline is detected."""
        service = StorylineEventService()

        # Create TD events for a specific player
        for i in range(4):
            event = RPGEvent(
                event_type=EventType.TOUCHDOWN_EVENT,
                player_id=sample_player.id,
                team_id=1,
                season_id=2025,
                week=5,
                game_id=f"GAME_{i}",
                payload={}
            )
            test_db.add(event)
        test_db.commit()

        storylines = service.check_for_storyline_triggers(test_db, team_id=1, season_id=2025, week=5)

        breakout = [s for s in storylines if s.storyline_type == StorylineType.BREAKOUT_PLAYER]
        assert len(breakout) == 1
        assert breakout[0].player_id == sample_player.id
