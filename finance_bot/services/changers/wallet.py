from datetime import UTC, datetime

from loguru import logger

from finance_bot.config import settings
from finance_bot.entities.exceptions import IntegrityWarning
from finance_bot.entities.db import WalletDB
from finance_bot.infra.repos import AccountRepo, WalletRepo


class WalletServiceChanger:
    def __init__(self, account_repo: AccountRepo, wallet_repo: WalletRepo) -> None:
        self._account_repo = account_repo
        self._wallet_repo = wallet_repo

    async def save(self, telegram_user_id: int, parameters: list[str]) -> WalletDB:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        name, amount = parameters[0], 0.0
        if len(parameters) >= 2:
            amount = parameters[1]

        if len(name) <= 5:
            logger.warning(
                f"[#{account_id}] The wallet name must be longer than 5 characters long! "
                "Specify the wallet name in the format: `wallet_name[:amount]`"
            )
            message = (
                "Длина названия кошелька/карты должна быть больше 5 символов!\n"
                "Укажите название кошелька/карты в формате:\n<code>название_кошелька_или_карты[:сумма]</code>"
            )
            raise IntegrityWarning(message=message)

        current_datetime: str = (
            datetime.now(tz=UTC)
            .replace(microsecond=0)
            .strftime(settings.UTC0_DATETIME_FORMAT)
        )

        item: WalletDB = WalletDB(
            name=name,
            amount=amount,
            account_id=account_id,
            created_at=current_datetime,
        )
        await self._wallet_repo.insert(item=item)

        logger.debug(f"[#{account_id}] The wallet `{name}` has been added.")
        return item

    async def delete(self, telegram_user_id: int, name: str) -> WalletDB:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )
        item: WalletDB = WalletDB(
            name=name,
            account_id=account_id,
        )
        await self._wallet_repo.delete(item=item)

        logger.debug(f"[#{account_id}] The wallet `{name}` has been deleted.")
        return item
