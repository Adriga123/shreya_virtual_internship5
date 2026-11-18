
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from knowledge_base import load_defects


# Project paths
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "chroma_db"

# Load historical bug records
print("Loading historical bug records...")
records = load_defects()

print("Total records:", len(records))

if not records:
    raise ValueError("No historical bug records found.")

# Load embedding model
print("\nLoading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Prepare documents and metadata
documents = []
metadatas = []
ids = []

for index, record in enumerate(records):

    title = str(record.get("title") or "")
    content = str(record.get("content") or "")
    resolution = str(record.get("resolution") or "")

    document = (
        f"Title: {title}\n"
        f"Description: {content}\n"
        f"Resolution: {resolution}"
    ).strip()

    documents.append(document)

    metadata = {}

    for field in [
        "bug_id",
        "project",
        "component",
        "chunk_type",
        "source_url"
    ]:
        value = record.get(field)

        if value is not None:
            metadata[field] = str(value)

    metadatas.append(metadata)

    record_id = record.get("chunk_id") or record.get("bug_id") or f"bug-{index}"
    ids.append(f"{record_id}-{index}")

# Generate embeddings
print("\nGenerating embeddings...")
embeddings = model.encode(
    documents,
    show_progress_bar=True
).tolist()

print("Embeddings generated:", len(embeddings))

# Initialize ChromaDB
client = chromadb.PersistentClient(path=str(DB_PATH))

# Rebuild this project's collection
try:
    client.delete_collection("bug_knowledge_base")
except Exception:
    pass

collection = client.create_collection(
    name="bug_knowledge_base",
    metadata={"description": "Historical software bug knowledge base"}
)

# Store records and embeddings
print("\nAdding records to ChromaDB...")

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

print("\nVECTOR DATABASE CREATED SUCCESSFULLY!")
print("Total indexed records:", collection.count())
print("Database location:", DB_PATH)
