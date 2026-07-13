import chromadb


class ChromaStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )
        self.collection = self.client.get_or_create_collection(
            name="construction_docs"
        )
    def add_documents(
            self,
            chunks,
            embeddings,
            source,
        ):
        self.collection.add(
            ids=[
                str(i)
                for i in range(len(chunks))
            ],
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=[
                        {
                            "source": source
                        }
                        for _ in chunks
                    ],
        )
    def search(
        self,
        query_embedding,
        n_results=3,
    ):
        return self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=n_results,
        )
    
    def is_empty(self):
        return self.collection.count() == 0
