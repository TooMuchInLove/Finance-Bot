from dataclasses import dataclass


@dataclass(slots=True)
class CategoryDB:
    name: str
    name_detail: str
    account_id: int
    created_at: str
