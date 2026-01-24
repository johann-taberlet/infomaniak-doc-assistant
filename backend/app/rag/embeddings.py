"""
Embedding provider factory.

Supports multiple embedding providers with a unified interface.
Primary provider: OpenRouter with Qwen embeddings.
"""

from functools import lru_cache
from typing import Protocol

from langchain_openai import OpenAIEmbeddings

from backend.app.core.config import LLMProvider, settings


class EmbeddingProvider(Protocol):
    """Protocol for embedding providers."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of documents."""
        ...

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query."""
        ...


class OpenRouterEmbeddings:
    """OpenRouter embeddings using OpenAI-compatible API."""

    def __init__(
        self,
        api_key: str,
        model: str = "qwen/qwen3-embedding-8b",
        dimensions: int | None = None,
    ):
        """
        Initialize OpenRouter embeddings.

        Args:
            api_key: OpenRouter API key
            model: Model identifier (e.g., "qwen/qwen3-embedding-8b")
            dimensions: Output dimensions (optional, model-specific)
        """
        # OpenRouter uses OpenAI-compatible API
        self._embeddings = OpenAIEmbeddings(
            api_key=api_key,
            model=model,
            base_url="https://openrouter.ai/api/v1",
            # Disable context length checking - OpenRouter handles this
            check_embedding_ctx_length=False,
            dimensions=dimensions,
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of documents."""
        return self._embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query."""
        return self._embeddings.embed_query(text)

    @property
    def model(self) -> str:
        """Get the model name."""
        return self._embeddings.model


class OllamaEmbeddings:
    """Ollama embeddings for local models."""

    def __init__(self, host: str = "http://localhost:11434", model: str = "nomic-embed-text"):
        """
        Initialize Ollama embeddings.

        Args:
            host: Ollama server URL
            model: Model name (e.g., "nomic-embed-text")
        """
        from langchain_ollama import OllamaEmbeddings as LangChainOllamaEmbeddings

        self._embeddings = LangChainOllamaEmbeddings(base_url=host, model=model)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of documents."""
        return self._embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query."""
        return self._embeddings.embed_query(text)

    @property
    def model(self) -> str:
        """Get the model name."""
        return self._embeddings.model


@lru_cache
def get_embeddings(
    provider: LLMProvider | None = None,
    model: str | None = None,
) -> OpenRouterEmbeddings | OllamaEmbeddings:
    """
    Factory function to get embeddings provider.

    Args:
        provider: LLM provider to use (defaults to settings)
        model: Model override (defaults to settings)

    Returns:
        Configured embeddings instance
    """
    provider = provider or settings.llm_provider

    if provider == LLMProvider.OPENROUTER:
        embedding_model = model or settings.openrouter_embedding_model
        return OpenRouterEmbeddings(
            api_key=settings.openrouter_api_key,
            model=embedding_model,
            # Don't specify dimensions - let the model use its native output size
            dimensions=None,
        )
    elif provider == LLMProvider.OLLAMA:
        return OllamaEmbeddings(
            host=settings.ollama_host,
            model=model or settings.ollama_embedding_model,
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_embedding_dimension(provider: LLMProvider | None = None) -> int:
    """
    Get the embedding dimension for the current provider/model.

    Returns:
        Embedding dimension (vector size)
    """
    provider = provider or settings.llm_provider

    # Known dimensions for common models
    dimensions = {
        # OpenRouter models (Qwen3 embedding series)
        "qwen/qwen3-embedding-8b": 4096,
        "qwen/qwen3-embedding-4b": 2560,
        "qwen/qwen3-embedding-0.6b": 1024,
        # Ollama models
        "nomic-embed-text": 768,
        "mxbai-embed-large": 1024,
        "all-minilm": 384,
    }

    if provider == LLMProvider.OPENROUTER:
        model = settings.openrouter_embedding_model
    else:
        model = settings.ollama_embedding_model

    return dimensions.get(model) or settings.rag_vector_dimension
