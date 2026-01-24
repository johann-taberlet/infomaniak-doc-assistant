"""Event types for streaming agent actions to the frontend.

Uses Vercel AI SDK Data Stream Protocol with `2:` prefix for custom events.
See: https://sdk.vercel.ai/docs/ai-sdk-ui/stream-protocol
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ToolStatus(str, Enum):
    """Status of a tool execution."""

    STARTING = "starting"
    EXECUTING = "executing"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class ToolStatusEvent:
    """Event emitted when a tool's status changes.

    Attributes:
        tool: Name of the tool being executed
        status: Current status of the tool
        message: Human-readable message describing the status
    """

    tool: str
    status: ToolStatus
    message: str

    def to_stream(self) -> str:
        """Serialize to Vercel AI SDK data stream format.

        Returns:
            String in format: 2:["tool-status", {...}]\n
        """
        payload = {
            "tool": self.tool,
            "status": self.status.value,
            "message": self.message,
        }
        return f'2:{json.dumps(["tool-status", payload])}\n'


@dataclass
class StateUpdateEvent:
    """Event emitted when frontend state should be updated.

    Attributes:
        path: Dot-notation path to the state key (e.g., "kmeet.currentMeeting")
        value: The new value to set at that path
    """

    path: str
    value: Any

    def to_stream(self) -> str:
        """Serialize to Vercel AI SDK data stream format.

        Returns:
            String in format: 2:["state-update", {...}]\n
        """
        payload = {
            "path": self.path,
            "value": self.value,
        }
        return f'2:{json.dumps(["state-update", payload])}\n'


@dataclass
class NavigateEvent:
    """Event emitted when the frontend should navigate to a new route.

    Attributes:
        route: The route to navigate to (e.g., "/kmeet", "/kdrive/files")
    """

    route: str

    def to_stream(self) -> str:
        """Serialize to Vercel AI SDK data stream format.

        Returns:
            String in format: 2:["navigate", {...}]\n
        """
        payload = {"route": self.route}
        return f'2:{json.dumps(["navigate", payload])}\n'


@dataclass
class ShowPanelEvent:
    """Event emitted when the frontend should display a panel/modal.

    Attributes:
        panel_id: Identifier for the panel component to show
        props: Properties to pass to the panel component
    """

    panel_id: str
    props: dict[str, Any] | None = None

    def to_stream(self) -> str:
        """Serialize to Vercel AI SDK data stream format.

        Returns:
            String in format: 2:["show-panel", {...}]\n
        """
        payload = {
            "panelId": self.panel_id,
            "props": self.props or {},
        }
        return f'2:{json.dumps(["show-panel", payload])}\n'


@dataclass
class ToastEvent:
    """Event emitted when the frontend should show a toast notification.

    Attributes:
        message: The message to display
        type: Type of toast (info, success, warning, error)
    """

    message: str
    type: str = "info"

    def to_stream(self) -> str:
        """Serialize to Vercel AI SDK data stream format.

        Returns:
            String in format: 2:["toast", {...}]\n
        """
        payload = {
            "message": self.message,
            "type": self.type,
        }
        return f'2:{json.dumps(["toast", payload])}\n'


# Type alias for any event that can be streamed
StreamEvent = ToolStatusEvent | StateUpdateEvent | NavigateEvent | ShowPanelEvent | ToastEvent
