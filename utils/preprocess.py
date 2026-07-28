## used in build_vector_store script to build the objections vector store

import re
import pandas as pd


def clean_text(text: str) -> str:
    """
    Basic text cleaning for embedding models.
    Keep preprocessing light since embedding models
    work best with natural language.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # lowercase
    text = text.lower()

    # remove line breaks
    text = text.replace("\n", " ")

    # collapse whitespace
    text = re.sub(r"\s+", " ", text)

    # remove repeated punctuation
    text = re.sub(r"[ ]+", " ", text)

    return text.strip()


def build_document(row) -> str:
    """
    Construct the document that will be embedded.

    Only the grounds of objection are embedded.
    Labels such as urgency and complexity remain metadata.
    """

    return clean_text(row["ExplanatoryNote"])