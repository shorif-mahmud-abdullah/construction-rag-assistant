import chromadb
import numpy as np
import pytest

from app.vectordb import chroma_store
from app.vectordb.chroma_store import ChromaStore


@pytest.fixture
def store(monkeypatch):
    # Use an in-memory ChromaDB instead of writing ./chroma_db, and start every
    # test from an empty collection (in-memory clients share state per process).
    monkeypatch.setattr(
        chroma_store.chromadb, "PersistentClient", lambda path: chromadb.EphemeralClient()
    )
    store = ChromaStore()
    store.client.delete_collection("construction_docs")
    store.collection = store.client.get_or_create_collection(name="construction_docs")
    return store


def embeddings(n):
    return np.random.default_rng(0).random((n, 4))


def test_new_store_is_empty(store):
    assert store.is_empty()


def test_chunks_from_different_documents_do_not_overwrite_each_other(store):
    # Regression test: ids used to be "0", "1", ... for every document, so the
    # second document's chunks collided with the first one's and were dropped.
    store.add_documents(["a1", "a2"], embeddings(2), "doc_a.pdf")
    store.add_documents(["b1", "b2", "b3"], embeddings(3), "doc_b.pdf")
    assert store.collection.count() == 5


def test_search_returns_source_metadata(store):
    store.add_documents(["alpha", "beta"], embeddings(2), "doc_a.pdf")
    results = store.search(embeddings(1)[0], n_results=2)
    assert {m["source"] for m in results["metadatas"][0]} == {"doc_a.pdf"}
