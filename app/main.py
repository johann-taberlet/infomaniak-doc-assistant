"""FastAPI application entry point."""

import json
import logging
import time
import uuid
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.agent.executor import get_agent
from app.agent.tools import collect_all_segments, reset_context
from app.models.schemas import ChatRequest, ChatResponse
from app.observability.langfuse import get_langfuse_handler

logger = logging.getLogger(__name__)

# Configure file logging for timeline analysis
_timeline_logger = logging.getLogger("timeline")
_timeline_logger.setLevel(logging.INFO)
_timeline_handler = logging.FileHandler("/tmp/agent_timeline.log", mode="a")
_timeline_handler.setFormatter(logging.Formatter("%(message)s"))
_timeline_logger.addHandler(_timeline_handler)

# Simple in-memory metrics
# PRODUCTION: Use asyncio.Lock for thread-safety, or prometheus_client for proper metrics
metrics = {
    "request_count": 0,
    "error_count": 0,
}

app = FastAPI(
    title="Infomaniak Doc Assistant",
    description="AI assistant for Infomaniak documentation",
    version="0.1.0",
)

# CORS middleware
# PRODUCTION: Restrict allow_origins to specific domains (e.g., ["https://app.infomaniak.com"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# PRODUCTION: Add rate limiting with slowapi or fastapi-limiter to prevent abuse

# Mount static files (absolute path for portability)
STATIC_DIR = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors with 400 status."""
    logger.error("Validation error: %s", exc.errors())
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors with 500 status."""
    logger.error("Internal error: %s", str(exc))
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/metrics")
async def get_metrics() -> dict[str, int]:
    """Return application metrics."""
    return metrics


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat endpoint that invokes the agent with the user's message."""
    metrics["request_count"] += 1

    try:
        agent = get_agent()

        # Use provided session_id or generate a new one
        session_id = request.session_id or str(uuid.uuid4())

        # Build config with optional Langfuse observability
        config: dict[str, Any] = {"configurable": {"thread_id": session_id}}
        langfuse_handler = get_langfuse_handler()
        if langfuse_handler:
            config["callbacks"] = [langfuse_handler]

        # Invoke agent with message and thread_id for memory
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config,
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
    except Exception:
        metrics["error_count"] += 1
        raise


def format_sse(data: dict[str, Any]) -> str:
    """Format data as a Server-Sent Event."""
    return f"data: {json.dumps(data)}\n\n"


async def sse_stream(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Generate SSE events from agent streaming response.

    Emits segments after all tools complete:
    - segment: Each content segment (text or component) with order
    - error: Signal that an error occurred with a user-friendly message
    - done: Signal that streaming is complete, includes language
    """
    try:
        agent = get_agent()

        # Reset context for this request
        reset_context()

        # Build config with optional Langfuse observability
        config: dict[str, Any] = {"configurable": {"thread_id": session_id}}
        langfuse_handler = get_langfuse_handler()
        if langfuse_handler:
            config["callbacks"] = [langfuse_handler]

        # Track state for status updates
        llm_call_count = 0
        search_completed = False
        last_status: str | None = None

        def make_status(status: str) -> str | None:
            """Only emit status if it changed."""
            nonlocal last_status
            if status != last_status:
                last_status = status
                return format_sse({"status": status})
            return None

        async for event in agent.astream_events(
            {"messages": [{"role": "user", "content": message}]},
            config,
            version="v2",
        ):
            event_kind = event.get("event", "unknown")
            event_name = event.get("name", "")

            # Emit status updates based on actual events
            if event_kind == "on_chat_model_start":
                llm_call_count += 1
                if llm_call_count == 1:
                    # First LLM call - understanding the question
                    if status_event := make_status("Understanding your question..."):
                        yield status_event
                elif search_completed:
                    # LLM call after search - generating response
                    if status_event := make_status("Generating response..."):
                        yield status_event

            elif event_kind == "on_tool_start" and event_name == "search_docs":
                if status_event := make_status("Searching documentation..."):
                    yield status_event

            elif event_kind == "on_tool_end" and event_name == "search_docs":
                search_completed = True
                if status_event := make_status("Found relevant documents"):
                    yield status_event

        # Collect all segments, sources, and language
        segments, sources, language = collect_all_segments()

        # Emit each segment in order
        for segment in segments:
            yield format_sse({"segment": segment})

        # Emit sources as final segment (no order, always last)
        if sources:
            yield format_sse({
                "segment": {
                    "type": "source_cards",
                    "id": str(uuid.uuid4()),
                    "sources": sources,
                }
            })

        # Send done event with language
        done_data: dict[str, Any] = {"done": True}
        if language:
            done_data["language"] = language
        yield format_sse(done_data)

    except Exception as e:
        # Log the full error for debugging
        logger.exception("Error during SSE stream: %s", str(e))
        metrics["error_count"] += 1

        # Send user-friendly error message
        error_message = "Sorry, an error occurred while processing your request. Please try again."

        # Include more specific message for known error types
        error_str = str(e).lower()
        if "parsing failed" in error_str or "could not be parsed" in error_str:
            error_message = "The AI model had trouble generating a response. Please try rephrasing your question."
        elif "rate limit" in error_str:
            error_message = "Too many requests. Please wait a moment and try again."
        elif "timeout" in error_str:
            error_message = "The request timed out. Please try again."

        logger.info("Sending error event to client: %s", error_message)
        yield format_sse({"error": error_message})


@app.get("/chat/stream")
async def chat_stream(message: str, session_id: str | None = None) -> StreamingResponse:
    """Streaming chat endpoint using Server-Sent Events."""
    sid = session_id or str(uuid.uuid4())
    return StreamingResponse(
        sse_stream(message, sid),
        media_type="text/event-stream",
    )
