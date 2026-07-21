"""
Interactive test for SignalExtractionTool.
"""

import json

from tools.signal_extraction_tool import SignalExtractionTool


def read_multiline():
    """
    Read multiple lines until a blank line is entered.
    """

    print("\nPaste objection below.")
    print("Press ENTER twice when finished.")
    print("Type 'exit' to quit.\n")

    lines = []

    while True:

        line = input()

        if line.lower() == "exit":
            return None

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines)


def print_section(title, items):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if not items:
        print("None")
        return

    for i, item in enumerate(items, start=1):

        print(f"\n{i}.")

        for key, value in item.items():
            print(f"  {key:<12}: {value}")


def main():

    tool = SignalExtractionTool()

    print("=" * 70)
    print("SIGNAL EXTRACTION TOOL TEST")
    print("=" * 70)

    while True:

        objection = read_multiline()

        if objection is None:
            break

        result = tool.extract(objection)

        print_section(
            "Exact Matches",
            result["exact_matches"]
        )

        print_section(
            "Semantic Matches",
            result["semantic_matches"]
        )

        print_section(
            "Combined Signals",
            result["combined_signals"]
        )

        print("\nStatistics")
        print("-" * 70)

        for k, v in result["statistics"].items():
            print(f"{k:<20}: {v}")

        print()

    print("Goodbye!")


if __name__ == "__main__":
    main()