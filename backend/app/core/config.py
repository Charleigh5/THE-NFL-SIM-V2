from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./nfl_sim.db"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
