from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_description: str
    app_version: str
    env: str
    mongo_db_url: str
    mongo_namespace_default: str
    jwt_secret: str
    jwt_expiration: int
    model_config = SettingsConfigDict(env_file=".env")

all_config = Settings()

APP_NAME = all_config.app_name
APP_DESCRIPTION = all_config.app_description
APP_VERSION = all_config.app_version

ENV = all_config.env
DEBUG = (ENV == "development")

MONGO_DB_URL = all_config.mongo_db_url
MONGO_NAMESPACE_DEFAULT = all_config.mongo_namespace_default

JWT_SECRET = all_config.jwt_secret
JWT_EXPIRATION = all_config.jwt_expiration