from app.chunking.base import BaseChunker
from app.llm.base import BaseLLM
from app.models.graph import Entity, Relation
from app.repositories.graph_db.base import BaseGraphRepo


def process_relation_and_entities(text: str) -> tuple[list[Entity], list[Relation]]:
    records = text.split("---")
    entities_dict: dict[str, Entity] = {}
    relations_dict: dict[str, Relation] = {}
    for r in records:
        if len(r) == 0:
            continue
        items = r.split("*")
        if "entity" in items[0]:
            entities_dict[items[1]] = Entity(
                entity_name=items[1].title(),
                entity_type=items[2].title(),
                description=items[3],
            )
    for r in records:
        if len(r) == 0:
            continue
        items = r.split("*")
        if "relationship" in items[0]:
            relations_dict[items[1] + items[2]] = Relation(
                entity_name_from=entities_dict[items[1]].entity_name,
                entity_name_to=entities_dict[items[2]].entity_name,
                entity_type_from=entities_dict[items[1]].entity_type,
                entity_type_to=entities_dict[items[2]].entity_type,
                description=items[3],
            )
    return entities_dict.values(), relations_dict.values()


class DataProcessor:

    def __init__(
        self, chunker: BaseChunker, graph_repo: BaseGraphRepo, llm: BaseLLM
    ) -> None:
        self.chunker = chunker
        self.graph_repo = graph_repo
        self.llm = llm

    def process(self, file_path: str):

        for text in self.chunker.chunk(file_path):
            llm_result_with_entities_and_relations = (
                self.llm.extract_entity_and_relation(text)
            )
            entities, relations = process_relation_and_entities(
                llm_result_with_entities_and_relations
            )

            # now, time to write the entities and relations into the graph
            with self.graph_repo.get_driver() as driver:
                for e in entities:
                    self.graph_repo.add_entity(
                        driver, e.entity_type, e.entity_name, e.description
                    )
                for r in relations:
                    self.graph_repo.add_relation(
                        driver,
                        r.entity_type_from,
                        r.entity_type_to,
                        r.entity_name_from,
                        r.entity_name_to,
                        r.description,
                    )
            break

    # chunker = TextChunker()
    # graph_repo = Neo4jGraphRepo()
    # llm = LLM()
    # data_processor = DataProcesser(chunker, graph_repo, llm)
    # data_processor.process("data.txt")
