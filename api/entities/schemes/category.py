from uuid import UUID

from api.entities.base import BaseModel


class CategoryScheme(BaseModel):
    account_id: UUID
    name: str
    sub_name: str
