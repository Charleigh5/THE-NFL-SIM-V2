"""
AI Services Module
==================
AI-powered services using Gemini via Vertex AI.
"""

from app.services.ai.gemini_client import GeminiClient, get_gemini_client  # type: ignore[import-not-found]

__all__ = ["GeminiClient", "get_gemini_client"]
