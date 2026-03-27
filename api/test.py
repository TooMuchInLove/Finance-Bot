from logging import getLogger
from asyncio import run as asyncio_run
from uuid import UUID

from .config import settings
from .entities.database import AccountDB, CategoryDB
from .infra.db_context import DataBaseContext
from .infra.repos import AccountRepo, CategoryRepo

logger = getLogger(__name__)


async def create_users() -> list[UUID]:
    data = [
        {
            "telegram_user_id": 1001,
            "telegram_username": "user_1001",
        },
        {
            "telegram_user_id": 1002,
            "telegram_username": "user_1002",
        },
    ]

    db_context = DataBaseContext(dsn=settings.POSTGRES_DSN)
    account_repo = AccountRepo(db_context=db_context, logger=logger)

    result = []
    for user in data:
        account = await account_repo.insert(
            item=AccountDB(**user)
        )
        logger.info(f"Inserted account: {account}")
        result.append(account.id)

    return result


async def create_categories(account_ids: list[UUID]) -> None:
    data = [
        # Food группа
        ("Food", "Pizza"),
        ("Food", "Pasta"),
        ("Food", "Burger"),
        # Sport группа
        ("Sport", "Football"),
        ("Sport", "Basketball"),
        # Shopping
        ("Shopping", "Clothes"),
        ("Shopping", "Electronics"),
    ]

    db_context = DataBaseContext(dsn=settings.POSTGRES_DSN)
    category_repo = CategoryRepo(db_context=db_context, logger=logger)

    for account_id in account_ids:
        for category in data:
            await category_repo.insert(
                item=CategoryDB(
                    account_id=account_id,
                    name=category[0],
                    sub_name=category[1],
                )
            )
            logger.info(f"[{account_id}] Inserted category: {category}")


async def main() -> None:
    account_ids: list[UUID] = await create_users()
    await create_categories(account_ids=account_ids)


if __name__ == "__main__":
    asyncio_run(main())
