from abc import ABC, abstractmethod
from typing import Iterable, List, Union

import numpy as np


class BaseVectorizer(ABC):

    @abstractmethod
    def vectorize(
        self, input: Union[str, List[str], Iterable[int], Iterable[Iterable[int]]]
    ) -> np.ndarray: ...
