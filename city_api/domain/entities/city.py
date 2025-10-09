import uuid
from dataclasses import dataclass


@dataclass
class CityDM:
    id: uuid.UUID
    district_id: uuid.UUID
    name: str
    obj_type: str
    population: int
