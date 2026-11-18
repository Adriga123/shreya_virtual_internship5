# Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance
## Milestone 1 implementation package

This repository contains a runnable prototype for bug submission, historical-example retrieval, and a five-stage diagnostic workflow.

### Included
- Streamlit bug-report submission interface
- Direct text entry for descriptions, stack traces, and logs
- `.txt`, `.log`, `.md`, and `.pdf` attachment support
- SQLite storage for submitted reports
- Local JSONL historical-defect sample collection
- TF-IDF + cosine-similarity retrieval
- Five logical agents coordinated by one orchestrator
- Architecture diagram, technical stack, schemas, and milestone checklist

### Run on Windows
Open a terminal in the project root and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run src/app.py
```

If PowerShell blocks activation, run this once in that terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Important scope note
The included historical examples are synthetic demonstrations, not official Mozilla, Apache, or Eclipse issue records. The current retrieval baseline uses TF-IDF rather than dense embeddings. The five agents are transparent rule-based Python modules, not autonomous LLM agents. Official dataset ingestion, dense embeddings, ChromaDB, and LLM integration are documented as next implementation steps and must not be reported as completed until implemented and tested.
