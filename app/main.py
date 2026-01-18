"""FastAPI application entry point."""

import asyncio
import json
import logging
import time
import uuid
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.agent.executor import search_documentation, stream_ndjson_response
from app.agent.tools import get_sources, reset_context
from app.auth import verify_demo_token
from app.config import settings
from app.models.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

# Configure file logging for timeline analysis
_timeline_logger = logging.getLogger("timeline")
_timeline_logger.setLevel(logging.INFO)
_timeline_handler = logging.FileHandler(settings.LOG_TIMELINE_PATH, mode="a")
_timeline_handler.setFormatter(logging.Formatter("%(message)s"))
_timeline_logger.addHandler(_timeline_handler)

# Thread-safe in-memory metrics
_metrics_lock = asyncio.Lock()
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


@app.get("/metrics", dependencies=[Depends(verify_demo_token)])
async def get_metrics() -> dict[str, int]:
    """Return application metrics."""
    async with _metrics_lock:
        return dict(metrics)


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(verify_demo_token)])
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat endpoint that invokes the agent with the user's message.

    Note: This endpoint is kept for backwards compatibility but the
    streaming endpoint (/chat/stream) is preferred for better UX.
    """
    async with _metrics_lock:
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
        async with _metrics_lock:
            metrics["error_count"] += 1
        raise


def format_sse(data: dict[str, Any], flush: bool = False) -> str:
    """Format data as a Server-Sent Event.

    Args:
        data: The data to send
        flush: If True, add padding to force buffer flush
    """
    event = f"data: {json.dumps(data)}\n\n"
    if flush:
        # Add padding to force buffer flush (some proxies buffer small responses)
        event += ": padding" + " " * 2048 + "\n\n"
    return event


def _create_source_cards_segment(sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Create a source_cards segment for SSE emission."""
    return {
        "segment": {
            "type": "source_cards",
            "id": str(uuid.uuid4()),
            "sources": sources,
        }
    }


def _get_user_friendly_error(exc: Exception) -> str:
    """Convert an exception to a user-friendly error message."""
    error_str = str(exc).lower()
    if "rate limit" in error_str:
        return "Too many requests. Please wait a moment and try again."
    if "timeout" in error_str:
        return "The request timed out. Please try again."
    return "Sorry, an error occurred while processing your request. Please try again."


class _StreamState:
    """Mutable state for SSE stream processing."""

    def __init__(self, start_time: float) -> None:
        self.start_time = start_time
        self.current_step_guide: dict[str, Any] | None = None
        self.first_content_emitted = False

    def elapsed(self) -> float:
        """Return elapsed time since stream start."""
        return time.perf_counter() - self.start_time


def _handle_text_segment(obj: dict[str, Any], state: _StreamState) -> str:
    """Handle a text segment from NDJSON."""
    segment = {
        "type": "text",
        "order": obj.get("order", 1),
        "content": obj.get("content", ""),
        "id": str(uuid.uuid4()),
    }
    _timeline_logger.info(
        "[T+%.3fs] EMIT TEXT - order=%s", state.elapsed(), obj.get("order")
    )
    return format_sse({"segment": segment})


def _handle_step_guide_start(obj: dict[str, Any], state: _StreamState) -> str:
    """Handle step_guide_start from NDJSON."""
    state.current_step_guide = {
        "type": "step_guide",
        "title": obj.get("title", ""),
        "order": obj.get("order", 2),
        "steps": [],
        "id": str(uuid.uuid4()),
    }
    _timeline_logger.info(
        "[T+%.3fs] STEP GUIDE START - title=%s", state.elapsed(), obj.get("title")
    )
    return format_sse({"segment": state.current_step_guide})


def _handle_step(obj: dict[str, Any], state: _StreamState) -> str | None:
    """Handle a step from NDJSON. Returns None if no current step guide."""
    if not state.current_step_guide:
        return None

    step: dict[str, Any] = {
        "number": obj.get("number", 1),
        "title": obj.get("title", ""),
        "description": obj.get("description", ""),
    }
    if "details" in obj:
        step["details"] = obj["details"]
    if "command" in obj:
        step["command"] = obj["command"]

    state.current_step_guide["steps"].append(step)
    _timeline_logger.info(
        "[T+%.3fs] EMIT STEP %d - %s",
        state.elapsed(),
        obj.get("number"),
        obj.get("title", "")[:30],
    )
    return format_sse({"segment": state.current_step_guide})


