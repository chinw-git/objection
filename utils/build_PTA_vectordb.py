from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
#from langchain_community.vectorstores import Chroma

import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

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
# Load PDF
# -----------------------------
print("Loading PTA PDF...")

loader = PyPDFLoader(file_path)

documents = loader.load()

print(f"Loaded {len(documents)} pages.")

# merge all extracted pages into a single document for chunking
all_text = "\n".join(doc.page_content for doc in documents)
merged_document = Document(page_content=all_text)

# -----------------------------
# Semantic Chunking
# -----------------------------
print("Chunking document...")

text_splitter = SemanticChunker(embedding_model)

chunks = text_splitter.split_documents([merged_document])

print(f"Created {len(chunks)} chunks.")

# -----------------------------
# Create Chroma Vector Store
# -----------------------------
print("Creating vector database...")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=VECTOR_DB_PATH,
    collection_name=COLLECTION_NAME,
)

print(f"Vector database saved to {VECTOR_DB_PATH}")