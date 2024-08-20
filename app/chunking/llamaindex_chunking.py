from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import Document
from llama_index.embeddings.openai import OpenAIEmbedding

from app.chunking.base import BaseChunker
from app.utils.config import env


class LLamaIndexChunker(BaseChunker):
    def __init__(
        self,
    ) -> None:
        self.openai_embedding_model = OpenAIEmbedding(
            api_base=env.OPENAI_BASE_URL, api_key=env.OPENAI_API_KEY
        )
        self.local_embedding_model = OpenAIEmbedding(
            api_base=env.XINFERENCE_ENDPOINT,
            api_key="NOT USEFUL",
            model_name=env.XINFERENCE_EMBEDDING_MODEL_UID,
        )

    def semantic_chunk(self, input: str) -> list[str]:
        embed_model = self.openai_embedding_model
        splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=65, embed_model=embed_model
        )

        documents = [Document(text=input)]

        nodes = splitter.get_nodes_from_documents(documents)

        return [node.text for node in nodes]

    def semantic_chunk_with_local(self, input: str) -> list[str]:
        embed_model = self.local_embedding_model
        splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=65, embed_model=embed_model
        )

        documents = [Document(text=input)]

        nodes = splitter.get_nodes_from_documents(documents)

        return [node.text for node in nodes]

    def chunk(self, input: str) -> list[str]:

        return self.semantic_chunk_with_local(input)
