from sqlalchemy import Boolean, Column, String, Uuid

from app.infrastructure.db.models.base import BaseModel


class District(BaseModel):
    __tablename__ = "district"

    id = Column(Uuid, primary_key=True)
    region_id = Column(Uuid)
    name = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False)
