import os
import shutil

import pandas as pd
import chromadb

from dotenv import load_dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from utils.preprocess import build_document


load_dotenv()

CSV_PATH = "data/Anonymised_Data.csv"

DB_PATH = "db/chroma"

COLLECTION_NAME = "property_objections"

EMBEDDING_MODEL = "text-embedding-3-large"


def main():

    print("Loading CSV...")

    df = pd.read_csv(CSV_PATH)

    # remove rows without objection text

    df = df.dropna(subset=["ExplanatoryNote"])

    print(f"{len(df)} objection cases loaded.")

    documents = []

    metadata = []

    ids = []

    for idx, row in df.iterrows():

        documents.append(build_document(row))

        metadata.append(
            {
                "urgency": str(row["Urgency Level"]),

                "complexity": int(row["Complexity Level"]),

                "primary_bucket": str(row["Primary Bucket"])
            }
        )

        ids.append(str(idx))

    if os.path.exists(DB_PATH):

        print("Existing vector store found.")

        shutil.rmtree(DB_PATH)

    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=EMBEDDING_MODEL
    )

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    print("Generating embeddings...")

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadata
    )

    print("--------------------------------")

    print(f"Documents indexed : {collection.count()}")

    print(f"Collection Name   : {COLLECTION_NAME}")

    print("Vector store built successfully.")


if __name__ == "__main__":

    main()