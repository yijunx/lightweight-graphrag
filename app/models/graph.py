from pydantic import BaseModel
from datetime import datetime


class GraphSettings(BaseModel):
    entity_types: list[str]
    node_properties: list[str]
    edge_properties: list[str]


class Description(BaseModel):
    id: str
    content: str
    created_at: datetime
    source: str


class EdgeDescription(Description):
    strength: int


class Node(BaseModel):
    id: str
    entity_name: str
    entity_type: str
    descriptions: list[Description]


class Edge(BaseModel):
    id: str
    entity_name_from: str
    entity_name_to: str
    entity_type_from: str
    entity_type_to: str
    descriptions: list[Description]



