from fastapi import FastAPI
from pydantic import BaseModel

from retrieval.retriever import retrieve
from generation.prompt_builder import build_prompt
from generation.llm import LLM
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse


app = FastAPI(
    title="Ancient Greece RAG API",
    description="Chat with Ancient Greece Wikipedia knowledge base"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = LLM()


class QuestionRequest(BaseModel):
    question: str

class Source(BaseModel):
    source: str
    section: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]

@app.get("/")
def home():

    return {
        "message": "Ancient Greece RAG API is running"
    }



@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: QuestionRequest):

    question = request.question


    results = retrieve(
        question,
        k=5
    )


    prompt = build_prompt(
        question,
        results
    )


    answer = llm.generate(prompt)

    return {
        "answer": answer,
        "sources": results
    }


    #return StreamingResponse(
    #llm.stream(prompt),
    #media_type="text/event-stream"
    #)