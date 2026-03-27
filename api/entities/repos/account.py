from api.entities.database import AccountDB


class IAccountRepo:
    async def insert(self, item: AccountDB) -> AccountDB:
        """Добавить пользователя"""
        raise NotImplementedError()

    async def select_by_telegram_user_id(self, telegram_user_id: int) -> AccountDB:
        """Получить данные конкретного пользователя"""
        raise NotImplementedError()
