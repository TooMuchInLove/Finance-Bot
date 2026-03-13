from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from loguru import logger

from finance_bot.user import (
    get_telegram_user_id,
    get_telegram_user_nick,
    get_telegram_user_name,
    get_telegram_user_link,
    get_parameters,
)
from finance_bot.send import send_telegram_message
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

router = Router(name=__name__)


@router.message(CommandStart(), flags={"middlewares": ["DIMiddleware"]})
async def command_start(
    message: Message, account_service_changer: AccountServiceChanger
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        telegram_user_nick = get_telegram_user_nick(message=message)
        telegram_user_name = get_telegram_user_name(message=message)
        telegram_user_link = get_telegram_user_link(message=message)

        response = (
            f"Привет, <a href='{telegram_user_link}'>{telegram_user_name}</a>!\n"
            f"Я финансовый бот в Telegram, который поможет вам быстро и удобно управлять личным бюджетом 💰, "
            f"отслеживать расходы 📊, создавать и контролировать планы сбережений 🏦, "
            f"а также получать полезные финансовые советы 💡\n\n"
            "<b>Ознакомьтесь со списком команд</b>:\n"
            "<code>01.</code> Начало работы: /start\n"
            "<code>02.</code> Данные об учётной записи: /info_account\n"
            "<code>03.</code> Добавить категорию: /add_category название_категории:название_подкатегории\n"
            "<code>04.</code> Просмотрите список категорий: /get_categories\n"
            "<code>05.</code> Информация о кошельках/картах: /info_wallet\n"
            "<code>06.</code> Введите расходы/доходы: "
            "/add_transaction название_подкатегории:название_кошелька_или_карты:[-]сумма[:описание]\n"
            "<code>07.</code> Просмотр расходов и доходов за день: /daily_all [YYYY-MM-DD]\n"
            "<code>08.</code> Просмотр расходов за день: /daily_expense [YYYY-MM-DD]\n"
            "<code>09.</code> Просмотр доходов за день: /daily_income [YYYY-MM-DD]\n"
            "<code>10.</code> Просмотр расходов и доходов за месяц: /monthly_all [YYYY-MM]\n"
            "<code>11.</code> Просмотр расходов за месяц: /monthly_expense [YYYY-MM]\n"
            "<code>12.</code> Просмотр доходов за месяц: /monthly_income [YYYY-MM]\n"
        )

        await account_service_changer.save(
            telegram_user_id=telegram_user_id, telegram_user_name=telegram_user_nick
        )

        await send_telegram_message(
            message=message,
            message_text=response,
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("info_account"), flags={"middlewares": ["DIMiddleware"]})
async def command_info_account(
    message: Message, account_service_selector: AccountServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message)

        response = await account_service_selector.get_info_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )

        await send_telegram_message(
            message=message,
            message_text=response,
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("add_category"), flags={"middlewares": ["DIMiddleware"]})
async def command_add_category(
    message: Message, category_service_changer: CategoryServiceChanger
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message)
        parameters = get_parameters(message=message)

        response = await category_service_changer.save(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message,
            message_text=response,
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("get_categories"), flags={"middlewares": ["DIMiddleware"]})
async def command_get_categories(
    message: Message, category_service_selector: CategoryServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message)

        response = await category_service_selector.get_categories_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("info_wallet"), flags={"middlewares": ["DIMiddleware"]})
async def command_info_wallet(
    message: Message, wallet_service_selector: WalletServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message)

        response = await wallet_service_selector.get_wallets_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("add_wallet"), flags={"middlewares": ["DIMiddleware"]})
async def command_add_wallet(
    message: Message, wallet_service_changer: WalletServiceChanger
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message)
        parameters = get_parameters(message=message)

        response = await wallet_service_changer.save(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("delete_wallet"), flags={"middlewares": ["DIMiddleware"]})
async def command_delete_wallet(
    message: Message, wallet_service_changer: WalletServiceChanger
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message)
        parameters = get_parameters(message=message)

        response = await wallet_service_changer.delete(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("add_transaction"), flags={"middlewares": ["DIMiddleware"]})
async def command_add_transaction(
    message: Message, transaction_service_changer: TransactionServiceChanger
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        response = await transaction_service_changer.save(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response, is_delete_message=True
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("daily_all"), flags={"middlewares": ["DIMiddleware"]})
async def command_daily_all(
    message: Message, transaction_service_selector: TransactionServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        response = await transaction_service_selector.get_daily_all(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("daily_expense"), flags={"middlewares": ["DIMiddleware"]})
async def command_daily_expense(
    message: Message, transaction_service_selector: TransactionServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        response = await transaction_service_selector.get_daily_expense(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("daily_income"), flags={"middlewares": ["DIMiddleware"]})
async def command_daily_income(
    message: Message, transaction_service_selector: TransactionServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        response = await transaction_service_selector.get_daily_income(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("monthly_all"), flags={"middlewares": ["DIMiddleware"]})
async def command_monthly_all(
    message: Message, transaction_service_selector: TransactionServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        response = await transaction_service_selector.get_monthly_all(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("monthly_expense"), flags={"middlewares": ["DIMiddleware"]})
async def command_monthly_expense(
    message: Message, transaction_service_selector: TransactionServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        response = await transaction_service_selector.get_monthly_expense(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)


@router.message(Command("monthly_income"), flags={"middlewares": ["DIMiddleware"]})
async def command_monthly_income(
    message: Message, transaction_service_selector: TransactionServiceSelector
) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        response = await transaction_service_selector.get_monthly_income(
            telegram_user_id=telegram_user_id, parameters=parameters
        )

        await send_telegram_message(
            message=message, message_text=response
        )
    except Exception as error:
        logger.exception(error)
