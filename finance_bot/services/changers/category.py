from datetime import UTC, datetime

from loguru import logger

from finance_bot.config import settings
from finance_bot.entities.db import CategoryDB
from finance_bot.infra.repos import AccountRepo, CategoryRepo


class CategoryServiceChanger:
    def __init__(self, account_repo: AccountRepo, category_repo: CategoryRepo) -> None:
        self._account_repo = account_repo
        self._category_repo = category_repo

    async def save(self, telegram_user_id: int, parameters: list[str]) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        if len(parameters) != 2:
            logger.warning(
                f"[#{account_id}] Not enough parameters! Specify the category names in the format: "
                "`/add_category category_name:sub_category_name`"
            )
            return (
                "Недостаточно параметров!\nУкажите названия категорий в формате:\n"
                "/add_category название_категории:название_подкатегории"
            )

        name, name_detail = parameters[0], parameters[1]
        current_datetime: str = (
            datetime.now(tz=UTC)
            .replace(microsecond=0)
            .strftime(settings.UTC0_DATETIME_FORMAT)
        )

        item: CategoryDB = CategoryDB(
            name=name,
            name_detail=name_detail,
            account_id=account_id,
            created_at=current_datetime,
        )
        await self._category_repo.insert(item=item)

        logger.debug(
            f"[#{account_id}] The category `{name}:{name_detail}` has been added."
        )
        return f"Категория `{name}:{name_detail}` была добавлена успешно."
