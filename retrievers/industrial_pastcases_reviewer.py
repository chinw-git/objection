"""
retrievers/industrial_pastcases_reviewer.py

Retrieves similar past objection cases from the vector store built by
tasks/industrial_pastcases_embedding_db.py.
"""

from dotenv import load_dotenv
load_dotenv()

import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

VECTOR_DB_PATH = "db/chroma"
COLLECTION_NAME = "property_objections"
EMBEDDING_MODEL = "text-embedding-3-large"

embedding_function = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name=EMBEDDING_MODEL,
)

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)


def retrieve_similar_cases(
    grounds_of_objection: str,
    category_filter: str = None,
    top_k: int = 5,
) -> list[dict]:
    """
    Given a new objection's grounds and (optionally) a category to filter by,
    returns the top-k most semantically similar past cases.
    """
    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    query_kwargs = {
        "query_texts": [grounds_of_objection],
        "n_results": top_k,
    }
    if category_filter:
        query_kwargs["where"] = {"category": category_filter}

    results = collection.query(**query_kwargs)

    similar_cases = []
    for doc, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        similar_cases.append({
            "explanatory_note": doc,
            "category": meta["category"],
            "reason": meta["reason"],
            "distance": round(distance, 4),
        })
    return similar_cases