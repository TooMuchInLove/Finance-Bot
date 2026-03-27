from collections.abc import AsyncIterable
from logging import Logger, NullHandler, getLogger

from dishka import Provider, Scope, from_context, provide
from dynaconf import Dynaconf

from api.entities.repos import IAccountRepo, ICategoryRepo
from api.entities.services import (
    IAccountServiceChanger,
    IAccountServiceSelector,
    ICategoryServiceChanger,
    ICategoryServiceSelector,
)
from api.infra.db_context import DataBaseContext
from api.infra.repos import AccountRepo, CategoryRepo
from api.services.changers import AccountServiceChanger, CategoryServiceChanger
from api.services.selectors import AccountServiceSelector, CategoryServiceSelector

logger = getLogger(__name__)


class AppProvider(Provider):
    config = from_context(provides=Dynaconf, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_logger(self) -> Logger:
        console = getLogger("finance-api")
        if not console.handlers:
            console.addHandler(NullHandler())

        return console

    @provide(scope=Scope.APP)
    async def get_database_context(self, config: Dynaconf) -> AsyncIterable[DataBaseContext]:
        async with DataBaseContext(dsn=config.POSTGRES_DSN) as db_context:
            yield db_context

    account_repo = provide(AccountRepo, scope=Scope.APP, provides=IAccountRepo)
    category_repo = provide(CategoryRepo, scope=Scope.APP, provides=ICategoryRepo)

    account_service_changer = provide(AccountServiceChanger, scope=Scope.REQUEST, provides=IAccountServiceChanger)
    account_service_selector = provide(AccountServiceSelector, scope=Scope.REQUEST, provides=IAccountServiceSelector)
    category_service_changer = provide(CategoryServiceChanger, scope=Scope.REQUEST, provides=ICategoryServiceChanger)
    category_service_selector = provide(CategoryServiceSelector, scope=Scope.REQUEST, provides=ICategoryServiceSelector)
