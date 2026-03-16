from loguru import logger

from finance_bot.entities.db import WalletDB
from finance_bot.infra.repos import AccountRepo, WalletRepo


class WalletServiceSelector:
    def __init__(self, account_repo: AccountRepo, wallet_repo: WalletRepo) -> None:
        self._account_repo = account_repo
        self._wallet_repo = wallet_repo

    async def get_by_telegram_user_id(self, telegram_user_id: int) -> list[WalletDB]:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        items: list[WalletDB] = await self._wallet_repo.get_by_account_id(
            account_id=account_id
        )
        if not items:
            logger.debug(f"[#{account_id}] No wallets were found.")
            return []

        logger.debug(f"[#{account_id}] The list of wallets has been received.")
        return items

    async def get_by_name_and_telegram_user_id(
        self, name: str, telegram_user_id: int
    ) -> WalletDB | None:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        item: WalletDB = await self._wallet_repo.get_by_name(
            name=name, account_id=account_id
        )
        if not item:
            logger.debug(f"[#{account_id}] No info of wallet `{name}` were found.")
            return None

        logger.debug(f"[#{account_id}] The info of wallet `{name}` has been received.")
        return item
