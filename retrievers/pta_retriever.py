"""
retrievers/pta_retriever.py

Retrieves relevant Property Tax Act sections from the vector store
built by tasks/pta_embedding_task.py.
"""

from dotenv import load_dotenv
load_dotenv()

import chromadb
from langchain_openai import OpenAIEmbeddings

VECTOR_DB_PATH = "vectordb/"
COLLECTION_NAME = "property_tax_act"

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


def retrieve_pta_sections(query: str, k: int = 3) -> str:
    """
    Embeds the query, retrieves top-k relevant PTA sections from Chroma,
    and compiles them into a single context string.
    """
    collection = client.get_collection(COLLECTION_NAME)
    query_embedding = embedding_model.embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )
    chunks = results["documents"][0]
    return "\n\n---\n\n".join(chunks)