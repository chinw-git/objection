class SignalMerger:

    @staticmethod
    def merge(

        exact_matches,

        semantic_matches,

        semantic_threshold=1.2

    ):

        combined = []

        seen = set()

        # Exact matches get HIGH confidence

        for signal in exact_matches:

            key = signal["phrase"].lower()

            combined.append(

                {

                    "phrase": signal["phrase"],

                    "category": signal["category"],

                    "confidence": "high",

                    "source": "exact"

                }

            )

            seen.add(key)

        # Semantic matches

        for signal in semantic_matches:

            if signal["distance"] > semantic_threshold:
                continue

            key = signal["phrase"].lower()

            if key in seen:
                continue

            combined.append(

                {

                    "phrase": signal["phrase"],

                    "category": signal["category"],

                    "confidence": "medium",

                    "source": "semantic",

                    "distance": signal["distance"]

                }

            )

        return combined