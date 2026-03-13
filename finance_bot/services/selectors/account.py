from loguru import logger

from finance_bot.entities.db import AccountDB
from finance_bot.infra.repos import AccountRepo


class AccountServiceSelector:
    def __init__(self, account_repo: AccountRepo) -> None:
        self._account_repo = account_repo

    async def get_info_by_telegram_user_id(self, telegram_user_id: int) -> str:
        account: AccountDB = await self._account_repo.get_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )

        logger.debug(
            f"[#{account.id}] Your account was created on `{account.created_at}`."
        )
        return f"Ваш аккаунт был создан <code>{account.created_at}</code>"
