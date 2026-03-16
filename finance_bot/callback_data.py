from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData


class ShowAccount(IntEnum):
    info = auto()
    back = auto()


class ShowAccountCallbackData(CallbackData, prefix="account"):
    slug: ShowAccount


class ShowCategory(IntEnum):
    add = auto()
    get = auto()
    edit = auto()
    delete = auto()


class ShowCategoryCallbackData(CallbackData, prefix="category"):
    slug: ShowCategory
    name: str | None = None
    name_detail: str | None = None


class ShowWallet(IntEnum):
    add = auto()
    get = auto()
    get_detail = auto()
    delete = auto()


class ShowWalletCallbackData(CallbackData, prefix="wallet"):
    slug: ShowWallet
    name: str | None = None
