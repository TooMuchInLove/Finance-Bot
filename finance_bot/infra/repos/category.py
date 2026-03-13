from finance_bot.entities.db import CategoryDB
from finance_bot.infra.db import DataBaseContext


class CategoryRepo:
    def __init__(self, db_context: DataBaseContext) -> None:
        self._db_context = db_context

    async def insert(self, item: CategoryDB) -> None:
        query = (
            "INSERT INTO category (name, name_detail, account_id, created_at) "
            "VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING;"
        )

        async with self._db_context as connection:
            await connection.execute(
                query, (item.name, item.name_detail, item.account_id, item.created_at)
            )
            await connection.commit()

    async def is_exists(self, name: str, account_id: int) -> bool:
        query = (
            "SELECT name_detail FROM category WHERE name_detail = ? AND account_id = ?;"
        )

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (name, account_id))
                row = await cursor.fetchone()
                if row and row[0]:
                    return True

                return False

    async def get_by_account_id(self, account_id: int) -> list[CategoryDB]:
        query = "SELECT name, name_detail, account_id, created_at FROM category WHERE account_id = ?;"

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (account_id,))
                rows = await cursor.fetchall()

                for index, row in enumerate(rows):
                    name, name_detail, account_id, created_at = row
                    rows[index] = CategoryDB(
                        name=name,
                        name_detail=name_detail,
                        account_id=account_id,
                        created_at=created_at,
                    )

                return rows
