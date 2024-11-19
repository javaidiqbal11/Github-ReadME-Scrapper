from qdrant_client import QdrantClient
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant


class QdrantManager:
    """
    Manages interactions with the Qdrant vector database.
    """

    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "github_readmes"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings()
        self.embedding_dim = 1536  # Fixed embedding dimension for OpenAI's text-embedding-ada-002 model

    def initialize_collection(self):
        """
        Initializes a collection in Qdrant for storing vectors.
        """
        try:
            # Try to get the collection
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists.")
        except Exception:
            # If the collection doesn't exist, create it
            print(f"Collection '{self.collection_name}' not found. Creating new collection...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vector_size=self.embedding_dim,  # Use fixed dimension
                distance="Cosine",
            )
            print(f"Collection '{self.collection_name}' created.")

    def store_readme(self, content: str):
        """
        Stores the README content as text embeddings in Qdrant.
        :param content: README content as a string.
        """
        vector_store = Qdrant(client=self.client, collection_name=self.collection_name, embeddings=self.embeddings)
        vector_store.add_texts([content])
        print("README content stored in Qdrant.")

    def create_retriever(self):
        """
        Creates a retriever object for Qdrant.
        :return: Retriever object.
        """
        vector_store = Qdrant(client=self.client, collection_name=self.collection_name, embeddings=self.embeddings)
        return vector_store.as_retriever()
