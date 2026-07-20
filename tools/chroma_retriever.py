import os
from typing import List, Dict

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()


class ChromaRetriever:
    """
    Handles all communication with ChromaDB.

    This class is framework-independent and can be reused by:
    - Streamlit
    - pytest
    - CrewAI tools
    """

    def __init__(
        self,
        db_path: str = "db/chroma",
        collection_name: str = "property_objections",
        embedding_model: str = "text-embedding-3-large",
    ):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found.")

        embedding_function = OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name=embedding_model,
        )

        client = chromadb.PersistentClient(path=db_path)

        self.collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_function,
        )

    def search(
        self,
        objection: str,
        top_k: int = 5,
    ) -> List[Dict]:

        results = self.collection.query(
            query_texts=[objection],
            n_results=top_k,
        )

        output = []

        for doc, meta, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):

            output.append(
                {
                    "grounds_of_objection": doc,
                    "urgency": meta["urgency"],
                    "complexity": meta["complexity"],
                    "primary_bucket": meta["primary_bucket"],
                    "distance": round(distance, 4),
                }
            )

        return output