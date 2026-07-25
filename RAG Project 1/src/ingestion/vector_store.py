import faiss
import numpy as np
import json
import os
from config import PROCESSED_DIR

#PROCESSED_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\RAG Project 1\data\processed"


def create_vector_store(embeddings, chunks):

    print("Creating folder:", PROCESSED_DIR)

    os.makedirs(
        PROCESSED_DIR,
        exist_ok=True
    )

    print("Folder exists:", os.path.exists(PROCESSED_DIR))


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
        os.path.join(PROCESSED_DIR, "faiss.index")
    )


    with open(
        os.path.join(PROCESSED_DIR, "chunks.json"),
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