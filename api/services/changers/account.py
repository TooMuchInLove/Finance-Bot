from datetime import UTC, datetime

from logging import Logger

from api.entities.database import AccountDB
from api.entities.repos import IAccountRepo
from api.entities.responses import AccountResponse
from api.entities.services import IAccountServiceChanger
from api.services.decorators import catch_api_errors


class AccountServiceChanger(IAccountServiceChanger):
    def __init__(self, account_repo: IAccountRepo, logger: Logger) -> None:
        self._account_repo = account_repo
        self._logger = logger

    @catch_api_errors
    async def create(self, telegram_user_id: int, telegram_username: str) -> AccountResponse:
        current_datetime = datetime.now(tz=UTC).replace(microsecond=0, tzinfo=UTC)

        item = await self._account_repo.insert(
            item=AccountDB(
                telegram_user_id=telegram_user_id,
                telegram_username=telegram_username,
                created_at=current_datetime,
            )
        )

        return AccountResponse(
            id=item.id,
            telegram_user_id=item.telegram_user_id,
            telegram_username=item.telegram_username,
            created_at=item.created_at,
        )
