from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#load the Chroma vector store for past objection cases
db = Chroma(
    persist_directory="vectordb/past_cases",
    embedding_function=embedding_model,
    collection_name="past_objections"
)

#simple similarity search based on the objection query
def retrieve_similar_cases(query: str):
    return db.similarity_search(query, k=5) # top 5 similar past objection cases