from typing import Iterable, List, Union

import numpy as np
from openai import Client

from app.embedding.base import BaseVectorizer


class XInferenceVectorizer(BaseVectorizer):
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model
        self.client = Client(base_url=self.base_url, api_key=self.api_key)
        self.dimension = self.vectorize("Hello, world!").shape[1]

    def vectorize(
        self, input: Union[str, List[str], Iterable[int], Iterable[Iterable[int]]]
    ) -> np.ndarray:
        """
        Vectorize the input text.
        Args:
            input (Union[str, List[str], Iterable[int], Iterable[Iterable[int]]]): input text
        Returns:
            np.ndarray: vectorized input, shape:(n, dimension)
        """
        response = self.client.embeddings.create(model=self.model_name, input=input)
        return np.array(
            [embedding.embedding for embedding in response.data], dtype=np.float32
        )


if __name__ == "__main__":
    from app.utils.config import env

    vectorizer = XInferenceVectorizer(
        base_url=env.EMBEDDING_ENDPOINT,
        api_key="speak and see it done",
        model=env.EMBEDDING_MODEL_UID,
    )
    res = vectorizer.vectorize(["Hello, world!", "Goodbye, world!"])
    import numpy as np

    print(res.shape)
