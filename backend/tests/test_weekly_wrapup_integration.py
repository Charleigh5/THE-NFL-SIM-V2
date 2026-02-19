"""
Integration test for the Weekly Wrap-Up system.
Verifies the flow: EventBus -> NewsFeedService -> Database -> WeeklyRecapService
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.engine.event_bus import EventBus, EventType
from app.models.base import Base
from app.models.news_item import NewsCategory, NewsItem
from app.models.rpg_event import RPGEvent
from app.services.news_feed_service import NewsFeedService
from app.services.weekly_recap_service import WeeklyRecapService


@pytest.fixture
def test_db():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestNewsFeedService:
    """Test suite for NewsFeedService."""

    def test_process_sack_event(self, test_db):
        """Verify that a SACK_EVENT creates both an RPGEvent and a NewsItem."""
        payload = {
            "season_id": 2025,
            "week": 5,
            "game_id": "GAME_123",
            "play_id": "PLAY_456",
            "sacked_player_id": 10,
            "defense_player_id": 55,
            "yards_lost": 8
        }

        # Process the event
        NewsFeedService.process_event(EventType.SACK_EVENT, payload, test_db)

        # Verify RPGEvent was created
        rpg_events = test_db.query(RPGEvent).all()
        assert len(rpg_events) == 1
        assert rpg_events[0].event_type == EventType.SACK_EVENT
        assert rpg_events[0].season_id == 2025
        assert rpg_events[0].week == 5
        assert rpg_events[0].processed is True

        # Verify NewsItem was created
        news_items = test_db.query(NewsItem).all()
        assert len(news_items) == 1
        assert "sack" in news_items[0].headline.lower()
        assert news_items[0].category == NewsCategory.GAME_RESULT

    def test_process_touchdown_event(self, test_db):
        """Verify that a TOUCHDOWN_EVENT creates a high-importance NewsItem."""
        payload = {
            "season_id": 2025,
            "week": 5,
            "game_id": "GAME_123",
            "play_id": "PLAY_789",
            "scoring_player_id": 20,
            "scoring_team_id": 1,
            "touchdown_type": "PASS",
            "yards": 45
        }

        NewsFeedService.process_event(EventType.TOUCHDOWN_EVENT, payload, test_db)

        news_items = test_db.query(NewsItem).all()
        assert len(news_items) == 1
        assert "touchdown" in news_items[0].headline.lower()
        assert news_items[0].importance_score == 0.7  # Touchdowns are important

    def test_get_news_filters_by_week(self, test_db):
        """Verify that get_news correctly filters by season and week."""
        service = NewsFeedService()

        # Create events for different weeks
        NewsFeedService.process_event(EventType.SACK_EVENT, {
            "season_id": 2025, "week": 5, "game_id": "G1", "play_id": "P1"
        }, test_db)
        NewsFeedService.process_event(EventType.SACK_EVENT, {
            "season_id": 2025, "week": 6, "game_id": "G2", "play_id": "P2"
        }, test_db)

        # Get news for week 5 only
        week5_news = service.get_news(test_db, season_id=2025, week=5)
        assert len(week5_news) == 1
        assert week5_news[0].week == 5


class TestWeeklyRecapService:
    """Test suite for WeeklyRecapService."""

    def test_generate_recap_creates_summary(self, test_db):
        """Verify that generate_recap aggregates events into a summary."""
        # First, create some events for the week
        NewsFeedService.process_event(EventType.TOUCHDOWN_EVENT, {
            "season_id": 2025, "week": 10, "game_id": "G1", "play_id": "P1",
            "scoring_player_id": 1, "scoring_team_id": 1, "yards": 75
        }, test_db)
        NewsFeedService.process_event(EventType.SACK_EVENT, {
            "season_id": 2025, "week": 10, "game_id": "G1", "play_id": "P2"
        }, test_db)

        # Generate the recap
        service = WeeklyRecapService()
        recap = service.generate_recap(test_db, season_id=2025, week=10)

        assert recap is not None
        assert recap.season_id == 2025
        assert recap.week == 10
        assert "Week 10" in recap.summary_text
        assert recap.play_of_the_week_id is not None  # Should have identified the TD

    def test_generate_recap_is_idempotent(self, test_db):
        """Verify that calling generate_recap twice returns the same recap."""
        NewsFeedService.process_event(EventType.SACK_EVENT, {
            "season_id": 2025, "week": 11, "game_id": "G1", "play_id": "P1"
        }, test_db)

        service = WeeklyRecapService()
        recap1 = service.generate_recap(test_db, season_id=2025, week=11)
        recap2 = service.generate_recap(test_db, season_id=2025, week=11)

        assert recap1.id == recap2.id  # Same record returned


class TestEventBusIntegration:
    """Test suite for EventBus -> Service integration."""

    def test_eventbus_subscription(self):
        """Verify that NewsFeedService subscribes to EventBus events."""
        # The NewsFeedService constructor subscribes to events
        service = NewsFeedService()

        # Check that subscriptions exist
        assert EventType.SACK_EVENT in EventBus._subscribers
        assert EventType.TOUCHDOWN_EVENT in EventBus._subscribers
