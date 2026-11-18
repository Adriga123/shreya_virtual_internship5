# System Architecture — Milestone 1

## 1. Purpose
The platform accepts a software bug report, validates and stores it, retrieves similar historical examples, and passes the report through five logical diagnostic agents to produce structured debugging guidance.

## 2. End-to-end workflow
1. **Submission:** user enters a title, description, stack trace, and error logs, or uploads a supported text/PDF file.
2. **Validation and extraction:** title and description are required; supported attachment text is extracted.
3. **Persistence:** report metadata and text are stored in SQLite.
4. **Knowledge retrieval:** the report text is compared with historical examples using TF-IDF vectors and cosine similarity.
5. **Orchestration:** the orchestrator invokes Triage, Log Analysis, Duplicate Detection, Root Cause, and Remediation modules in sequence.
6. **Presentation:** the UI displays category, provisional priority, log clues, similar examples, hypotheses, and recommended debugging steps.

## 3. Agent responsibilities
| Agent | Responsibility | Output |
|---|---|---|
| Triage | Classify broad issue category and provisional priority | category, priority |
| Log Analysis | Identify exception names, HTTP codes, and recognizable error clues | detected clues |
| Duplicate Detection | Present the closest retrieved historical examples | ranked similar defects |
| Root Cause | Form cautious hypotheses based on report evidence and retrieved examples | hypotheses |
| Remediation | Suggest practical debugging and verification steps | recommended actions |

These are logical modules in one Python application, coordinated by an orchestrator. They are not five independently deployed services.

## 4. Data model

### Submitted bug report
| Field | Meaning |
|---|---|
| bug_id | UUID for the report |
| title | Short issue title |
| description | User's description and reproduction context |
| stack_trace | Optional stack trace |
| error_logs | Optional logs and extracted attachment text |
| attachment_name | Optional original filename |
| status | Submission/diagnosis state |
| category | Provisional category |
| priority | Provisional priority |
| created_at | UTC creation timestamp |

### Historical defect record
| Field | Meaning |
|---|---|
| chunk_id | Unique record/chunk identifier |
| bug_id | Source issue identifier |
| project | Source project label |
| component | Affected component |
| title | Short defect title |
| content | Text used for retrieval |
| chunk_type | Description, stack trace, comment, or resolution |
| resolution | Resolution summary |
| source_url | Source issue URL, when available |

## 5. Knowledge-base preparation
The current demo reads JSONL records from `data/sample/historical_defects.jsonl`. The retrieval module combines title, content, component, and resolution into searchable text. TF-IDF converts these records into sparse vectors; cosine similarity ranks records against a submitted report.

For the full research implementation, collect public issue records from Mozilla, Apache, and Eclipse; preserve source URLs and licences/terms; normalize fields; remove duplicates and noise; split long descriptions, comments, logs, and resolutions into meaningful chunks; generate dense embeddings; and persist vectors plus metadata in a vector database such as ChromaDB.

## 6. Architecture limitations and next steps
- Replace illustrative sample records with verified public issue data.
- Add robust preprocessing, chunking, and dataset provenance.
- Evaluate retrieval with a labelled query set and ranking metrics.
- Add dense Sentence Transformers embeddings and ChromaDB.
- Add an approved LLM provider for evidence-grounded reasoning only after configuration.
- Add tests, error handling, authentication, privacy controls, and deployment hardening.

The current prototype demonstrates the workflow; it does not claim production-grade diagnosis or measured model accuracy.
