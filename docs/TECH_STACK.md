# Technology Stack

| Layer | Selected technology | Use |
|---|---|---|
| UI | Streamlit | Bug submission and diagnosis display |
| Programming language | Python | Backend logic and agents |
| PDF parsing | PyMuPDF | Extract text from PDF attachments |
| Structured persistence | SQLite | Store submitted bug reports |
| Historical sample store | JSON Lines | Store sample defect records |
| Text retrieval | scikit-learn TF-IDF | Convert text to sparse feature vectors |
| Similarity | Cosine similarity | Rank related historical examples |
| Architecture documentation | Mermaid | Render system flow diagram |
| Version control | Git and GitHub | Track and submit project work |

## Planned extensions (not yet implemented)
- Sentence Transformers (`all-MiniLM-L6-v2`) for dense semantic embeddings
- ChromaDB for persistent vector storage and metadata filtering
- FastAPI for a separated backend API
- An approved LLM API for evidence-grounded diagnosis and fix suggestions
- Curated Mozilla, Apache, and Eclipse issue datasets
