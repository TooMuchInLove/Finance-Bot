class DataBaseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class OperationalError(DataBaseError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ConnectionError(DataBaseError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class BaseWarning(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class NotEnoughParametersWarning(BaseWarning):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class IntegrityWarning(BaseWarning):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
