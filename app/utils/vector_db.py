import weaviate
from weaviate.classes.config import Configure, DataType, Property

from app.models.chunk import CollectionPropertyNameEnum
from app.utils.config import env


class WeaviateClientManager:
    # this context manager makes sure the client is closed after use
    def __init__(self):
        self.client = None

    def __enter__(self) -> weaviate.client.WeaviateClient:
        self.client = weaviate.connect_to_custom(
            http_host=env.WEAVIATE_HTTP_HOST,
            http_port=env.WEAVIATE_HTTP_PORT,
            grpc_host=env.WEAVIATE_GRPC_HOST,
            grpc_port=env.WEAVIATE_GRPC_PORT,
            http_secure=env.WEAVIATE_HTTP_SECURE,
            grpc_secure=env.WEAVIATE_GRPC_SECURE,
            headers=(
                None
                if env.WEAVIATE_TOKEN is None
                else {"Authorization": f"Bearer {env.WEAVIATE_TOKEN}"}
            ),
        )
        return self.client

    def __exit__(self, exc_type, exc_value, tb):
        self.client.close()


if __name__ == "__main__":
    # migration is here

    with WeaviateClientManager() as client:
        collection_names = [env.WEAVIATE_COLLECTION_NAME]
        for collection_name in collection_names:
            if not client.collections.exists(collection_name):
                collection = client.collections.create(
                    name=collection_name,
                    # description=env.EMBEDDING_MODEL_UID,
                    vectorizer_config=[
                        # Set a named vector
                        Configure.NamedVectors.none(
                            name=CollectionPropertyNameEnum.text_vector.value
                        )
                    ],
                    properties=[  # Define properties
                        Property(
                            name=CollectionPropertyNameEnum.chunk_name.value,
                            data_type=DataType.TEXT,
                        ),
                        Property(
                            name=CollectionPropertyNameEnum.text.value,
                            data_type=DataType.TEXT,
                        ),
                        Property(
                            name=CollectionPropertyNameEnum.open_url.value,
                            data_type=DataType.TEXT,
                        ),
                    ],
                )
