M1.1 – Research and Technical Understanding
Project: Creation of Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance
1. Purpose of this research
The purpose of this study is to understand how software bugs are reported and investigated, and how information retrieval and language-processing techniques can help developers find related defects and possible fixes.

The proposed platform accepts a new bug report, searches previously reported defects, analyses the available information and presents findings that can help a developer investigate the problem.
2. Software defect analysis workflow
A software defect is an error or problem in a software application that causes it to behave incorrectly or unexpectedly.

A typical defect-analysis workflow contains these stages:
1. Bug reporting: A user or tester reports the problem with a title, description, steps to reproduce it, expected behaviour and actual behaviour.
2. Initial review and triage: The report is checked, categorised and assigned a priority so the team can decide how urgently it should be handled.
3. Log and evidence analysis: Developers examine stack traces, error messages, logs, screenshots and reproduction steps.
4. Duplicate checking: The team checks whether the same or a closely related issue has already been reported.
5. Investigation and root-cause analysis: Developers inspect the code, environment and related reports to identify the likely cause.
6. Fix and verification: A correction is made and tested to confirm that the issue is resolved.
7. Closure and documentation: The report is updated with the resolution and relevant information for future reference.
How this applies to this project
The platform is intended to support the early investigation stages. It collects bug details, performs initial triage, analyses logs, searches for similar historical reports and suggests possible causes and remedies. The final decision and verification remain with the developer.
3. Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation, commonly called RAG, combines an information-retrieval step with a language-generation step.

A normal language model generates an answer using information learned during training and the prompt supplied by the user. In a RAG system, the application first searches an external knowledge source for relevant information. The retrieved information is then supplied to the language model as context for generating an answer.
Basic RAG workflow
1. Prepare a collection of reference documents.
2. Divide long documents into smaller, meaningful chunks.
3. Convert the chunks into embeddings.
4. Store the embeddings and their metadata in a searchable index or vector database.
5. Convert a new user query into an embedding.
6. Retrieve the most relevant chunks.
7. Provide the query and retrieved context to the language model.
8. Generate an answer grounded in the retrieved information.
How RAG applies to bug diagnosis
When a developer submits a new bug report, the system can search historical bug reports for related symptoms, stack traces, discussions and resolutions. The retrieved reports can provide useful context for the diagnosis and fix suggestions.

RAG does not guarantee that an answer is correct. Retrieved information may be incomplete or unrelated, so the system should show the supporting reports and the developer should verify suggestions.

Research reference: Lewis et al. introduced RAG as an approach combining a pre-trained generator with retrieved external knowledge. See the reference list.
4. Semantic similarity and embeddings
Two bug reports may describe the same underlying problem using different words. A simple keyword search may fail to connect them.

For example:
- Report A: “Application crashes when the user signs in.”
- Report B: “Login causes the program to terminate unexpectedly.”
The wording is different, but the meaning is similar.

Semantic similarity is the process of estimating how close two pieces of text are in meaning.

An embedding is a numerical representation of text. An embedding model converts a sentence or document into a list of numbers (a vector). Texts with related meanings may have vectors that are close to one another in the embedding space.

A common similarity measure is cosine similarity. It compares the direction of two vectors. A higher score generally indicates greater similarity for models designed for this task. The score should not automatically be treated as a probability or as proof that two bugs are duplicates.
Proposed approach
The proposed technology stack lists Sentence Transformers with the all-MiniLM-L6-v2 model to create text embeddings. The system can compare a new report with historical bug-report chunks and return the most relevant matches.

The current prototype uses a lightweight, locally implemented TF-IDF-style word and bigram similarity method. It does not currently generate dense Sentence Transformer embeddings.
5. Vector search and vector databases
A vector database stores vector representations together with information about the original records. It provides a way to search for vectors that are close to a query vector.

For this project, a historical bug record could contain:
- Bug or issue ID
- Title
- Description
- Stack trace or error details
- Comments
- Resolution
- Source project
- URL or source reference
- Embedding for the relevant text chunk
When a new report is submitted, its embedding can be compared with stored embeddings. The system can retrieve the closest matching records and show their titles, source details and resolutions.
Proposed technology
The proposed technology stack identifies ChromaDB as the vector database. It is intended to store embeddings and metadata and support semantic retrieval.

