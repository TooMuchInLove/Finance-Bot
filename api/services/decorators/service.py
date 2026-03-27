from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar

from api.entities.exceptions import (
    ConflictError,
    DatabaseError,
    NotFoundError,
    ProgrammingError,
    RemoteServerError,
)

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def catch_api_errors(function: F) -> F:
    @wraps(function)
    async def _wrapper(self, *args, **kwargs) -> Any:
        try:
            return await function(self, *args, **kwargs)
        except ConflictError as err:
            raise ConflictError(err.message) from err
        except NotFoundError as err:
            raise NotFoundError(err.message) from err
        except (DatabaseError, ProgrammingError) as err:
            raise RemoteServerError(err.message) from err

    return _wrapper  # type: ignore[return-value]
