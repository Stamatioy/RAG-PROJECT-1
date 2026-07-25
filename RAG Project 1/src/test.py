from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents


docs = load_documents()

chunks = chunk_documents(docs)

print("Chunks:", len(chunks))

print(chunks[0])