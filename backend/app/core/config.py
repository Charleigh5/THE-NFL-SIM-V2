from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # Database
    DATABASE_URL: str = "sqlite:///./nfl_sim.db"
    ASYNC_DATABASE_URL: str | None = None

    @property
    def async_database_url(self) -> str:
        if self.ASYNC_DATABASE_URL:
            return self.ASYNC_DATABASE_URL

        if "sqlite" in self.DATABASE_URL:
            return self.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600

    # API Configuration
    API_TITLE: str = "Stellar Sagan - NFL Simulation Engine"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "Backend API for the Stellar Sagan NFL Football Simulation."

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
        "http://localhost:5199",
        "http://127.0.0.1:5199",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "text"
    LOG_DIR: str = "logs"
    LOG_MAX_BYTES: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5

    # Application
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # External Real-Time Roster API Configuration
    RAPIDAPI_KEY: str | None = None
    RAPIDAPI_HOST: str = "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    SPORTSDATAIO_API_KEY: str | None = None
    ROSTER_SYNC_PROVIDER: str = "auto"  # 'auto', 'tank01', 'sportsdataio', 'nflverse'

    # Redis & High-Throughput Caching
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    ROSTER_CACHE_TTL_SECONDS: int = 60

    # VoiceStudio Sidecar & Narrator Cache (TASK-NARRATOR-001)
    VOICESTUDIO_BASE_URL: str = "http://127.0.0.1:3900"
    VOICESTUDIO_VOICE_ID: str = "en_anchor_male"
    VOICESTUDIO_MODEL: str = "OmniVoice"  # Note: k2-fsa/OmniVoice weights are CC-BY-NC (non-commercial)
    VOICESTUDIO_SEED: int = 42
    NARRATOR_CACHE_DIR: str = "logs/narrator_cache"
    NARRATOR_CACHE_MAX_FILES: int = 128

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
