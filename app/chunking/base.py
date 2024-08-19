from abc import ABC, abstractmethod
from typing import Generator, Iterable


class BaseChunker(ABC):

    @abstractmethod
    def chunk(self, text_file_path: str) -> Iterable[str]: ...
