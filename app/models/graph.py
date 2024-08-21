from datetime import datetime

from pydantic import BaseModel


class GraphSettings(BaseModel):
    entity_types: list[str]
    node_properties: list[str]
    edge_properties: list[str]


# class Description(BaseModel):
#     id: str
#     describee_id: str
#     content: str
#     # created_at: datetime
#     # source: str


# class EdgeDescription(Description):
#     strength: int


class Entity(BaseModel):
    entity_name: str
    entity_type: str
    description: str


class Relation(BaseModel):
    entity_name_from: str
    entity_name_to: str
    entity_type_from: str
    entity_type_to: str
    description: str


# on neo4j:
#

graph_settings = GraphSettings(
    entity_types=["PERSON", "ORGANIZATION", "LOCATION"],
    node_properties=["name", "description"],
    edge_properties=["strength", "description"],
)
