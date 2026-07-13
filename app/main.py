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




# from app.loader.pdf_loader import PDFLoader

# loader = PDFLoader()

# text = loader.load("documents/01_construction_safety_regulations.pdf")
# from app.chunking.text_chunker import TextChunker
# chunker = TextChunker()
# chunks = chunker.chunk(text)

# from app.embeddings.embedding_model import EmbeddingModel
# embedding_model = EmbeddingModel()
# embeddings = embedding_model.embed(chunks)
# print(len(embeddings))
# print(embeddings.shape)
# print(type(embeddings[0]))

# from app.vectordb.chroma_store import ChromaStore
# db = ChromaStore()
# db.add_documents(
#     chunks,
#     embeddings,
# )

# query = "At what heights does OSHA require fall protection in general construction versus scaffolds?"
# query_embedding = embedding_model.embed([query])[0]
# results = db.search(query_embedding)
# print(len(results["documents"][0]))