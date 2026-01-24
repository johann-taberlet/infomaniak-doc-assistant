"""Tests for agent primitives."""

import pytest

from backend.app.agents.events import (
    NavigateEvent,
    ShowPanelEvent,
    StateUpdateEvent,
    ToastEvent,
    ToastType,
    ToolStatus,
    ToolStatusEvent,
)
from backend.app.agents.fakedb import reset_fakedb
from backend.app.agents.primitives import Primitives, ToolResult


class TestPrimitivesUpdateState:
    """Tests for the updateState primitive."""

    @pytest.fixture
    def primitives(self):
        """Get a Primitives instance with fresh DB."""
        reset_fakedb()
        return Primitives()

    @pytest.mark.asyncio
    async def test_update_state_success(self, primitives):
        """Test successful state update."""
        result = await primitives.update_state("activeApp", "kmeet")

        assert result.success is True
        assert result.data["path"] == "activeApp"
        assert result.data["value"] == "kmeet"
        assert result.error is None

    @pytest.mark.asyncio
    async def test_update_state_emits_events(self, primitives):
        """Test that state update emits correct events."""
        result = await primitives.update_state("kmeet.currentMeeting", {"id": "m1"})

        # Should have: starting, state-update, success
        assert len(result.events) == 3

        # First event: starting
        assert isinstance(result.events[0], ToolStatusEvent)
        assert result.events[0].status == ToolStatus.STARTING

        # Second event: state update
        assert isinstance(result.events[1], StateUpdateEvent)
        assert result.events[1].path == "kmeet.currentMeeting"
        assert result.events[1].value == {"id": "m1"}

        # Third event: success
        assert isinstance(result.events[2], ToolStatusEvent)
        assert result.events[2].status == ToolStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_update_state_empty_path_fails(self, primitives):
        """Test that empty path causes failure."""
        result = await primitives.update_state("", "value")

        assert result.success is False
        assert result.error is not None
        assert "non-empty string" in result.error

    @pytest.mark.asyncio
    async def test_update_state_with_emitter(self):
        """Test that emitter is called for each event."""
        emitted = []

        def emit(event):
            emitted.append(event)

        primitives = Primitives(emit=emit)
        await primitives.update_state("test.path", 123)

        assert len(emitted) == 3


class TestPrimitivesQueryDB:
    """Tests for the queryDB primitive."""

    @pytest.fixture
    def primitives(self):
        """Get a Primitives instance with fresh DB."""
        reset_fakedb()
        return Primitives()

    @pytest.mark.asyncio
    async def test_query_db_all(self, primitives):
        """Test querying all items from a collection."""
        result = await primitives.query_db("contacts")

        assert result.success is True
        assert len(result.data) >= 5

    @pytest.mark.asyncio
    async def test_query_db_with_filter(self, primitives):
        """Test querying with a filter."""
        result = await primitives.query_db("contacts", {"name_contains": "smith"})

        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]["name"] == "John Smith"

    @pytest.mark.asyncio
    async def test_query_db_unknown_collection(self, primitives):
        """Test querying unknown collection fails."""
        result = await primitives.query_db("unknown")

        assert result.success is False
        assert "Unknown collection" in result.error

    @pytest.mark.asyncio
    async def test_query_db_emits_events(self, primitives):
        """Test that queryDB emits correct events."""
        result = await primitives.query_db("files", {"type": "image"})

        # Should have: starting, success
        assert len(result.events) == 2

        assert result.events[0].status == ToolStatus.STARTING
        assert result.events[1].status == ToolStatus.SUCCESS
        assert "1 item" in result.events[1].message


