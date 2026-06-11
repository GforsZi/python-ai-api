from abc import ABC, abstractmethod
import logging
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_seeder_registry: list[Type["BaseSeeder"]] = []

class BaseSeeder(ABC):
    order: int = 100
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def run(self) -> None:
        pass

    async def log(self, message: str) -> None:
        logger.info(f"[{self.__class__.__name__}] {message}")

def register_seeder(cls: Type[BaseSeeder]) -> Type[BaseSeeder]:
    _seeder_registry.append(cls)
    return cls

def get_registered_seeders() -> list[Type[BaseSeeder]]:
    return _seeder_registry


