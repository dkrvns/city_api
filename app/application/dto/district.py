import uuid
from dataclasses import dataclass


@dataclass(slots=True)
class NewDistrictDTO:
    region_id: uuid.UUID
    name: str
