"""
tasks/pta_embedding_task.py

Builds the Property Tax Act vector store from the source PDF.
Run this once (or whenever the source PDF changes) to populate vectordb/.
"""

from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

import os

# ---------------------------------------------------------
# Load environment variables — explicit path so this works
# regardless of which directory the script is run from
# ---------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY not found. Check that .env exists at the repo root "
        f"({ROOT_DIR / '.env'}) and contains OPENAI_API_KEY=sk-..."
    )

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
PDF_PATH = ROOT_DIR / "data" / "PropertyTaxAct.pdf"
VECTOR_DB_PATH = ROOT_DIR / "vectordb"
COLLECTION_NAME = "property_tax_act"

# ---------------------------------------------------------
# Embedding model
# ---------------------------------------------------------
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


def build_vectordb():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

    print(f"Loading PDF from {PDF_PATH}...")
    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()
    print(f"Loaded {len(documents)} pages.")

    print("Chunking with SemanticChunker (this calls the embeddings API per chunk boundary check)...")
    splitter = SemanticChunker(embedding_model)
    chunks = splitter.split_documents(documents)
    print(f"Produced {len(chunks)} semantic chunks.")

    print(f"Embedding and writing to Chroma at {VECTOR_DB_PATH} (collection: {COLLECTION_NAME})...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DB_PATH),
    )

    print(f"Done. Collection '{COLLECTION_NAME}' now has {vectordb._collection.count()} entries.")
    return vectordb


if __name__ == "__main__":
    build_vectordb()