class TestPrimitivesShowPanel:
    """Tests for the showPanel primitive."""

    @pytest.fixture
    def primitives(self):
        """Get a Primitives instance with fresh DB."""
        reset_fakedb()
        return Primitives()

    @pytest.mark.asyncio
    async def test_show_panel_success(self, primitives):
        """Test successful panel display."""
        result = await primitives.show_panel("filePreview", {"fileId": "file_1"})

        assert result.success is True
        assert result.data["panel_id"] == "filePreview"
        assert result.data["props"]["fileId"] == "file_1"

    @pytest.mark.asyncio
    async def test_show_panel_without_props(self, primitives):
        """Test panel display without props."""
        result = await primitives.show_panel("contactCard")

        assert result.success is True
        assert result.data["props"] is None

    @pytest.mark.asyncio
    async def test_show_panel_emits_events(self, primitives):
        """Test that showPanel emits correct events."""
        result = await primitives.show_panel("meetingJoin", {"meetingId": "m1"})

        # Should have: starting, show-panel, success
        assert len(result.events) == 3

        assert isinstance(result.events[1], ShowPanelEvent)
        assert result.events[1].panel_id == "meetingJoin"
        assert result.events[1].props["meetingId"] == "m1"

    @pytest.mark.asyncio
    async def test_show_panel_empty_id_fails(self, primitives):
        """Test that empty panel ID fails."""
        result = await primitives.show_panel("")

        assert result.success is False
        assert "non-empty string" in result.error


class TestPrimitivesNavigate:
    """Tests for the navigate primitive."""

    @pytest.fixture
    def primitives(self):
        """Get a Primitives instance with fresh DB."""
        reset_fakedb()
        return Primitives()

    @pytest.mark.asyncio
    async def test_navigate_success(self, primitives):
        """Test successful navigation."""
        result = await primitives.navigate("/kmeet")

        assert result.success is True
        assert result.data["route"] == "/kmeet"

    @pytest.mark.asyncio
    async def test_navigate_emits_events(self, primitives):
        """Test that navigate emits correct events."""
        result = await primitives.navigate("/kdrive/files/folder_1")

        # Should have: starting, navigate, success
        assert len(result.events) == 3

        assert isinstance(result.events[1], NavigateEvent)
        assert result.events[1].route == "/kdrive/files/folder_1"

    @pytest.mark.asyncio
    async def test_navigate_empty_route_fails(self, primitives):
        """Test that empty route fails."""
        result = await primitives.navigate("")

        assert result.success is False
        assert "non-empty string" in result.error


class TestPrimitivesToast:
    """Tests for the toast primitive."""

    @pytest.fixture
    def primitives(self):
        """Get a Primitives instance with fresh DB."""
        reset_fakedb()
        return Primitives()

    @pytest.mark.asyncio
    async def test_toast_info(self, primitives):
        """Test info toast (default type)."""
        result = await primitives.toast("File uploaded")

        assert result.success is True
        assert result.data["message"] == "File uploaded"
        assert result.data["type"] == "info"

    @pytest.mark.asyncio
    async def test_toast_error(self, primitives):
        """Test error toast."""
        result = await primitives.toast("Something went wrong", "error")

        assert result.success is True
        assert result.data["type"] == "error"

    @pytest.mark.asyncio
    async def test_toast_emits_events(self, primitives):
        """Test that toast emits correct events."""
        result = await primitives.toast("Saved!", "success")

        # Should have: starting, toast, success
        assert len(result.events) == 3

        assert isinstance(result.events[1], ToastEvent)
        assert result.events[1].message == "Saved!"
        assert result.events[1].toast_type == ToastType.SUCCESS

    @pytest.mark.asyncio
    async def test_toast_invalid_type_fails(self, primitives):
        """Test that invalid toast type fails."""
        result = await primitives.toast("Hello", "invalid_type")

        assert result.success is False
        assert "Must be one of" in result.error

    @pytest.mark.asyncio
    async def test_toast_empty_message_fails(self, primitives):
        """Test that empty message fails."""
        result = await primitives.toast("")

        assert result.success is False
        assert "non-empty string" in result.error


class TestToolResultStructure:
    """Tests for ToolResult structure."""

    def test_tool_result_defaults(self):
        """Test ToolResult default values."""
        result = ToolResult(success=True)

        assert result.success is True
        assert result.data is None
        assert result.error is None
        assert result.events == []

    def test_tool_result_with_all_fields(self):
        """Test ToolResult with all fields."""
        events = [ToolStatusEvent("test", ToolStatus.SUCCESS, "done")]
        result = ToolResult(
            success=False,
            data={"key": "value"},
            error="Test error",
            events=events,
        )

        assert result.success is False
        assert result.data == {"key": "value"}
        assert result.error == "Test error"
        assert len(result.events) == 1
