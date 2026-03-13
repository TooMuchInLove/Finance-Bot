from datetime import UTC, datetime

from loguru import logger

from finance_bot.config import settings
from finance_bot.entities.db import AccountDB
from finance_bot.infra.repos import AccountRepo


class AccountServiceChanger:
    def __init__(self, account_repo: AccountRepo) -> None:
        self._account_repo = account_repo

    async def save(self, telegram_user_id: int, telegram_user_name: str) -> None:
        current_datetime: str = (
            datetime.now(tz=UTC)
            .replace(microsecond=0)
            .strftime(settings.UTC0_DATETIME_FORMAT)
        )

        item: AccountDB = AccountDB(
            telegram_user_id=telegram_user_id,
            telegram_username=telegram_user_name,
            created_at=current_datetime,
        )
        await self._account_repo.insert(item=item)

        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        logger.debug(f"[#{account_id}] Registration/initialization of the user.")
