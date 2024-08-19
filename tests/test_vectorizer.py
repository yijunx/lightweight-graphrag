from app.embedding.x_vectorizer import XInferenceVectorizer
from app.utils.config import env


def test_vectorizer():
    vectorizer = XInferenceVectorizer(
        base_url=env.EMBEDDING_ENDPOINT,
        api_key="speak and see it done",
        model=env.EMBEDDING_MODEL_UID,
    )
    res = vectorizer.vectorize(["Hello, world!", "Goodbye, world!"])
    import numpy as np

    assert res.shape == (2, vectorizer.dimension)
    assert np.allclose(res[0], res[1]) is False
