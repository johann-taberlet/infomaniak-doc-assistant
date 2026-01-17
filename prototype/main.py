"""FastAPI prototype for ReAct pattern with interleaved text + UI components.

This prototype validates that the ReAct pattern can produce truly interleaved
text and UI components by making ALL output go through tool calls.
"""

import json
import logging
import os
import sys
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

# Add parent directory to path for imports when running standalone
sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.prompts import SYSTEM_PROMPT
from prototype.tools import ALL_TOOLS, get_sources, pop_segment, reset_segments

# =============================================================================
# Logging Setup - File + Console
# =============================================================================

LOG_FILE = Path(__file__).parent / "prototype.log"

# Create file handler for detailed logging
file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

# Create console handler for basic info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

# Configure root logger
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

# Also capture httpx logs (LLM API calls)
logging.getLogger("httpx").setLevel(logging.DEBUG)


def log_separator(title: str = "") -> None:
    """Log a visual separator for easier reading."""
    sep = "=" * 80
    if title:
        logger.debug(f"\n{sep}\n{title}\n{sep}")
    else:
        logger.debug(sep)


def log_json(label: str, data: Any) -> None:
    """Log JSON data in a readable format."""
    try:
        if isinstance(data, str):
            formatted = data
        else:
            formatted = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        logger.debug(f"{label}:\n{formatted}")
    except Exception as e:
        logger.debug(f"{label}: [Error formatting: {e}] {data}")


# =============================================================================
# FastAPI App
# =============================================================================

