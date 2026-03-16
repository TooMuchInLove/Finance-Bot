from loguru import logger

from finance_bot.entities.db import CategoryDB
from finance_bot.infra.repos import AccountRepo, CategoryRepo


class CategoryServiceSelector:
    def __init__(self, account_repo: AccountRepo, category_repo: CategoryRepo) -> None:
        self._account_repo = account_repo
        self._category_repo = category_repo

    async def get_by_telegram_user_id(self, telegram_user_id: int) -> list[CategoryDB]:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        items: list[CategoryDB] = await self._category_repo.get_by_account_id(
            account_id=account_id
        )
        if not items:
            logger.debug(f"[#{account_id}] No categories were found.")
            return []

        logger.debug(f"[#{account_id}] The list of categories has been received.")
        return items
