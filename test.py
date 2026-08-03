# from tools.retrieve_PTA import retrieve_legislation
# from tools.retrieve_past_obj import retrieve_similar_cases
# from utils.load_rubrics import load_rubrics

# objection = """
# I object to the Annual Value because the ground floor is rented
# for $3,800/month while the upper floor is owner occupied.
# Please review the Annual Value.
# """

# pta_docs = retrieve_legislation(objection)
# past_cases = retrieve_similar_cases(objection)
# rubrics = load_rubrics()

# print("\n")
# print("=" * 80)
# print("PROPERTY TAX ACT")
# print("=" * 80)

# for i, doc in enumerate(pta_docs, start=1):
#     print(f"\nDocument {i}")
#     print("-" * 80)
#     print(doc.page_content)

# print("\n")
# print("=" * 80)
# print("SIMILAR PAST CASES")
# print("=" * 80)

# for i, doc in enumerate(past_cases, start=1):

#     print(f"\nCase {i}")
#     print("-" * 80)

#     print("Metadata")
#     print(doc.metadata)

#     print("\nContent")
#     print(doc.page_content)

# print("\n")
# print("=" * 80)
# print("COMPLEXITY RUBRIC")
# print("=" * 80)

# print(rubrics)

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

db = Chroma(
    persist_directory="vectordb/past_cases",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="past_objections",
)

# Retrieve a few documents directly
docs = db.similarity_search("property", k=3)

for i, doc in enumerate(docs, start=1):
    print("=" * 80)
    print(f"Document {i}")
    print("-" * 80)
    print(doc.page_content)
    print("-" * 80)
    print("repr:")
    print(repr(doc.page_content))
    print("-" * 80)
    print("metadata:")
    print(doc.metadata)