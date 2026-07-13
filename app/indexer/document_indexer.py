import os

from app.loader.pdf_loader import PDFLoader
from app.chunking.text_chunker import TextChunker
from app.embeddings.embedding_model import EmbeddingModel
from app.vectordb.chroma_store import ChromaStore


class DocumentIndexer:

    def __init__(self):
        self.loader = PDFLoader()
        self.chunker = TextChunker()
        self.embedding_model = EmbeddingModel()
        self.vector_db = ChromaStore()

    def index_folder(self, folder):
        for file in os.listdir(folder):
            if not file.endswith(".pdf"):
                continue
            path = os.path.join(folder, file)
            print(f"Indexing {file}")
            text = self.loader.load(path)
            chunks = self.chunker.chunk(text)
            embeddings = self.embedding_model.embed(chunks)
            self.vector_db.add_documents(
                chunks,
                embeddings,
                source=file,
            )
            