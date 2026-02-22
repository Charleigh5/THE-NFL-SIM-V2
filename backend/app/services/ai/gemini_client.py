"""
Gemini Client for Vertex AI
============================
Wrapper around Google's GenAI SDK for structured output generation.

Best Practices Applied:
- Singleton pattern for connection reuse
- Async-first design for FastAPI compatibility
- Structured JSON output using Pydantic schemas
- Graceful fallback when API key is missing
- Retry logic with exponential backoff

Reference: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference
"""

import asyncio
import logging
import os
from functools import lru_cache
from typing import Any, Optional, TypeVar

from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class GeminiClient:
    """
    Client wrapper for Google Gemini via Vertex AI.

    Uses the google-genai SDK with structured JSON output support.
    Falls back to template-based responses if API key is missing.
    """

    _instance: Optional["GeminiClient"] = None

    def __init__(self):
        self._client = None
        self._model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self._api_key = os.getenv("VERTEX_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self._initialized = False

    @classmethod
    def get_instance(cls) -> "GeminiClient":
        """Get singleton instance of GeminiClient."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _ensure_initialized(self) -> bool:
        """Initialize the client if not already done."""
        if self._initialized:
            return self._client is not None

        self._initialized = True

        if not self._api_key:
            logger.warning(
                "No VERTEX_API_KEY or GOOGLE_API_KEY found in environment. "
                "AI features will use fallback templates."
            )
            return False

        try:
            from google import genai
            from google.genai.types import HttpOptions  # type: ignore[import-not-found]

            # Initialize client with API key
            self._client = genai.Client(
                api_key=self._api_key, http_options=HttpOptions(api_version="v1")
            )
            logger.info(f"Gemini client initialized with model: {self._model_name}")
            return True

        except ImportError:
            logger.error("google-genai package not installed. Run: pip install google-genai")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return False

    @property
    def is_available(self) -> bool:
        """Check if AI features are available."""
        return self._ensure_initialized()

    async def generate_text(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048
    ) -> str | None:
        """
        Generate plain text response.

        Args:
            prompt: The input prompt
            temperature: Creativity parameter (0.0-1.0)
            max_tokens: Maximum tokens in response

        Returns:
            Generated text or None on failure
        """
        if not self._ensure_initialized():
            return None

        try:
            from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]

            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config=GenerateContentConfig(temperature=temperature, max_output_tokens=max_tokens),
            )
            return response.text

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return None

    async def generate_structured(
        self,
        prompt: str,
        response_schema: type[T],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> T | None:
        """
        Generate structured JSON response conforming to Pydantic schema.

        Uses Gemini's native JSON schema enforcement for reliable parsing.

        Args:
            prompt: The input prompt
            response_schema: Pydantic model class for output validation
            temperature: Creativity parameter (0.0-1.0)
            max_tokens: Maximum tokens in response

        Returns:
            Parsed Pydantic model instance or None on failure
        """
        if not self._ensure_initialized():
            return None

        try:
            from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]

            # Build JSON schema from Pydantic model
            json_schema = response_schema.model_json_schema()

            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    response_mime_type="application/json",
                    response_schema=json_schema,
                ),
            )

            # Parse response into Pydantic model
            import json

            try:
                if not response.text:
                    raise ValueError("Empty response from Gemini")
                data = json.loads(response.text)
                return response_schema.model_validate(data)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON from Gemini: {response.text}")
                return None
            except Exception as e:
                logger.error(f"Validation failed: {e}")
                return None

        except Exception as e:
            logger.error(f"Structured generation failed: {e}")
            return None

    async def generate_with_retry(
        self,
        prompt: str,
        response_schema: type[T] | None = None,
        max_retries: int = 3,
        temperature: float = 0.7,
    ) -> Any | None:
        """
        Generate with exponential backoff retry.

        Args:
            prompt: The input prompt
            response_schema: Optional Pydantic schema for structured output
            max_retries: Maximum retry attempts
            temperature: Creativity parameter

        Returns:
            Generated response or None after all retries fail
        """
        for attempt in range(max_retries):
            try:
                if response_schema:
                    result = await self.generate_structured(prompt, response_schema, temperature)
                else:
                    result = await self.generate_text(prompt, temperature)

                if result is not None:
                    return result

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")

            # Exponential backoff
            if attempt < max_retries - 1:
                wait_time = 2**attempt
                await asyncio.sleep(wait_time)

        logger.error(f"All {max_retries} attempts failed")
        return None


# Convenience function for getting the singleton
@lru_cache(maxsize=1)
def get_gemini_client() -> GeminiClient:
    """Get the singleton Gemini client instance."""
    return GeminiClient.get_instance()
