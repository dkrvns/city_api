from sqlalchemy import Boolean, Column, LargeBinary, String, Uuid

from app.infrastructure.db.models import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(
        Uuid,
        primary_key=True,
    )
    email = Column(String, unique=True)
    hashed_password = Column(LargeBinary)
    is_deleted = Column(Boolean, default=False)
