from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class JWTSettings(BaseSettings):
    # HACK:  production do NOT rely on a plain .env file — provide secrets via real environment variables or a secret manager (K8s Secret, AWS Secrets Manager, Vault, etc.).
    """Usual Settings for auth via GitHub"""

    GITHUB_ID: SecretStr
    GITHUB_SECRET: SecretStr
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class LinksSettings(BaseSettings):
    # NOTE: This class will be expanded
    MAIN_PAGE: SecretStr


# NOTE: Idk but GitSettings doesn't work here's the solution but no answers why https://github.com/pydantic/pydantic/issues/3753, they said about dataclass_transform but link was deleted though their solution is workable 1.git_settings = GitSettings.model_validate({})
# BUG: With field and lru_cache doesn't work properly so remain like this
git_settings = JWTSettings.model_validate({})
links = LinksSettings.model_validate({})
