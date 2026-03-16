from loguru import logger

from finance_bot.entities.db import AccountDB
from finance_bot.infra.repos import AccountRepo


class AccountServiceSelector:
    def __init__(self, account_repo: AccountRepo) -> None:
        self._account_repo = account_repo

    async def get_by_telegram_user_id(self, telegram_user_id: int) -> AccountDB:
        item: AccountDB = await self._account_repo.get_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )

        logger.debug(f"[#{item.id}] Your account was created on `{item.created_at}`.")
        return item
