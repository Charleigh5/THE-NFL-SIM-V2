#!/usr/bin/env python3
"""
Unit Tests for AI Services
==========================
Tests for GeminiClient and ScoutingAIService.

Tests cover:
- GeminiClient fallback behavior when API key is missing
- ScoutingAIService report generation with fallback
- ScoutingAIService backstory generation with fallback
- Caching behavior
"""

from unittest.mock import MagicMock, patch

import pytest

from app.schemas.scouting import PlayerBackstory, ScoutingReportAI  # type: ignore[import-not-found]
from app.services.ai.gemini_client import (  # type: ignore[import-not-found]
    GeminiClient,
)
from app.services.ai.scouting_ai import (  # type: ignore[import-not-found]
    ScoutingAIService,
    _backstory_cache,
    _report_cache,
    clear_scouting_cache,
    get_scouting_ai_service,
)

# ============================================================================
# GEMINI CLIENT TESTS
# ============================================================================

class TestGeminiClient:
    """Tests for GeminiClient wrapper."""

    def test_singleton_pattern(self):
        """Singleton returns same instance."""
        client1 = GeminiClient.get_instance()
        client2 = GeminiClient.get_instance()
        assert client1 is client2

    def test_not_available_without_api_key(self):
        """Client reports unavailable when no API key set."""
        # Create fresh instance without API key
        with patch.dict("os.environ", {}, clear=True):
            client = GeminiClient()
            client._api_key = None
            client._initialized = False

            # Should return False when no API key
            assert not client._ensure_initialized()

    @pytest.mark.asyncio
    async def test_generate_text_returns_none_without_client(self):
        """generate_text returns None when client unavailable."""
        client = GeminiClient()
        client._initialized = True
        client._client = None  # Simulate unavailable

        result = await client.generate_text("test prompt")
        assert result is None

    @pytest.mark.asyncio
    async def test_generate_structured_returns_none_without_client(self):
        """generate_structured returns None when client unavailable."""
        client = GeminiClient()
        client._initialized = True
        client._client = None

        result = await client.generate_structured("test", ScoutingReportAI)
        assert result is None


# ============================================================================
# SCOUTING AI SERVICE TESTS
# ============================================================================

class TestScoutingAIService:
    """Tests for ScoutingAIService."""

    @pytest.fixture(autouse=True)
    def clear_cache_before_each(self):
        """Clear caches before each test."""
        clear_scouting_cache()
        yield
        clear_scouting_cache()

    @pytest.fixture
    def service(self):
        """Create service with mocked client."""
        svc = ScoutingAIService()
        # Mock client as unavailable to trigger fallbacks
        svc.client = MagicMock()
        svc.client.is_available = False
        return svc

    @pytest.mark.asyncio
    async def test_generate_scouting_report_fallback(self, service):
        """Fallback generates valid report when AI unavailable."""
        report = await service.generate_scouting_report(
            player_name="Test Player",
            position="QB",
            overall_rating=85
        )

        assert report is not None
        assert isinstance(report, ScoutingReportAI)
        assert report.summary is not None
        assert len(report.strengths) >= 2
        assert len(report.weaknesses) >= 1
        assert report.draft_grade in ["A", "B+", "B", "C+", "C", "D", "F"]

    @pytest.mark.asyncio
    async def test_generate_backstory_fallback(self, service):
        """Fallback generates valid backstory when AI unavailable."""
        backstory = await service.generate_backstory(
            player_name="Test Player",
            position="WR",
            college="Ohio State"
        )

        assert backstory is not None
        assert isinstance(backstory, PlayerBackstory)
        assert backstory.hometown is not None
        assert backstory.background is not None
        assert len(backstory.personality_traits) >= 2

    @pytest.mark.asyncio
    async def test_report_caching(self, service):
        """Reports are cached and reused."""
        # Generate first report
        report1 = await service.generate_scouting_report(
            player_name="Cache Test",
            position="RB",
            overall_rating=80
        )

        # Generate same report - should come from cache
        report2 = await service.generate_scouting_report(
            player_name="Cache Test",
            position="RB",
            overall_rating=80
        )

        assert report1 is report2  # Same object from cache

    @pytest.mark.asyncio
    async def test_report_cache_bypass(self, service):
        """Cache can be bypassed with use_cache=False."""
        # Generate first report
        report1 = await service.generate_scouting_report(
            player_name="Bypass Test",
            position="WR",
            overall_rating=75
        )

        # Generate again with cache bypass
        report2 = await service.generate_scouting_report(
            player_name="Bypass Test",
            position="WR",
            overall_rating=75,
            use_cache=False
        )

        # Should be different objects (both fallbacks, but regenerated)
        # Note: Content may be same, but they're independently generated
        assert report1 is not report2

    @pytest.mark.asyncio
    async def test_backstory_caching(self, service):
        """Backstories are cached and reused."""
        backstory1 = await service.generate_backstory(
            player_name="Story Test",
            position="TE"
        )

        backstory2 = await service.generate_backstory(
            player_name="Story Test",
            position="TE"
        )

        assert backstory1 is backstory2

    def test_clear_cache(self, service):
        """Cache clearing works correctly."""
        # Pre-populate caches
        _report_cache[("Test", "QB", 90)] = MagicMock()
        _backstory_cache[("Test", "WR")] = MagicMock()

        result = clear_scouting_cache()

        assert result["reports_cleared"] == 1
        assert result["backstories_cleared"] == 1
        assert len(_report_cache) == 0
        assert len(_backstory_cache) == 0

    @pytest.mark.asyncio
    async def test_high_rated_player_gets_high_grade(self, service):
        """Players with high overall get appropriate draft grades."""
        report = await service.generate_scouting_report(
            player_name="Elite Player",
            position="QB",
            overall_rating=95
        )

        assert report.draft_grade == "A"
        assert "All-Pro" in report.ceiling_projection or "Pro Bowl" in report.ceiling_projection

    @pytest.mark.asyncio
    async def test_low_rated_player_gets_low_grade(self, service):
        """Players with low overall get appropriate draft grades."""
        report = await service.generate_scouting_report(
            player_name="Project Player",
            position="LB",
            overall_rating=55
        )

        assert report.draft_grade in ["C", "C+"]


# ============================================================================
# SINGLETON TESTS
# ============================================================================

class TestServiceSingleton:
    """Tests for service singleton pattern."""

    def test_get_scouting_ai_service_singleton(self):
        """get_scouting_ai_service returns same instance."""
        svc1 = get_scouting_ai_service()
        svc2 = get_scouting_ai_service()
        assert svc1 is svc2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
