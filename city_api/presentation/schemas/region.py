import uuid

from pydantic import BaseModel


class Region(BaseModel):
    id: uuid.UUID
    name: str
    capital: str


class CreateRegion(BaseModel):
    name: str
    capital: str
