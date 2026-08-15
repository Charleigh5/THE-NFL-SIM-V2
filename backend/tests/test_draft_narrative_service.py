"""Unit tests for the DraftNarrativeService."""
import pytest
from unittest.mock import MagicMock
from app.services.draft_narrative_service import DraftNarrativeService
from app.models.player import Player, Position
from app.models.team import Team
from app.models.news_item import NewsItem, NewsCategory
from app.schemas.offseason import FreeAgentSigning


class MockPlayer:
    def __init__(self, id, first_name, last_name, position, overall_rating):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position.value if isinstance(position, Position) else position
        self.overall_rating = overall_rating


class MockTeam:
    def __init__(self, id, name, city="Detroit"):
        self.id = id
        self.name = name
        self.city = city


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def narrative_service(mock_db):
    return DraftNarrativeService(mock_db)


def test_pick_narrative_top_5_selection(narrative_service, mock_db):
    """Test cornerstone narrative generated for top 5 overall selection."""
    player = MockPlayer(1, "Caleb", "Williams", "QB", 92)
    team = MockTeam(1, "Bears", "Chicago")

    def get_side_effect(model_cls, pk):
        if model_cls == Player:
            return player
        if model_cls == Team:
            return team
        return None

    mock_db.get.side_effect = get_side_effect

    news = narrative_service.generate_pick_narrative(
        season_id=1,
        round_num=1,
        pick_number=1,
        team_id=1,
        player_id=1
    )

    assert news is not None
    assert "Cornerstone Selected" in news.headline
    assert news.importance_score == 1.0
    assert news.category == NewsCategory.DRAFT_NEWS
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_free_agency_narrative_blockbuster(narrative_service, mock_db):
    """Test blockbuster headline generated for superstar free agent signing."""
    signings = [
        FreeAgentSigning(
            player_id=10,
            player_name="Justin Jefferson",
            position="WR",
            overall_rating=96,
            age=26,
            team_id=5,
            team_name="Minnesota Vikings",
            contract_years=4,
            total_value=140_000_000,
            guaranteed=100_000_000,
            annual_avg=35_000_000,
            signing_grade="A+",
            signing_round=1,
            bidding_teams_count=8
        )
    ]

    items = narrative_service.generate_free_agency_narratives(season_id=1, signings=signings)
    assert len(items) == 1
    item = items[0]
    assert "BLOCKBUSTER" in item.headline
    assert item.importance_score >= 0.90
    assert item.category == NewsCategory.TRANSACTION
    mock_db.commit.assert_called()
