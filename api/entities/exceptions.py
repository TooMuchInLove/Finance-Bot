class DatabaseError(Exception):
    """Exception raised for errors that are related to the database."""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)


class ProgrammingError(DatabaseError):
    """Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc."""

    def __init__(self, message) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}"


class DomainError(Exception):
    """Base exception."""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class RemoteClientError(DomainError):
    """4xx exceptions."""

    def __init__(self, message) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}"


class ValidationError(DomainError):
    """4xx exceptions."""

    def __init__(self, message) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}"


class NotFoundError(RemoteClientError):
    """404 exception."""

    def __init__(self, message) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}"


class ConflictError(RemoteClientError):
    """409 exception."""

    def __init__(self, message) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}"


class RemoteServerError(DomainError):
    """5xx exceptions."""

    def __init__(self, message) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}"
