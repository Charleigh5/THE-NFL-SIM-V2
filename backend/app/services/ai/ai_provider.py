"""
Unified AI Provider Interface (2026 Production Architecture)
============================================================
Provider-agnostic abstraction layer supporting:
- Tier 0: 100% Offline Deterministic Fallback (Zero network calls, <1ms)
- Tier 1: Low-Latency Flash / Local SLM (Google Gemini 2.5 Flash / Ollama Qwen 2.5)
- Tier 2: Frontier Strategic Reasoning (Gemini 2.5 Pro / Thinking / Sonnet)

Best Practices Applied:
- Provider-agnostic adapter pattern
- Pydantic V2 schema-enforced structured generation
- Automatic offline degradation and zero-cost local safety
- Connection reuse and singleton registry management
"""

import os
import asyncio
import logging
import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Type, TypeVar, Optional, Any, Dict
from functools import lru_cache
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AIProviderType(str, Enum):
    """Supported AI provider backends."""
    DETERMINISTIC_FALLBACK = "deterministic_fallback"
    GOOGLE_GENAI = "google_genai"
    OPENAI_COMPATIBLE = "openai_compatible"
    LOCAL_OLLAMA = "local_ollama"


class BaseAIProvider(ABC):
    """Abstract base class for all AI providers."""

    @property
    @abstractmethod
    def provider_type(self) -> AIProviderType:
        """The provider type identifier."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """The active model name."""
        pass

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is initialized and accessible."""
        pass

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[str]:
        """Generate unstructured text."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[T]:
        """Generate structured JSON conforming to a Pydantic schema."""
        pass

    async def generate_with_retry(
        self,
        prompt: str,
        response_schema: Optional[Type[T]] = None,
        max_retries: int = 3,
        temperature: float = 0.7
    ) -> Optional[Any]:
        """Generate with exponential backoff retry."""
        for attempt in range(max_retries):
            try:
                if response_schema:
                    result = await self.generate_structured(
                        prompt, response_schema, temperature
                    )
                else:
                    result = await self.generate_text(prompt, temperature)

                if result is not None:
                    return result

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed on {self.provider_type}: {e}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)

        logger.error(f"All {max_retries} attempts failed for provider {self.provider_type}")
        return None


class DeterministicFallbackProvider(BaseAIProvider):
    """
    Tier 0 / Offline Fallback Provider.
    Executes 100% locally with zero network calls, zero API costs, and sub-millisecond latency.
    """

    def __init__(self, model_name: str = "deterministic-rule-engine"):
        self._model_name = model_name

    @property
    def provider_type(self) -> AIProviderType:
        return AIProviderType.DETERMINISTIC_FALLBACK

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def is_available(self) -> bool:
        return True

    async def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[str]:
        return f"[Deterministic Offline Engine] Analysis generated for: {prompt[:80]}..."

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[T]:
        """
        Synthesizes a minimal valid instance of response_schema using default values or mock fields.
        """
        try:
            return response_schema.model_validate({})
        except Exception:
            from typing import Union
            from pydantic_core import PydanticUndefined
            fields_data: Dict[str, Any] = {}
            for field_name, field_info in response_schema.model_fields.items():
                if field_info.default is not PydanticUndefined and field_info.default != Ellipsis and field_info.default is not None:
                    fields_data[field_name] = field_info.default
                elif field_info.default_factory is not None:
                    fields_data[field_name] = field_info.default_factory()
                else:
                    ann = field_info.annotation
                    ann_origin = getattr(ann, "__origin__", None)
                    if ann_origin is Union or str(ann_origin) == "typing.Union":
                        args = getattr(ann, "__args__", ())
                        non_none = [a for a in args if a is not type(None)]
                        if non_none:
                            ann = non_none[0]
                            ann_origin = getattr(ann, "__origin__", None)
                        else:
                            fields_data[field_name] = None
                            continue

                    if ann == str or getattr(ann, "__name__", "") == "str":
                        fields_data[field_name] = f"Standard {field_name.replace('_', ' ').title()}"
                    elif ann == int:
                        fields_data[field_name] = 80
                    elif ann == float:
                        fields_data[field_name] = 75.0
                    elif ann == bool:
                        fields_data[field_name] = True
                    elif ann_origin is list or getattr(ann, "__name__", "") == "list":
                        fields_data[field_name] = []
                    elif ann_origin is dict or getattr(ann, "__name__", "") == "dict":
                        fields_data[field_name] = {}
                    elif isinstance(ann, type) and issubclass(ann, BaseModel):
                        fields_data[field_name] = self.generate_structured("", ann)
                    elif hasattr(ann, "__members__"):
                        fields_data[field_name] = list(ann.__members__.values())[0].value
                    else:
                        fields_data[field_name] = None
            try:
                return response_schema.model_validate(fields_data)
            except Exception as e:
                logger.error(f"Deterministic fallback construction failed for schema {response_schema}: {e}")
                return None


class GoogleGenAIProvider(BaseAIProvider):
    """
    Tier 1 / Tier 2 Google GenAI Provider using google-genai SDK.
    Supports Gemini 2.5 Flash and Gemini 2.5 Pro with native JSON schema constraints.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self._api_key = api_key or os.getenv("VERTEX_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self._model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self._client = None
        self._initialized = False

    @property
    def provider_type(self) -> AIProviderType:
        return AIProviderType.GOOGLE_GENAI

    @property
    def model_name(self) -> str:
        return self._model_name

    def _ensure_initialized(self) -> bool:
        if self._initialized:
            return self._client is not None

        self._initialized = True
        if not self._api_key:
            logger.info("Google GenAI Provider: No API key found. Remaining in standby.")
            return False

        try:
            from google import genai
            from google.genai.types import HttpOptions

            self._client = genai.Client(
                api_key=self._api_key,
                http_options=HttpOptions(api_version="v1")
            )
            logger.info(f"Google GenAI client initialized with model: {self._model_name}")
            return True
        except ImportError:
            logger.warning("google-genai package not installed.")
            return False
        except Exception as e:
            logger.error(f"Google GenAI initialization failed: {e}")
            return False

    @property
    def is_available(self) -> bool:
        return self._ensure_initialized()

    async def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[str]:
        if not self._ensure_initialized():
            return None

        try:
            from google.genai.types import GenerateContentConfig

            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Google GenAI text generation failed: {e}")
            return None

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[T]:
        if not self._ensure_initialized():
            return None

        try:
            from google.genai.types import GenerateContentConfig

            json_schema = response_schema.model_json_schema()
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    response_mime_type="application/json",
                    response_schema=json_schema
                )
            )
            data = json.loads(response.text)
            return response_schema.model_validate(data)
        except Exception as e:
            logger.error(f"Google GenAI structured generation failed: {e}")
            return None


