"""Tool definitions for LLM integration.

These definitions follow the OpenAI function calling format, which is
widely supported by LLM providers including OpenRouter and Ollama.
"""

from __future__ import annotations

from typing import Any

# Tool definitions in OpenAI function calling format
TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "updateState",
            "description": (
                "Update the frontend application state. Use this to modify "
                "reactive UI state like the current meeting, selected file, "
                "or any other application state."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Dot-notation path to the state key. "
                            "Examples: 'activeApp', 'kmeet.currentMeeting', "
                            "'kdrive.selectedFile'"
                        ),
                    },
                    "value": {
                        "description": (
                            "The new value to set. Can be any JSON-serializable value "
                            "(string, number, boolean, object, array, null)."
                        ),
                    },
                },
                "required": ["path", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "queryDB",
            "description": (
                "Search the fake database for contacts, files, folders, channels, "
                "messages, or meetings. Use this to find information before taking actions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "collection": {
                        "type": "string",
                        "enum": [
                            "contacts",
                            "files",
                            "folders",
                            "channels",
                            "messages",
                            "meetings",
                        ],
                        "description": "The collection to query.",
                    },
                    "filter": {
                        "type": "object",
                        "description": (
                            "Optional filters. Use exact match (e.g., {'name': 'John'}) "
                            "or contains match (e.g., {'name_contains': 'john'} for "
                            "case-insensitive substring search). Multiple filters are "
                            "combined with AND logic."
                        ),
                    },
                },
                "required": ["collection"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "showPanel",
            "description": (
                "Display a UI panel or modal component. Use this to show "
                "file previews, contact details, meeting join dialogs, etc."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "panelId": {
                        "type": "string",
                        "description": (
                            "Identifier for the panel to show. "
                            "Examples: 'filePreview', 'contactCard', 'meetingJoin', "
                            "'shareDialog', 'createFolder'"
                        ),
                    },
                    "props": {
                        "type": "object",
                        "description": (
                            "Properties to pass to the panel component. "
                            "The structure depends on the panel type."
                        ),
                    },
                },
                "required": ["panelId"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "navigate",
            "description": (
                "Navigate to a different route in the application. "
                "Use this to switch between apps or views."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "route": {
                        "type": "string",
                        "description": (
                            "The route to navigate to. "
                            "Examples: '/kmeet', '/kdrive', '/kchat', "
                            "'/kdrive/files/folder_1', '/kchat/channel/general'"
                        ),
                    },
                },
                "required": ["route"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "toast",
            "description": (
                "Show a toast notification to the user. Use this to provide "
                "feedback about completed actions, warnings, or errors."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to display in the toast.",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["info", "success", "warning", "error"],
                        "description": "The type of toast. Defaults to 'info'.",
                    },
                },
                "required": ["message"],
            },
        },
    },
]


def get_tool_by_name(name: str) -> dict[str, Any] | None:
    """Get a tool definition by its function name.

    Args:
        name: The function name to look up

    Returns:
        The tool definition, or None if not found
    """
    for tool in TOOL_DEFINITIONS:
        if tool["function"]["name"] == name:
            return tool
    return None


def get_tool_names() -> list[str]:
    """Get list of all available tool names.

    Returns:
        List of function names
    """
    return [tool["function"]["name"] for tool in TOOL_DEFINITIONS]
