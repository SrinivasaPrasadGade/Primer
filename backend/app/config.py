from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    database_url: str = "postgresql+asyncpg://primer:primer_dev@localhost:5432/primer"
    redis_url: str = "redis://localhost:6379"
    gemini_api_key: str = ""

    jwt_secret_key: str = "primer-hackathon-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:19006"]
    upload_dir: str = "./uploads"


settings = Settings()
