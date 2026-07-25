import re


BAD_HEADINGS = [
    "References",
    "External links",
    "Bibliography",
    "Further reading",
    "Notes",
    "See also",
    "Sources",
    "Citations",
    "Works cited",
    "Modern authors",
    "Classical authors",
    "Secondary sources",
    "Footnotes",
    "Ancient sources",
    "Modern sources",
]


def clean_text(text):
    """
    Remove unwanted Wikipedia sections and citation markers.
    """

    for heading in BAD_HEADINGS:

        # Everything from this heading until the end
        pattern = (
            r"\n" + 
            re.escape(heading) +
            r"\n.*"
        )

        text = re.split(
            pattern,
            text,
            flags=re.DOTALL
        )[0]


    # Remove Wikipedia citations like [1], [23]
    text = re.sub(
        r"\[\d+\]",
        "",
        text
    )

    return text.strip()



def clean_article(article):
    """
    Remove useless Wikipedia sections.
    """

    original_count = len(article["sections"])

    cleaned_sections = []

    for section in article["sections"]:

        title = section["title"].strip()

        if title in BAD_HEADINGS:
            continue

        # Remove empty sections
        if not section["text"].strip():
            continue

        cleaned_sections.append(section)


    article["sections"] = cleaned_sections


    print(
        f"{article['title']}: "
        f"{original_count} sections -> "
        f"{len(cleaned_sections)} sections"
    )


    return article