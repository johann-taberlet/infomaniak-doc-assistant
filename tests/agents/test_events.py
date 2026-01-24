"""Tests for agent event types and serialization."""

import json

from backend.app.agents.events import (
    NavigateEvent,
    ShowPanelEvent,
    StateUpdateEvent,
    ToastEvent,
    ToastType,
    ToolStatus,
    ToolStatusEvent,
)


class TestToolStatusEvent:
    """Tests for ToolStatusEvent serialization."""

    def test_starting_status(self):
        """Test starting status event serialization."""
        event = ToolStatusEvent(
            tool="queryDB",
            status=ToolStatus.STARTING,
            message="Querying contacts",
        )
        output = event.to_stream()

        assert output.startswith('2:["tool-status",')
        assert output.endswith("]\n")

        # Parse the JSON payload
        json_part = output[2:-1]  # Remove "2:" prefix and "\n" suffix
        parsed = json.loads(json_part)

        assert parsed[0] == "tool-status"
        assert parsed[1]["tool"] == "queryDB"
        assert parsed[1]["status"] == "starting"
        assert parsed[1]["message"] == "Querying contacts"

    def test_success_status(self):
        """Test success status event serialization."""
        event = ToolStatusEvent(
            tool="navigate",
            status=ToolStatus.SUCCESS,
            message="Navigation complete",
        )
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["status"] == "success"

    def test_error_status(self):
        """Test error status event serialization."""
        event = ToolStatusEvent(
            tool="toast",
            status=ToolStatus.ERROR,
            message="Invalid toast type",
        )
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["status"] == "error"
        assert parsed[1]["message"] == "Invalid toast type"


class TestStateUpdateEvent:
    """Tests for StateUpdateEvent serialization."""

    def test_simple_value(self):
        """Test state update with a simple string value."""
        event = StateUpdateEvent(path="activeApp", value="kmeet")
        output = event.to_stream()

        assert output.startswith('2:["state-update",')

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[0] == "state-update"
        assert parsed[1]["path"] == "activeApp"
        assert parsed[1]["value"] == "kmeet"

    def test_nested_path(self):
        """Test state update with nested path."""
        event = StateUpdateEvent(
            path="kmeet.currentMeeting",
            value={"id": "meeting_1", "title": "Weekly Standup"},
        )
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["path"] == "kmeet.currentMeeting"
        assert parsed[1]["value"]["id"] == "meeting_1"

    def test_null_value(self):
        """Test state update with null value."""
        event = StateUpdateEvent(path="selectedFile", value=None)
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["value"] is None

    def test_array_value(self):
        """Test state update with array value."""
        event = StateUpdateEvent(
            path="kdrive.recentFiles",
            value=["file_1", "file_2", "file_3"],
        )
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["value"] == ["file_1", "file_2", "file_3"]


class TestNavigateEvent:
    """Tests for NavigateEvent serialization."""

    def test_simple_route(self):
        """Test navigation to a simple route."""
        event = NavigateEvent(route="/kmeet")
        output = event.to_stream()

        assert output.startswith('2:["navigate",')

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[0] == "navigate"
        assert parsed[1]["route"] == "/kmeet"

    def test_nested_route(self):
        """Test navigation to a nested route."""
        event = NavigateEvent(route="/kdrive/files/folder_1")
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["route"] == "/kdrive/files/folder_1"


class TestShowPanelEvent:
    """Tests for ShowPanelEvent serialization."""

    def test_panel_without_props(self):
        """Test showing panel without props."""
        event = ShowPanelEvent(panel_id="filePreview")
        output = event.to_stream()

        assert output.startswith('2:["show-panel",')

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[0] == "show-panel"
        assert parsed[1]["panelId"] == "filePreview"
        assert parsed[1]["props"] == {}

    def test_panel_with_props(self):
        """Test showing panel with props."""
        event = ShowPanelEvent(
            panel_id="contactCard",
            props={"contactId": "contact_1", "showActions": True},
        )
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["panelId"] == "contactCard"
        assert parsed[1]["props"]["contactId"] == "contact_1"
        assert parsed[1]["props"]["showActions"] is True


class TestToastEvent:
    """Tests for ToastEvent serialization."""

    def test_info_toast(self):
        """Test info toast (default type)."""
        event = ToastEvent(message="File uploaded successfully")
        output = event.to_stream()

        assert output.startswith('2:["toast",')

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[0] == "toast"
        assert parsed[1]["message"] == "File uploaded successfully"
        assert parsed[1]["type"] == "info"

    def test_error_toast(self):
        """Test error toast."""
        event = ToastEvent(message="Failed to save file", toast_type=ToastType.ERROR)
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["type"] == "error"

    def test_success_toast(self):
        """Test success toast."""
        event = ToastEvent(message="Changes saved", toast_type=ToastType.SUCCESS)
        output = event.to_stream()

        json_part = output[2:-1]
        parsed = json.loads(json_part)

        assert parsed[1]["type"] == "success"
