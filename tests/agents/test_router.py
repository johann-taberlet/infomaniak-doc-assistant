"""
Tests for Intent Router.

Tests classification of user queries as RAG or Action intents.
"""

import time
from unittest.mock import MagicMock, patch

import pytest

from backend.app.agents.router import (
    DEFAULT_SKILLS,
    Intent,
    IntentClassificationError,
    IntentRouter,
    IntentType,
    SkillInfo,
    get_available_skills,
)


class TestIntentType:
    """Tests for IntentType enum."""

    def test_rag_value(self):
        assert IntentType.RAG.value == "rag"

    def test_action_value(self):
        assert IntentType.ACTION.value == "action"


class TestIntent:
    """Tests for Intent dataclass."""

    def test_is_action_true(self):
        """High confidence action should return True."""
        intent = Intent(type=IntentType.ACTION, confidence=0.9, skill="start-meeting")
        assert intent.is_action() is True

    def test_is_action_low_confidence(self):
        """Low confidence action should return False."""
        intent = Intent(type=IntentType.ACTION, confidence=0.5, skill="start-meeting")
        assert intent.is_action() is False

    def test_is_action_rag_type(self):
        """RAG type should return False even with high confidence."""
        intent = Intent(type=IntentType.RAG, confidence=0.95)
        assert intent.is_action() is False

    def test_intent_with_reasoning(self):
        """Intent should store reasoning."""
        intent = Intent(
            type=IntentType.RAG,
            confidence=0.9,
            reasoning="This is a documentation question",
        )
        assert intent.reasoning == "This is a documentation question"


class TestSkillInfo:
    """Tests for SkillInfo dataclass."""

    def test_skill_info_creation(self):
        skill = SkillInfo(
            name="test-skill",
            description="A test skill",
            trigger_phrases=["do test", "run test"],
        )
        assert skill.name == "test-skill"
        assert skill.description == "A test skill"
        assert len(skill.trigger_phrases) == 2

    def test_default_skills_exist(self):
        """Default skills should be defined."""
        assert len(DEFAULT_SKILLS) >= 3
        skill_names = [s.name for s in DEFAULT_SKILLS]
        assert "start-meeting" in skill_names
        assert "share-file" in skill_names
        assert "send-message" in skill_names

    def test_get_available_skills(self):
        """get_available_skills should return default skills."""
        skills = get_available_skills()
        assert skills == DEFAULT_SKILLS


class TestIntentRouterParsing:
    """Tests for IntentRouter response parsing."""

    @pytest.fixture
    def router(self):
        """Create router without LLM for parsing tests."""
        with patch.object(IntentRouter, "__init__", lambda self, **kwargs: None):
            router = IntentRouter()
            router.model = "test-model"
            return router

    def test_parse_rag_response(self, router):
        """Should parse RAG response correctly."""
        response = '{"type": "rag", "confidence": 0.95, "skill": null, "reasoning": "Documentation question"}'
        intent = router._parse_response(response)
        assert intent.type == IntentType.RAG
        assert intent.confidence == 0.95
        assert intent.skill is None
        assert intent.reasoning == "Documentation question"

    def test_parse_action_response(self, router):
        """Should parse action response correctly."""
        response = '{"type": "action", "confidence": 0.88, "skill": "start-meeting", "reasoning": "Imperative command"}'
        intent = router._parse_response(response)
        assert intent.type == IntentType.ACTION
        assert intent.confidence == 0.88
        assert intent.skill == "start-meeting"

    def test_parse_markdown_code_block(self, router):
        """Should handle markdown code blocks."""
        response = '```json\n{"type": "rag", "confidence": 0.9, "skill": null, "reasoning": "test"}\n```'
        intent = router._parse_response(response)
        assert intent.type == IntentType.RAG
        assert intent.confidence == 0.9

    def test_parse_invalid_json_defaults_to_rag(self, router):
        """Invalid JSON should default to RAG."""
        response = "This is not valid JSON"
        intent = router._parse_response(response)
        assert intent.type == IntentType.RAG
        assert intent.confidence == 0.5
        assert "Parse error" in intent.reasoning

    def test_parse_clamps_confidence(self, router):
        """Confidence should be clamped to 0-1."""
        response = '{"type": "rag", "confidence": 1.5, "skill": null, "reasoning": "test"}'
        intent = router._parse_response(response)
        assert intent.confidence == 1.0

        response = '{"type": "rag", "confidence": -0.5, "skill": null, "reasoning": "test"}'
        intent = router._parse_response(response)
        assert intent.confidence == 0.0

    def test_parse_null_string_skill(self, router):
        """Skill "null" string should become None."""
        response = '{"type": "rag", "confidence": 0.9, "skill": "null", "reasoning": "test"}'
        intent = router._parse_response(response)
        assert intent.skill is None

    def test_parse_empty_skill(self, router):
        """Empty skill string should become None."""
        response = '{"type": "rag", "confidence": 0.9, "skill": "", "reasoning": "test"}'
        intent = router._parse_response(response)
        assert intent.skill is None


