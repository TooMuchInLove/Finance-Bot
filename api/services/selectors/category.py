from uuid import UUID

from logging import Logger

from api.entities.database import CategoryDB
from api.entities.repos import ICategoryRepo
from api.entities.responses import CategoryResponse
from api.entities.services import ICategoryServiceSelector
from api.services.decorators import catch_api_errors


class CategoryServiceSelector(ICategoryServiceSelector):
    def __init__(self, category_repo: ICategoryRepo, logger: Logger) -> None:
        self._category_repo = category_repo
        self._logger = logger

    @catch_api_errors
    async def get_by_account(self, account_id: UUID) -> list[CategoryResponse]:
        """Получить данные по всем категориям:подкатегориям для пользователя"""

        result: list[CategoryResponse] = []
        items = await self._category_repo.select_by_account(account_id=account_id)
        if not items:
            return result

        for item in items:
            result.append(
                CategoryResponse(
                    account_id=item.account_id,
                    name=item.name,
                    sub_name=item.sub_name,
                    created_at=item.created_at,
                )
            )

        return result

    @catch_api_errors
    async def get_by_account_and_category(self, account_id: UUID, name: str) -> list[CategoryResponse]:
        """Получить данные по всем подкатегориям для пользователя и категории"""

        result: list[CategoryResponse] = []
        items = await self._category_repo.select_by_account_and_category(
            item=CategoryDB(
                account_id=account_id,
                name=name,
            ),
        )
        if not items:
            return result

        for item in items:
            result.append(
                CategoryResponse(
                    account_id=item.account_id,
                    name=item.name,
                    sub_name=item.sub_name,
                    created_at=item.created_at,
                )
            )

        return result

    @catch_api_errors
    async def get_by_account_and_category_and_subcategory(self, account_id: UUID, name: str, sub_name: str) -> CategoryResponse:
        """Получить данные по подкатегории для пользователя и категории"""

        item = await self._category_repo.select_by_account_and_category_and_subcategory(
            item=CategoryDB(
                account_id=account_id,
                name=name,
                sub_name=sub_name,
            ),
        )

        return CategoryResponse(
            account_id=item.account_id,
            name=item.name,
            sub_name=item.sub_name,
            created_at=item.created_at,
        )
