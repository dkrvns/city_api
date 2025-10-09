from dataclasses import dataclass


@dataclass(slots=True)
class NewRegionDTO:
    name: str
    capital: str
