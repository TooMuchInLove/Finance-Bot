from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
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
    WalletServiceChanger,
)
from finance_bot.services.selectors import (
    AccountServiceSelector,
    CategoryServiceSelector,
    WalletServiceSelector,
)
from finance_bot.callback_data import (
    ShowAccount,
    ShowAccountCallbackData,
    ShowCategory,
    ShowCategoryCallbackData,
    ShowWallet,
    ShowWalletCallbackData,
)
from finance_bot.states import StateWallet, StateCategory
from finance_bot.inline_buttons import (
    create_buttons,
    create_main_buttons,
    create_account_back_button,
    create_categories_buttons,
    create_category_add_buttons,
    create_wallets_buttons,
    create_wallet_add_buttons,
    create_wallet_get_back_button,
)

router = Router(name=__name__)


@router.callback_query(ShowAccountCallbackData.filter(F.slug == ShowAccount.info))
async def callback_account_info(
    query: CallbackQuery,
    state: FSMContext,
    account_service_selector: AccountServiceSelector,
) -> None:
    try:
        await query.answer()

        telegram_user_id = get_telegram_user_id(message=query)
        account = await account_service_selector.get_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )

        response = f"Ваш аккаунт был создан {account.created_at}"
        await send_telegram_message(
            message=query,
            message_text=response,
            is_update_text=True,
            buttons=create_buttons(create_account_back_button()),
        )

        await state.clear()
    except Exception as error:
        logger.exception(error)


