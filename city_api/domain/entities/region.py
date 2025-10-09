import uuid
from dataclasses import dataclass


@dataclass
class RegionDM:
    id: uuid.UUID
    name: str
    capital: str
