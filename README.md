# Gemini RAG Classifier — README

## 1. Short Project Summary
Gemini_Application_Checker_RAG is a Retrieval-Augmented Generation (RAG) application that inspects software project repositories to help reviewers quickly understand a candidate’s work and technical depth. It ingests project README files, builds a searchable knowledge base, and answers questions with grounded, cited responses. This solves the “project inspection” problem for recruiters and engineers by turning scattered repository documentation into a reliable, queryable evaluation surface. The system implements RAG by retrieving relevant README snippets and using them to generate concise, evidence-backed answers. Outputs are structured responses that include citations pointing to the exact README chunks used.

## 2. Technical Overview
### Ingestion (README-first)
The ingestion pipeline treats README files as the primary knowledge objects. This prioritization is deliberate: READMEs encode author-intent, high-level architecture, and usage details that are most useful for evaluation, while raw source code is verbose and context-heavy. By focusing on READMEs, the system captures the most recruiter-relevant signal with lower indexing cost and clearer grounding.

### Chunking Strategy
README content is split into semantically meaningful sections (e.g., headings and paragraph blocks). Each chunk is stored with metadata such as project name, file path, and section title. This provides context for retrieval and enables precise citations in the final response.

### Embeddings
Each chunk is converted into a vector representation using a local embedding model. Local embeddings keep costs predictable, remove dependency on external APIs, and allow reproducible indexing. Embeddings are generated once per corpus update and cached for reuse.

### Indexing & Retrieval (FAISS)
All embeddings are stored in a FAISS index for fast similarity search. When a user asks a question, the query is embedded with the same model and used to retrieve the top-k most similar chunks. This yields grounded context for the generator.

### Prompt Construction & Grounding
Retrieved chunks are inserted into a prompt template that instructs the LLM to answer only using the provided context. The prompt explicitly demands grounded responses and disallows unsupported claims.

### Citations Enforcement
Citations are enforced by attaching chunk identifiers to each retrieved passage and requiring the model to reference those identifiers in its output. This ensures traceability back to the original README text and reduces hallucination risk.

## 3. Folder Structure (Core Section)
```
Gemini_Application_Checker_RAG/
├── app/                 # UI layer for querying the RAG system
├── rag/                 # Core RAG logic
│   ├── ingestion/       # README ingestion and chunking
│   ├── indexing/        # Embedding + FAISS index build
│   ├── retrieval/       # Query embedding + top-k retrieval
│   └── prompting/       # Prompt templates + grounding rules
├── projects/            # Project README corpus to index
├── build_index.py       # Orchestrates ingestion + indexing
├── config.py            # Central configuration (models, paths)
└── requirements.txt     # Dependencies
```

**Ingestion:** `rag/ingestion/` reads README files from `projects/`, parses headings/sections, and emits chunk objects with metadata.

**Indexing:** `rag/indexing/` embeds chunks and stores them in a FAISS index; `build_index.py` orchestrates the process.

**Retrieval:** `rag/retrieval/` embeds the query and fetches the top-k chunks from FAISS.

**Prompting:** `rag/prompting/` builds a grounded prompt that includes retrieved chunks and citation rules.

**UI:** `app/` exposes an interface for asking questions and receiving cited answers.

## 4. Engineering & Design Decisions
- **Why FAISS?** It is a fast, mature vector index with excellent performance for approximate nearest-neighbor search and integrates easily with Python pipelines.
- **Why local embeddings?** Local embedding models reduce cost, avoid API dependency, and allow repeatable evaluation of candidate projects.
- **Why modular separation?** Ingestion, indexing, retrieval, and prompting are isolated for easy replacement or extension (e.g., swapping embedding models, adding new chunkers, or changing prompt constraints).
- **Limitations:**
  - **Hallucination control:** The system relies on prompt constraints and citations, but model behavior can still drift if context is weak.
  - **Scale:** A README-first corpus is small and efficient, but very large project sets may require sharding or distributed indexing.
  - **Context coverage:** README-only ingestion omits low-level implementation details that may matter for deeper technical review.

## 5. What This Project Demonstrates
- **RAG literacy:** Clear separation of retrieval and generation, grounded responses, and citation enforcement.
- **System architecture:** A modular pipeline that mirrors production RAG systems (ingest → embed → index → retrieve → generate).
- **ML + software integration:** Practical use of embeddings, vector search, and prompt engineering to solve a real evaluation problem.
