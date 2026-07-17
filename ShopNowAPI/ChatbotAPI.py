from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from ModelDeployment import generate_response
from ShopNowAIAssistat import generate_response_from_agents
from AISearch import getRelevantContentFromAISearch

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


# @app.options("/chat")
# async def chat_options(request: Request) -> Response:
#     origin = request.headers.get("origin", "http://localhost:3000")
#     response = Response(status_code=200)
#     response.headers["Access-Control-Allow-Origin"] = origin
#     response.headers["Access-Control-Allow-Credentials"] = "true"
#     response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type"
#     return response


def build_llm_prompt(query: str, docs: list[dict]) -> str:
    try:
        if not isinstance(docs, list):
            print("build_llm_prompt: docs is not a list, falling back to query-only prompt")
            docs = []

        if not docs:
            return f"User question: {query}"

        prompt_lines = [
            f"User question: {query}",
            "Retrieved documents:",
        ]

        for i, doc in enumerate(docs, start=1):
            title = doc.get("title", "Untitled")
            chunk = doc.get("chunk", "")
            prompt_lines.append(f"{i}) {title}\n{chunk}")

        prompt_lines.append("\nAnswer the user using only the retrieved documents.")
        return "\n\n".join(prompt_lines)
    except Exception as exc:
        print(f"build_llm_prompt failed: {exc}")
        return query


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        relevant_docs = getRelevantContentFromAISearch(request.message)
    except Exception as exc:
        print(f"Failed to get relevant content: {exc}")
        relevant_docs = []

    print(f"relevant_docs: {relevant_docs}")

    prompt = build_llm_prompt(request.message, relevant_docs)
    print(f"LLM prompt:\n{prompt}")

    try:
        reply = generate_response_from_agents(prompt)
    except Exception as exc:
        print(f"Failed to generate response from agent: {exc}")
        raise HTTPException(status_code=500, detail="Unable to generate chat response at this time")

    return ChatResponse(response=reply)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ChatbotAPI:app", host="0.0.0.0", port=8000, reload=True)
