
# M1.4 – Historical Defect Knowledge Base

## 1. Overview

The Historical Defect Knowledge Base stores previously reported software bugs and allows the system to retrieve similar defects using semantic search.

It supports the Retrieval-Augmented Generation (RAG) approach planned for the Intelligent Bug Diagnosis Platform.

## 2. Dataset Sources

The project uses three public sources and five illustrative sample records.

| Source | Records |
|---|---:|
| Mozilla Bugzilla | 20 |
| Apache Hadoop Jira | 20 |
| Eclipse Platform GitHub Issues | 18 |
| Illustrative sample records | 5 |
| **Total** | **63** |

Note: Eclipse records were collected from the official Eclipse Platform GitHub repository because Eclipse Bugzilla was unavailable.

The five sample records are illustrative examples, not real public bug reports.

## 3. Data Collection

Python scripts were developed to collect bug reports from the public sources.

The collected data includes available fields such as:
- Bug ID
- Title
- Description
- Comments
- Project
- Component
- Priority
- Status
- Resolution
- Source URL

The available fields vary depending on the source.

## 4. Data Cleaning and Standardisation

Separate cleaning scripts were implemented for each dataset.

Files:
- `src/clean_mozilla_bugs.py`
- `src/clean_apache_bugs.py`
- `src/clean_eclipse_bugs.py`

The cleaning process includes:
- Removing unnecessary whitespace.
- Standardising text fields.
- Extracting relevant bug information.
- Combining titles, descriptions and available comments.
- Creating a common content field for retrieval.
- Saving the cleaned records in JSONL format.

Processed files:
- `data/processed/mozilla_cleaned.jsonl`
- `data/processed/apache_cleaned.jsonl`
- `data/processed/eclipse_cleaned.jsonl`

## 5. Knowledge Base Integration

The `src/knowledge_base.py` module loads the cleaned datasets and illustrative sample records.

All records are combined into a single collection for further processing.

Verified total: **63 historical defect records**.

## 6. Embedding Generation

The Sentence Transformers model `all-MiniLM-L6-v2` is used to generate vector embeddings.

Each historical bug record is converted into a numerical representation based on its textual content.

These embeddings enable semantic similarity search.

## 7. Vector Database

ChromaDB is used as the persistent vector database.

Implementation file:
`src/build_vector_db.py`

Collection name:
`bug_knowledge_base`

Database location:
`data/chroma_db`

The database stores:
- Bug document content
- Vector embeddings
- Bug identifiers
- Project information
- Component information
- Source URLs

A total of 63 records were successfully indexed.

## 8. Semantic Retrieval

The `src/test_vector_search.py` module tests semantic retrieval.

The process:
1. Accepts a natural-language bug query.
2. Generates an embedding for the query.
3. Searches the ChromaDB collection.
4. Retrieves the five closest historical records.
5. Displays bug IDs, project information, document content and distances.

Lower distance indicates greater similarity for the configured ChromaDB distance metric.

## 9. Testing and Observations

### Test 1 – Apache Hadoop

Query:
"Hadoop slow RPC logging should include user information and caller context"

Observation:
The search retrieved HADOOP-20085 as the first result. HADOOP-20082 also appeared among the top three results.

This indicated relevant retrieval for the Hadoop query.

### Test 2 – Mozilla Firefox

Query:
"Firefox browser crashes when opening a new tab"

Observation:
The search returned some unrelated historical records, including a result about Firefox file handling and another about the Ctrl-Q exit shortcut.

This demonstrated that retrieval relevance is not consistent across all queries.

## 10. Limitations

- The knowledge base currently contains a limited number of records.
- Some historical reports have incomplete descriptions or missing metadata.
- The Eclipse dataset uses GitHub Issues rather than Bugzilla.
- Five sample records are illustrative rather than real historical defects.
- Semantic retrieval can return unrelated records.
- Retrieval quality requires further evaluation and improvement.
- The current implementation retrieves similar defects but does not independently establish the actual root cause.

## 11. Conclusion

The Historical Defect Knowledge Base was implemented using public software bug reports, data cleaning scripts, Sentence Transformers embeddings and ChromaDB.

A total of 63 records were successfully loaded and indexed.

Semantic retrieval was tested using Apache Hadoop and Mozilla Firefox queries. The results demonstrated that the vector search pipeline works, while also identifying retrieval relevance as an area for future improvement.
