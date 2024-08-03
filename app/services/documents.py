import chromadb

'''
 Chroma db has AsyncHttpClient for async requests, for simplicity i'm using PersistentClient
'''
chroma_client = chromadb.PersistentClient(path="/data")


class DocumentsService:
    def __init__(self):
        self.collection = chroma_client.get_or_create_collection(name="documents")

    def get_similar_by_query(self, query: str, n_results: int):
        return self.collection.query(
            query_embeddings=[query],
            n_results=n_results
        )

    def save_new_embedding(self, path: str, vector: list):
        self.collection.add(ids=[path], embeddings=[vector])
