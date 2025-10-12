from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GITHUB_ID : str
    GITHUB_SECRET : str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
