from app.embeddings.embedding_model import EmbeddingModel
from app.vectordb.chroma_store import ChromaStore
from app.llm.client import LLMClient


class RAGService:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_db = ChromaStore()
        self.llm = LLMClient()

    def ask(self, question: str):
        query_embedding = self.embedding_model.embed([question])[0]
        results = self.vector_db.search(query_embedding)
        contexts = results["documents"][0]
        sources = results["metadatas"][0]
        context = ""
        for doc, meta in zip(contexts, sources):
            context += f"""
                        Source: {meta['source']}
                        {doc}
                        ------------------
                    """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a construction engineering assistant.\n"
                    "Answer ONLY using the provided context and give the source information from which document you find the answer.\n"
                    "If the answer is not in the context, say:\n"
                    "'I couldn't find that information in the provided documents.'"
                )
            },
            {
                "role": "user",
                "content": f"""
                    Context:
                    {context}
                    Question:
                    {question}
            """
            }
        ]
        return self.llm.chat(messages)
