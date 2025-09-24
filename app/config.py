from os import environ as env

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    user: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
