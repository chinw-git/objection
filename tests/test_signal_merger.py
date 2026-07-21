from utils.signal_merger import SignalMerger


def main():

    exact_matches = [

        {
            "phrase": "vacancy",
            "category": "property"
        },

        {
            "phrase": "major renovation",
            "category": "property"
        }

    ]

    semantic_matches = [

        {
            "phrase": "vacancy",
            "category": "property",
            "distance": 0.04
        },

        {
            "phrase": "market rent",
            "category": "valuation",
            "distance": 0.23
        },

        {
            "phrase": "lease",
            "category": "property",
            "distance": 1.80
        }

    ]

    merged = SignalMerger.merge(

        exact_matches,

        semantic_matches,

        semantic_threshold=1.2

    )

    print("\nMerged Signals")
    print("=" * 60)

    for signal in merged:

        print(signal)


if __name__ == "__main__":
    main()