from abc import ABC, abstractmethod
from typing import TypeVar

DBDriver = TypeVar(name="DBDriver")


class BaseGraphRepo(ABC):
    """this is for all kinds of graph db!"""

    @abstractmethod
    def add_entity(
        self, driver: DBDriver, entity_type: str, name: str, description_id: str
    ): ...
    @abstractmethod
    def add_relation(
        self,
        driver: DBDriver,
        entity_type_from: str,
        entity_type_to: str,
        name_from: str,
        name_to: str,
        description_id: str,
        strength: int,
    ): ...
    @abstractmethod
    def get_driver(self) -> DBDriver: ...
    @abstractmethod
    def execute_query(self, driver: DBDriver, query: str): ...
