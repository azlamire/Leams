from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GITHUB_ID: str
    GITHUB_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
