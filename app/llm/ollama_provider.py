"""Ollama LLM provider implementation."""

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama, OllamaEmbeddings

from app.config import settings
from app.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    """LLM provider using local Ollama server."""

    def get_chat_model(self) -> BaseChatModel:
        """Return the Ollama chat model instance.

        Returns:
            BaseChatModel: ChatOllama configured with settings.
        """
        return ChatOllama(
            model=settings.OLLAMA_CHAT_MODEL,
            base_url=settings.OLLAMA_HOST,
            temperature=settings.LLM_TEMPERATURE,
            num_ctx=4096,
        )

    def get_embeddings(self) -> Embeddings:
        """Return the Ollama embeddings model instance.

        Returns:
            Embeddings: OllamaEmbeddings configured with settings.
        """
        return OllamaEmbeddings(
            model=settings.OLLAMA_EMBEDDING_MODEL,
            base_url=settings.OLLAMA_HOST,
        )
