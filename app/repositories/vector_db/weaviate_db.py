from weaviate.client import WeaviateClient

from app.models.chunk import ChunkSavedInVDB, CollectionPropertyNameEnum
from app.repositories.vector_db.base import BaseChunkRepo


class WeaviateChunkRepo(BaseChunkRepo):

    def __init__(self, client: WeaviateClient, collection_name: str):
        self.client = client
        self.collection = self.client.collections.get(collection_name)

    def create(self, chunk: ChunkSavedInVDB):

        uuid = self.collection.data.insert(
            properties={
                CollectionPropertyNameEnum.chunk_name.value: chunk.chunk_name,
                CollectionPropertyNameEnum.text.value: chunk.text,
                CollectionPropertyNameEnum.open_url.value: chunk.open_url,
            },
            vector={
                CollectionPropertyNameEnum.text_vector.value: chunk.vector,
            },
        )
        return uuid
