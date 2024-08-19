import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    NEO4J_DB: str

    EMBEDDING_ENDPOINT: str
    EMBEDDING_MODEL_UID: str

    WEAVIATE_HTTP_HOST: str
    WEAVIATE_HTTP_PORT: int
    WEAVIATE_HTTP_SECURE: bool
    WEAVIATE_GRPC_HOST: str
    WEAVIATE_GRPC_PORT: int
    WEAVIATE_GRPC_SECURE: bool
    WEAVIATE_TOKEN: Optional[str] = None

    WEAVIATE_COLLECTION_NAME: str


class DeployedSettings(EnvSettings): ...


class LocalDevSettings(EnvSettings):
    model_config = SettingsConfigDict(env_file="config", extra="ignore")


def find_config() -> EnvSettings:
    if os.getenv("ENV"):
        return DeployedSettings()

    return LocalDevSettings()


env = find_config()
