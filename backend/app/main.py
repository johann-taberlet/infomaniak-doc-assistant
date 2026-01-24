"""
FastAPI application entry point for kSuite Documentation Assistant.

Provides a REST API for RAG-based chat with Infomaniak documentation.
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.chat import router as chat_router
from backend.app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler for startup/shutdown."""
    # Startup
    print(f"Starting kSuite Assistant (model: {settings.generation_model})")
    print(f"Qdrant: {settings.qdrant_host}")
    yield
    # Shutdown
    print("Shutting down kSuite Assistant")


app = FastAPI(
    title="kSuite Documentation Assistant",
    description="AI-powered assistant for Infomaniak kSuite documentation (kDrive, kMeet, kChat)",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API info."""
    return {
        "name": "kSuite Documentation Assistant",
        "version": "2.0.0",
        "docs": "/docs",
    }
