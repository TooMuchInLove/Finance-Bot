from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from loguru import logger

from finance_bot.entities.exceptions import NotEnoughParametersWarning, IntegrityWarning
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
from finance_bot.services.selectors import TransactionServiceSelector
from finance_bot.states import StateWallet, StateCategory
from finance_bot.inline_buttons import create_buttons, create_main_buttons

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
            "<code>01.</code> Введите расходы/доходы: "
            "/add_transaction название_подкатегории:название_кошелька_или_карты:[-]сумма[:описание]\n"
            "<code>02.</code> Просмотр расходов и доходов за день: /daily_all [YYYY-MM-DD]\n"
            "<code>03.</code> Просмотр расходов за день: /daily_expense [YYYY-MM-DD]\n"
            "<code>04.</code> Просмотр доходов за день: /daily_income [YYYY-MM-DD]\n"
            "<code>05.</code> Просмотр расходов и доходов за месяц: /monthly_all [YYYY-MM]\n"
            "<code>06.</code> Просмотр расходов за месяц: /monthly_expense [YYYY-MM]\n"
            "<code>07.</code> Просмотр доходов за месяц: /monthly_income [YYYY-MM]\n"
        )
        await account_service_changer.save(
            telegram_user_id=telegram_user_id, telegram_user_name=telegram_user_nick
        )

        await send_telegram_message(
            message=message,
            message_text=response,
            buttons=create_buttons(create_main_buttons()),
        )
    except Exception as error:
        logger.exception(error)


@router.message(StateCategory.add, F.text, flags={"middlewares": ["DIMiddleware"]})
async def command_add_category(message: Message, state: FSMContext, category_service_changer: CategoryServiceChanger) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        category = await category_service_changer.save(
            telegram_user_id=telegram_user_id, parameters=parameters
        )
        response = f"Категория `{category.name}:{category.name_detail}` была добавлена успешно."
        await send_telegram_message(message=message, message_text=response, is_delete_message=True)

        await state.clear()
    except (NotEnoughParametersWarning, IntegrityWarning) as warning:
        await send_telegram_message(message=message, message_text=str(warning), is_delete_message=True)
    except Exception as error:
        logger.exception(error)


@router.message(StateWallet.add, F.text, flags={"middlewares": ["DIMiddleware"]})
async def command_add_wallet(message: Message, state: FSMContext, wallet_service_changer: WalletServiceChanger) -> None:
    try:
        telegram_user_id = get_telegram_user_id(message=message)
        parameters = get_parameters(message=message)

        wallet = await wallet_service_changer.save(
            telegram_user_id=telegram_user_id, parameters=parameters
        )
        response = f"Кошелёк/карта `{wallet.name}` была добавлена."
        await send_telegram_message(message=message, message_text=response, is_delete_message=True)

        await state.clear()
    except (NotEnoughParametersWarning, IntegrityWarning) as warning:
        await send_telegram_message(message=message, message_text=str(warning), is_delete_message=True)
    except Exception as error:
        logger.exception(error)


# TODO: переделать на кнопки!!!
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


# TODO: переделать на кнопки!!!
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

        await send_telegram_message(message=message, message_text=response)
    except Exception as error:
        logger.exception(error)


# TODO: переделать на кнопки!!!
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

        await send_telegram_message(message=message, message_text=response)
    except Exception as error:
        logger.exception(error)


# TODO: переделать на кнопки!!!
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

        await send_telegram_message(message=message, message_text=response)
    except Exception as error:
        logger.exception(error)


# TODO: переделать на кнопки!!!
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

        await send_telegram_message(message=message, message_text=response)
    except Exception as error:
        logger.exception(error)


# TODO: переделать на кнопки!!!
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

        await send_telegram_message(message=message, message_text=response)
    except Exception as error:
        logger.exception(error)


# TODO: переделать на кнопки!!!
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

        await send_telegram_message(message=message, message_text=response)
    except Exception as error:
        logger.exception(error)
