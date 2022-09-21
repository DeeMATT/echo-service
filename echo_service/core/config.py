import os

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DEBUG: bool
    APP_HOST: str
    APP_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"


class DevelopmentConfig(Settings):
    ENV: str = "development"
    DEBUG: bool = True


class ProductionConfig(Settings):
    ENV: str = "production"
    DEBUG: bool = False


@lru_cache()
def get_settings():
    env = os.getenv("ENV", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Settings = get_settings()
