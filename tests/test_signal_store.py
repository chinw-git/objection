"""
Interactive tester for the Property Signal vector store.

- Supports multi-line objections
- Prints similarity scores
- Groups results neatly
"""

import os

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()


def read_multiline():
    """
    Read multiple lines from the console.

    Press ENTER twice to finish.
    """

    print("\nPaste objection below.")
    print("Press ENTER twice when finished.\n")

    lines = []

    while True:

        line = input()

        if line == "":

            if len(lines) == 0:
                return None

            break

        lines.append(line)

    return "\n".join(lines)


def print_results(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n")
    print("=" * 80)
    print("Top Semantic Matches")
    print("=" * 80)

    for i, (doc, meta, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):

        similarity = max(0, 1 - distance)

        print(f"\n{i}. Signal")

        print(f"   Phrase      : {doc}")
        print(f"   Category    : {meta['category']}")
        print(f"   Distance    : {distance:.4f}")
        print(f"   Similarity  : {similarity:.2%}")

    print("=" * 80)


def main():

    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-large",
    )

    client = chromadb.PersistentClient(
        path="db/chroma"
    )

    collection = client.get_collection(
        name="property_signals",
        embedding_function=embedding_function,
    )

    print("=" * 80)
    print("PROPERTY SIGNAL VECTOR STORE TEST")
    print("=" * 80)

    while True:

        query = read_multiline()

        if query is None:
            continue

        if query.lower().strip() == "exit":
            break

        print("\nSearching...")

        results = collection.query(
            query_texts=[query],
            n_results=10,
        )

        print_results(results)

    print("\nGoodbye!")


if __name__ == "__main__":
    main()