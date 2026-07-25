import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

MIN_SCORE =  0.4
# Paths
INDEX_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\Ancient Greece RAG\data\processed\faiss.index"
CHUNKS_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\Ancient Greece RAG\data\processed\chunks.json"


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def load_vector_store():
    """
    Loads FAISS index and chunk metadata.
    """

    index = faiss.read_index(
        INDEX_PATH
    )

    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)

    return index, chunks



def retrieve(
        query,
        k=5
):
    """
    Retrieve the k most relevant chunks.
    """

    index, chunks = load_vector_store()


    # Convert query to embedding
    query_embedding = model.encode(
        [query]
    )


    # Search FAISS
    distances, indices = index.search(
        np.array(query_embedding),
        k
    )


    results = []


    for score, idx in zip(distances[0], indices[0]):

        if score < MIN_SCORE:
            continue

        results.append(
            {
                "score": float(score),
                "text": chunks[idx]["text"],
                "source": chunks[idx]["source"],
                "section": chunks[idx]["section"],
                "url": chunks[idx]["url"],
            }
        )


    return results



if __name__ == "__main__":

    question = input(
        "Ask a question: "
    )


    results = retrieve(
        question,
        k=5
    )


    print("\nTop results:\n")


    for i, result in enumerate(results):

        print("=" * 80)

        print(
            f"Result {i+1}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Score: {result['score']}"
        )

        print()

        print(
            result["text"][:500]
        )

        print()