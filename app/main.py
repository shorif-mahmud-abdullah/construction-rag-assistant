from app.vectordb.chroma_store import ChromaStore
from app.indexer.document_indexer import DocumentIndexer
indexer = DocumentIndexer()
db = ChromaStore()
if db.is_empty():
    indexer.index_folder("documents")


from app.rag.rag_service import RAGService
rag = RAGService()
while True:
    question = input("\nQuestion: ")
    if question.lower() == "exit":
        break
    answer = rag.ask(question)
    print("\nAnswer:\n")
    print(answer)
    