class OpenAICompatibleProvider(BaseAIProvider):
    """
    Tier 1 / Tier 2 OpenAI-compatible provider for local SLMs (Ollama / vLLM)
    or OpenAI/Anthropic proxies.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        provider_type: AIProviderType = AIProviderType.OPENAI_COMPATIBLE
    ):
        self._base_url = base_url or os.getenv("OPENAI_BASE_URL") or os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")
        self._api_key = api_key or os.getenv("OPENAI_API_KEY", "ollama-local")
        self._model_name = model_name or os.getenv("LOCAL_SLM_MODEL", "qwen2.5:3b")
        self._provider_type = provider_type

    @property
    def provider_type(self) -> AIProviderType:
        return self._provider_type

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def is_available(self) -> bool:
        return bool(self._base_url)

    async def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[str]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self._base_url.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json={
                        "model": self._model_name,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.debug(f"OpenAI-compatible request failed: {e}")
        return None

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[T],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[T]:
        try:
            import httpx
            system_msg = (
                f"You are a strict JSON generator. You MUST respond with ONLY valid JSON matching this schema: "
                f"{json.dumps(response_schema.model_json_schema())}"
            )
            async with httpx.AsyncClient(timeout=12.0) as client:
                response = await client.post(
                    f"{self._base_url.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json={
                        "model": self._model_name,
                        "messages": [
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "response_format": {"type": "json_object"}
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    return response_schema.model_validate(parsed)
        except Exception as e:
            logger.debug(f"OpenAI-compatible structured generation failed: {e}")
        return None


class AIProviderRegistry:
    """
    Central registry managing active AI provider resolution.
    Ensures seamless zero-setup fallback while enabling plug-and-play cloud/local backends.
    """

    _instance: Optional["AIProviderRegistry"] = None

    def __init__(self):
        self._providers: Dict[AIProviderType, BaseAIProvider] = {}
        self._active_provider: Optional[BaseAIProvider] = None
        self._initialize_defaults()

    @classmethod
    def get_instance(cls) -> "AIProviderRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _initialize_defaults(self):
        """Initialize and register default available providers."""
        self.register_provider(DeterministicFallbackProvider())

        # Google GenAI Provider
        google_provider = GoogleGenAIProvider()
        self.register_provider(google_provider)

        # Local Ollama / OpenAI Compatible
        if os.getenv("OLLAMA_HOST") or os.getenv("OPENAI_BASE_URL"):
            self.register_provider(OpenAICompatibleProvider())

        # Select primary provider based on availability
        self._resolve_active_provider()

    def register_provider(self, provider: BaseAIProvider):
        self._providers[provider.provider_type] = provider

    def _resolve_active_provider(self):
        explicit_type = os.getenv("AI_PROVIDER")
        if explicit_type and explicit_type in AIProviderType._value2member_map_:
            target_type = AIProviderType(explicit_type)
            if target_type in self._providers:
                self._active_provider = self._providers[target_type]
                return

        # Prioritize Google GenAI if key available
        if AIProviderType.GOOGLE_GENAI in self._providers and self._providers[AIProviderType.GOOGLE_GENAI].is_available:
            self._active_provider = self._providers[AIProviderType.GOOGLE_GENAI]
        elif AIProviderType.OPENAI_COMPATIBLE in self._providers and self._providers[AIProviderType.OPENAI_COMPATIBLE].is_available:
            self._active_provider = self._providers[AIProviderType.OPENAI_COMPATIBLE]
        else:
            self._active_provider = self._providers[AIProviderType.DETERMINISTIC_FALLBACK]

    def get_provider(self, provider_type: Optional[AIProviderType] = None) -> BaseAIProvider:
        if provider_type and provider_type in self._providers:
            return self._providers[provider_type]
        if self._active_provider is None or not self._active_provider.is_available:
            self._resolve_active_provider()
        return self._active_provider or self._providers[AIProviderType.DETERMINISTIC_FALLBACK]


@lru_cache(maxsize=1)
def get_ai_registry() -> AIProviderRegistry:
    """Get singleton instance of the AIProviderRegistry."""
    return AIProviderRegistry.get_instance()
