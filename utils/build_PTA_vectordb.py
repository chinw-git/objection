from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
#from langchain_community.vectorstores import Chroma

import os
import shutil

# -----------------------------
# Paths
# -----------------------------
file_path = "data/PropertyTaxAct.pdf"

VECTOR_DB_PATH = "vectordb/legislation"

COLLECTION_NAME = "property_tax_act"

# -----------------------------
# Embedding model
# -----------------------------
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# -----------------------------
# Builds (or rebuilds) the PTA vector database.
# -----------------------------
def build_PTA_vectordb(file_path: str = "data/PropertyTaxAct.pdf"):

    # Delete existing vector store
    if os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)

    # Load PDF
    print("Loading Property Tax Act PDF...")

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    print(f"✓ Loaded {len(documents)} pages.")

    ## merge all extracted pages into a single document for chunking
    all_text = "\n".join(doc.page_content for doc in documents)
    merged_document = Document(page_content=all_text)

    # Semantic Chunking
    print("Performing semantic chunking...")

    text_splitter = SemanticChunker(embedding_model)
    chunks = text_splitter.split_documents([merged_document])

    print(f"✓ Created {len(chunks)} semantic chunks.")

    # Create Chroma Vector Store
    print("Creating vector database...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=VECTOR_DB_PATH,
        collection_name=COLLECTION_NAME,
    )

    print(f"✓ Property Tax Act vector database saved to '{VECTOR_DB_PATH}'.")


if __name__ == "__main__":
    build_PTA_vectordb()