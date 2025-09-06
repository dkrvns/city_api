from sqlalchemy import Boolean, Column, Integer, String, Uuid

from app.infrastructure.db.models.base import BaseModel


class City(BaseModel):
    __tablename__ = "city"

    id = Column(Uuid, primary_key=True)
    district_id = Column(Uuid)
    name = Column(String(100), nullable=False)
    obj_type = Column(String(50))
    population = Column(Integer)
    is_deleted = Column(Boolean, default=False)
