"""
AI Services Module
==================
AI-powered services using Gemini via Vertex AI.
"""

from app.services.ai.gemini_client import (  # type: ignore[import-not-found]
    GeminiClient,
    get_gemini_client,
)

__all__ = ["GeminiClient", "get_gemini_client"]
