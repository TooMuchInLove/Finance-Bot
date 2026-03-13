from finance_bot.entities.db import WalletDB
from finance_bot.infra.db import DataBaseContext


class WalletRepo:
    def __init__(self, db_context: DataBaseContext) -> None:
        self._db_context = db_context

    async def insert(self, item: WalletDB) -> None:
        query = (
            "INSERT INTO wallet (name, amount, account_id, created_at) "
            "VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING;"
        )

        async with self._db_context as connection:
            await connection.execute(
                query, (item.name, item.amount, item.account_id, item.created_at)
            )
            await connection.commit()

    async def update(self, item: WalletDB) -> None:
        query = "UPDATE wallet SET amount = ? WHERE name = ? AND account_id = ?;"

        async with self._db_context as connection:
            await connection.execute(query, (item.amount, item.name, item.account_id))
            await connection.commit()

    async def delete(self, item: WalletDB) -> None:
        query = "DELETE FROM wallet WHERE name = ? AND account_id = ?;"

        async with self._db_context as connection:
            await connection.execute(query, (item.name, item.account_id))
            await connection.commit()

    async def is_exists(self, name: str, account_id: int) -> bool:
        query = "SELECT name FROM wallet WHERE name = ? AND account_id = ?;"

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (name, account_id))
                row = await cursor.fetchone()
                if row and row[0]:
                    return True

                return False

    async def get_by_name(self, name: str, account_id: int) -> WalletDB:
        query = "SELECT name, amount, account_id, created_at FROM wallet WHERE name = ? AND account_id = ?;"

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (name, account_id))
                row = await cursor.fetchone()
                name, amount, account_id, created_at = row

                return WalletDB(
                    name=name,
                    amount=amount,
                    account_id=account_id,
                    created_at=created_at,
                )

    async def get_by_account_id(self, account_id: int) -> list[WalletDB]:
        query = "SELECT name, amount, account_id, created_at FROM wallet WHERE account_id = ?;"

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (account_id,))
                rows = await cursor.fetchall()

                for index, row in enumerate(rows):
                    name, amount, account_id, created_at = row
                    rows[index] = WalletDB(
                        name=name,
                        amount=amount,
                        account_id=account_id,
                        created_at=created_at,
                    )

                return rows
