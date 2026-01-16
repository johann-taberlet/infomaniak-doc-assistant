"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel


class LLMProvider(ABC):
    """Abstract base class for LLM providers.

    Subclasses must implement get_chat_model() and get_embeddings()
    to provide their specific LLM and embedding implementations.
    """

    @abstractmethod
    def get_chat_model(self) -> BaseChatModel:
        """Return the chat model instance.

        Returns:
            BaseChatModel: A LangChain-compatible chat model.
        """
        ...

    @abstractmethod
    def get_embeddings(self) -> Embeddings:
        """Return the embeddings model instance.

        Returns:
            Embeddings: A LangChain-compatible embeddings model.
        """
        ...