app = FastAPI(
    title="ReAct Pattern Prototype",
    description="Prototype for interleaved text + UI components using ReAct",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memory for conversation persistence
_checkpointer = InMemorySaver()


def get_chat_model():
    """Get chat model based on environment variables.

    Supports the same providers as the main app.
    """
    provider = os.getenv("LLM_PROVIDER", "mistral").lower()
    logger.debug(f"Using LLM provider: {provider}")

    if provider == "mistral":
        from langchain_mistralai import ChatMistralAI
        model_name = os.getenv("MISTRAL_CHAT_MODEL", "mistral-large-latest")
        logger.debug(f"Mistral model: {model_name}")
        return ChatMistralAI(
            model=model_name,
            api_key=os.getenv("MISTRAL_API_KEY"),
            temperature=0.1,
        )
    elif provider == "openrouter":
        from langchain_openai import ChatOpenAI
        model_name = os.getenv("OPENROUTER_CHAT_MODEL", "mistralai/ministral-8b")
        logger.debug(f"OpenRouter model: {model_name}")
        return ChatOpenAI(
            model=model_name,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=0.1,
        )
    elif provider == "ollama":
        from langchain_ollama import ChatOllama
        model_name = os.getenv("OLLAMA_CHAT_MODEL", "qwen3:8b")
        logger.debug(f"Ollama model: {model_name}")
        return ChatOllama(
            model=model_name,
            base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            temperature=0.1,
        )
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")


def get_agent():
    """Create the ReAct agent with tools."""
    model = get_chat_model()
    return create_react_agent(
        model=model,
        tools=ALL_TOOLS,
        checkpointer=_checkpointer,
        prompt=SYSTEM_PROMPT,
    )


def format_sse(data: dict[str, Any]) -> str:
    """Format data as a Server-Sent Event."""
    return f"data: {json.dumps(data)}\n\n"


async def sse_stream(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Generate SSE events from agent streaming response.

    Emits segment events as tools complete, building the response incrementally.

    Handles parallel tool calls by buffering segments and emitting them in the
    order they were called by the LLM (not the order they completed).
    """
    log_separator(f"NEW REQUEST - Session: {session_id}")
    logger.debug(f"User message: {message}")
    log_json("System prompt", SYSTEM_PROMPT)

    agent = get_agent()
    reset_segments()

    config: dict[str, Any] = {"configurable": {"thread_id": session_id}}
    response_complete = False
    turn_count = 0

    logger.info(f"Starting stream for session {session_id[:8]}...")

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": message}]},
        config,
        version="v2",
    ):
        kind = event.get("event")

        # Log all events at debug level
        if kind not in ("on_chat_model_stream",):  # Skip noisy streaming chunks
            log_json(f"Event [{kind}]", {
                "name": event.get("name"),
                "run_id": str(event.get("run_id", ""))[:8],
                "data_keys": list(event.get("data", {}).keys()) if isinstance(event.get("data"), dict) else None,
            })

        if kind == "on_chat_model_start":
            turn_count += 1
            log_separator(f"LLM TURN {turn_count}")
            # Log the input messages to the LLM
            messages = event.get("data", {}).get("input", {}).get("messages", [])
            for i, msg in enumerate(messages):
                msg_type = type(msg).__name__
                content = getattr(msg, "content", str(msg))
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    log_json(f"  Message {i} [{msg_type}] with tool_calls", {
                        "content": content[:200] if content else None,
                        "tool_calls": [
                            {"name": tc.get("name"), "args": tc.get("args")}
                            for tc in msg.tool_calls
                        ]
                    })
                else:
                    content_preview = content[:500] if isinstance(content, str) else str(content)[:500]
                    logger.debug(f"  Message {i} [{msg_type}]: {content_preview}")

        elif kind == "on_chat_model_end":
            # Log the LLM response
            output = event.get("data", {}).get("output", {})
            if hasattr(output, "content"):
                logger.debug(f"LLM response content: {output.content[:500] if output.content else '(empty)'}")
            if hasattr(output, "tool_calls") and output.tool_calls:
                log_json("LLM tool_calls", [
                    {"name": tc.get("name"), "args": tc.get("args")}
                    for tc in output.tool_calls
                ])

        elif kind == "on_tool_start":
            tool_name = event.get("name", "")
            tool_input = event.get("data", {}).get("input", {})
            log_separator(f"TOOL START: {tool_name}")
            log_json("Tool input", tool_input)

        elif kind == "on_tool_end":
            tool_name = event.get("name", "")
            tool_output = event.get("data", {}).get("output", "")
            # Handle both string and ToolMessage output
            output_str = str(tool_output.content if hasattr(tool_output, 'content') else tool_output)

            logger.debug(f"TOOL END: {tool_name}")
            logger.debug(f"Tool output: {output_str[:300]}")

            # Check if this is the finish signal
            if "RESPONSE_COMPLETE" in output_str:
                response_complete = True
                logger.debug("Received RESPONSE_COMPLETE signal")

                # Collect ALL segments and sort by order before emitting
                all_segments: list[dict[str, Any]] = []
                while True:
                    segment = pop_segment()
                    if segment is None:
                        break
                    all_segments.append(segment)

                # Sort by order field (default to 999 if missing)
                all_segments.sort(key=lambda s: s.get("order", 999))

                logger.info(f"Emitting {len(all_segments)} segments in order")
                for segment in all_segments:
                    order = segment.get("order", "?")
                    logger.info(f"Emitting segment: {segment.get('type')} (order={order})")
                    log_json(f"Segment [{segment.get('type')}]", segment)
                    yield format_sse({"segment": segment})
                # Don't break - let the agent complete naturally to preserve history

            # For non-finish tools, segments accumulate in the queue
            # They will be sorted and emitted when finish_response is called

        elif kind == "on_chat_model_stream":
            # Log streaming chunks (very verbose, only first few chars)
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content") and chunk.content:
                # Only log non-empty content chunks
                pass  # Too verbose, skip

    # Emit sources at the very end
    sources = get_sources()
    if sources:
        logger.info(f"Emitting {len(sources)} sources")
        log_json("Sources", sources)
        yield format_sse({
            "segment": {
                "type": "source_cards",
                "sources": sources,
            }
        })

    yield format_sse({"done": True})
    log_separator(f"REQUEST COMPLETE - Session: {session_id}")
    logger.info(f"Stream complete for session {session_id[:8]} ({turn_count} LLM turns)")


@app.get("/")
async def index():
    """Serve the chat UI."""
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/chat/stream")
async def chat_stream(message: str, session_id: str | None = None) -> StreamingResponse:
    """Streaming chat endpoint using Server-Sent Events."""
    sid = session_id or str(uuid.uuid4())
    logger.info(f"New chat request - session: {sid[:8]}, message: {message[:50]}...")
    return StreamingResponse(
        sse_stream(message, sid),
        media_type="text/event-stream",
    )


@app.on_event("startup")
async def startup_event():
    """Log startup info."""
    log_separator("PROTOTYPE SERVER STARTING")
    logger.info(f"Log file: {LOG_FILE}")
    logger.info(f"LLM Provider: {os.getenv('LLM_PROVIDER', 'mistral')}")


if __name__ == "__main__":
    import uvicorn

    # Load .env from parent directory
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")

    # Clear log file on fresh start
    LOG_FILE.write_text(f"# Prototype log started at {datetime.now().isoformat()}\n\n")

    logger.info(f"Logging to: {LOG_FILE}")
    uvicorn.run(app, host="0.0.0.0", port=8001)
