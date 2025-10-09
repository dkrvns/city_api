from collections.abc import AsyncGenerator
from uuid import uuid4

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from city_api.application.interface.transaction_manager import TransactionManager
from city_api.application.interface.uuid_generator import UUIDGenerator
from city_api.config import Config
from city_api.infrastructure.db.main import new_session_maker
from city_api.infrastructure.db.transaction_manager import SqlAlchemyTransactionManager


class CoreProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid4


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    transaction_manager = provide(
        SqlAlchemyTransactionManager, scope=Scope.REQUEST, provides=TransactionManager
    )
