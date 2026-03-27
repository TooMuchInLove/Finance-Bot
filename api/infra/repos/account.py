from logging import Logger

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from api.entities.exceptions import ConflictError, NotFoundError
from api.entities.database import AccountDB
from api.entities.repos import IAccountRepo
from api.infra.db_context import DataBaseContext
from api.infra.models import AccountModel


class AccountRepo(IAccountRepo):
    def __init__(self, db_context: DataBaseContext, logger: Logger) -> None:
        self._db_context = db_context
        self._logger = logger

    async def insert(self, item: AccountDB) -> AccountDB:
        try:
            async with self._db_context.get_session() as session:
                data = insert(AccountModel).values(**item.model_dump()).returning(AccountModel)
                result = await session.execute(data)
                account = result.scalar_one()
                await session.commit()

                return AccountDB.model_validate(account, from_attributes=True)
        except IntegrityError as err:
            message = f"[{item.telegram_user_id}] The user already exists"
            raise ConflictError(message=message) from err

    async def select_by_telegram_user_id(self, telegram_user_id: int) -> AccountDB:
        async with self._db_context.get_session() as session:
            data = select(AccountModel).where(AccountModel.telegram_user_id == telegram_user_id)
            result = await session.execute(data)
            account = result.scalar_one_or_none()

            if not account:
                raise NotFoundError(f"[{telegram_user_id}] Account with not found")

            return AccountDB.model_validate(account, from_attributes=True)
