from dataclasses import dataclass
from enum import Enum
from typing import Optional

from numpy import ndarray


# i put here, cos i am lazy to create new file
# bad example, dont learn from me
class CollectionPropertyNameEnum(str, Enum):
    text_vector = "text_vector"
    text = "text"
    chunk_name = "chunk_name"
    open_url = "open_url"


# here i am using dataclass, cos pydantic
# does not take ndarray...
@dataclass
class ChunkSavedInVDB:
    open_url: str
    vector: ndarray
    chunk_name: str
    text: Optional[str] = None
