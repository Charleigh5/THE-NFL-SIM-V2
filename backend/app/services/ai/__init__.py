"""
AI Services Module (2026 Production Architecture)
=================================================
Provider-agnostic AI services with multi-tier intelligence routing:
- Tier 0: 100% Offline Deterministic Rules & Template Fallbacks
- Tier 1: Low-Latency Flash / Local SLM Generation
- Tier 2: Deep Strategic Multi-Agent Reasoning
"""

from app.services.ai.gemini_client import GeminiClient, get_gemini_client
from app.services.ai.ai_provider import (
    AIProviderType,
    BaseAIProvider,
    DeterministicFallbackProvider,
    GoogleGenAIProvider,
    OpenAICompatibleProvider,
    AIProviderRegistry,
    get_ai_registry,
)
from app.services.ai.scouting_ai import (
    ScoutingAIService,
    get_scouting_ai_service,
)

__all__ = [
    "GeminiClient",
    "get_gemini_client",
    "AIProviderType",
    "BaseAIProvider",
    "DeterministicFallbackProvider",
    "GoogleGenAIProvider",
    "OpenAICompatibleProvider",
    "AIProviderRegistry",
    "get_ai_registry",
    "ScoutingAIService",
    "get_scouting_ai_service",
]
