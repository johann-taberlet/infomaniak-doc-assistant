"""FastAPI application entry point."""

import json
import logging
import re
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
from app.agent.tools import ALL_TOOLS, get_pending_ui_components
from app.models.schemas import ChatRequest, ChatResponse

# Tool names for filtering out tool call text from stream
TOOL_NAMES = {tool.name for tool in ALL_TOOLS}
from app.observability.langfuse import get_langfuse_handler

logger = logging.getLogger(__name__)

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




def extract_language(text: str) -> tuple[str, str | None]:
    """Extract language marker from end of text and return (cleaned_text, language)."""
    # Match [LANG:xx] at the end of text (with possible trailing whitespace)
    match = re.search(r"\[LANG:(\w{2})\]\s*$", text)
    if match:
        lang = match.group(1).lower()
        cleaned = text[: match.start()].rstrip()
        return cleaned, lang
    return text, None


async def sse_stream(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Generate SSE events from agent streaming response.

    Emits three types of events:
    - token: Streamed text tokens from the LLM
    - ui_component: Rich UI components (SourceCards, StepGuide, etc.)
    - done: Signal that streaming is complete, with optional language code
    """
    # PRODUCTION: Wrap in try/except to send error event on failure instead of silent disconnect
    agent = get_agent()

    # Clear any stale UI components from previous requests
    get_pending_ui_components()

    # Build config with optional Langfuse observability
    config: dict[str, Any] = {"configurable": {"thread_id": session_id}}
    langfuse_handler = get_langfuse_handler()
    if langfuse_handler:
        config["callbacks"] = [langfuse_handler]

    # Accumulate full response to extract language marker at the end
    full_response = ""
    # Buffer to detect tool calls that arrive in chunks
    pending_buffer = ""
    # Track when we're in tool execution to skip streaming tool call content
    in_tool_call = False

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": message}]},
        config,
        version="v2",
    ):
        kind = event.get("event")

        # Track tool execution state
        if kind == "on_tool_start":
            in_tool_call = True
            pending_buffer = ""  # Discard any buffered tool call text
            continue

        if kind == "on_tool_end":
            in_tool_call = False
            # Emit any pending UI components
            for component in get_pending_ui_components():
                component_dict = component.model_dump()
                yield format_sse({"ui_component": component_dict})
            continue

        # Stream AI message content tokens (skip during tool calls)
        if kind == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk:
                # Skip if this is a tool call chunk
                if hasattr(chunk, "tool_call_chunks") and chunk.tool_call_chunks:
                    in_tool_call = True
                    pending_buffer = ""
                    continue
                # Skip if we're in the middle of tool execution
                if in_tool_call:
                    continue
                # Only stream actual text content
                if hasattr(chunk, "content") and chunk.content:
                    content = chunk.content
                    pending_buffer += content

                    # Check if buffer looks like start of a tool call
                    # Pattern: tool_name{ or tool_name(
                    buffer_stripped = pending_buffer.strip()
                    is_tool_call_start = False
                    for name in TOOL_NAMES:
                        if buffer_stripped.startswith(name):
                            # Could be a tool call, wait for more or detect completion
                            if name + "{" in buffer_stripped or name + "(" in buffer_stripped:
                                # Definitely a tool call
                                in_tool_call = True
                                pending_buffer = ""
                                is_tool_call_start = True
                                break
                            elif len(buffer_stripped) <= len(name) + 5:
                                # Still accumulating, might be tool call
                                is_tool_call_start = True
                                break

                    if is_tool_call_start:
                        continue

                    # Not a tool call, flush buffer
                    if pending_buffer:
                        full_response += pending_buffer
                        yield format_sse({"token": pending_buffer})
                        pending_buffer = ""

    # Flush any remaining buffer (shouldn't normally have content)
    if pending_buffer and not in_tool_call:
        full_response += pending_buffer
        yield format_sse({"token": pending_buffer})

    # Extract language from accumulated response
    _, language = extract_language(full_response)

    # Send done event with language if detected
    done_data: dict[str, Any] = {"done": True}
    if language:
        done_data["language"] = language
    yield format_sse(done_data)


@app.get("/chat/stream")
async def chat_stream(message: str, session_id: str | None = None) -> StreamingResponse:
    """Streaming chat endpoint using Server-Sent Events."""
    sid = session_id or str(uuid.uuid4())
    return StreamingResponse(
        sse_stream(message, sid),
        media_type="text/event-stream",
    )
