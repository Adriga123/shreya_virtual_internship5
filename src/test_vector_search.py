
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "chroma_db"

# Connect to existing database
client = chromadb.PersistentClient(path=str(DB_PATH))
collection = client.get_collection("bug_knowledge_base")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Test bug description
query = "Firefox crashes when network connection times out"

# Convert query into embedding
query_embedding = model.encode(query).tolist()

# Search for similar historical bugs
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("\nSEMANTIC SEARCH RESULTS")
print("=" * 50)

for i in range(len(results["ids"][0])):
    print(f"\nResult {i + 1}")
    print("Bug ID:", results["metadatas"][0][i].get("bug_id"))
    print("Project:", results["metadatas"][0][i].get("project"))
    print("Title:", results["documents"][0][i])
    print("Distance:", results["distances"][0][i])
