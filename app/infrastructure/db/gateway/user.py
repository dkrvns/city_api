import uuid

from sqlalchemy import and_, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interface.user.user import UserDeleter, UserReader, UserSaver
from app.domain.entities.user import UserDM
from app.infrastructure.db.models import User


class UserGateway(UserSaver, UserReader, UserDeleter):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: UserDM) -> uuid.UUID:
        stmt = insert(User).values(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
        )

        await self._session.execute(stmt)
        await self._session.commit()

        return user.id

    async def read_by_email(self, email: str) -> UserDM:
        stmt = select(User).where(and_(User.email == email, User.is_deleted == False))

        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()

        return self._map_row_to_read_model(row)

    async def user_exist(self, user: UserDM) -> bool:
        stmt = select(User).where(
            or_(
                User.email == user.email,
            )
        )

        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row:
            return True

        return False

    async def delete(self, user: UserDM) -> None:
        stmt = update(User).where(and_(User.id == user.id)).values(is_deleted=True)
        await self._session.execute(stmt)
        await self._session.commit()

    @staticmethod
    def _map_row_to_read_model(row: User) -> UserDM:
        return UserDM(
            id=row.id,
            email=row.email,
            hashed_password=row.hashed_password,
        )
