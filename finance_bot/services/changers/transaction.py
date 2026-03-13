from datetime import UTC, datetime

from loguru import logger

from finance_bot.config import settings
from finance_bot.entities.db import WalletDB, TransactionDB
from finance_bot.infra.repos import (
    AccountRepo,
    CategoryRepo,
    WalletRepo,
    TransactionRepo,
)


class TransactionServiceChanger:
    def __init__(
        self,
        account_repo: AccountRepo,
        category_repo: CategoryRepo,
        transaction_repo: TransactionRepo,
        wallet_repo: WalletRepo,
    ) -> None:
        self._account_repo = account_repo
        self._category_repo = category_repo
        self._transaction_repo = transaction_repo
        self._wallet_repo = wallet_repo

    async def save(self, telegram_user_id: int, parameters: list[str]) -> str:
        account_id: int = await self._account_repo.get_id(
            telegram_user_id=telegram_user_id
        )

        if len(parameters) < 3:
            logger.warning(
                f"[#{account_id}] Not enough parameters! "
                f"Specify the name of the sub-category, wallet and amount in the format: "
                f"`/add_transaction название_подкатегории:название_кошелька_или_карты:[-]сумма[:описание]`"
            )
            return (
                "Недостаточно параметров!\nУкажите название подкатегории, кошелька/карты и сумму в формате:\n"
                "/add_transaction название_подкатегории:название_кошелька_или_карты:[-]сумма[:описание]"
            )

        if len(parameters) == 4:
            category_name, wallet_name, amount, description = parameters
        else:
            category_name, wallet_name, amount = parameters
            description = ""

        amount = float(amount)
        current_datetime: str = (
            datetime.now(tz=UTC)
            .replace(microsecond=0)
            .strftime(settings.UTC0_DATETIME_FORMAT)
        )

        is_category: bool = await self._category_repo.is_exists(
            name=category_name, account_id=account_id
        )
        if not is_category:
            logger.debug(
                f"[#{account_id}] The category `{category_name}` does not exist."
            )
            return f"Категория `{category_name}` не существует."

        is_wallet: bool = await self._wallet_repo.is_exists(
            name=wallet_name, account_id=account_id
        )
        if not is_wallet:
            logger.debug(f"[#{account_id}] The wallet `{wallet_name}` does not exist.")
            return f"Кошелёк/карта `{wallet_name}` не существует."

        wallet: WalletDB = await self._wallet_repo.get_by_name(
            name=wallet_name, account_id=account_id
        )

        item: TransactionDB = TransactionDB(
            account_id=account_id,
            category_name=category_name,
            wallet_name=wallet_name,
            amount=amount,
            created_at=current_datetime,
            description=description,
        )
        await self._transaction_repo.insert(item=item)

        await self._wallet_repo.update(
            item=WalletDB(
                name=wallet_name,
                account_id=account_id,
                amount=wallet.amount + amount,
            ),
        )

        logger.debug(f"[#{account_id}] Transaction added successfully.")
        return "Расходы/доходы успешно добавлены."
