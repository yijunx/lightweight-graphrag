from abc import ABC, abstractmethod

from typing import TypeVar

DBDriver = TypeVar(name="DBDriver")


class BaseFriendRepo(ABC):
    """this is for all kinds of graph db!"""

    @abstractmethod
    def add_friend(self, driver: DBDriver, name: str, friend_name: str): ...
    @abstractmethod
    def print_friends(self, driver: DBDriver, name: str): ...
    @abstractmethod
    def get_driver(self) -> DBDriver: ...
