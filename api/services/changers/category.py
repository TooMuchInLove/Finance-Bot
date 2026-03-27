from datetime import UTC, datetime
from uuid import UUID

from logging import Logger

from api.entities.database import CategoryDB
from api.entities.repos import ICategoryRepo
from api.entities.responses import CategoryResponse
from api.entities.services import ICategoryServiceChanger
from api.services.decorators import catch_api_errors


class CategoryServiceChanger(ICategoryServiceChanger):
    def __init__(self, category_repo: ICategoryRepo, logger: Logger) -> None:
        self._category_repo = category_repo
        self._logger = logger

    @catch_api_errors
    async def create(self, account_id: UUID, name: str, sub_name: str) -> CategoryResponse:
        """Создать категорию:подкатегорию"""

        current_datetime = datetime.now(tz=UTC).replace(microsecond=0, tzinfo=UTC)

        item = await self._category_repo.insert(
            item=CategoryDB(
                account_id=account_id,
                name=name,
                sub_name=sub_name,
                created_at=current_datetime,
            )
        )

        return CategoryResponse(
            account_id=item.account_id,
            name=item.name,
            sub_name=item.sub_name,
            created_at=item.created_at,
        )
