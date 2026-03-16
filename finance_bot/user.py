from aiogram.types import CallbackQuery, Message


async def get_index_emoji(index: int) -> str:
    indexes = {
        0: "0️⃣",
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
    }
    result = ""
    for symbol in str(index):
        result = f"{result}{indexes.get(int(symbol))}"

    return result


def get_telegram_user_id(message: Message | CallbackQuery) -> int:
    if isinstance(message, Message):
        return message.from_user.id  # type: ignore[union-attr]

    return message.message.chat.id  # type: ignore[union-attr]


def get_telegram_user_name(message: Message | CallbackQuery) -> str:
    user = message.from_user
    first_name = user.first_name  # type: ignore[union-attr]
    last_name = user.last_name  # type: ignore[union-attr]
    is_premium = user.is_premium  # type: ignore[union-attr]

    if first_name and not last_name:
        return f"{_get_premium_status(is_premium)}{first_name}"
    elif not first_name and last_name:
        return f"{_get_premium_status(is_premium)}{last_name}"
    elif not first_name and not last_name:
        return "<user_name_empty>"

    return f"{_get_premium_status(is_premium)}{first_name} {last_name}"


def get_telegram_user_nick(message: Message | CallbackQuery) -> str:
    user_nick = message.from_user.username  # type: ignore[union-attr]

    if not user_nick:
        return "<user_name_empty>"

    return user_nick


def get_telegram_user_link(message: Message | CallbackQuery) -> str:
    user_link = message.from_user.username  # type: ignore[union-attr]

    if not user_link:
        return "#"

    return f"https://t.me/{user_link}"


def get_parameters(message: str | Message) -> list[str]:
    if isinstance(message, Message):
        string = _join_words_with_spaces(message=message)
        if not string:
            return []
    else:
        string = message

    return string.split(":")


def _join_words_with_spaces(message: Message | list[str]) -> str:
    if isinstance(message, Message):
        message = _get_entered_words(message=message)

    return " ".join(message)


def _get_entered_words(message: Message) -> list[str]:
    return message.text.split()  # type: ignore[union-attr]


def _get_premium_status(is_premium: bool | None) -> str:
    if is_premium:
        return "⭐"

    return ""
