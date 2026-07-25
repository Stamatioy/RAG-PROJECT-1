from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.embedder import create_embeddings
from ingestion.vector_store import create_vector_store


documents = load_documents()

print(
    f"Documents loaded: {len(documents)}"
)


chunks = chunk_documents(
    documents
)

print(
    f"Chunks created: {len(chunks)}"
)


embeddings = create_embeddings(
    chunks
)


create_vector_store(
    embeddings,
    chunks
)


print("Ingestion complete!")