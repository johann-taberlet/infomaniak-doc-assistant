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

from app.agent.executor import search_documentation, stream_ndjson_response
from app.agent.tools import get_sources, reset_context
from app.models.schemas import ChatRequest, ChatResponse

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
    """Chat endpoint that invokes the agent with the user's message.

    Note: This endpoint is kept for backwards compatibility but the
    streaming endpoint (/chat/stream) is preferred for better UX.
    """
    metrics["request_count"] += 1

    try:
        # Use provided session_id or generate a new one
        session_id = request.session_id or str(uuid.uuid4())

        # Reset context for this request
        reset_context()

        # 1. Search documentation
        search_context = await search_documentation(request.message)
        sources = get_sources()

        # 2. Collect full NDJSON response
        full_response = ""
        async for chunk in stream_ndjson_response(
            request.message, search_context, session_id
        ):
            full_response += chunk

        # Extract text content from NDJSON for simple response
        answer_parts = []
        for line in full_response.split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get("type") == "text":
                    answer_parts.append(obj.get("content", ""))
            except json.JSONDecodeError:
                pass

        answer = "\n".join(answer_parts) if answer_parts else full_response

        return ChatResponse(
            answer=answer, sources=[s.get("url", "") for s in sources if s.get("url")]
        )
    except Exception:
        metrics["error_count"] += 1
        raise


def format_sse(data: dict[str, Any]) -> str:
    """Format data as a Server-Sent Event."""
    return f"data: {json.dumps(data)}\n\n"


