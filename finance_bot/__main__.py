from asyncio import run as asyncio_run

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from finance_bot.config import settings, db_settings
from finance_bot.routers import router
from finance_bot.bot import TelegramBot
from finance_bot.infra.db import DataBaseContext
from finance_bot.infra.repos import (
    AccountRepo,
    CategoryRepo,
    WalletRepo,
    TransactionRepo,
)
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


async def main() -> None:
    db_context = DataBaseContext(dsn=db_settings.dsn())

    account_repo = AccountRepo(db_context=db_context)
    category_repo = CategoryRepo(db_context=db_context)
    wallet_repo = WalletRepo(db_context=db_context)
    transaction_repo = TransactionRepo(db_context=db_context)

    account_service_changer = AccountServiceChanger(account_repo=account_repo)
    account_service_selector = AccountServiceSelector(account_repo=account_repo)
    category_service_changer = CategoryServiceChanger(
        account_repo=account_repo, category_repo=category_repo
    )
    category_service_selector = CategoryServiceSelector(
        account_repo=account_repo, category_repo=category_repo
    )
    transaction_service_selector = TransactionServiceSelector(
        account_repo=account_repo,
        transaction_repo=transaction_repo,
    )
    transaction_service_changer = TransactionServiceChanger(
        account_repo=account_repo,
        category_repo=category_repo,
        transaction_repo=transaction_repo,
        wallet_repo=wallet_repo,
    )
    wallet_service_changer = WalletServiceChanger(
        account_repo=account_repo, wallet_repo=wallet_repo
    )
    wallet_service_selector = WalletServiceSelector(
        account_repo=account_repo, wallet_repo=wallet_repo
    )

    dp = Dispatcher()
    default = DefaultBotProperties(parse_mode="HTML")
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=default,
    )
    telegram_bot = TelegramBot(
        dp=dp,
        account_service_changer=account_service_changer,
        account_service_selector=account_service_selector,
        category_service_changer=category_service_changer,
        category_service_selector=category_service_selector,
        transaction_service_changer=transaction_service_changer,
        transaction_service_selector=transaction_service_selector,
        wallet_service_changer=wallet_service_changer,
        wallet_service_selector=wallet_service_selector,
    )

    dp.startup.register(telegram_bot.register_handlers)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting...")
    try:
        asyncio_run(main())
    except KeyboardInterrupt:
        logger.warning("The bot is disabled.")
    except Exception as err:
        logger.exception(err)
    finally:
        logger.info("Stopping...")
