from uuid import UUID

from pydantic import BaseModel


class City(BaseModel):
    id: UUID
    district_id: UUID
    name: str
    obj_type: str
    population: int
