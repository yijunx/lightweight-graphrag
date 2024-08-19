from app.chunking.simple_chunking import SimpleChunker


def test_chunking():
    chunker = SimpleChunker()
    chunks = chunker.chunk("oldmanandthesea.txt")
