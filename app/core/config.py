from typing import Optional, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, EmailStr, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Template"
    API_V1_STR: str = "/api/v1"

    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_SERVER: str
    MYSQL_PORT: int = 3306
    MYSQL_DB: str

    # Security
    SECRET_KEY: str = "changethis123456789"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_MINUTES: int = 15

    # Redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> any:
        if isinstance(v, str):
            return v
        return f"mysql+aiomysql://{info.data['MYSQL_USER']}:{info.data['MYSQL_PASSWORD']}@{info.data['MYSQL_SERVER']}:{info.data['MYSQL_PORT']}/{info.data['MYSQL_DB']}"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
