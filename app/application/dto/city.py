import uuid
from dataclasses import dataclass


@dataclass(slots=True)
class NewCityDTO:
    district_id: uuid.UUID
    name: str
    obj_type: str
    population: int
