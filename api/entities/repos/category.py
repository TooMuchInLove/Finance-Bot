from uuid import UUID

from api.entities.database import CategoryDB


class ICategoryRepo:
    async def insert(self, item: CategoryDB) -> CategoryDB:
        """Добавить категорию:подкатегорию"""
        raise NotImplementedError()

    async def select_by_account(self, account_id: UUID) -> list[CategoryDB]:
        """Получить данные по всем категориям:подкатегориям для пользователя"""
        raise NotImplementedError()

    async def select_by_account_and_category(self, item: CategoryDB) -> list[CategoryDB]:
        """Получить данные по всем подкатегориям для пользователя и категории"""
        raise NotImplementedError()

    async def select_by_account_and_category_and_subcategory(self, item: CategoryDB) -> CategoryDB:
        """Получить данные по подкатегории для пользователя и категории"""
        raise NotImplementedError()
