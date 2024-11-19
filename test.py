from qdrant_client import QdrantClient

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)  # Adjust host and port if necessary

# Perform health check
try:
    health = client.api_cluster.is_healthy()
    print(f"Qdrant health status: {health}")
except Exception as e:
    print(f"Failed to connect to Qdrant: {e}")
