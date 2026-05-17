# CineRAG: AI Cinema Expert Agent <img width="30" height="30" alt="image" src="https://github.com/user-attachments/assets/f1cbbf62-eab3-42b0-8352-a6f68cdc4892" />

> Ask anything about films, directors and screenplays. CineRAG searches your documents and answers with depth.
---

## How RAG Works

**Retrieval-Augmented Generation (RAG)** is an architecture that combines a retrieval system with a language model, allowing the LLM to answer questions grounded in a specific knowledge base — instead of relying solely on what it learned during training.

### The problem RAG solves

Large language models (LLMs) like LLaMA have a knowledge cutoff and no access to private or domain-specific documents. Without RAG, asking an LLM about a specific screenplay or a niche film analysis returns generic answers — or hallucinations. RAG solves this by giving the model real context at query time.

### Pipeline overview

```
User Query
    │
    ▼
┌─────────────────────┐
│   Embedding Model   │  ← Converts the query into a vector
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│     ChromaDB        │  ← Searches for the most similar document chunks
│   (Vector Store)    │     using cosine similarity
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Retrieved Chunks   │  ← The top-k most relevant passages from docs/
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│   Prompt Builder    │  ← Injects retrieved chunks into the LLM prompt
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  LLaMA 3.3 (Groq)   │  ← Generates the final answer using the context
└─────────────────────┘
    │
    ▼
  Response
```

### Step-by-step breakdown

**1. Ingestion (`ingest.py`)**

Before any query can be answered, documents must be processed and stored:

- Each `.txt` file in `docs/` is loaded and split into smaller **chunks** (overlapping text segments)
- Each chunk is converted into a **vector embedding** using `sentence-transformers` — a numerical representation that captures semantic meaning
- All embeddings are stored in **ChromaDB**, a local vector database

```
docs/roteiro-aftersun.txt
        │
        ▼
   Text Splitter         →  ["Charlotte Wells directed...", "The film explores grief...", ...]
        │
        ▼
  Embedding Model        →  [[0.23, -0.87, 0.41, ...], [0.11, 0.95, -0.33, ...], ...]
        │
        ▼
     ChromaDB            →  Stored with metadata (source file, chunk index)
```

**2. Retrieval**

When the user submits a question:

- The query is embedded using the same model as the ingestion step
- ChromaDB performs a **similarity search** — finding the chunks whose vectors are closest to the query vector
- The top-k chunks (by default, the most semantically similar) are retrieved

**3. Generation (`rag.py`)**

The retrieved chunks are injected into a structured prompt sent to the LLM:

```
System: You are a cinema expert. Answer based only on the context below.

Context:
[Chunk 1: "Aftersun is Charlotte Wells' debut feature..."]
[Chunk 2: "The film uses video camera footage to represent memory..."]

Question: Who directed Aftersun?
```

The LLM (LLaMA 3.3 via Groq) generates an answer **grounded in the retrieved documents**, reducing hallucinations and improving accuracy on domain-specific knowledge.

### Why local embeddings?

CineRAG uses `sentence-transformers` to generate embeddings locally — no API calls, no cost, no data leaving your machine. The model runs entirely on CPU/GPU during ingestion and retrieval.

### Key concepts

| Concept | Description |
|---|---|
| **Embedding** | A vector (list of numbers) representing the semantic meaning of a text |
| **Vector Store** | A database optimized for similarity search over embeddings |
| **Chunk** | A small segment of a document, typically 300–1000 tokens with overlap |
| **Similarity Search** | Finding vectors closest to a query vector using cosine or dot-product distance |
| **Context Window** | The maximum text an LLM can receive; RAG keeps it relevant by selecting only the top-k chunks |
| **Grounding** | Anchoring LLM responses to retrieved facts, reducing hallucinations |

---

## Stack

| Layer | Technology |
|-------|-----------|
| Embeddings | sentence-transformers (local, free) |
| Vector Store | ChromaDB |
| LLM | LLaMA 3.3 via Groq |
| Backend | FastAPI + Python |
| Frontend | React + TypeScript + Vite |

---

## How to run

### Backend

```bash
cd backend
pip install -r requirements.txt
python ingest.py   # ingest documents
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Access `http://localhost:5173`

---

## Structure

```
cinerag/
├── backend/
│   ├── ingest.py   # Ingestion + chunking + embeddings
│   ├── rag.py      # RAG pipeline with LangChain
│   └── main.py     # FastAPI server
├── docs/           # Ingested cinema documents
└── frontend/       # React interface
```

<img width="934" height="836" alt="image" src="https://github.com/user-attachments/assets/b8138672-7a8b-4429-8d0f-65078df97332" />
