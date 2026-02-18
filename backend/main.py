from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import get_ai_response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = get_ai_response(req.message)
    return {"response": response}
@app.post("/chat-stream")
async def chat_stream(req: ChatRequest):

    def generate():
        text = get_ai_response(req.message)
        for word in text.split():
            yield word + " "

    return StreamingResponse(generate(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )