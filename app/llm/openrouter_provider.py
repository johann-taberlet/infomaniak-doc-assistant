"""OpenRouter LLM provider implementation.

OpenRouter provides access to multiple LLM providers through a unified API.
Uses the OpenAI-compatible endpoint for easy integration.

Supports both chat models and embedding models via OpenRouter's API.
"""

from openai import OpenAI

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.config import settings
from app.llm.base import LLMProvider


class OpenRouterEmbeddings(Embeddings):
    """Custom embeddings class for OpenRouter API.

    Uses the OpenAI SDK directly to properly support encoding_format parameter
    required by OpenRouter's embedding models.
    """

    def __init__(self, model: str, api_key: str, site_url: str, site_name: str):
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.site_url = site_url
        self.site_name = site_name

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of documents."""
        response = self.client.embeddings.create(
            extra_headers={
                "HTTP-Referer": self.site_url,
                "X-Title": self.site_name,
            },
            model=self.model,
            input=texts,
            encoding_format="float",
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query."""
        return self.embed_documents([text])[0]


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

        Returns:
            Embeddings: OpenRouterEmbeddings configured for the embedding model.
        """
        return OpenRouterEmbeddings(
            model=settings.OPENROUTER_EMBEDDING_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            site_url=settings.OPENROUTER_SITE_URL,
            site_name=settings.OPENROUTER_SITE_NAME,
        )
