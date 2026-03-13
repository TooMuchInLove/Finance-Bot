from datetime import UTC, datetime

from loguru import logger

from finance_bot.config import settings
from finance_bot.entities.db import WalletDB
from finance_bot.infra.repos import AccountRepo, WalletRepo


class WalletServiceChanger:
    def __init__(self, account_repo: AccountRepo, wallet_repo: WalletRepo) -> None:
        self._account_repo = account_repo
        self._wallet_repo = wallet_repo

    async def save(self, telegram_user_id: int, parameters: list[str]) -> str:
        account_id: int = await self._account_repo.get_id(telegram_user_id=telegram_user_id)

        if len(parameters) == 0:
            logger.warning(
                f"[#{account_id}] Not enough parameters! Specify the wallet name in the format: "
                "`/add_wallet название_кошелька_или_карты[:сумма]`"
            )
            return (
                "Недостаточно параметров!\nУкажите название кошелька/карты в формате:\n"
                "/add_wallet название_кошелька_или_карты[:сумма]"
            )

        name, amount = parameters[0], 0.0
        if len(parameters) == 2:
            amount = parameters[1]

        current_datetime: str = (
            datetime.now(tz=UTC).replace(microsecond=0).strftime(settings.UTC0_DATETIME_FORMAT)
        )

        item: WalletDB = WalletDB(
            name=name,
            amount=amount,
            account_id=account_id,
            created_at=current_datetime,
        )
        await self._wallet_repo.insert(item=item)

        logger.debug(f"[#{account_id}] The wallet `{name}` has been added.")
        return f"Кошелёк/карта `{name}` была добавлена."

    async def delete(self, telegram_user_id: int, parameters: list[str]) -> str:
        account_id: int = await self._account_repo.get_id(telegram_user_id=telegram_user_id)

        if len(parameters) != 1:
            logger.warning(
                f"[#{account_id}] Not enough parameters! Specify the wallet name in the format: "
                "`/delete_wallet название_кошелька_или_карты`"
            )
            return (
                "Недостаточно параметров!\nУкажите название кошелька/карты в формате:\n"
                "/delete_wallet название_кошелька_или_карты"
            )

        name = parameters[0]

        is_wallet: bool = await self._wallet_repo.is_exists(
            name=name, account_id=account_id
        )
        if not is_wallet:
            logger.debug(f"[#{account_id}] The wallet `{name}` does not exist.")
            return f"Кошелёк/карта `{name}` не существует."

        item: WalletDB = WalletDB(
            name=name,
            account_id=account_id,
        )
        await self._wallet_repo.delete(item=item)

        logger.debug(f"[#{account_id}] The wallet `{name}` has been deleted.")
        return f"Кошелёк/карта `{name}` была удалена."
