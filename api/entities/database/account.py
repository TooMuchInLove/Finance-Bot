from datetime import datetime
from uuid import UUID

from api.entities.base import BaseModelDB


class AccountDB(BaseModelDB):
    telegram_user_id: int
    telegram_username: str
    created_at: datetime
    id: UUID | None = None