class TestIntentRouterPrompt:
    """Tests for prompt building."""

    @pytest.fixture
    def router(self):
        """Create router without LLM for prompt tests."""
        with patch.object(IntentRouter, "__init__", lambda self, **kwargs: None):
            router = IntentRouter()
            router.model = "test-model"
            return router

    def test_build_prompt_includes_query(self, router):
        """Prompt should include the query."""
        prompt = router._build_prompt("How do I share a file?", DEFAULT_SKILLS)
        assert "How do I share a file?" in prompt

    def test_build_prompt_includes_skills(self, router):
        """Prompt should include available skills."""
        prompt = router._build_prompt("test query", DEFAULT_SKILLS)
        assert "start-meeting" in prompt
        assert "share-file" in prompt
        assert "send-message" in prompt

    def test_build_prompt_includes_history(self, router):
        """Prompt should include conversation history."""
        history = [
            {"role": "user", "content": "Previous question"},
            {"role": "assistant", "content": "Previous answer"},
        ]
        prompt = router._build_prompt("new query", DEFAULT_SKILLS, history)
        assert "Previous question" in prompt
        assert "Previous answer" in prompt

    def test_build_prompt_truncates_long_history(self, router):
        """Long history messages should be truncated."""
        history = [
            {"role": "user", "content": "x" * 500},
        ]
        prompt = router._build_prompt("query", DEFAULT_SKILLS, history)
        # Should be truncated to 200 chars
        assert "x" * 200 in prompt
        assert "x" * 201 not in prompt


class TestIntentRouterClassify:
    """Tests for classify method with mocked LLM."""

    @pytest.fixture
    def mock_router(self):
        """Create router with mocked LLM."""
        with patch.object(IntentRouter, "__init__", lambda self, **kwargs: None):
            router = IntentRouter()
            router.model = "test-model"
            router._llm = MagicMock()
            return router

    def test_classify_empty_query(self, mock_router):
        """Empty query should return RAG with high confidence."""
        intent = mock_router.classify("")
        assert intent.type == IntentType.RAG
        assert intent.confidence == 1.0
        assert "Empty query" in intent.reasoning

    def test_classify_whitespace_query(self, mock_router):
        """Whitespace-only query should return RAG."""
        intent = mock_router.classify("   ")
        assert intent.type == IntentType.RAG
        assert intent.confidence == 1.0

    def test_classify_calls_llm(self, mock_router):
        """Should call LLM for non-empty queries."""
        mock_router._llm.invoke.return_value.content = (
            '{"type": "rag", "confidence": 0.9, "skill": null, "reasoning": "test"}'
        )
        intent = mock_router.classify("How do I share?")
        mock_router._llm.invoke.assert_called_once()
        assert intent.type == IntentType.RAG

    def test_classify_with_custom_skills(self, mock_router):
        """Should use provided skills."""
        mock_router._llm.invoke.return_value.content = (
            '{"type": "action", "confidence": 0.9, "skill": "custom-skill", "reasoning": "test"}'
        )
        custom_skills = [SkillInfo(name="custom-skill", description="Custom action")]
        intent = mock_router.classify("Do custom thing", available_skills=custom_skills)
        assert intent.skill == "custom-skill"


