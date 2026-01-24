"""
Agents module for intent routing and action execution.

This module provides:
- IntentRouter: Classifies user queries as RAG or Action
- Intent: Classification result with type, confidence, and skill
- IntentType: Enum for intent types (rag, action)
- SkillInfo: Metadata about available skills
- IntentClassificationError: Raised when classification fails
- Primitives: Low-level primitives for agent-frontend interaction
- Events: Streaming event types for Vercel AI SDK
- Tools: LLM tool definitions in OpenAI format
- FakeDB: Simulated database for agent queries
- Skills: Skill loading and parsing for agentic system
"""

from backend.app.agents.events import (
    NavigateEvent,
    ShowPanelEvent,
    StateUpdateEvent,
    StreamEvent,
    ToastEvent,
    ToastType,
    ToolStatus,
    ToolStatusEvent,
)
from backend.app.agents.fakedb import FakeDB, get_fakedb, reset_fakedb
from backend.app.agents.primitives import EventEmitter, Primitives, ToolResult
from backend.app.agents.router import (
    Intent,
    IntentClassificationError,
    IntentRouter,
    IntentType,
    SkillInfo,
)
from backend.app.agents.skills import (
    Skill,
    SkillLoader,
    SkillMetadata,
    SkillNotFoundError,
    SkillParseError,
    get_skill_loader,
    reset_skill_loader,
)
from backend.app.agents.tools import TOOL_DEFINITIONS, get_tool_by_name, get_tool_names

__all__ = [
    # Router
    "IntentRouter",
    "Intent",
    "IntentType",
    "SkillInfo",
    "IntentClassificationError",
    # Events
    "NavigateEvent",
    "ShowPanelEvent",
    "StateUpdateEvent",
    "StreamEvent",
    "ToastEvent",
    "ToastType",
    "ToolStatus",
    "ToolStatusEvent",
    # FakeDB
    "FakeDB",
    "get_fakedb",
    "reset_fakedb",
    # Primitives
    "EventEmitter",
    "Primitives",
    "ToolResult",
    # Tools
    "TOOL_DEFINITIONS",
    "get_tool_by_name",
    "get_tool_names",
    # Skills
    "Skill",
    "SkillLoader",
    "SkillMetadata",
    "SkillNotFoundError",
    "SkillParseError",
    "get_skill_loader",
    "reset_skill_loader",
]
