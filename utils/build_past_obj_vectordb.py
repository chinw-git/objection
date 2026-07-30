from dotenv import load_dotenv

#from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
#from langchain_community.vectorstores import Chroma

import os
import pandas as pd
import shutil


db_path = "vectordb/past_cases"

if os.path.exists(db_path):
    shutil.rmtree(db_path)

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Paths
# -----------------------------
file_path = "data/classified_objections.csv"

VECTOR_DB_PATH = "vectordb/past_cases"

COLLECTION_NAME = "past_objections"

# -----------------------------
# Embedding model
# -----------------------------
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# -----------------------------
# Load CSV
# -----------------------------
print("Loading objection cases...")

df = pd.read_csv(file_path)

print(f"Loaded {len(df)} objection cases.")

# ------------------------------------
# Convert each row into one Document
# ------------------------------------
documents = []

for _, row in df.iterrows():
    #structure each document with relevant information
    strata = "Strata" if row["IS_STRATA"] == 1 else "Non-strata"

    document_text = f"""
                    **Property Type**  
                    {row["Team"]}

                    **Development**  
                    {row["DEV"]}

                    **Strata Classification**  
                    {strata}

                    **Grounds of Objection**  
                    {row["ExplanatoryNote"]}

                    **Number of Uploaded Files**  
                    {row["FileUploadCount"]}

                    **Reasoning**  
                    {row["Reason"]}
                    """
    documents.append(
        Document(
            page_content=document_text,
            #add metadata (excl from embedding) for filtering and retrieval
            metadata={
                "team": row["Team"],
                "is_strata": bool(row["IS_STRATA"]),
                "complexity": row["Category"],
                "file_upload_count": int(row["FileUploadCount"])
            }
        )
    )

print(f"Created {len(documents)} LangChain documents.")

# -----------------------------
# No need Chunking
# -----------------------------

# -----------------------------
# Create Chroma Vector Store
# -----------------------------
print("Creating vector database...")

vector_db = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=VECTOR_DB_PATH,
    collection_name=COLLECTION_NAME,
)

print(f"Vector database saved to {VECTOR_DB_PATH}")