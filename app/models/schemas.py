"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=5000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    answer: str
    sources: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Response model for health endpoint."""

    status: str
