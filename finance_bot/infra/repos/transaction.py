from finance_bot.entities.base import AmountChoices
from finance_bot.entities.db import TransactionDB
from finance_bot.infra.db import DataBaseContext


class TransactionRepo:
    def __init__(self, db_context: DataBaseContext) -> None:
        self._db_context = db_context

    async def insert(self, item: TransactionDB) -> None:
        query = (
            "INSERT INTO transactions (account_id, category_name, wallet_name, amount, created_at, description) "
            "VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING;"
        )

        async with self._db_context as connection:
            await connection.execute(
                query,
                (
                    item.account_id,
                    item.category_name,
                    item.wallet_name,
                    item.amount,
                    item.created_at,
                    item.description,
                ),
            )
            await connection.commit()

    async def get_daily_by_account_id(self, account_id: int, day: str, tag: AmountChoices) -> list[TransactionDB]:
        query = (
            "SELECT id, account_id, category_name, wallet_name, amount, created_at, description "
            "FROM transactions "
            "WHERE account_id = ? AND DATE(created_at) = DATE(?) "
        )
        if tag == AmountChoices.expense:
            query += "AND amount < 0 "
        elif tag == AmountChoices.income:
            query += "AND amount >= 0 "
        query += "ORDER BY created_at DESC;"

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (account_id, day))
                rows = await cursor.fetchall()

                for index, row in enumerate(rows):
                    id_, account_id, category_name, wallet_name, amount, created_at, description = row
                    rows[index] = TransactionDB(
                        id=id_,
                        account_id=account_id,
                        category_name=category_name,
                        wallet_name=wallet_name,
                        amount=amount,
                        created_at=created_at,
                        description=description,
                    )

                return rows

    async def get_monthly_by_account_id(self, account_id: int, day: str, tag: AmountChoices) -> list[TransactionDB]:
        query = (
            "SELECT id, account_id, category_name, wallet_name, amount, created_at, description "
            "FROM transactions "
            "WHERE account_id = ? AND strftime('%Y-%m', created_at) = ? "
        )
        if tag == AmountChoices.expense:
            query += "AND amount < 0 "
        elif tag == AmountChoices.income:
            query += "AND amount >= 0 "
        query += "ORDER BY created_at DESC;"

        async with self._db_context as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (account_id, day))
                rows = await cursor.fetchall()

                for index, row in enumerate(rows):
                    id_, account_id, category_name, wallet_name, amount, created_at, description = row
                    rows[index] = TransactionDB(
                        id=id_,
                        account_id=account_id,
                        category_name=category_name,
                        wallet_name=wallet_name,
                        amount=amount,
                        created_at=created_at,
                        description=description,
                    )

                return rows
