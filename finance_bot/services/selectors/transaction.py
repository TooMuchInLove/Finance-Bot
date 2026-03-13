from datetime import UTC, datetime

from loguru import logger

from finance_bot.config import settings
from finance_bot.entities.base import AmountChoices
from finance_bot.entities.db import TransactionDB
from finance_bot.infra.repos import AccountRepo, TransactionRepo
from finance_bot.user import get_index_emoji


class TransactionServiceSelector:
    def __init__(
        self,
        account_repo: AccountRepo,
        transaction_repo: TransactionRepo,
    ) -> None:
        self._account_repo = account_repo
        self._transaction_repo = transaction_repo

    async def get_daily_all(self, telegram_user_id: int, parameters: list[str]) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        day: str = (
            datetime.now(tz=UTC).replace(microsecond=0).strftime(settings.DAY_FORMAT)
        )
        if len(parameters) > 0:
            day = parameters[0]

        response: str = f"<b>Расходы и доходы за <code>{day}</code></b>:\n"

        transactions: list[TransactionDB] = (
            await self._transaction_repo.get_daily_by_account_id(
                account_id=account_id, day=day, tag=AmountChoices.all
            )
        )
        if not transactions:
            logger.debug(
                f"[#{account_id}] Expenses and income for `{day}` were not found."
            )
            return f"{response}┗\t Не найдено."

        for index, item in enumerate(transactions, start=1):
            if index == len(transactions):
                response += "┗\t"
            else:
                response += "┣\t"
            index_emoji: str = await get_index_emoji(index=index)
            response += (
                f"{index_emoji} {item.created_at} [<code>{item.wallet_name}</code>] "
                f"<code>{item.category_name}</code> 💵<tg-spoiler>{item.amount} ₽</tg-spoiler>"
                f"{f' <i>({item.description})</i>' if item.description else ''}\n"
            )

        return response

    async def get_daily_expense(
        self, telegram_user_id: int, parameters: list[str]
    ) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        day: str = (
            datetime.now(tz=UTC).replace(microsecond=0).strftime(settings.DAY_FORMAT)
        )
        if len(parameters) > 0:
            day = parameters[0]

        response: str = f"<b>Расходы за <code>{day}</code></b>:\n"

        transactions: list[TransactionDB] = (
            await self._transaction_repo.get_daily_by_account_id(
                account_id=account_id, day=day, tag=AmountChoices.expense
            )
        )
        if not transactions:
            logger.debug(f"[#{account_id}] Expenses for `{day}` were not found.")
            return f"{response}┗\t Не найдено."

        for index, item in enumerate(transactions, start=1):
            if index == len(transactions):
                response += "┗\t"
            else:
                response += "┣\t"
            index_emoji: str = await get_index_emoji(index=index)
            response += (
                f"{index_emoji} {item.created_at} [<code>{item.wallet_name}</code>] "
                f"<code>{item.category_name}</code> 💵<tg-spoiler>{item.amount} ₽</tg-spoiler>"
                f"{f' <i>({item.description})</i>' if item.description else ''}\n"
            )

        return response

    async def get_daily_income(
        self, telegram_user_id: int, parameters: list[str]
    ) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        day: str = (
            datetime.now(tz=UTC).replace(microsecond=0).strftime(settings.DAY_FORMAT)
        )
        if len(parameters) > 0:
            day = parameters[0]

        response: str = f"<b>Доходы за <code>{day}</code></b>:\n"

        transactions: list[TransactionDB] = (
            await self._transaction_repo.get_daily_by_account_id(
                account_id=account_id, day=day, tag=AmountChoices.income
            )
        )
        if not transactions:
            logger.debug(f"[#{account_id}] Income for `{day}` were not found.")
            return f"{response}┗\t Не найдено."

        for index, item in enumerate(transactions, start=1):
            if index == len(transactions):
                response += "┗\t"
            else:
                response += "┣\t"
            index_emoji: str = await get_index_emoji(index=index)
            response += (
                f"{index_emoji} {item.created_at} [<code>{item.wallet_name}</code>] "
                f"<code>{item.category_name}</code> 💵<tg-spoiler>{item.amount} ₽</tg-spoiler>"
                f"{f' <i>({item.description})</i>' if item.description else ''}\n"
            )

        return response

    async def get_monthly_all(
        self, telegram_user_id: int, parameters: list[str]
    ) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        month: str = (
            datetime.now(tz=UTC).replace(microsecond=0).strftime(settings.MONTH_FORMAT)
        )
        if len(parameters) > 0:
            month = parameters[0]

        response: str = f"<b>Расходы и доходы за <code>{month}</code></b>:\n"

        transactions: list[TransactionDB] = (
            await self._transaction_repo.get_monthly_by_account_id(
                account_id=account_id, day=month, tag=AmountChoices.all
            )
        )
        if not transactions:
            logger.debug(
                f"[#{account_id}] Expenses and income for `{month}` were not found."
            )
            return f"{response}┗\t Не найдено."

        for index, item in enumerate(transactions, start=1):
            if index == len(transactions):
                response += "┗\t"
            else:
                response += "┣\t"
            index_emoji: str = await get_index_emoji(index=index)
            response += (
                f"{index_emoji} {item.created_at} [<code>{item.wallet_name}</code>] "
                f"<code>{item.category_name}</code> 💵<tg-spoiler>{item.amount} ₽</tg-spoiler>"
                f"{f' <i>({item.description})</i>' if item.description else ''}\n"
            )

        return response

    async def get_monthly_expense(
        self, telegram_user_id: int, parameters: list[str]
    ) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        day: str = (
            datetime.now(tz=UTC).replace(microsecond=0).strftime(settings.MONTH_FORMAT)
        )
        if len(parameters) > 0:
            day = parameters[0]

        response: str = f"<b>Расходы за <code>{day}</code></b>:\n"

        transactions: list[TransactionDB] = (
            await self._transaction_repo.get_monthly_by_account_id(
                account_id=account_id, day=day, tag=AmountChoices.expense
            )
        )
        if not transactions:
            logger.debug(f"[#{account_id}] Expenses for `{day}` were not found.")
            return f"{response}┗\t Не найдено."

        for index, item in enumerate(transactions, start=1):
            if index == len(transactions):
                response += "┗\t"
            else:
                response += "┣\t"
            index_emoji: str = await get_index_emoji(index=index)
            response += (
                f"{index_emoji} {item.created_at} [<code>{item.wallet_name}</code>] "
                f"<code>{item.category_name}</code> 💵<tg-spoiler>{item.amount} ₽</tg-spoiler>"
                f"{f' <i>({item.description})</i>' if item.description else ''}\n"
            )

        return response

    async def get_monthly_income(
        self, telegram_user_id: int, parameters: list[str]
    ) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        day: str = (
            datetime.now(tz=UTC).replace(microsecond=0).strftime(settings.MONTH_FORMAT)
        )
        if len(parameters) > 0:
            day = parameters[0]

        response: str = f"<b>Доходы за <code>{day}</code></b>:\n"

        transactions: list[TransactionDB] = (
            await self._transaction_repo.get_monthly_by_account_id(
                account_id=account_id, day=day, tag=AmountChoices.income
            )
        )
        if not transactions:
            logger.debug(f"[#{account_id}] Income for `{day}` were not found.")
            return f"{response}┗\t Не найдено."

        for index, item in enumerate(transactions, start=1):
            if index == len(transactions):
                response += "┗\t"
            else:
                response += "┣\t"
            index_emoji: str = await get_index_emoji(index=index)
            response += (
                f"{index_emoji} {item.created_at} [<code>{item.wallet_name}</code>] "
                f"<code>{item.category_name}</code> 💵<tg-spoiler>{item.amount} ₽</tg-spoiler>"
                f"{f' <i>({item.description})</i>' if item.description else ''}\n"
            )

        return response
