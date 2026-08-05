from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#simple similarity search based on the objection query
def retrieve_similar_cases(query: str, top_k: int = 5) -> list[dict]:

    #load the Chroma vector store for past objection cases
    db = Chroma(
        persist_directory="vectordb/past_cases",
        embedding_function=embedding_model,
        collection_name="past_objections"
    )

    docs = db.similarity_search(query, k=top_k)

    similar_cases = []

    for doc in docs:
        # similar_cases.append({
            
        #     "content": doc.page_content,
        #     "complexity": doc.metadata.get("complexity", "Unknown"),
        # })
        
        similar_cases.append({
            "property_type": doc.metadata.get("Property Type"),
            "development": doc.metadata.get("Development"),
            "strata_classification": doc.metadata.get("Strata Classification"),
            "grounds_of_objection": doc.page_content,
            "file_upload_count": doc.metadata.get("File Upload Count"),
            "complexity": doc.metadata.get("Complexity"),
            "reasoning": doc.metadata.get("Reasoning"),
        })
    return similar_cases