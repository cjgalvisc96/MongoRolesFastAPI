from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class SettingsTest(BaseSettings):
    PROJECT_NAME: str = (
        "Mongo and FastAPI Role Based Access Control Auth Service"
    )
    API_V1_PREFIX: str = "/api/v1"
    APP_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    USERS_OPEN_REGISTRATION: str
    FIRST_SUPER_ADMIN_EMAIL: str
    FIRST_SUPER_ADMIN_PASSWORD: str
    FIRST_SUPER_ADMIN_ACCOUNT_NAME: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    MONGO_DATABASE_URI: str = None

    @validator("MONGO_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return f"mongodb://{values.get('DB_HOST')}:{values.get('DB_PORT')}"

    class Config:
        case_sensitive = True
        env_file = ".env.test"


@lru_cache()
def get_settings():
    return SettingsTest()


settings_test = get_settings()