async def sse_stream(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Generate SSE events from NDJSON streaming response.

    Parses NDJSON lines and emits SSE events progressively:
    - status: Progress updates during processing
    - segment: Each content segment (text or component)
    - error: Signal that an error occurred
    - done: Signal that streaming is complete, includes language
    """
    try:
        # Reset context for this request
        reset_context()

        # Timeline logging
        start_time = time.perf_counter()
        tlog = _timeline_logger
        tlog.info("=" * 60)
        tlog.info(
            "[T+0.000s] REQUEST START - Message: %s (session: %s)",
            message[:80],
            session_id,
        )

        # Status: searching
        yield format_sse({"status": "Searching documentation..."})
        tlog.info("[T+%.3fs] STATUS - Searching", time.perf_counter() - start_time)

        # 1. RAG Search
        search_context = await search_documentation(message)
        sources = get_sources()

        tlog.info(
            "[T+%.3fs] SEARCH COMPLETE - %d sources",
            time.perf_counter() - start_time,
            len(sources),
        )

        # Status: generating
        yield format_sse({"status": "Generating response..."})
        tlog.info("[T+%.3fs] STATUS - Generating", time.perf_counter() - start_time)

        # 2. Stream NDJSON and parse line by line
        buffer = ""
        current_step_guide: dict[str, Any] | None = None
        first_content_emitted = False

        async for token in stream_ndjson_response(message, search_context, session_id):
            buffer += token

            # Parse complete lines
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()

                if not line:
                    continue

                try:
                    obj = json.loads(line)
                    obj_type = obj.get("type")

                    if not first_content_emitted:
                        first_content_emitted = True
                        tlog.info(
                            "[T+%.3fs] FIRST CONTENT - type=%s",
                            time.perf_counter() - start_time,
                            obj_type,
                        )

                    if obj_type == "text":
                        # Emit text segment
                        segment = {
                            "type": "text",
                            "order": obj.get("order", 1),
                            "content": obj.get("content", ""),
                            "id": str(uuid.uuid4()),
                        }
                        tlog.info(
                            "[T+%.3fs] EMIT TEXT - order=%s",
                            time.perf_counter() - start_time,
                            obj.get("order"),
                        )
                        yield format_sse({"segment": segment})

                    elif obj_type == "step_guide_start":
                        # Start a new step guide (emit skeleton)
                        current_step_guide = {
                            "type": "step_guide",
                            "title": obj.get("title", ""),
                            "order": obj.get("order", 2),
                            "steps": [],
                            "id": str(uuid.uuid4()),
                        }
                        tlog.info(
                            "[T+%.3fs] STEP GUIDE START - title=%s",
                            time.perf_counter() - start_time,
                            obj.get("title"),
                        )
                        yield format_sse({"segment": current_step_guide})

                    elif obj_type == "step":
                        # Add step to current guide and emit update
                        if current_step_guide:
                            step = {
                                "number": obj.get("number", 1),
                                "title": obj.get("title", ""),
                                "description": obj.get("description", ""),
                            }
                            # Add optional fields if present
                            if "details" in obj:
                                step["details"] = obj["details"]
                            if "command" in obj:
                                step["command"] = obj["command"]

                            current_step_guide["steps"].append(step)
                            tlog.info(
                                "[T+%.3fs] EMIT STEP %d - %s",
                                time.perf_counter() - start_time,
                                obj.get("number"),
                                obj.get("title", "")[:30],
                            )
                            yield format_sse({"segment": current_step_guide})

                    elif obj_type == "step_guide_end":
                        # Mark step guide as complete
                        tlog.info(
                            "[T+%.3fs] STEP GUIDE END",
                            time.perf_counter() - start_time,
                        )
                        current_step_guide = None

                    elif obj_type == "quick_actions":
                        # Emit quick actions
                        segment = {
                            "type": "quick_actions",
                            "order": obj.get("order", 99),
                            "actions": obj.get("actions", []),
                            "id": str(uuid.uuid4()),
                        }
                        tlog.info(
                            "[T+%.3fs] EMIT QUICK ACTIONS",
                            time.perf_counter() - start_time,
                        )
                        yield format_sse({"segment": segment})

                    elif obj_type == "done":
                        # Emit sources
                        if sources:
                            tlog.info(
                                "[T+%.3fs] EMIT SOURCES - %d items",
                                time.perf_counter() - start_time,
                                len(sources),
                            )
                            yield format_sse(
                                {
                                    "segment": {
                                        "type": "source_cards",
                                        "id": str(uuid.uuid4()),
                                        "sources": sources,
                                    }
                                }
                            )

                        # Emit done
                        language = obj.get("language", "en")
                        tlog.info(
                            "[T+%.3fs] EMIT DONE - lang=%s",
                            time.perf_counter() - start_time,
                            language,
                        )
                        tlog.info("=" * 60)
                        yield format_sse({"done": True, "language": language})
                        return

                except json.JSONDecodeError:
                    # Invalid JSON line - log but continue
                    tlog.warning(
                        "[T+%.3fs] INVALID JSON: %s",
                        time.perf_counter() - start_time,
                        line[:50],
                    )

        # Handle remaining buffer (in case no trailing newline)
        if buffer.strip():
            try:
                obj = json.loads(buffer.strip())
                if obj.get("type") == "done":
                    if sources:
                        yield format_sse(
                            {
                                "segment": {
                                    "type": "source_cards",
                                    "id": str(uuid.uuid4()),
                                    "sources": sources,
                                }
                            }
                        )
                    yield format_sse(
                        {"done": True, "language": obj.get("language", "en")}
                    )
                    return
            except json.JSONDecodeError:
                pass

        # Fallback: emit sources and done if we didn't get a done signal
        tlog.warning(
            "[T+%.3fs] FALLBACK DONE (no done signal received)",
            time.perf_counter() - start_time,
        )
        if sources:
            yield format_sse(
                {
                    "segment": {
                        "type": "source_cards",
                        "id": str(uuid.uuid4()),
                        "sources": sources,
                    }
                }
            )
        yield format_sse({"done": True})

    except Exception as e:
        # Log the full error for debugging
        logger.exception("Error during SSE stream: %s", str(e))
        metrics["error_count"] += 1

        # Send user-friendly error message
        error_message = (
            "Sorry, an error occurred while processing your request. Please try again."
        )

        # Include more specific message for known error types
        error_str = str(e).lower()
        if "rate limit" in error_str:
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
