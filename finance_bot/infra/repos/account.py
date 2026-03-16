from finance_bot.entities.db import AccountDB
from finance_bot.infra.db import DataBaseContext


class AccountRepo:
    def __init__(self, db_context: DataBaseContext) -> None:
        self._db_context = db_context

    async def insert(self, item: AccountDB) -> None:
        query = (
            "INSERT INTO account (telegram_user_id, telegram_username, created_at) "
            "VALUES (?, ?, ?) ON CONFLICT DO NOTHING;"
        )

        async with self._db_context as connection:
            await connection.execute(
                query, (item.telegram_user_id, item.telegram_username, item.created_at)
            )
            await connection.commit()

    async def get_id(self, telegram_user_id: int) -> int:
        query = "SELECT id FROM account WHERE telegram_user_id = ?;"

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (telegram_user_id,))
                row = await cursor.fetchone()

                return row[0]  # type: ignore[index]

    async def get_by_telegram_user_id(self, telegram_user_id: int) -> AccountDB:
        query = (
            "SELECT id, telegram_user_id, telegram_username, created_at "
            "FROM account "
            "WHERE telegram_user_id = ?;"
        )

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (telegram_user_id,))
                row = await cursor.fetchone()
                id, telegram_user_id, telegram_username, created_at = row  # type: ignore[misc]

                return AccountDB(
                    id=id,
                    telegram_user_id=telegram_user_id,
                    telegram_username=telegram_username,
                    created_at=created_at,
                )
