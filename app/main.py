"""FastAPI application entry point."""

import json
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.agent.executor import get_agent
from app.models.schemas import ChatRequest, ChatResponse

app = FastAPI(
    title="Infomaniak Doc Assistant",
    description="AI assistant for Infomaniak documentation",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat endpoint that invokes the agent with the user's message."""
    agent = get_agent()

    # Use provided session_id or generate a new one
    session_id = request.session_id or str(uuid.uuid4())

    # Invoke agent with message and thread_id for memory
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": request.message}]},
        {"configurable": {"thread_id": session_id}},
    )

    # Extract the final answer from the agent response
    messages = response.get("messages", [])
    answer = ""
    sources: list[str] = []

    if messages:
        # Get the last AI message
        last_message = messages[-1]
        answer = last_message.content if hasattr(last_message, "content") else str(last_message)

        # Extract sources from tool messages
        for msg in messages:
            if hasattr(msg, "content") and "Source:" in str(msg.content):
                # Parse source URLs from tool responses
                content = str(msg.content)
                for line in content.split("\n"):
                    if line.strip().startswith("Source:"):
                        source = line.replace("Source:", "").strip()
                        if source and source not in sources:
                            sources.append(source)

    return ChatResponse(answer=answer, sources=sources)


def format_sse(data: dict) -> str:
    """Format data as a Server-Sent Event."""
    return f"data: {json.dumps(data)}\n\n"


async def sse_stream(message: str, session_id: str):
    """Generate SSE events from agent streaming response."""
    agent = get_agent()

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": message}]},
        {"configurable": {"thread_id": session_id}},
        version="v2",
    ):
        kind = event.get("event")
        # Stream AI message content tokens
        if kind == "on_chat_model_stream":
            content = event.get("data", {}).get("chunk")
            if content and hasattr(content, "content") and content.content:
                yield format_sse({"token": content.content})

    yield format_sse({"done": True})


@app.get("/chat/stream")
async def chat_stream(message: str, session_id: str | None = None) -> StreamingResponse:
    """Streaming chat endpoint using Server-Sent Events."""
    sid = session_id or str(uuid.uuid4())
    return StreamingResponse(
        sse_stream(message, sid),
        media_type="text/event-stream",
    )
