from datetime import datetime
from uuid import UUID

from api.entities.base import BaseModelDB


class CategoryDB(BaseModelDB):
    account_id: UUID
    name: str | None = None
    sub_name: str | None = None
    created_at: datetime | None = None
