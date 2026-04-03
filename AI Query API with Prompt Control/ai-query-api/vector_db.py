# vector_db.py

import chromadb
from sentence_transformers import SentenceTransformer
from config import DB_PERSIST_PATH, COLLECTION_NAME

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_PERSIST_PATH)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def add_documents(self, documents, metadatas=None):
        """
        Adds documents to the ChromaDB collection.
        """
        if not documents:
            return

        embeddings = self.embedding_model.encode(documents).tolist()
        ids = [str(i) for i in range(len(documents))]

        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int):
        """
        Queries the collection for the most relevant documents.
        """
        query_embedding = self.embedding_model.encode([query_text]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

# Initialize the vector DB
vector_db = VectorDB()
