from os import environ as env
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    user: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')


class AuthSettings(BaseModel):
    jwt_secret: str = Field(alias='JWT_SECRET')
    jwt_algorithm: Literal[
        'HS256',
        'HS384',
        'HS512',
        'RS256',
        'RS384',
        'RS512',
    ] = Field(alias='JWT_ALGORITHM')
    access_token_expire_minutes: int = Field(alias='SESSION_TTL_MIN')
    refresh_token_expire_days: int = Field(alias='SESSION_REFRESH_EXPIRES')


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    auth_settings: AuthSettings = Field(default_factory=lambda: AuthSettings(**env))
