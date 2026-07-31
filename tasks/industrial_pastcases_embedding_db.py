"""
tasks/industrial_pastcases_embedding_db.py

Builds a vector store of past classified objection cases from pastcases.xlsx.
Each case is embedded on its ExplanatoryNote, with Category/Reason/etc as metadata.
"""

from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(f"OPENAI_API_KEY not found. Check .env at {ROOT_DIR / '.env'}")

EXCEL_PATH = ROOT_DIR / "data" / "pastcases.xlsx"
VECTOR_DB_PATH = str(ROOT_DIR / "db" / "chroma")
COLLECTION_NAME = "property_objections"
EMBEDDING_MODEL = "text-embedding-3-large"


def build_pastcases_vectordb():
    print(f"Loading {EXCEL_PATH}...")
    df = pd.read_excel(EXCEL_PATH)
    print(f"Loaded {len(df)} past cases.")

    df = df.dropna(subset=["ExplanatoryNote"])
    print(f"{len(df)} rows have valid ExplanatoryNote.")

    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=EMBEDDING_MODEL,
    )

    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    documents = df["ExplanatoryNote"].astype(str).tolist()
    ids = [f"case_{i}" for i in range(len(df))]

    metadatas = []
    for _, row in df.iterrows():
        metadatas.append({
            "category": str(row.get("Category", "")),
            "reason": str(row.get("Reason", "")),
            "file_upload_count": float(row.get("FileUploadCount", 0)),
            "is_strata": bool(row.get("IS_STRATA", 0)),
            "dev": str(row.get("DEV", "")),
            "done": bool(row.get("Done", False)),
        })

    print(f"Embedding {len(documents)} cases with {EMBEDDING_MODEL}...")
    collection.add(documents=documents, metadatas=metadatas, ids=ids)

    print(f"Done. Collection '{COLLECTION_NAME}' now has {collection.count()} entries.")


if __name__ == "__main__":
    build_pastcases_vectordb()