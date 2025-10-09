from uuid import UUID

from pydantic import BaseModel


class District(BaseModel):
    id: UUID
    region_id: UUID
    name: str
