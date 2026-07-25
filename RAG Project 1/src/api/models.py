from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str
    section: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]