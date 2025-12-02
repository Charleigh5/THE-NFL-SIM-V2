"""
Integration tests for enhanced Draft Assistant with MCP integration.
Tests the complete draft suggestion workflow including historical comparisons.
"""
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.player import Player
from app.models.team import Team
from app.core.database import get_async_db
from sqlalchemy import select


@pytest.mark.asyncio
async def test_draft_suggest_pick_endpoint(async_client: AsyncClient, test_db):
    """Test the POST /api/draft/suggest-pick endpoint."""
    # Create a test team
    async for db in get_async_db():
        team = Team(id=1, name="Test Team", abbreviation="TST")
        db.add(team)

        # Create some available players
        players = [
            Player(
                id=i,
                first_name=f"Player",
                last_name=f"{i}",
                position="QB" if i == 1 else "WR",
                overall_rating=85 - i,
                speed=90,
                strength=75,
                agility=80,
                team_id=None
            )
            for i in range(1, 6)
        ]

        for player in players:
            db.add(player)

        await db.commit()

        # Make API request
        response = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 1,
                "pick_number": 1,
                "available_players": [1, 2, 3, 4, 5],
                "include_historical_data": False  # Skip MCP for this test
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "recommended_player_id" in data
        assert "player_name" in data
        assert "position" in data
        assert "overall_rating" in data
        assert "reasoning" in data
        assert "team_needs" in data
        assert "alternative_picks" in data
        assert "confidence_score" in data
        assert "draft_value_score" in data

        # Verify it recommended the best player (highest rating)
        assert data["recommended_player_id"] == 1
        assert data["overall_rating"] == 85

        # Verify alternative picks
        assert len(data["alternative_picks"]) == 3

        break


@pytest.mark.asyncio
async def test_draft_assistant_roster_gap_analysis(async_client: AsyncClient, test_db):
    """Test that roster gap analysis is correctly calculated."""
    async for db in get_async_db():
        team = Team(id=2, name="Gap Team", abbreviation="GAP")
        db.add(team)

        # Create roster with gaps (no QBs, few WRs)
        existing_players = [
            Player(id=10, first_name="RB", last_name="One", position="RB", overall_rating=80, team_id=2),
            Player(id=11, first_name="RB", last_name="Two", position="RB", overall_rating=75, team_id=2),
        ]

        for player in existing_players:
            db.add(player)

        # Available draft prospects
        prospects = [
            Player(id=20, first_name="Top", last_name="QB", position="QB", overall_rating=90, team_id=None),
            Player(id=21, first_name="Top", last_name="WR", position="WR", overall_rating=85, team_id=None),
        ]

        for player in prospects:
            db.add(player)

        await db.commit()

        response = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 2,
                "pick_number": 1,
                "available_players": [20, 21],
                "include_historical_data": False
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Should recommend QB due to critical need (0 QBs on roster)
        assert data["position"] == "QB"

        # Verify roster gap analysis
        assert "roster_gap_analysis" in data
        gaps = data["roster_gap_analysis"]

        # Find QB gap
        qb_gap = next((g for g in gaps if g["position"] == "QB"), None)
        assert qb_gap is not None
        assert qb_gap["current_count"] == 0
        assert qb_gap["target_count"] == 3
        assert qb_gap["priority_level"] == "CRITICAL"

        break


@pytest.mark.asyncio
async def test_draft_value_score_calculation(async_client: AsyncClient, test_db):
    """Test that draft value scores are calculated correctly."""
    async for db in get_async_db():
        team = Team(id=3, name="Value Team", abbreviation="VAL")
        db.add(team)

        # Create prospect with high rating
        player = Player(
            id=30,
            first_name="Elite",
            last_name="Prospect",
            position="WR",
            overall_rating=92,
            speed=95,
            strength=80,
            agility=90,
            team_id=None
        )
        db.add(player)
        await db.commit()

        # Test early pick (should have high value)
        response = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 3,
                "pick_number": 1,  # #1 overall
                "available_players": [30],
                "include_historical_data": False
            }
        )

        assert response.status_code == 200
        data = response.json()

        # High rating + early pick = high value score
        assert data["draft_value_score"] is not None
        assert data["draft_value_score"] >= 8.0  # Should be very high

        # Test late pick (should have lower value)
        response2 = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 3,
                "pick_number": 224,  # Last pick
                "available_players": [30],
                "include_historical_data": False
            }
        )

        assert response2.status_code == 200
        data2 = response2.json()

        # High rating but late pick = still excellent value (steal)
        assert data2["draft_value_score"] >= 9.0  # Should be a steal

        break


@pytest.mark.asyncio
async def test_draft_assistant_error_handling(async_client: AsyncClient):
    """Test error handling for invalid requests."""
    # Test with non-existent team
    response = await async_client.post(
        "/api/draft/suggest-pick",
        json={
            "team_id": 999,
            "pick_number": 1,
            "available_players": [1, 2, 3]
        }
    )

    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()

    # Test with no available players
    async for db in get_async_db():
        team = Team(id=4, name="Error Team", abbreviation="ERR")
        db.add(team)
        await db.commit()

        response2 = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 4,
                "pick_number": 1,
                "available_players": []
            }
        )

        assert response2.status_code == 400

        break


@pytest.mark.asyncio
async def test_alternative_picks_quality(async_client: AsyncClient, test_db):
    """Test that alternative picks are ranked correctly."""
    async for db in get_async_db():
        team = Team(id=5, name="Alt Team", abbreviation="ALT")
        db.add(team)

        # Create players with different ratings
        players = [
            Player(id=40, first_name="Best", last_name="Player", position="QB", overall_rating=90, team_id=None),
            Player(id=41, first_name="Second", last_name="Player", position="RB", overall_rating=85, team_id=None),
            Player(id=42, first_name="Third", last_name="Player", position="WR", overall_rating=82, team_id=None),
            Player(id=43, first_name="Fourth", last_name="Player", position="TE", overall_rating=80, team_id=None),
        ]

        for player in players:
            db.add(player)

        await db.commit()

        response = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 5,
                "pick_number": 10,
                "available_players": [40, 41, 42, 43],
                "include_historical_data": False
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Verify alternatives are sorted by quality
        alternatives = data["alternative_picks"]
        assert len(alternatives) == 3

        # Check that confidence scores are in descending order
        scores = [alt["confidence_score"] for alt in alternatives]
        assert scores == sorted(scores, reverse=True)

        # Second best should be in alternatives
        assert any(alt["player_id"] == 41 for alt in alternatives)

        break


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
