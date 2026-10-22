"""Shared test setup.

The real embedding model (sentence-transformers + torch) is large and needs a
model download, so tests replace the `sentence_transformers` module with a tiny
stub. Everything else (chunking, PDF loading, ChromaDB, the RAG prompt) runs for real.
"""
import sys
import types

import numpy as np

stub = types.ModuleType("sentence_transformers")


class _FakeSentenceTransformer:
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, texts, convert_to_numpy=True):
        return np.array([[float(len(t)), 1.0, 0.0, 0.5] for t in texts])


stub.SentenceTransformer = _FakeSentenceTransformer
sys.modules["sentence_transformers"] = stub
