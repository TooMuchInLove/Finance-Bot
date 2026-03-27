from datetime import datetime
from uuid import UUID

from api.entities.base import BaseModel


class AccountResponse(BaseModel):
    id: UUID
    telegram_user_id: int
    telegram_username: str
    created_at: datetime
