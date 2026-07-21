"""
Builds a Chroma vector store containing property-domain signals.

Each signal is stored as its own document.

Example

Document:
    "major renovation"

Metadata:
    {
        "category": "property"
    }

This collection is later queried by the SignalExtractionTool.
"""

import json
import os
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------------
# Configuration
# --------------------------------------------------------

SIGNAL_FILE = Path("config/property_signals.json")

DB_PATH = "db/chroma"

COLLECTION_NAME = "property_signals"

EMBEDDING_MODEL = "text-embedding-3-large"


# --------------------------------------------------------
# Load API Key
# --------------------------------------------------------

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in .env"
    )


embedding_function = OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name=EMBEDDING_MODEL
)


# --------------------------------------------------------
# Initialise Chroma
# --------------------------------------------------------

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


# --------------------------------------------------------
# Clear existing signals
# --------------------------------------------------------

count = collection.count()

if count > 0:

    print(f"Removing {count} existing signals...")

    ids = collection.get()["ids"]

    collection.delete(ids=ids)


# --------------------------------------------------------
# Read signal dictionary
# --------------------------------------------------------

with open(SIGNAL_FILE, "r") as f:

    signal_dictionary = json.load(f)


documents = []

metadatas = []

ids = []

index = 0


# --------------------------------------------------------
# Convert JSON into documents
# --------------------------------------------------------

for category, signals in signal_dictionary.items():

    for signal in signals:

        documents.append(signal)

        metadatas.append(
            {
                "category": category
            }
        )

        ids.append(str(index))

        index += 1


# --------------------------------------------------------
# Build Vector Store
# --------------------------------------------------------

collection.add(

    documents=documents,

    metadatas=metadatas,

    ids=ids
)


# --------------------------------------------------------
# Summary
# --------------------------------------------------------

print("=" * 60)

print("Signal Vector Store Built Successfully")

print("=" * 60)

print(f"Collection : {COLLECTION_NAME}")

print(f"Signals    : {collection.count()}")

print(f"Categories : {len(signal_dictionary)}")

print("=" * 60)