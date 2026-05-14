# CineRAG — AI Cinema Expert Agent

> Ask anything about films, directors and screenplays. CineRAG searches your documents and answers with depth.

<img width="934" height="836" alt="image" src="https://github.com/user-attachments/assets/b8138672-7a8b-4429-8d0f-65078df97332" />

## Example questions

- _"What philosophical themes does Kubrick explore in his films?"_
- _"Compare the narrative structure of Pulp Fiction and Memento"_
- _"Which directors influenced the visual style of Drive?"_

## Stack

| Layer | Technology |
|-------|-----------|
| Embeddings | sentence-transformers (local, free) |
| Vector Store | ChromaDB |
| LLM | LLaMA 3.3 via Groq |
| Backend | FastAPI + Python |
| Frontend | React + TypeScript + Vite |

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
