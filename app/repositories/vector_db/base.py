from abc import ABC, abstractmethod

from app.models.chunk import ChunkSavedInVDB


class BaseChunkRepo(ABC):

    @abstractmethod
    def create(self, chunk: ChunkSavedInVDB):
        pass
