import faiss
import numpy as np
import json
import os


PROCESSED_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\Ancient Greece RAG\data\processed"


def create_vector_store(embeddings, chunks):

    print("Creating folder:", PROCESSED_PATH)

    os.makedirs(
        PROCESSED_PATH,
        exist_ok=True
    )

    print("Folder exists:", os.path.exists(PROCESSED_PATH))


    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        np.array(embeddings)
    )

    print("Saving FAISS index...")

    faiss.write_index(
        index,
        os.path.join(PROCESSED_PATH, "faiss.index")
    )


    with open(
        os.path.join(PROCESSED_PATH, "chunks.json"),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=4
        )

    print("Vector store complete")