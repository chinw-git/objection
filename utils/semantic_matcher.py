import os

import chromadb
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from collections import Counter

load_dotenv()


class SemanticMatcher:

    def __init__(self):

        embedding_function = OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-large"
        )

        from pathlib import Path

        BASE_DIR = Path(__file__).resolve().parent.parent

        DB_PATH = BASE_DIR / "db" / "chroma"

        client = chromadb.PersistentClient(
            path=str(DB_PATH)
        )

        self.collection = client.get_collection(
            name="bucket_signals",
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
                    "signal": doc,
                    "primary_bucket": meta["category"],
                    "distance": float(distance)
                }

            )

        matches.sort(key=lambda x: x["distance"])

        def predict_bucket(
            self,
            text,
            n_results=5
        ):

            matches = self.match(
                text=text,
                n_results=n_results
            )

            bucket_counter = Counter(
                m["primary_bucket"]
                for m in matches
            )

            predicted_bucket = bucket_counter.most_common(1)[0][0]

            return predicted_bucket, matches
        
        return matches