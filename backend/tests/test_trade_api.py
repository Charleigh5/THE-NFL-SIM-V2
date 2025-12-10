"""Tests for the Trade API endpoints."""

import pytest

class TestTradeEvaluateEndpoint:
    """Tests for POST /api/trades/evaluate endpoint."""

    @pytest.mark.asyncio
    async def test_evaluate_trade_success(self, async_client, sample_players, sample_teams):
        """Test successful trade evaluation with real DB data."""
        # Use sample data IDs
        response = await async_client.post(
            "/api/trades/evaluate",
            json={
                "offered_player_ids": [1], # Patrick Mahomes
                "requested_player_ids": [3], # Josh Allen
                "target_team_id": 2 # Bills
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "decision" in data
        assert "score" in data
        assert "reasoning" in data
        assert data["decision"] in ["ACCEPT", "REJECT", "COUNTER"]

    @pytest.mark.asyncio
    async def test_evaluate_trade_missing_target_team(self, async_client):
        """Test trade evaluation with non-existent target team."""
        response = await async_client.post(
            "/api/trades/evaluate",
            json={
                "offered_player_ids": [1],
                "requested_player_ids": [2],
                "target_team_id": 99999
            }
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_evaluate_trade_empty_request(self, async_client, sample_teams):
        """Test trade evaluation with empty assets."""
        response = await async_client.post(
            "/api/trades/evaluate",
            json={
                "offered_player_ids": [],
                "requested_player_ids": [],
                "target_team_id": 2
            }
        )
        # Should return 400 because trade must include assets
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_evaluate_trade_invalid_player_id(self, async_client, sample_teams):
        """Test trade evaluation with invalid player ID."""
        response = await async_client.post(
            "/api/trades/evaluate",
            json={
                "offered_player_ids": [99999],
                "requested_player_ids": [],
                "target_team_id": 2
            }
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_evaluate_trade_player_wrong_team(self, async_client, sample_players):
        """Test trade evaluation where requested player belongs to wrong team."""
        # Request Mahomes (Team 1) from Team 2
        response = await async_client.post(
            "/api/trades/evaluate",
            json={
                "offered_player_ids": [],
                "requested_player_ids": [1], # Mahomes (Team 1)
                "target_team_id": 2 # Bills
            }
        )
        # This currently returns 400 in the implementation
        assert response.status_code == 400


class TestTradeOfferEndpoint:
    """Tests for POST /api/trades/offer endpoint."""

    @pytest.mark.asyncio
    async def test_submit_offer_stub(self, async_client, sample_players):
        """Test that offer endpoint returns stub response."""
        response = await async_client.post(
            "/api/trades/offer",
            json={
                "offered_player_ids": [1],
                "requested_player_ids": [3],
                "target_team_id": 2
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PENDING"
        assert data["offer_id"] == 0


class TestTradePendingEndpoint:
    """Tests for GET /api/trades/pending/{team_id} endpoint."""

    @pytest.mark.asyncio
    async def test_get_pending_offers_stub(self, async_client):
        """Test that pending offers endpoint returns empty lists."""
        response = await async_client.get("/api/trades/pending/1")
        assert response.status_code == 200
        data = response.json()
        assert data["incoming"] == []
        assert data["outgoing"] == []
