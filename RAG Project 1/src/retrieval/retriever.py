import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from api.exceptions import RetrievalError
from config import INDEX_PATH, CHUNKS_PATH, EMBEDDING_MODEL, MIN_SCORE, TOP_K


#INDEX_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\RAG Project 1\data\processed\faiss.index"
#CHUNKS_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\RAG Project 1\data\processed\chunks.json"



print("Loading embedding model...")

try:
    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

except Exception as e:
    raise RetrievalError(
        f"Failed loading embedding model: {e}"
    )



print("Loading FAISS index...")

try:
    index = faiss.read_index(
        str(INDEX_PATH)
    )

except Exception as e:
    raise RetrievalError(
        f"Failed loading FAISS index: {e}"
    )



print("Loading chunks...")

try:
    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)

except Exception as e:
    raise RetrievalError(
        f"Failed loading chunks: {e}"
    )


print("Retriever ready.")



def retrieve(
        query,
        k=TOP_K
):

    try:

        query_embedding = model.encode(
            [query]
        )


        distances, indices = index.search(
            np.array(query_embedding),
            k
        )


        results = []


        for score, idx in zip(
            distances[0],
            indices[0]
        ):

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


    except Exception as e:

        raise RetrievalError(
            f"Retrieval failed: {e}"
        )



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