from dataclasses import dataclass


@dataclass(slots=True)
class WalletDB:
    name: str
    account_id: int
    amount: float | None = None
    created_at: str | None = None
