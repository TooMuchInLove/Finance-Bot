from uuid import UUID

from api.entities.responses import CategoryResponse


class ICategoryServiceChanger:
    async def create(self, account_id: UUID, name: str, sub_name: str) -> CategoryResponse:
        """Создать категорию:подкатегорию"""
        raise NotImplementedError()


class ICategoryServiceSelector:
    async def get_by_account(self, account_id: UUID) -> list[CategoryResponse]:
        """Получить данные по всем категориям:подкатегориям для пользователя"""
        raise NotImplementedError()

    async def get_by_account_and_category(self, account_id: UUID, name: str) -> list[CategoryResponse]:
        """Получить данные по всем подкатегориям для пользователя и категории"""
        raise NotImplementedError()

    async def get_by_account_and_category_and_subcategory(self, account_id: UUID, name: str, sub_name: str) -> CategoryResponse:
        """Получить данные по подкатегории для пользователя и категории"""
        raise NotImplementedError()
