#from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
#from langchain_community.vectorstores import Chroma

import os
import pandas as pd
import shutil
from textwrap import dedent

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
# Builds (or rebuilds) the past objection vector database.
# -----------------------------
def build_past_case_vectordb(csv_path: str = "data/classified_objections.csv"):
    
    # Delete existing vector store
    if os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)

    print("Loading objection cases...")

    # Load CSV
    df = pd.read_csv(csv_path)

    print(f"Loaded {len(df)} objection cases.")

    documents = []

    # ------------------------------------
    # Convert each row into one Document
    # ------------------------------------
    for _, row in df.iterrows():
        strata = "Strata" if row["IS_STRATA"] == 1 else "Non-strata"

        ##don't use triple quotes for the document text, as it can introduce formatting issues
        #only include objection text for embedding so that similarity search is based purely on the objection content
        document_text = f"**Grounds of Objection**  \n{str(row['ExplanatoryNote']).strip()}"

        # document_text = "\n\n".join([
        #     f"**Property Type**  \n{row['Team']}",
        #     f"**Development**  \n{row['DEV']}",
        #     f"**Strata Classification**  \n{strata}",
        #     f"**Grounds of Objection**  \n{str(row['ExplanatoryNote']).strip()}",
        #     f"**Number of Uploaded Files**  \n{row['FileUploadCount']}",
        #     f"**Reasoning**  \n{str(row['Reason']).strip()}",
        # ])

        #structure each document with relevant information
        documents.append(
            Document(
                page_content=document_text,
                #add metadata (excl from embedding) for filtering and/or retrieval
                metadata={
                    "Property Type": row["Team"],
                    "Development": row["DEV"],
                    "Strata Classification": strata,
                    "File Upload Count": int(row["FileUploadCount"]),
                    "Complexity": row["Category"],
                    "Reasoning": str(row["Reason"]).strip()
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

    print(f"✓ Past Objection vector database saved to {VECTOR_DB_PATH}")


if __name__ == "__main__":
    build_past_case_vectordb()