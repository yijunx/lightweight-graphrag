from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def extract_entity_and_relation(self, context: str) -> str: ...

    @abstractmethod
    def contruct_cypher(self, question: str) -> str: ...
