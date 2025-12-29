from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


# HACK: Production do NOT rely on a plain .env file — provide secrets via real environment variables or a secret manager (K8s Secret, AWS Secrets Manager, Vault, etc.).
# NOTE: These settings is much better than using usual .env cause' 1. getenv() return str | None and pyright give a lot errors 2. Settings is more like typification


# https://github.com/login/oauth/select_account?client_id=Ov23liSQ51mWVK40l9Vs&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2F&response_type=code&scope=user%3Aemail
class JWTSettings(BaseSettings):
    """This class include all JWT stuff from .env"""

    GITHUB_ID: SecretStr
    GITHUB_SECRET: SecretStr
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class RedisSettings(BaseSettings):
    """This class is for redis"""

    BROKER: SecretStr
    BACKEND_REDIS: SecretStr
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class S3Settings(BaseSettings):
    """This class is for redis"""

    S3_ACCESS_KEY: SecretStr
    S3_SECRET_KEY: SecretStr
    S3_ENDPOINT_KEY: SecretStr
    S3_BUCKET_NAME: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class LinksSettings(BaseSettings):
    """This class include all links stuff from .env"""

    MAIN_PAGE: str
    SYNC_PSQL: str
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# NOTE: Idk but GitSettings doesn't work here's the solution but no answers why https://github.com/pydantic/pydantic/issues/3753, they said about dataclass_transform but link was deleted though their solution is workable 1.git_settings = GitSettings.model_validate({})
# BUG: With field and lru_cache doesn't work properly so remain like this
def get_git_settings():
    return JWTSettings.model_validate({})


def get_links_settings():
    return LinksSettings.model_validate({})


def get_s3_settings():
    return S3Settings.model_validate({})


def get_redis_settings():
    return RedisSettings.model_validate({})
