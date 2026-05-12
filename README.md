# CineRAG — AI Cinema Expert Agent

A RAG (Retrieval-Augmented Generation) agent specialized in cinema.
Ask deep questions about films, directors, screenplays, and critiques
based on your own document collection.

## 💡 What it does

- Ingests screenplays, reviews, and articles about films
- Generates semantic embeddings and stores them in a vector database
- Answers complex questions grounded in your documents

> "What philosophical themes does Kubrick explore?"
> "Compare the narrative structure of Pulp Fiction and Memento."

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Embeddings | sentence-transformers (local, free) |
| Vector Store | ChromaDB |
| LLM | Groq (LLaMA 3) |
| Backend | FastAPI |
| Frontend | React + TypeScript |

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key" > .env

# Ingest documents
cd backend && python ingest.py

# Run the RAG pipeline
python rag.py
```

## Project Structure

```
cinerag/
├── backend/
│   ├── ingest.py   # Document ingestion + chunking
│   ├── rag.py      # RAG pipeline
│   └── main.py     # FastAPI server
├── docs/           # Your cinema documents
└── frontend/       # React interface
```