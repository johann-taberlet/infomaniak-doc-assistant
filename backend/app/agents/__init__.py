"""
Agents module for intent routing and action execution.

This module provides:
- IntentRouter: Classifies user queries as RAG or Action
- Intent: Classification result with type, confidence, and skill
- IntentType: Enum for intent types (rag, action)
- SkillInfo: Metadata about available skills
"""

from backend.app.agents.router import Intent, IntentRouter, IntentType, SkillInfo

__all__ = ["IntentRouter", "Intent", "IntentType", "SkillInfo"]
