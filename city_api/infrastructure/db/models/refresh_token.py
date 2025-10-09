from sqlalchemy import Boolean, Column, DateTime, String

from city_api.infrastructure.db.models import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = 'refresh_token'
    token = Column(String, primary_key=True)
    username = Column(String)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)
