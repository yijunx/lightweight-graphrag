from typing import Generator, Iterable

from app.chunking.base import BaseChunker


class SimpleChunker(BaseChunker):
    def __init__(self, number_of_lines_per_chunk: int = 20) -> None:
        self.number_of_lines_per_chunk = number_of_lines_per_chunk

    def chunk(self, text_file_path: str) -> Iterable[str]:  # Generator[str, None, None]
        with open(text_file_path, "r") as file:
            text = file.read()
            lines = text.split("\n\n")

        for i in range(0, len(lines), self.number_of_lines_per_chunk):
            yield "\n\n".join(lines[i : i + self.number_of_lines_per_chunk])
