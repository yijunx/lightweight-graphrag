from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class EnvSettings(BaseSettings):
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    NEO4J_DB: str


class DeployedSettings(EnvSettings): ...


class LocalDevSettings(EnvSettings):
    model_config = SettingsConfigDict(env_file="config", extra="ignore")


def find_config() -> EnvSettings:
    if os.getenv("ENV"):
        return DeployedSettings()

    return LocalDevSettings()


env = find_config()
