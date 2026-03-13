from dataclasses import dataclass


@dataclass(slots=True)
class TransactionDB:
    account_id: int
    category_name: str
    wallet_name: str
    amount: float
    created_at: str
    id: int | None = None
    description: str = ""
