from sqlalchemy import and_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.auth.refresh_token import RefreshTokenDM
from app.infrastructure.auth.interface.auth_gateway import (
    RefreshTokenDeleter,
    RefreshTokenReader,
    RefreshTokenSaver,
)
from app.infrastructure.db.models.refresh_token import RefreshToken


class RefreshTokenGateway(RefreshTokenSaver, RefreshTokenReader, RefreshTokenDeleter):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, refresh_token: RefreshTokenDM) -> None:
        query = insert(RefreshToken).values(
            token=refresh_token.token,
            username=refresh_token.username,
            expires_at=refresh_token.expires_at,
            revoked=False,
        )

        await self._session.execute(query)
        await self._session.commit()

    async def get_by_username(self, username: str) -> RefreshTokenDM | None:
        query = select(RefreshToken).where(and_(RefreshToken.username == username))
        result = await self._session.execute(query)

        row = result.scalar_one_or_none()
        if not row:
            return None

        return self._map_row_to_read_model(row)

    async def delete(self, token: str) -> None:
        query = (
            update(RefreshToken)
            .where(and_(RefreshToken.token == token))
            .values(revoked=True)
        )

        await self._session.execute(query)
        await self._session.commit()

    @staticmethod
    def _map_row_to_read_model(row: RefreshToken) -> RefreshTokenDM:
        return RefreshTokenDM(
            token=row.token,
            username=row.username,
            expires_at=row.expires_at,
            revoked=row.revoked,
        )
