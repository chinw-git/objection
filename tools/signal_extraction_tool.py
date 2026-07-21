import json
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr

from utils.keyword_matcher import KeywordMatcher
from utils.semantic_matcher import SemanticMatcher
from utils.signal_merger import SignalMerger


class SignalExtractionInput(BaseModel):
    """
    Input schema for SignalExtractionTool.
    """

    objection: str = Field(
        ...,
        description="Grounds of objection."
    )


class SignalExtractionTool(BaseTool):
    """
    Extracts business signals from a property objection using:

    1. Exact keyword matching
    2. Semantic vector search
    3. Merges both into one result
    """

    name: str = "Signal Extraction Tool"

    description: str = "..."

    args_schema: Type[BaseModel] = SignalExtractionInput

    semantic_threshold: float = 1.20

    _keyword_matcher: KeywordMatcher = PrivateAttr()
    _semantic_matcher: SemanticMatcher = PrivateAttr()


    description: str = (
        "Extracts property-related business signals from the "
        "grounds of objection using exact keyword matching "
        "and semantic similarity search."
    )

    

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self._keyword_matcher = KeywordMatcher()
        self._semantic_matcher = SemanticMatcher()

    def extract(self, objection: str):

        exact_matches = self._keyword_matcher.match(objection)

        semantic_matches = self._semantic_matcher.match(
            objection,
            n_results=10
        )

        merged = SignalMerger.merge(
            exact_matches,
            semantic_matches,
            semantic_threshold=self.semantic_threshold
        )

        return {
            "exact_matches": exact_matches,
            "semantic_matches": semantic_matches,
            "combined_signals": merged,
            "statistics": {
                "exact_matches": len(exact_matches),
                "semantic_matches": len(semantic_matches),
                "combined_signals": len(merged)
            }
        }

    def _run(self, objection: str) -> str:

        result = self.extract(objection)

        return json.dumps(
            result,
            indent=4
        )