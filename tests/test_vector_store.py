from utils.chroma_retriever import ChromaRetriever


def print_results(results):

    print("\n" + "=" * 80)

    print(f"Retrieved {len(results)} similar objections")

    print("=" * 80)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")

        print("-" * 40)

        print(f"Distance       : {result['distance']}")
        print(f"Urgency        : {result['urgency']}")
        print(f"Complexity     : {result['complexity']}")
        print(f"Primary Bucket : {result['primary_bucket']}")

        print("\nGrounds of Objection")

        print(result["grounds_of_objection"])

        print("-" * 40)

# main
def main():

    retriever = ChromaRetriever()

    while True:

        query = input(
            "\nEnter objection (or type 'exit'): "
        )

        if query.lower() == "exit":
            break

        results = retriever.search(query)

        print_results(results)


if __name__ == "__main__":

    main()