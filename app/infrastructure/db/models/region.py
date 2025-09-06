from sqlalchemy import Boolean, Column, String, Uuid

from app.infrastructure.db.models.base import BaseModel


class Region(BaseModel):
    __tablename__ = "region"

    id = Column(Uuid, primary_key=True)
    name = Column(String(100), nullable=False)
    capital = Column(String(100))
    is_deleted = Column(Boolean, default=False)
