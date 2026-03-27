from logging import Logger

from api.entities.repos import IAccountRepo
from api.entities.responses import AccountResponse
from api.entities.services import IAccountServiceSelector
from api.services.decorators import catch_api_errors


class AccountServiceSelector(IAccountServiceSelector):
    def __init__(self, account_repo: IAccountRepo, logger: Logger) -> None:
        self._account_repo = account_repo
        self._logger = logger

    @catch_api_errors
    async def get_by_telegram_user_id(self, telegram_user_id: int) -> AccountResponse:
        item = await self._account_repo.select_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )

        return AccountResponse(
            id=item.id,
            telegram_user_id=item.telegram_user_id,
            telegram_username=item.telegram_username,
            created_at=item.created_at,
        )