class TestIntentRouterRetry:
    """Tests for retry behavior and error handling."""

    @pytest.fixture
    def mock_router(self):
        """Create router with mocked LLM."""
        with patch.object(IntentRouter, "__init__", lambda self, **kwargs: None):
            router = IntentRouter()
            router.model = "test-model"
            router._llm = MagicMock()
            return router

    def test_retry_succeeds_after_transient_failure(self, mock_router):
        """Should retry and succeed after transient failure."""
        mock_router._llm.invoke.side_effect = [
            Exception("API timeout"),
            MagicMock(content='{"type": "rag", "confidence": 0.9, "skill": null, "reasoning": "ok"}'),
        ]
        with patch("backend.app.agents.router.RETRY_DELAY_SECONDS", 0):
            intent = mock_router.classify("test query")
        assert intent.type == IntentType.RAG
        assert mock_router._llm.invoke.call_count == 2

    def test_raises_exception_after_all_retries_exhausted(self, mock_router):
        """Should raise IntentClassificationError after all retries fail."""
        mock_router._llm.invoke.side_effect = Exception("Persistent failure")
        with patch("backend.app.agents.router.RETRY_DELAY_SECONDS", 0):
            with patch("backend.app.agents.router.MAX_RETRIES", 3):
                with pytest.raises(IntentClassificationError) as exc_info:
                    mock_router.classify("test query")
        assert "Persistent failure" in str(exc_info.value)
        assert mock_router._llm.invoke.call_count == 3

    def test_exception_contains_retry_count(self, mock_router):
        """Exception message should mention retry count."""
        mock_router._llm.invoke.side_effect = Exception("Network error")
        with patch("backend.app.agents.router.RETRY_DELAY_SECONDS", 0):
            with patch("backend.app.agents.router.MAX_RETRIES", 2):
                with pytest.raises(IntentClassificationError) as exc_info:
                    mock_router.classify("test query")
        assert "2 retries" in str(exc_info.value)


@pytest.mark.integration
class TestIntentRouterIntegration:
    """
    Integration tests that call actual LLM.

    Run with: pytest -m integration tests/agents/test_router.py -v
    Requires: OPENROUTER_API_KEY environment variable
    """

    @pytest.fixture
    def router(self):
        """Create real router."""
        return IntentRouter()

    @pytest.mark.parametrize(
        "query,expected_type,expected_skill",
        [
            ("How do I share a file?", IntentType.RAG, None),
            ("What is kMeet?", IntentType.RAG, None),
            ("Can I use kDrive offline?", IntentType.RAG, None),
            ("Start a meeting with John", IntentType.ACTION, "start-meeting"),
            ("Share budget.xlsx with Sarah", IntentType.ACTION, "share-file"),
            ("Send a message to the team", IntentType.ACTION, "send-message"),
            ("Create a video call with David", IntentType.ACTION, "start-meeting"),
            ("Give John access to my folder", IntentType.ACTION, "share-file"),
        ],
    )
    def test_classification_accuracy(self, router, query, expected_type, expected_skill):
        """Test classification accuracy on example queries."""
        start = time.time()
        intent = router.classify(query)
        latency = time.time() - start

        assert intent.type == expected_type, f"Query '{query}' classified as {intent.type}, expected {expected_type}"

        if expected_skill:
            assert intent.skill == expected_skill, f"Query '{query}' got skill {intent.skill}, expected {expected_skill}"

        # Latency check - allow up to 10s for network variability in CI
        assert latency < 10.0, f"Classification took {latency:.2f}s, expected < 10s"

    def test_long_query_no_crash(self, router):
        """Very long query should not crash."""
        long_query = "How do I " + "really " * 100 + "share a file?"
        intent = router.classify(long_query)
        assert intent.type in [IntentType.RAG, IntentType.ACTION]
        assert 0.0 <= intent.confidence <= 1.0