def _handle_quick_actions(obj: dict[str, Any], state: _StreamState) -> str:
    """Handle quick_actions from NDJSON."""
    segment = {
        "type": "quick_actions",
        "order": obj.get("order", 99),
        "actions": obj.get("actions", []),
        "id": str(uuid.uuid4()),
    }
    _timeline_logger.info("[T+%.3fs] EMIT QUICK ACTIONS", state.elapsed())
    return format_sse({"segment": segment})


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

        # Initialize stream state
        state = _StreamState(time.perf_counter())
        tlog = _timeline_logger
        tlog.info("=" * 60)
        tlog.info(
            "[T+0.000s] REQUEST START - Message: %s (session: %s)",
            message[:80],
            session_id,
        )

        # Status: understanding
        yield format_sse({"status": "Understanding your question..."}, flush=True)
        tlog.info("[T+%.3fs] STATUS - Understanding", state.elapsed())

        # Minimal delay to flush the event before blocking
        await asyncio.sleep(0.01)

        # Status: searching
        yield format_sse({"status": "Searching documentation..."}, flush=True)
        tlog.info("[T+%.3fs] STATUS - Searching", state.elapsed())

        # Minimal delay to flush the event before blocking on search
        await asyncio.sleep(0.01)

        # 1. RAG Search
        search_context = await search_documentation(message)
        sources = get_sources()

        tlog.info("[T+%.3fs] SEARCH COMPLETE - %d sources", state.elapsed(), len(sources))

        # Status: generating
        yield format_sse({"status": "Generating response..."}, flush=True)
        tlog.info("[T+%.3fs] STATUS - Generating", state.elapsed())

        # 2. Stream NDJSON and parse line by line
        buffer = ""

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

                    if not state.first_content_emitted:
                        state.first_content_emitted = True
                        tlog.info("[T+%.3fs] FIRST CONTENT - type=%s", state.elapsed(), obj_type)

                    if obj_type == "text":
                        yield _handle_text_segment(obj, state)

                    elif obj_type == "step_guide_start":
                        yield _handle_step_guide_start(obj, state)

                    elif obj_type == "step":
                        result = _handle_step(obj, state)
                        if result:
                            yield result

                    elif obj_type == "step_guide_end":
                        tlog.info("[T+%.3fs] STEP GUIDE END", state.elapsed())
                        state.current_step_guide = None

                    elif obj_type == "quick_actions":
                        yield _handle_quick_actions(obj, state)

                    elif obj_type == "done":
                        # Emit sources and done
                        if sources:
                            tlog.info("[T+%.3fs] EMIT SOURCES - %d items", state.elapsed(), len(sources))
                            yield format_sse(_create_source_cards_segment(sources))

                        language = obj.get("language", "en")
                        tlog.info("[T+%.3fs] EMIT DONE - lang=%s", state.elapsed(), language)
                        tlog.info("=" * 60)
                        yield format_sse({"done": True, "language": language})
                        return

                except json.JSONDecodeError:
                    tlog.warning("[T+%.3fs] INVALID JSON: %s", state.elapsed(), line[:50])

        # Handle remaining buffer (in case no trailing newline)
        if buffer.strip():
            try:
                obj = json.loads(buffer.strip())
                if obj.get("type") == "done":
                    if sources:
                        yield format_sse(_create_source_cards_segment(sources))
                    yield format_sse({"done": True, "language": obj.get("language", "en")})
                    return
            except json.JSONDecodeError:
                pass

        # Fallback: emit sources and done if we didn't get a done signal
        tlog.warning("[T+%.3fs] FALLBACK DONE (no done signal received)", state.elapsed())
        if sources:
            yield format_sse(_create_source_cards_segment(sources))
        yield format_sse({"done": True})

    except Exception as e:
        logger.exception("Error during SSE stream: %s", str(e))
        async with _metrics_lock:
            metrics["error_count"] += 1

        error_message = _get_user_friendly_error(e)
        logger.info("Sending error event to client: %s", error_message)
        yield format_sse({"error": error_message})


@app.get("/chat/stream", dependencies=[Depends(verify_demo_token)])
async def chat_stream(message: str, session_id: str | None = None) -> StreamingResponse:
    """Streaming chat endpoint using Server-Sent Events."""
    sid = session_id or str(uuid.uuid4())
    return StreamingResponse(
        sse_stream(message, sid),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate, no-transform",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
            "Connection": "keep-alive",
        },
    )
