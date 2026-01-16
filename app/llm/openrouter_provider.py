"""OpenRouter LLM provider implementation.

OpenRouter provides access to multiple LLM providers through a unified API.
Uses the OpenAI-compatible endpoint for easy integration.

Supports both chat models and embedding models via OpenRouter's API.
"""

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.config import settings
from app.llm.base import LLMProvider


class OpenRouterProvider(LLMProvider):
    """LLM provider using OpenRouter API.

    OpenRouter provides access to models from OpenAI, Anthropic, Google,
    Meta, Mistral, Qwen and others through a single API.
    """

    def get_chat_model(self) -> BaseChatModel:
        """Return the OpenRouter chat model instance.

        Returns:
            BaseChatModel: ChatOpenAI configured for OpenRouter.
        """
        return ChatOpenAI(
            model=settings.OPENROUTER_CHAT_MODEL,
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.7,
            default_headers={
                "HTTP-Referer": settings.OPENROUTER_SITE_URL,
                "X-Title": settings.OPENROUTER_SITE_NAME,
            },
        )

    def get_embeddings(self) -> Embeddings:
        """Return the OpenRouter embeddings model instance.

        Uses OpenRouter's embedding API with the configured model.

        Returns:
            Embeddings: OpenAIEmbeddings configured for OpenRouter.
        """
        return OpenAIEmbeddings(
            model=settings.OPENROUTER_EMBEDDING_MODEL,
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
        )