@router.callback_query(
    ShowAccountCallbackData.filter(F.slug == ShowAccount.back),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_account_back(
    query: CallbackQuery,
    state: FSMContext,
    account_service_changer: AccountServiceChanger,
) -> None:
    try:
        await query.answer()

        telegram_user_id = get_telegram_user_id(message=query)
        telegram_user_nick = get_telegram_user_nick(message=query)
        telegram_user_name = get_telegram_user_name(message=query)
        telegram_user_link = get_telegram_user_link(message=query)

        await account_service_changer.save(
            telegram_user_id=telegram_user_id, telegram_user_name=telegram_user_nick
        )

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
        await send_telegram_message(
            message=query,
            message_text=response,
            is_update_text=True,
            buttons=create_buttons(create_main_buttons()),
        )

        await state.clear()
    except Exception as error:
        logger.exception(error)


@router.callback_query(
    ShowCategoryCallbackData.filter(F.slug == ShowCategory.get),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_category_get(
    query: CallbackQuery,
    state: FSMContext,
    category_service_selector: CategoryServiceSelector,
) -> None:
    try:
        await query.answer()

        response = "📚 <b>Список категорий</b>:\n"
        telegram_user_id = get_telegram_user_id(message=query)
        categories = await category_service_selector.get_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )
        if not categories:
            response = f"{response}┗\t Не найдено."
        names_categories: list[tuple[str, str]] = [
            (category.name, category.name_detail) for category in categories if category
        ]

        await send_telegram_message(
            message=query,
            message_text=response,
            is_update_text=True,
            buttons=create_buttons(
                create_categories_buttons(names=names_categories),
                create_account_back_button(),
                create_category_add_buttons(),
            ),
        )

        await state.clear()
    except Exception as error:
        logger.exception(error)


@router.callback_query(ShowCategoryCallbackData.filter(F.slug == ShowCategory.add))
async def callback_category_add(query: CallbackQuery, state: FSMContext) -> None:
    try:
        await query.answer()
        await state.set_state(StateCategory.add)

        response = "Укажите названия категорий в формате:\n<code>название_категории:название_подкатегории</code>"
        await send_telegram_message(
            message=query, message_text=response, is_delete_message=True
        )
    except Exception as error:
        logger.exception(error)


@router.callback_query(ShowCategoryCallbackData.filter(F.slug == ShowCategory.delete))
async def callback_category_delete(
    query: CallbackQuery,
    state: FSMContext,
    category_service_changer: CategoryServiceChanger,
) -> None:
    try:
        await query.answer()

        telegram_user_id = get_telegram_user_id(message=query)
        *_, name, name_detail = get_parameters(message=query.data)  # type: ignore[arg-type]
        category = await category_service_changer.delete(
            telegram_user_id=telegram_user_id, name=name, name_detail=name_detail
        )

        response = f"Категория `{category.name_detail}` была удалена."
        await send_telegram_message(
            message=query, message_text=response, is_delete_message=True
        )

        await state.clear()
    except Exception as error:
        logger.exception(error)


@router.callback_query(
    ShowWalletCallbackData.filter(F.slug == ShowWallet.get),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_wallet_get(
    query: CallbackQuery,
    state: FSMContext,
    wallet_service_selector: WalletServiceSelector,
) -> None:
    try:
        await query.answer()

        response = "💳 <b>Список кошельков/карт</b>:\n"
        telegram_user_id = get_telegram_user_id(message=query)
        wallets = await wallet_service_selector.get_by_telegram_user_id(
            telegram_user_id=telegram_user_id
        )
        if not wallets:
            response = f"{response}┗\t Не найдено."
        names_wallets = [wallet.name for wallet in wallets if wallet and wallet.name]

        await send_telegram_message(
            message=query,
            message_text=response,
            is_update_text=True,
            buttons=create_buttons(
                create_wallets_buttons(names_wallets),
                create_account_back_button(),
                create_wallet_add_buttons(),
            ),
        )

        await state.clear()
    except Exception as error:
        logger.exception(error)


@router.callback_query(ShowWalletCallbackData.filter(F.slug == ShowWallet.add))
async def callback_wallet_add(query: CallbackQuery, state: FSMContext) -> None:
    try:
        await query.answer()
        await state.set_state(StateWallet.add)

        response = "Укажите название кошелька/карты в формате:\n<code>название_кошелька_или_карты[:сумма]</code>"
        await send_telegram_message(
            message=query, message_text=response, is_delete_message=True
        )
    except Exception as error:
        logger.exception(error)


@router.callback_query(ShowWalletCallbackData.filter(F.slug == ShowWallet.delete))
async def callback_wallet_delete(
    query: CallbackQuery,
    state: FSMContext,
    wallet_service_changer: WalletServiceChanger,
) -> None:
    try:
        await query.answer()

        telegram_user_id = get_telegram_user_id(message=query)
        *_, wallet_name = get_parameters(message=query.data)  # type: ignore[arg-type]
        wallet = await wallet_service_changer.delete(
            telegram_user_id=telegram_user_id, name=wallet_name
        )

        response = f"Кошелёк/карта `{wallet.name}` была удалена."
        await send_telegram_message(
            message=query, message_text=response, is_delete_message=True
        )

        await state.clear()
    except Exception as error:
        logger.exception(error)


@router.callback_query(
    ShowWalletCallbackData.filter(F.slug == ShowWallet.get_detail),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_wallet_get_detail(
    query: CallbackQuery,
    state: FSMContext,
    wallet_service_selector: WalletServiceSelector,
) -> None:
    try:
        await query.answer()

        response = f"💳 <b>Информация о кошельке/карте</b>!\n\n"
        telegram_user_id = get_telegram_user_id(message=query)
        *_, wallet_name = get_parameters(message=query.data)  # type: ignore[arg-type]
        wallet = await wallet_service_selector.get_by_name_and_telegram_user_id(
            name=wallet_name, telegram_user_id=telegram_user_id
        )
        if not wallet:
            response = f"{response}┗\t Не найдено."
        else:
            response = (
                f"{response}Название кошелька/карты: <code>{wallet.name}</code>\n"
                f"Сумма на балансе: 💵<tg-spoiler>{wallet.amount} ₽</tg-spoiler>\n"
                f"Дата создания: {wallet.created_at}\n"
            )

        await send_telegram_message(
            message=query,
            message_text=response,
            is_update_text=True,
            buttons=create_buttons(
                create_wallet_get_back_button(), create_account_back_button()
            ),
        )

        await state.clear()
    except Exception as error:
        logger.exception(error)
