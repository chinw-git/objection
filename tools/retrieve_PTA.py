from crewai.tools import tool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# multi-query retrieval
@tool("Retrieve Property Tax Act") #makes it a crewAI tool
def retrieve_legislation(query: str) -> str:
    """
    Retrieves the most relevant Property Tax Act sections.
    """
    print(type(query))
    print(query)

    #load the Chroma vector store for the Property Tax Act
    db = Chroma(
        persist_directory="vectordb/legislation",
        embedding_function=embedding_model,
        collection_name="property_tax_act"
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )

    #use MultiQueryRetreiever for PTA since terminology may vary across sections of the Act
    retriever = MultiQueryRetriever.from_llm(
        retriever=db.as_retriever(search_kwargs={"k": 5}),
        llm=llm,
    )

    docs = retriever.invoke(query)

    return "\n\n".join(doc.page_content for doc in docs)