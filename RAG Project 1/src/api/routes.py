from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json

from retrieval.retriever import retrieve
from generation.prompt_builder import build_prompt
from generation.llm import LLM

from api.models import QuestionRequest


router = APIRouter()

llm = LLM()


@router.post("/chat")
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


    def event_generator():

        for token in llm.stream(prompt):

            payload = json.dumps({
                "type": "token",
                "content": token
            })

            yield f"data: {payload}\n\n"


        sources = [
            {
                "source": r["source"],
                "section": r["section"],
                "url": r["url"]
            }
            for r in results
        ]


        payload = json.dumps({
            "type": "sources",
            "content": sources
        })

        yield f"data: {payload}\n\n"


        yield "data: [DONE]\n\n"



    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )