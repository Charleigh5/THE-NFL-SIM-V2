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

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from typing import Optional

from app.services.ai.gemini_client import GeminiClient, get_gemini_client  # type: ignore[import-not-found]
from app.services.ai.scouting_ai import (  # type: ignore[import-not-found]
    ScoutingAIService,
    get_scouting_ai_service,
    clear_scouting_cache,
    _report_cache,
    _backstory_cache
)
from app.schemas.scouting import ScoutingReportAI, PlayerBackstory  # type: ignore[import-not-found]


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

# ============================================================================
# AI PROVIDER REGISTRY & ADAPTER TESTS
# ============================================================================

from app.services.ai.ai_provider import (
    AIProviderType,
    BaseAIProvider,
    DeterministicFallbackProvider,
    GoogleGenAIProvider,
    OpenAICompatibleProvider,
    AIProviderRegistry,
    get_ai_registry
)
from app.services.broadcasting_service import (
    BroadcastingService,
    BroadcastStyle,
    GameContext,
    BroadcastCommentaryAI
)
from app.services.playbook.gameplan_ai import (
    GameplanAIService,
    OpponentFilmTendency,
    GameplanCounterProposal
)
from app.services.weekly_recap_service import (
    format_deterministic_recap_script,
    mock_gemini_recap_script
)


class TestAIProviderArchitecture:
    """Tests for the provider-agnostic AI adapter framework."""

    def test_registry_singleton(self):
        reg1 = get_ai_registry()
        reg2 = get_ai_registry()
        assert reg1 is reg2

    def test_deterministic_fallback_always_available(self):
        provider = DeterministicFallbackProvider()
        assert provider.is_available is True
        assert provider.provider_type == AIProviderType.DETERMINISTIC_FALLBACK

    @pytest.mark.asyncio
    async def test_deterministic_fallback_structured_output(self):
        provider = DeterministicFallbackProvider()
        result = await provider.generate_structured("prompt", BroadcastCommentaryAI)
        assert result is not None
        assert isinstance(result, BroadcastCommentaryAI)
        assert result.energy_level is not None

    def test_provider_resolution_without_keys(self):
        with patch.dict("os.environ", {}, clear=True):
            reg = AIProviderRegistry()
            active = reg.get_provider()
            assert active.provider_type == AIProviderType.DETERMINISTIC_FALLBACK


class TestBroadcastingAICommentary:
    """Tests for Tier 1 Broadcast commentary generation."""

    @pytest.fixture
    def game_context(self):
        return GameContext(
            home_team="Kansas City Chiefs",
            away_team="Baltimore Ravens",
            home_score=24,
            away_score=21,
            quarter=4,
            time_remaining="1:45",
            down=3,
            yards_to_go=7,
            field_position=65,
            possession_team="Kansas City Chiefs",
            is_redzone=False,
            is_two_minute=True
        )

    @pytest.mark.asyncio
    async def test_generate_commentary_ai_fallback(self, game_context):
        service = BroadcastingService(style=BroadcastStyle.ESPN)
        play_data = {
            "qb": "Patrick Mahomes",
            "receiver": "Travis Kelce",
            "yards": 18
        }

        commentary = await service.generate_commentary_ai("PASS_COMPLETE", play_data, game_context)
        assert commentary is not None
        assert isinstance(commentary, BroadcastCommentaryAI)
        assert len(commentary.call) > 0
        assert commentary.energy_level >= 5


class TestGameplanAIService:
    """Tests for Tier 2 Opponent Film Study & Gameplan counter-scheming."""

    @pytest.fixture
    def gameplan_service(self):
        return GameplanAIService()

    @pytest.mark.asyncio
    async def test_formulate_gameplan_deep_pass_counter(self, gameplan_service):
        tendencies = OpponentFilmTendency(
            opponent_team_name="Buffalo Bills",
            deep_pass_rate=0.35,
            blitz_rate_3rd_down=0.20,
            star_offensive_threat="Josh Allen"
        )
        plan = await gameplan_service.formulate_gameplan("Buffalo Bills", tendencies)
        assert plan is not None
        assert isinstance(plan, GameplanCounterProposal)
        assert "Cover 4" in plan.defensive_counter.primary_coverage
        assert plan.confidence_rating >= 80

    @pytest.mark.asyncio
    async def test_formulate_gameplan_heavy_blitz_counter(self, gameplan_service):
        tendencies = OpponentFilmTendency(
            opponent_team_name="Minnesota Vikings",
            deep_pass_rate=0.15,
            blitz_rate_3rd_down=0.45,
            star_offensive_threat="Justin Jefferson"
        )
        plan = await gameplan_service.formulate_gameplan("Minnesota Vikings", tendencies)
        assert plan is not None
        assert "Quick" in plan.offensive_counter.primary_concept or "Screens" in plan.offensive_counter.primary_concept


class TestWeeklyRecapScript:
    """Tests for weekly wrap-up recap script generation."""

    def test_deterministic_recap_script_output(self):
        script = format_deterministic_recap_script(1, [], [])
        assert "# Week 1 Around the League" in script
        assert mock_gemini_recap_script(1, [], []) == script


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

