from logging import Logger
from uuid import UUID

from sqlalchemy import insert, select, and_
from sqlalchemy.exc import IntegrityError

from api.entities.exceptions import ConflictError, NotFoundError
from api.entities.database import CategoryDB
from api.entities.repos import ICategoryRepo
from api.infra.db_context import DataBaseContext
from api.infra.models import CategoryModel


class CategoryRepo(ICategoryRepo):
    def __init__(self, db_context: DataBaseContext, logger: Logger) -> None:
        self._db_context = db_context
        self._logger = logger

    async def insert(self, item: CategoryDB) -> CategoryDB:
        """Добавить категорию:подкатегорию"""

        try:
            async with self._db_context.get_session() as session:
                data = insert(CategoryModel).values(**item.model_dump()).returning(CategoryModel)
                result = await session.execute(data)
                category = result.scalar_one()
                await session.commit()

                return CategoryDB.model_validate(category, from_attributes=True)
        except IntegrityError as err:
            message = f"[{item.account_id}] Category `{item.name}:{item.sub_name}` already exists"
            self._logger.error(message)
            raise ConflictError(message=message) from err

    async def select_by_account(self, account_id: UUID) -> list[CategoryDB]:
        """Получить данные по всем категориям:подкатегориям для пользователя"""

        async with self._db_context.get_session() as session:
            data = select(CategoryModel).where(CategoryModel.account_id == account_id)
            result = await session.execute(data)
            categories = result.scalars()

            items = []
            for category in categories:
                items.append(CategoryDB.model_validate(category, from_attributes=True))

            return items

    async def select_by_account_and_category(self, item: CategoryDB) -> list[CategoryDB]:
        """Получить данные по всем подкатегориям для пользователя и категории"""

        async with self._db_context.get_session() as session:
            data = select(CategoryModel).where(
                and_(
                    CategoryModel.account_id == item.account_id,
                    CategoryModel.name == item.name,
                ),
            )
            result = await session.execute(data)
            categories = result.scalars()

            items = []
            for category in categories:
                items.append(CategoryDB.model_validate(category, from_attributes=True))

            return items

    async def select_by_account_and_category_and_subcategory(self, item: CategoryDB) -> CategoryDB:
        """Получить данные по подкатегории для пользователя и категории"""

        async with self._db_context.get_session() as session:
            data = select(CategoryModel).where(
                and_(
                    CategoryModel.account_id == item.account_id,
                    CategoryModel.name == item.name,
                    CategoryModel.sub_name == item.sub_name,
                ),
            )
            result = await session.execute(data)
            category = result.scalar_one_or_none()

            if not category:
                message = f"[{item.account_id}] Sub-category with not found"
                self._logger.error(message)
                raise NotFoundError(message)

            return CategoryDB.model_validate(category, from_attributes=True)
