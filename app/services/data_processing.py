from app.chunking.base import BaseChunker
from app.repositories.graph_db.base import BaseGraphRepo
from app.llm.base import BaseLLM
from app.models.graph import Entity, Relation


def process_relation_and_entities(text: str) -> tuple[list[Entity], list[Relation]]:
    records = text.split("---")
    entities = []
    relations = []
    for r in records:
        if len(r) == 0:
            continue
        items = r.split(", ")
        if "entity" in items[0]:
            entities.append(
                Entity(
                    id=items[1],
                    entity_name=items[2],
                    entity_type=items[3],
                    descriptions=[],
                )
            )
        if "relationship" in items[0]:
            relations.append(
                Relation(
                    id=items[1],
                    entity_name_from=items[2],
                    entity_name_to=items[3],
                    entity_type_from=items[4],
                    entity_type_to=items[5],
                    descriptions=[],
                )
            )
    return entities, relations


class DataProcesser:

    def __init__(
        self, chunker: BaseChunker, graph_repo: BaseGraphRepo, llm: BaseLLM
    ) -> None:
        self.chunker = chunker
        self.graph_repo = graph_repo
        self.llm = llm

    def process(self, file_path: str):
        for text in self.chunker.chunk(file_path):

            relation_and_entities = self.llm.extract_entity_and_relation(text)
