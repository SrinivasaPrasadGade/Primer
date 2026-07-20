from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _BACKEND_DIR.parent


class Settings(BaseSettings):
    # Anchored to this file, not the working directory. A bare ".env" is resolved
    # relative to cwd, so `uvicorn app.main:app` from backend/ silently missed the
    # repo-root .env and every key fell back to its default — an empty
    # GEMINI_API_KEY and, worse, the placeholder JWT secret, with no error.
    # Later files win, so backend/.env can override the shared root one.
    model_config = SettingsConfigDict(
        env_file=(_REPO_ROOT / ".env", _BACKEND_DIR / ".env"),
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://primer:primer_dev@localhost:5432/primer"
    redis_url: str = "redis://localhost:6379"
    gemini_api_key: str = ""

    jwt_secret_key: str = "primer-hackathon-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:19006"]
    upload_dir: str = "./uploads"


settings = Settings()
