"""Pydantic models for API request/response schemas."""

import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


def to_camel(string: str) -> str:
    """Convert snake_case to camelCase."""
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=5000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    answer: str
    sources: list[str] = Field(default_factory=list)


# ============================================================
# Generative UI Component Models
# ============================================================


class SourceDocument(BaseModel):
    """A source document for attribution."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str
    product: str  # kDrive, kMeet, kChat, etc.
    url: str
    snippet: str
    relevance_score: float | None = None


class SourceCardsComponent(BaseModel):
    """UI component showing source documents as cards."""

    type: Literal["source_cards"] = "source_cards"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sources: list[SourceDocument]


class Step(BaseModel):
    """A single step in a procedure."""

    number: int
    title: str
    description: str
    details: str | None = None
    command: str | None = None


class StepGuideComponent(BaseModel):
    """UI component for interactive step-by-step guides."""

    type: Literal["step_guide"] = "step_guide"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    steps: list[Step]


class QuickAction(BaseModel):
    """A quick action button."""

    label: str
    url: str | None = None
    action: Literal["open_docs", "contact_support", "copy"] | None = None
    icon: str | None = None


class QuickActionsComponent(BaseModel):
    """UI component for contextual action buttons."""

    type: Literal["quick_actions"] = "quick_actions"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    actions: list[QuickAction]


Platform = Literal["web", "windows", "macos", "ios", "android", "linux"]
Availability = Literal["full", "partial", "none"]


class PlatformStatus(BaseModel):
    """Availability status for a single platform."""

    platform: Platform
    availability: Availability
    notes: str | None = None


class PlatformAvailabilityComponent(BaseModel):
    """UI component showing feature availability across platforms."""

    type: Literal["platform_availability"] = "platform_availability"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    feature: str
    platforms: list[PlatformStatus]


# Union type for all UI components
UIComponent = (
    SourceCardsComponent
    | StepGuideComponent
    | QuickActionsComponent
    | PlatformAvailabilityComponent
)
