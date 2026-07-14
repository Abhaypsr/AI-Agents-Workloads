from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from ModelDeployment import generate_response
from ShopNowAIAssistat import generate_response_from_agents

app = FastAPI(title="Chatbot API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_origin_regex=r"http://localhost(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Chatbot API is running"}


@app.options("/chat")
async def chat_options(request: Request) -> Response:
    origin = request.headers.get("origin", "http://localhost:3000")
    response = Response(status_code=200)
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    reply = generate_response_from_agents(request.message)
    return ChatResponse(response=reply)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ChatbotAPI:app", host="0.0.0.0", port=8000, reload=True)
