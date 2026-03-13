from collections import defaultdict

from loguru import logger

from finance_bot.entities.db import CategoryDB
from finance_bot.infra.repos import AccountRepo, CategoryRepo
from finance_bot.user import get_index_emoji


class CategoryServiceSelector:
    def __init__(self, account_repo: AccountRepo, category_repo: CategoryRepo) -> None:
        self._account_repo = account_repo
        self._category_repo = category_repo

    async def get_categories_by_telegram_user_id(self, telegram_user_id: int) -> str:
        response: str = "📚 <b>КАТЕГОРИИ</b>:\n"

        account_id: int = await self._account_repo.get_id(telegram_user_id=telegram_user_id)

        items: list[CategoryDB] = await self._category_repo.get_by_account_id(account_id=account_id)
        if not items:
            logger.debug(f"[#{account_id}] No categories were found.")
            return f"{response}┗\t Не найдено."

        categories: defaultdict = defaultdict(list)
        for index, item in enumerate(items):
            categories[item.name].append(item.name_detail)

        for key, items in categories.items():
            response += f"┃\n┣\t<code>{key}</code>:\n┃\t┃\n"
            for index, item in enumerate(items, start=1):
                index_emoji: str = await get_index_emoji(index=index)
                if index == len(items):
                    response += f"┃\t┗\t{index_emoji} <code>{item}</code>\n"
                else:
                    response += f"┃\t┣\t{index_emoji} <code>{item}</code>\n"

        logger.debug(f"[#{account_id}] The list of categories has been received.")
        return response
