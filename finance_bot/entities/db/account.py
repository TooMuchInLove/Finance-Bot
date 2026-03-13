from dataclasses import dataclass


@dataclass(slots=True)
class AccountDB:
    telegram_user_id: int
    telegram_username: str
    created_at: str
    id: int | None = None
