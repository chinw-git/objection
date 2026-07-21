import os

import chromadb
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv()


class SemanticMatcher:

    def __init__(self):

        embedding_function = OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-large"
        )

        client = chromadb.PersistentClient(
            path="db/chroma"
        )

        self.collection = client.get_collection(
            name="property_signals",
            embedding_function=embedding_function
        )

    def match(
        self,
        text,
        n_results=5
    ):

        results = self.collection.query(

            query_texts=[text],

            n_results=n_results
        )

        matches = []

        for doc, meta, distance in zip(

            results["documents"][0],

            results["metadatas"][0],

            results["distances"][0]

        ):

            matches.append(

                {
                    "phrase": doc,
                    "category": meta["category"],
                    "distance": distance
                }

            )

        return matches