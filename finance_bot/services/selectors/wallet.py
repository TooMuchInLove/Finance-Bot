from loguru import logger

from finance_bot.entities.db import WalletDB
from finance_bot.infra.repos import AccountRepo, WalletRepo
from finance_bot.user import get_index_emoji


class WalletServiceSelector:
    def __init__(self, account_repo: AccountRepo, wallet_repo: WalletRepo) -> None:
        self._account_repo = account_repo
        self._wallet_repo = wallet_repo

    async def get_wallets_by_telegram_user_id(self, telegram_user_id: int) -> str:
        response: str = (
            "<b>Ознакомьтесь со списком команд</b>:\n"
            "1. Добавить кошелёк/карту: /add_wallet название_кошелька_или_карты[:сумма]\n"
            "2. Удалить кошелёк/карту: /delete_wallet название_кошелька_или_карты\n\n"
            "💳 <b>КОШЕЛЬКИ/КАРТЫ</b>:\n"
        )

        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        wallets: list[WalletDB] = await self._wallet_repo.get_by_account_id(
            account_id=account_id
        )
        if not wallets:
            logger.debug(f"[#{account_id}] No wallets were found.")
            return f"{response}┗\t Не найдено."

        for index, item in enumerate(wallets, start=1):
            if index == len(wallets):
                response += "┗\t"
            else:
                response += "┣\t"
            index_emoji: str = await get_index_emoji(index=index)
            response += f"{index_emoji} [<code>{item.name}</code>] 💵<tg-spoiler>{item.amount} ₽</tg-spoiler>\n"

        logger.debug(f"[#{account_id}] The list of wallets has been received.")
        return response
