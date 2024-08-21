from typing import Iterable

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import Document
from llama_index.embeddings.openai import OpenAIEmbedding

from app.chunking.base import BaseChunker


class LLamaIndexChunker(BaseChunker):
    def __init__(self, base_url: str, api_key: str, model: str = None) -> None:
        self.openai_embedding_model = OpenAIEmbedding(
            api_base=base_url, api_key=api_key
        )
        # free one
        self.local_embedding_model = OpenAIEmbedding(
            api_base=base_url,
            api_key="NOT USEFUL",
            model_name=model,
        )

    def semantic_chunk(self, text: str) -> list[str]:
        """need to pay for openai"""

        embed_model = self.openai_embedding_model
        splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=65, embed_model=embed_model
        )

        documents = [Document(text=text)]

        nodes = splitter.get_nodes_from_documents(documents)

        return [node.text for node in nodes]

    def semantic_chunk_with_local(self, text: str) -> list[str]:
        """use local model"""
        embed_model = self.local_embedding_model
        splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=65, embed_model=embed_model
        )
        documents = [Document(text=text)]

        nodes = splitter.get_nodes_from_documents(documents)

        return [node.text for node in nodes]

    def chunk(self, text_file_path: str) -> Iterable[str]:
        with open(text_file_path, "r") as file:
            text = file.read()
        # yay we use the free one, coz i have xinference running
        # thus no need to pay
        return self.semantic_chunk_with_local(text)


if __name__ == "__main__":
    from app.utils.config import env

    chunker = LLamaIndexChunker(
        base_url=env.EMBEDDING_ENDPOINT,
        api_key="bro",
        model=env.EMBEDDING_MODEL_UID,
    )
    res = chunker.chunk("oldmanandthesea.txt")
