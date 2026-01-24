"""Tests for LLM tool definitions."""

import pytest

from backend.app.agents.tools import (
    TOOL_DEFINITIONS,
    get_tool_by_name,
    get_tool_names,
)


class TestToolDefinitions:
    """Tests for TOOL_DEFINITIONS structure."""

    def test_all_tools_have_required_structure(self):
        """Each tool must have type=function and function dict with name/description/parameters."""
        for tool in TOOL_DEFINITIONS:
            assert tool["type"] == "function", f"Tool must have type=function"
            assert "function" in tool, f"Tool must have function key"

            func = tool["function"]
            assert "name" in func, f"Function must have name"
            assert "description" in func, f"Function must have description"
            assert "parameters" in func, f"Function must have parameters"

            # Parameters should be a valid JSON schema object
            params = func["parameters"]
            assert params["type"] == "object", f"Parameters must be object type"
            assert "properties" in params, f"Parameters must have properties"

    def test_tool_names_are_unique(self):
        """Tool names must be unique to avoid dispatch ambiguity."""
        names = [tool["function"]["name"] for tool in TOOL_DEFINITIONS]
        assert len(names) == len(set(names)), "Duplicate tool names found"

    def test_required_parameters_are_specified(self):
        """Each tool's required array must contain valid property names."""
        for tool in TOOL_DEFINITIONS:
            func = tool["function"]
            params = func["parameters"]
            properties = params.get("properties", {})
            required = params.get("required", [])

            for req_param in required:
                assert req_param in properties, (
                    f"Tool '{func['name']}' has required param '{req_param}' "
                    f"not in properties"
                )

    def test_expected_tools_exist(self):
        """Verify all 5 expected tools are defined."""
        expected = {"updateState", "queryDB", "showPanel", "navigate", "toast"}
        actual = set(get_tool_names())
        assert expected == actual, f"Missing tools: {expected - actual}"

    def test_tool_descriptions_are_meaningful(self):
        """Tool descriptions should not be empty."""
        for tool in TOOL_DEFINITIONS:
            desc = tool["function"]["description"]
            assert len(desc) > 20, (
                f"Tool '{tool['function']['name']}' has too short description"
            )


class TestGetToolByName:
    """Tests for get_tool_by_name function."""

    def test_finds_existing_tool(self):
        """Test that known tools are found."""
        tool = get_tool_by_name("updateState")
        assert tool is not None
        assert tool["function"]["name"] == "updateState"

    def test_finds_all_tools(self):
        """Test that all tools can be found by name."""
        for name in get_tool_names():
            tool = get_tool_by_name(name)
            assert tool is not None, f"Tool '{name}' not found"
            assert tool["function"]["name"] == name

    def test_returns_none_for_unknown_tool(self):
        """Test that unknown tool names return None."""
        result = get_tool_by_name("nonexistent_tool")
        assert result is None

    def test_case_sensitivity(self):
        """Verify tool lookup is case-sensitive."""
        # Correct case should work
        assert get_tool_by_name("updateState") is not None

        # Wrong case should not find it
        assert get_tool_by_name("updatestate") is None
        assert get_tool_by_name("UPDATESTATE") is None
        assert get_tool_by_name("UpdateState") is None


class TestGetToolNames:
    """Tests for get_tool_names function."""

    def test_returns_all_tool_names(self):
        """Test that all 5 tools are listed."""
        names = get_tool_names()
        assert len(names) == 5

    def test_names_match_definitions(self):
        """Verify returned names match TOOL_DEFINITIONS."""
        names = get_tool_names()
        definition_names = [t["function"]["name"] for t in TOOL_DEFINITIONS]
        assert names == definition_names

    def test_returns_list_of_strings(self):
        """Verify return type is list of strings."""
        names = get_tool_names()
        assert isinstance(names, list)
        assert all(isinstance(n, str) for n in names)


class TestToolParameterDetails:
    """Tests for specific tool parameter definitions."""

    def test_update_state_parameters(self):
        """Test updateState has path and value parameters."""
        tool = get_tool_by_name("updateState")
        params = tool["function"]["parameters"]

        assert "path" in params["properties"]
        assert "value" in params["properties"]
        assert "path" in params["required"]
        assert "value" in params["required"]

    def test_query_db_parameters(self):
        """Test queryDB has collection parameter with enum."""
        tool = get_tool_by_name("queryDB")
        params = tool["function"]["parameters"]

        assert "collection" in params["properties"]
        assert "filter" in params["properties"]
        assert "collection" in params["required"]

        # Collection should have enum of valid collections
        collection = params["properties"]["collection"]
        assert "enum" in collection
        expected_collections = {"contacts", "files", "folders", "channels", "messages", "meetings"}
        assert set(collection["enum"]) == expected_collections

    def test_show_panel_parameters(self):
        """Test showPanel has panelId parameter."""
        tool = get_tool_by_name("showPanel")
        params = tool["function"]["parameters"]

        assert "panelId" in params["properties"]
        assert "props" in params["properties"]
        assert "panelId" in params["required"]

    def test_navigate_parameters(self):
        """Test navigate has route parameter."""
        tool = get_tool_by_name("navigate")
        params = tool["function"]["parameters"]

        assert "route" in params["properties"]
        assert "route" in params["required"]

    def test_toast_parameters(self):
        """Test toast has message and type parameters."""
        tool = get_tool_by_name("toast")
        params = tool["function"]["parameters"]

        assert "message" in params["properties"]
        assert "type" in params["properties"]
        assert "message" in params["required"]

        # Type should have enum of valid toast types
        toast_type = params["properties"]["type"]
        assert "enum" in toast_type
        expected_types = {"info", "success", "warning", "error"}
        assert set(toast_type["enum"]) == expected_types
