from datetime import UTC, datetime

from loguru import logger

from finance_bot.config import settings
from finance_bot.entities.exceptions import NotEnoughParametersWarning, IntegrityWarning
from finance_bot.entities.db import CategoryDB
from finance_bot.infra.repos import AccountRepo, CategoryRepo


class CategoryServiceChanger:
    def __init__(self, account_repo: AccountRepo, category_repo: CategoryRepo) -> None:
        self._account_repo = account_repo
        self._category_repo = category_repo

    async def save(self, telegram_user_id: int, parameters: list[str]) -> CategoryDB:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        if len(parameters) < 2:
            logger.warning(
                f"[#{account_id}] Not enough parameters! Specify the category names in the format: "
                "`category_name:subcategory_name`"
            )
            message = (
                "Недостаточно параметров!\nУкажите названия категорий в формате:\n"
                "<code>название_категории:название_подкатегории</code>"
            )
            raise NotEnoughParametersWarning(message=message)

        name, name_detail = parameters[0], parameters[1]
        if len(name) < 3 or len(name_detail) < 3:
            logger.warning(
                f"[#{account_id}] The categories names must be longer than 2 characters long! "
                "Specify the category names in the format: `category_name:subcategory_name`"
            )
            message = (
                "Длина названия категорий должна быть больше 2 символов!\n"
                "Укажите названия категорий в формате:\n<code>название_категории:название_подкатегории</code>"
            )
            raise IntegrityWarning(message=message)

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

        logger.debug(f"[#{account_id}] The category `{name}:{name_detail}` has been added.")
        return item

    async def delete(self, telegram_user_id: int, name: str, name_detail: str) -> CategoryDB:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )
        item: CategoryDB = CategoryDB(
            name=name,
            name_detail=name_detail,
            account_id=account_id,
        )
        await self._category_repo.delete(item=item)

        logger.debug(f"[#{account_id}] The category `{name_detail}` has been deleted.")
        return item
