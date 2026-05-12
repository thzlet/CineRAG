from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import load_rag_chain

app = FastAPI(title="CineRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chain = load_rag_chain()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.get("/")
def root():
    return {"status": "CineRAG online 🎬"}

@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    result = chain.invoke(request.question)
    return AnswerResponse(answer=result)