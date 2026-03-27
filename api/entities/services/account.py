from api.entities.responses import AccountResponse


class IAccountServiceChanger:
    async def create(self, telegram_user_id: int, telegram_username: str) -> AccountResponse:
        raise NotImplementedError()


class IAccountServiceSelector:
    async def get_by_telegram_user_id(self, telegram_user_id: int) -> AccountResponse:
        raise NotImplementedError()
