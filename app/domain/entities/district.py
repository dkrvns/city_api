import uuid
from dataclasses import dataclass


@dataclass
class DistrictDM:
    id: uuid.UUID
    region_id: uuid.UUID
    name: str
