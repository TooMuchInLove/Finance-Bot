from datetime import datetime
from uuid import UUID

from api.entities.base import BaseModel


class CategoryResponse(BaseModel):
    account_id: UUID
    name: str
    sub_name: str
    created_at: datetime
