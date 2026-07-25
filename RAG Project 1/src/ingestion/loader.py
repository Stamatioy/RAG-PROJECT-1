import os
import json


RAW_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\Ancient Greece RAG\data\raw"


def load_documents():

    documents = []

    for filename in os.listdir(RAW_PATH):

        if filename.endswith(".json"):

            filepath = os.path.join(
                RAW_PATH,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                documents.append(data)

    return documents


if __name__ == "__main__":

    docs = load_documents()

    print(f"Loaded {len(docs)} documents")

    print(docs[0]["title"])
    print(docs[0]["text"][:500])