from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    chunks = []

    for doc in documents:

        for section in doc["sections"]:

            section_title = section["title"]
            text = section["text"]


            section_chunks = splitter.split_text(
                text
            )


            for i, chunk in enumerate(section_chunks):

                chunks.append(
                    {
                        "text": chunk,
                        "source": doc["title"],
                        "section": section_title,
                        "chunk_id": i,
                        "url": doc["url"]
                    }
                )


    return chunks