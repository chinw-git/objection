import json
from pathlib import Path


class KeywordMatcher:

    def __init__(self, signal_file="config/property_signals.json"):

        with open(signal_file, "r") as f:
            self.signal_dictionary = json.load(f)

    def match(self, text: str):

        text = text.lower()

        matches = []

        for category, phrases in self.signal_dictionary.items():

            for phrase in phrases:

                if phrase.lower() in text:

                    matches.append(
                        {
                            "phrase": phrase,
                            "category": category
                        }
                    )

        return matches