"""Core primitives for agent interactions with the frontend.

These low-level primitives are the building blocks that the agent uses
to interact with the frontend application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .events import (
    NavigateEvent,
    ShowPanelEvent,
    StateUpdateEvent,
    StreamEvent,
    ToastEvent,
    ToolStatus,
    ToolStatusEvent,
)
from .fakedb import FakeDB, get_fakedb


class EventEmitter(Protocol):
    """Protocol for event emission callbacks."""

    def __call__(self, event: StreamEvent) -> None:
        """Emit an event to the stream."""
        ...


@dataclass
class ToolResult:
    """Result of a primitive execution.

    Attributes:
        success: Whether the operation succeeded
        data: Result data if successful
        error: Error message if failed
        events: List of events that were emitted
    """

    success: bool
    data: Any = None
    error: str | None = None
    events: list[StreamEvent] = field(default_factory=list)


class Primitives:
    """Low-level primitives for agent-frontend interaction.

    Each primitive:
    1. Emits ToolStatusEvent (starting)
    2. Performs the action
    3. Emits relevant state/navigation events
    4. Emits ToolStatusEvent (success/error)
    5. Returns ToolResult with success, data, error, events
    """

    def __init__(
        self,
        emit: EventEmitter | None = None,
        db: FakeDB | None = None,
    ):
        """Initialize primitives.

        Args:
            emit: Optional callback to emit events to the stream
            db: Optional FakeDB instance (uses singleton if not provided)
        """
        self._emit = emit
        self._db = db or get_fakedb()
        self._events: list[StreamEvent] = []

    def _emit_event(self, event: StreamEvent) -> None:
        """Emit an event and track it.

        Args:
            event: The event to emit
        """
        self._events.append(event)
        if self._emit:
            self._emit(event)

    def _start_tool(self, tool: str, message: str) -> None:
        """Emit starting status for a tool.

        Args:
            tool: Name of the tool
            message: Starting message
        """
        self._emit_event(
            ToolStatusEvent(tool=tool, status=ToolStatus.STARTING, message=message)
        )

    def _success_tool(self, tool: str, message: str) -> None:
        """Emit success status for a tool.

        Args:
            tool: Name of the tool
            message: Success message
        """
        self._emit_event(
            ToolStatusEvent(tool=tool, status=ToolStatus.SUCCESS, message=message)
        )

    def _error_tool(self, tool: str, message: str) -> None:
        """Emit error status for a tool.

        Args:
            tool: Name of the tool
            message: Error message
        """
        self._emit_event(
            ToolStatusEvent(tool=tool, status=ToolStatus.ERROR, message=message)
        )

    def _make_result(
        self,
        success: bool,
        data: Any = None,
        error: str | None = None,
    ) -> ToolResult:
        """Create a ToolResult and reset event tracking.

        Args:
            success: Whether the operation succeeded
            data: Result data if successful
            error: Error message if failed

        Returns:
            ToolResult with tracked events
        """
        result = ToolResult(
            success=success,
            data=data,
            error=error,
            events=self._events.copy(),
        )
        self._events = []
        return result

    async def update_state(self, path: str, value: Any) -> ToolResult:
        """Update the frontend application state.

        Args:
            path: Dot-notation path to the state key (e.g., "kmeet.currentMeeting")
            value: The new value to set at that path

        Returns:
            ToolResult indicating success or failure
        """
        self._start_tool("updateState", f"Updating state: {path}")

        try:
            # Validate path format
            if not path or not isinstance(path, str):
                raise ValueError("Path must be a non-empty string")

            # Emit the state update event
            self._emit_event(StateUpdateEvent(path=path, value=value))

            self._success_tool("updateState", f"State updated: {path}")
            return self._make_result(success=True, data={"path": path, "value": value})

        except Exception as e:
            error_msg = str(e)
            self._error_tool("updateState", error_msg)
            return self._make_result(success=False, error=error_msg)

    async def query_db(
        self, collection: str, filter: dict[str, Any] | None = None
    ) -> ToolResult:
        """Query the fake database.

        Args:
            collection: Name of the collection to query
                (contacts, files, folders, channels, messages, meetings)
            filter: Optional filters to apply
                - Exact match: {"name": "John Smith"}
                - Contains: {"name_contains": "john"}

        Returns:
            ToolResult with matching items in data field
        """
        filter_desc = f" with filter {filter}" if filter else ""
        self._start_tool("queryDB", f"Querying {collection}{filter_desc}")

        try:
            results = self._db.query(collection, filter)

            self._success_tool(
                "queryDB", f"Found {len(results)} item(s) in {collection}"
            )
            return self._make_result(success=True, data=results)

        except ValueError as e:
            error_msg = str(e)
            self._error_tool("queryDB", error_msg)
            return self._make_result(success=False, error=error_msg)

    async def show_panel(
        self, panel_id: str, props: dict[str, Any] | None = None
    ) -> ToolResult:
        """Display a UI panel/modal component.

        Args:
            panel_id: Identifier for the panel component to show
            props: Optional properties to pass to the panel

        Returns:
            ToolResult indicating success or failure
        """
        self._start_tool("showPanel", f"Showing panel: {panel_id}")

        try:
            if not panel_id or not isinstance(panel_id, str):
                raise ValueError("Panel ID must be a non-empty string")

            # Emit the show panel event
            self._emit_event(ShowPanelEvent(panel_id=panel_id, props=props))

            self._success_tool("showPanel", f"Panel displayed: {panel_id}")
            return self._make_result(
                success=True, data={"panel_id": panel_id, "props": props}
            )

        except Exception as e:
            error_msg = str(e)
            self._error_tool("showPanel", error_msg)
            return self._make_result(success=False, error=error_msg)

    async def navigate(self, route: str) -> ToolResult:
        """Navigate to a different route in the frontend.

        Args:
            route: The route to navigate to (e.g., "/kmeet", "/kdrive/files")

        Returns:
            ToolResult indicating success or failure
        """
        self._start_tool("navigate", f"Navigating to: {route}")

        try:
            if not route or not isinstance(route, str):
                raise ValueError("Route must be a non-empty string")

            # Emit the navigate event
            self._emit_event(NavigateEvent(route=route))

            self._success_tool("navigate", f"Navigated to: {route}")
            return self._make_result(success=True, data={"route": route})

        except Exception as e:
            error_msg = str(e)
            self._error_tool("navigate", error_msg)
            return self._make_result(success=False, error=error_msg)

    async def toast(self, message: str, type: str = "info") -> ToolResult:
        """Show a toast notification.

        Args:
            message: The message to display
            type: Type of toast (info, success, warning, error)

        Returns:
            ToolResult indicating success or failure
        """
        self._start_tool("toast", f"Showing toast: {type}")

        try:
            if not message or not isinstance(message, str):
                raise ValueError("Message must be a non-empty string")

            valid_types = {"info", "success", "warning", "error"}
            if type not in valid_types:
                raise ValueError(f"Type must be one of: {', '.join(valid_types)}")

            # Emit the toast event
            self._emit_event(ToastEvent(message=message, type=type))

            self._success_tool("toast", "Toast displayed")
            return self._make_result(
                success=True, data={"message": message, "type": type}
            )

        except Exception as e:
            error_msg = str(e)
            self._error_tool("toast", error_msg)
            return self._make_result(success=False, error=error_msg)
