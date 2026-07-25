from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.exceptions import RetrievalError
from api.routes import router


app = FastAPI(
    title="Ancient Greece RAG API",
    description="Chat with Ancient Greece Wikipedia knowledge base"
)

@app.exception_handler(RetrievalError)
async def retrieval_error_handler(
    request: Request,
    exc: RetrievalError
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "retrieval_error",
            "message": str(exc)
        }
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


app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "Ancient Greece RAG API is running"
    }