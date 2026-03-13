from aiosqlite import Connection, connect
from aiosqlite import OperationalError as AiosqliteOperationalError

from finance_bot.entities.exceptions import OperationalError


class DataBaseContext:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._connection: Connection | None = None

    async def __aenter__(self) -> Connection:
        return await self.get_connection()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._connection:
            await self._connection.close()
        self._connection = None

    async def get_connection(self) -> Connection:
        try:
            self._connection = connect(database=self._dsn)
            return await self._connection
        except AiosqliteOperationalError as err:
            message = "Unable to open database file."
            raise OperationalError(message) from err
