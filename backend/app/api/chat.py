"""
Chat API endpoint with Vercel AI SDK streaming protocol support.

Implements the Vercel AI SDK Data Stream Protocol for streaming responses:
https://sdk.vercel.ai/docs/ai-sdk-ui/stream-protocol#data-stream-protocol
"""

import json
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from backend.app.agents.router import IntentRouter, IntentType, get_available_skills
from backend.app.core.config import settings
from backend.app.rag.generator import AnswerGenerator
from backend.app.rag.hybrid_retriever import HybridConfig, HybridRetriever, RetrievalMode

router = APIRouter()


class Message(BaseModel):
    """Chat message in Vercel AI SDK format."""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat request in Vercel AI SDK format."""

    messages: list[Message] = Field(..., description="Conversation history")


async def generate_action_stub(intent) -> AsyncIterator[str]:
    """
    Generate a stub response for action intents.

    This is a placeholder until Phase C2 implements the agent executor.
    """
    skill_name = intent.skill or "unknown"
    message = f"[Action Mode] I understood you want to execute: {skill_name}\n\nThis feature is coming soon! For now, I can only answer questions about kSuite documentation."

    # Stream in Vercel AI SDK format
    yield f'0:"{json.dumps(message)[1:-1]}"\n'
    yield 'd:{"finishReason": "stop", "usage": {"promptTokens": 0, "completionTokens": 0}}\n'


def format_context(results: list) -> str:
    """Format retrieval results into context string."""
    if not results:
        return "No relevant documentation found."

    context_parts = []
    for i, result in enumerate(results, 1):
        # Use context window if available (sentence window strategy)
        content = result.context_window or result.content
        source = result.metadata.get("source", "Unknown")
        product = result.metadata.get("product", "kSuite")

        context_parts.append(f"[{i}] ({product}) {source}\n{content}")

    return "\n\n---\n\n".join(context_parts)


async def generate_stream(question: str, context: str) -> AsyncIterator[str]:
    """
    Generate streaming response using Vercel AI SDK Data Stream Protocol.

    The protocol uses line-delimited format with type prefixes:
    - '0:' for text chunks
    - 'e:' for errors
    - 'd:' for done signal with usage info
    """
    generator = AnswerGenerator(
        model=settings.generation_model,
        temperature=0.7,
    )

    try:
        # Generate the full response (LangChain doesn't support streaming easily)
        response = generator.generate(question, context)

        # Stream the response in chunks for better UX
        chunk_size = 20  # Characters per chunk
        for i in range(0, len(response), chunk_size):
            chunk = response[i : i + chunk_size]
            # Vercel AI SDK text format: 0:"text chunk"\n
            yield f'0:"{json.dumps(chunk)[1:-1]}"\n'

        # Send finish signal with usage info
        usage = generator.last_usage
        finish_data = {
            "finishReason": "stop",
            "usage": {
                "promptTokens": usage.input_tokens if usage else 0,
                "completionTokens": usage.output_tokens if usage else 0,
            },
        }
        yield f"d:{json.dumps(finish_data)}\n"

    except Exception as e:
        # Send error in Vercel AI SDK format
        error_data = {"error": str(e)}
        yield f"e:{json.dumps(error_data)}\n"


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """
    Chat endpoint with RAG and streaming response.

    Uses Vercel AI SDK Data Stream Protocol for frontend compatibility.
    """
    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    # Get the last user message
    user_messages = [m for m in request.messages if m.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user message found")

    question = user_messages[-1].content

    # Classify intent (RAG or Action)
    intent_router = IntentRouter()
    intent = intent_router.classify(
        query=question,
        available_skills=get_available_skills(),
        history=[{"role": m.role, "content": m.content} for m in request.messages[-4:-1]],
    )

    # Route to action stub if high-confidence action
    if intent.is_action():
        return StreamingResponse(
            generate_action_stub(intent),
            media_type="text/plain; charset=utf-8",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Vercel-AI-Data-Stream": "v1",
            },
        )

    # Continue with RAG flow for documentation questions
    # Default collection for hybrid search
    collection_name = "infomaniak_hybrid_full_doc_no_images"

    # Initialize hybrid retriever
    retriever = HybridRetriever(
        collection_name=collection_name,
        config=HybridConfig(mode=RetrievalMode.HYBRID),
    )

    # Check if collection exists
    if not retriever.collection_exists():
        # Fall back to dense-only collection
        collection_name = "infomaniak_full_doc_no_images"
        from backend.app.rag.retriever import QdrantRetriever

        dense_retriever = QdrantRetriever(collection_name=collection_name)
        if not dense_retriever.collection_exists():
            raise HTTPException(
                status_code=503,
                detail="No indexed documentation found. Run ingestion first.",
            )
        results = dense_retriever.search(question)
    else:
        results = retriever.search(question)

    # Format context
    context = format_context(results)

    # Return streaming response
    return StreamingResponse(
        generate_stream(question, context),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Vercel-AI-Data-Stream": "v1",
        },
    )


@router.get("/collections")
async def list_collections() -> dict:
    """List available document collections."""
    from qdrant_client import QdrantClient

    client = QdrantClient(url=settings.qdrant_host)

    try:
        collections = client.get_collections()
        return {
            "collections": [
                {"name": c.name}
                for c in collections.collections
                if c.name.startswith("infomaniak")
            ]
        }
    except Exception as e:
        return {"collections": [], "error": str(e)}
