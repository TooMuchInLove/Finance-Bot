from abc import ABC, abstractmethod


class BaseRepo(ABC):
    @abstractmethod
    async def save(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def select(self) -> None:
        raise NotImplementedError()
