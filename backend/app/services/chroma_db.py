import chromadb
from pathlib import Path

DB_PATH=Path("vector_store")

client=chromadb.PersistentClient(path=str(DB_PATH))


collection=client.get_or_create_collection(name="company_documents",metadata={"hnsw:space":"cosine"})