The current prototype does not yet use ChromaDB. Its initial retrieval module compares text against a small local JSONL sample using a lightweight TF-IDF-style method.
6. Historical bug-report sources and preparation
Historical defect reports are useful because they contain examples of real software problems, discussions and resolutions. The project identifies Mozilla, Apache and Eclipse as potential sources.
- Mozilla: Bugzilla provides a REST API that can be used to access bug records from supported Bugzilla installations. The Mozilla Bugzilla REST API documentation describes this interface.
- Apache: Apache projects use issue-tracking systems, including Jira for many projects. Relevant project issues can be examined for titles, descriptions, comments, status and resolution, subject to the source's access and usage conditions.
- Eclipse: Eclipse project issue trackers provide historical issue information that can be studied for defect descriptions, discussions and resolutions. The available fields and access method depend on the tracker used by the project.
Proposed data preparation process
1. Select relevant projects and define which issue fields are needed.
2. Collect records using the source's permitted API or export facility.
3. Keep the original issue ID and source reference so each record can be traced.
4. Remove empty, irrelevant or unusable records.
5. Standardise field names and text formats.
6. Separate long reports into meaningful chunks, such as description, stack trace, discussion and resolution.
7. Generate embeddings for the chunks.
8. Store the vectors and metadata in the vector database.
9. Test retrieval with sample bug reports and manually check whether the returned records are relevant.
The project should record the source and collection date for each dataset. Public availability does not automatically mean that every record can be copied or redistributed without restrictions; source terms and project policies should be checked.

Current data status: The prototype's bundled historical_defects.jsonl contains illustrative sample records. These should not be described as downloaded Mozilla, Apache or Eclipse records. Collection and preparation of real historical records remains a planned task.
7. Proposed technology choices
The following choices are based on the project's proposed technology stack. The purpose column explains how each technology fits into the design.
Area	Proposed technology	Intended use
Programming language	Python	Main application logic and text processing
User interface	Streamlit	Bug-report form and results display
Backend / API	FastAPI	API endpoints and communication between interface and processing modules
Data processing	Pandas and Python text-processing libraries	Cleaning and preparing bug reports and datasets
Embedding model	Sentence Transformers (all-MiniLM-L6-v2)	Converting report text into dense vector embeddings
Vector database	ChromaDB	Storing embeddings and retrieving similar historical chunks
RAG framework	LangChain	Connecting retrieval results to the language-model workflow
Language model	Google Gemini API	Generating explanations and fix suggestions using the report and retrieved context
Submission database	SQLite	Storing submitted reports and processing information during initial development
Version control	Git and GitHub	Tracking changes and hosting the source code


Implementation note
This table records the proposed design, not a claim that every technology is already integrated. The current prototype uses Streamlit, SQLite, local JSONL sample records, lightweight custom text similarity and provisional rule-based agent functions. FastAPI, dense Sentence Transformer embeddings, ChromaDB, LangChain and Gemini API integration are not yet part of the verified prototype.
8. Summary
This research identifies the main ideas needed for the proposed platform:
- Defect analysis provides the workflow for reviewing and resolving software problems.
- RAG can bring relevant historical bug information into the diagnosis process.
- Embeddings and semantic similarity can help find reports that describe similar problems in different words.
- Vector search can retrieve relevant historical bug-report chunks efficiently.
- Mozilla, Apache and Eclipse issue trackers are potential sources of historical defect information.
The next implementation work is to collect real historical defect records, prepare and chunk the data, generate embeddings, build the vector index and evaluate retrieval quality. The platform's suggestions should support developer investigation rather than replace developer verification.
References
1. Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. https://arxiv.org/abs/2005.11401
2. Sentence Transformers documentation. Semantic Textual Similarity. https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html
3. Sentence Transformers documentation. Usage. https://sbert.net/docs/sentence_transformer/usage/usage.html
4. Mozilla Wiki. Bugzilla: REST API. https://wiki.mozilla.org/Bugzilla:REST_API