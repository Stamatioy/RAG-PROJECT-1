import wikipediaapi
import os
import json
from datetime import datetime
from ingestion.cleaner import clean_article


RAW_DATA_PATH = rf"D:\Programming\Projects\RAG\Simple RAG\Ancient Greece RAG\data\raw"


ARTICLES = [
    "Ancient Greece",
    "Sparta",
    "Peloponnesian War",
    "Persian Wars",
    "Pericles",
    "Socrates",
    "Plato",
    "Aristotle",
    "Alexander the Great",
    "Delian League",
    "Minoan civilization",
    "Mycenaean Greece",
    "Greek Dark Ages",
    "Archaic Greece",
    "Hellenistic Greece"
]


def extract_sections(page):

    sections = []

    def process_section(section):

        if section.text.strip():

            sections.append(
                {
                    "title": section.title,
                    "text": section.text
                }
            )

        for subsection in section.sections:
            process_section(subsection)


    for section in page.sections:
        process_section(section)


    return sections

def get_wikipedia_article(title):
    """
    Downloads a Wikipedia article.
    """

    wiki = wikipediaapi.Wikipedia(
        user_agent="AncientGreeceRAG/1.0 (contact@example.com)",
        language="en"
    )

    page = wiki.page(title)

    if not page.exists():
        print(f"Article not found: {title}")
        return None

    article = {
        "title": page.title,
        "summary": page.summary,
        "sections": extract_sections(page),
        "url": page.fullurl,
        "downloaded_at": datetime.now().isoformat()
    }

    article = clean_article(article)

    return article


def save_article(article):

    filename = (
        article["title"]
        .replace(" ", "_")
        .replace("/", "_")
    )

    filepath = os.path.join(
        RAW_DATA_PATH,
        f"{filename}.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            article,
            f,
            ensure_ascii=False,
            indent=4
        )


def main():

    os.makedirs(
        RAW_DATA_PATH,
        exist_ok=True
    )

    for title in ARTICLES:

        print(f"Downloading: {title}")

        article = get_wikipedia_article(title)

        if article:
            save_article(article)
            print(f"Saved: {article['title']}")

        print("-" * 40)


if __name__ == "__main__":
    main()