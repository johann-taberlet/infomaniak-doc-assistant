"""Factory functions for LLM providers."""

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel

from app.config import settings
from app.llm.base import LLMProvider
from app.llm.ollama_provider import OllamaProvider
from app.llm.openrouter_provider import OpenRouterProvider

# Provider registry for extensibility
_PROVIDERS: dict[str, type[LLMProvider]] = {
    "ollama": OllamaProvider,
    "openrouter": OpenRouterProvider,
}


def get_provider() -> LLMProvider:
    """Return the LLM provider based on configuration.

    Returns:
        LLMProvider: The configured LLM provider instance.

    Raises:
        ValueError: If the configured provider is not supported.
    """
    provider_name = settings.LLM_PROVIDER.lower()
    provider_class = _PROVIDERS.get(provider_name)

    if provider_class is None:
        supported = ", ".join(_PROVIDERS.keys())
        raise ValueError(f"Unsupported LLM provider: {provider_name}. Supported: {supported}")

    return provider_class()


def get_chat_model() -> BaseChatModel:
    """Return the chat model from the configured provider.

    Returns:
        BaseChatModel: A LangChain-compatible chat model.
    """
    return get_provider().get_chat_model()


def get_embeddings() -> Embeddings:
    """Return the embeddings model from the configured provider.

    Returns:
        Embeddings: A LangChain-compatible embeddings model.
    """
    return get_provider().get_embeddings()
