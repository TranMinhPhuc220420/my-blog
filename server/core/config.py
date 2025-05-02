from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  app_name: str
  app_description: str
  app_version: str

  env: str

  api_key: str

  mongo_db_url: str
  mongo_namespace_default: str

  jwt_secret_key: str
  jwt_access_token_expire_minutes: int
  jwt_refresh_secret_key: str
  jwt_refresh_token_expire_minutes: int
  jwt_algorithm: str

  fernet_key: str

  model_config = SettingsConfigDict(env_file=".env")

all_config = Settings()

APP_NAME = all_config.app_name
APP_DESCRIPTION = all_config.app_description
APP_VERSION = all_config.app_version

ENV = all_config.env
DEBUG = (ENV == "development")

API_KEY = all_config.api_key

MONGO_DB_URL = all_config.mongo_db_url
MONGO_NAMESPACE_DEFAULT = all_config.mongo_namespace_default

JWT_SECRET_KEY = all_config.jwt_secret_key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = all_config.jwt_access_token_expire_minutes
JWT_REFRESH_SECRET_KEY = all_config.jwt_refresh_secret_key
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = all_config.jwt_refresh_token_expire_minutes
JWT_ALGORITHM = all_config.jwt_algorithm

FERNET_KEY = all_config.fernet_key

# Constant Keys
KEY_TOKEN_TYPE = "token_type"
KEY_ACCESS_TOKEN = "access_token"
KEY_REFRESH_TOKEN = "refresh_token"

# Error Code
BAD_REQUEST_ERROR_CODE = "bad_request"
EXPIRED_ACCESS_TOKEN_ERROR_CODE = "expired_access_token"
INVALID_ACCESS_TOKEN_ERROR_CODE = "invalid_access_token"