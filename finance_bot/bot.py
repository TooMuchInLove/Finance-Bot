from aiogram import Dispatcher

from finance_bot.di import DIMiddleware
from finance_bot.services.changers import (
    AccountServiceChanger,
    CategoryServiceChanger,
    TransactionServiceChanger,
    WalletServiceChanger,
)
from finance_bot.services.selectors import (
    AccountServiceSelector,
    CategoryServiceSelector,
    TransactionServiceSelector,
    WalletServiceSelector,
)


class TelegramBot:
    def __init__(
        self,
        dp: Dispatcher,
        account_service_changer: AccountServiceChanger,
        account_service_selector: AccountServiceSelector,
        category_service_changer: CategoryServiceChanger,
        category_service_selector: CategoryServiceSelector,
        transaction_service_changer: TransactionServiceChanger,
        transaction_service_selector: TransactionServiceSelector,
        wallet_service_changer: WalletServiceChanger,
        wallet_service_selector: WalletServiceSelector,
    ) -> None:
        self._dp = dp
        self._account_service_changer = account_service_changer
        self._account_service_selector = account_service_selector
        self._category_service_changer = category_service_changer
        self._category_service_selector = category_service_selector
        self._transaction_service_changer = transaction_service_changer
        self._transaction_service_selector = transaction_service_selector
        self._wallet_service_changer = wallet_service_changer
        self._wallet_service_selector = wallet_service_selector

    async def register_handlers(self) -> None:
        await self.setup_di()
        self._dp.message.middleware(DIMiddleware(di=self._dp["di"]))
        self._dp.callback_query.middleware(DIMiddleware(di=self._dp["di"]))

    async def setup_di(self) -> None:
        self._dp["di"] = {}
        self._dp["account_service_changer"] = self._account_service_changer
        self._dp["account_service_selector"] = self._account_service_selector
        self._dp["category_service_changer"] = self._category_service_changer
        self._dp["category_service_selector"] = self._category_service_selector
        self._dp["transaction_service_changer"] = self._transaction_service_changer
        self._dp["transaction_service_selector"] = self._transaction_service_selector
        self._dp["wallet_service_changer"] = self._wallet_service_changer
        self._dp["wallet_service_selector"] = self._wallet_service_selector
