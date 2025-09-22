import uuid
from dataclasses import dataclass


@dataclass(slots=True)
class NewCityDTO:
    district_id: uuid.UUID
    name: str
    obj_type: str
    population: int


@dataclass(slots=True)
class UpdatedCityDTO:
    city_id: uuid.UUID
    district_id: uuid.UUID
    name: str
    obj_type: str
    population: int
