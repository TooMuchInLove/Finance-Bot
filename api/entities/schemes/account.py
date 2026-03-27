from api.entities.base import BaseModel


class AccountScheme(BaseModel):
    telegram_user_id: int
    telegram_username: str
