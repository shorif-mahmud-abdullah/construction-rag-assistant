from app.chunking.text_chunker import TextChunker


def test_short_text_is_a_single_chunk():
    assert TextChunker().chunk("hello") == ["hello"]


def test_empty_text_gives_no_chunks():
    assert TextChunker().chunk("") == []


def test_chunks_are_never_longer_than_chunk_size():
    chunks = TextChunker(chunk_size=50, overlap=10).chunk("x" * 333)
    assert all(len(c) <= 50 for c in chunks)


def test_consecutive_chunks_overlap():
    text = "".join(chr(65 + i % 26) for i in range(200))
    chunks = TextChunker(chunk_size=50, overlap=10).chunk(text)
    assert chunks[0][-10:] == chunks[1][:10]


def test_no_text_is_lost():
    text = "".join(chr(65 + i % 26) for i in range(500))
    chunker = TextChunker(chunk_size=100, overlap=20)
    chunks = chunker.chunk(text)
    rebuilt = chunks[0] + "".join(c[chunker.overlap:] for c in chunks[1:])
    assert rebuilt == text
