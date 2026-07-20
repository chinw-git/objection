import json
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from tools.chroma_retriever import ChromaRetriever


class ObjectionRAGInput(BaseModel):
    objection: str = Field(
        ...,
        description="Grounds of objection to search for."
    )


class ObjectionRAGTool(BaseTool):

    name: str = "Property Objection Retrieval Tool"

    description: str = (
        "Searches historical property objection cases "
        "using semantic similarity."
    )

    args_schema: Type[BaseModel] = ObjectionRAGInput

    retriever: ChromaRetriever = ChromaRetriever()

    def _run(self, objection: str) -> str:

        results = self.retriever.search(objection)

        return json.dumps(results, indent=4)