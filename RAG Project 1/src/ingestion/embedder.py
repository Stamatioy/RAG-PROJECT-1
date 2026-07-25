from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


model = SentenceTransformer(
    EMBEDDING_MODEL
)


def create_embeddings(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
    texts,
    normalize_embeddings=True
    )

    return embeddings