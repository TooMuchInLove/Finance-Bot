from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from finance_bot.callback_data import (
    ShowAccount,
    ShowAccountCallbackData,
    ShowCategory,
    ShowCategoryCallbackData,
    ShowWallet,
    ShowWalletCallbackData,
)


def create_buttons(*list_buttons) -> InlineKeyboardMarkup:
    buttons = []
    for button in list_buttons:
        buttons.extend(button)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_main_buttons() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text="ℹ️ Аккаунт",
                callback_data=ShowAccountCallbackData(slug=ShowAccount.info).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="📚 Список категорий",
                callback_data=ShowCategoryCallbackData(slug=ShowCategory.get).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="💳 Список кошельков",
                callback_data=ShowWalletCallbackData(slug=ShowWallet.get).pack(),
            ),
        ],
    ]


def create_account_back_button() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text="⬅️ В главное меню",
                callback_data=ShowAccountCallbackData(slug=ShowAccount.back).pack(),
            ),
        ]
    ]


def create_categories_buttons(names: list[tuple[str, str]]) -> list[list[InlineKeyboardButton]]:
    buttons = []
    for item in names:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{item[0]}, {item[1]}",
                    callback_data = ShowCategoryCallbackData(slug=ShowCategory.edit).pack(),
                ),
                InlineKeyboardButton(
                    text="❌ Удалить",
                    callback_data=ShowCategoryCallbackData(slug=ShowCategory.delete, name=item[0], name_detail=item[1]).pack(),
                ),
            ]
        )

    return buttons


def create_category_add_buttons() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text="✅ Добавить",
                callback_data=ShowCategoryCallbackData(slug=ShowCategory.add).pack(),
            ),
            InlineKeyboardButton(
                text="🔄 Обновить",
                callback_data=ShowCategoryCallbackData(slug=ShowCategory.get).pack(),
            ),
        ]
    ]


def create_wallets_buttons(names: list[str]) -> list[list[InlineKeyboardButton]]:
    buttons = []
    for name in names:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=name,
                    callback_data=ShowWalletCallbackData(slug=ShowWallet.get_detail, name=name).pack(),
                ),
                InlineKeyboardButton(
                    text="❌ Удалить",
                    callback_data=ShowWalletCallbackData(slug=ShowWallet.delete, name=name).pack(),
                ),
            ]
        )

    return buttons


def create_wallet_add_buttons() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text="✅ Добавить",
                callback_data=ShowWalletCallbackData(slug=ShowWallet.add).pack(),
            ),
            InlineKeyboardButton(
                text="🔄 Обновить",
                callback_data=ShowWalletCallbackData(slug=ShowWallet.get).pack(),
            ),
        ]
    ]


def create_wallet_get_back_button() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=ShowWalletCallbackData(slug=ShowWallet.get).pack(),
            ),
        ]
    ]
