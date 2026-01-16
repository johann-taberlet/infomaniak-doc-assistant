"""Mistral API LLM provider implementation."""

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings

from app.config import settings
from app.llm.base import LLMProvider


class MistralAPIProvider(LLMProvider):
    """LLM provider using Mistral API."""

    def get_chat_model(self) -> BaseChatModel:
        """Return the Mistral chat model instance.

        Returns:
            BaseChatModel: ChatMistralAI configured with settings.
        """
        return ChatMistralAI(
            model=settings.MISTRAL_CHAT_MODEL,
            api_key=settings.MISTRAL_API_KEY,
            temperature=0.7,
        )

    def get_embeddings(self) -> Embeddings:
        """Return the Mistral embeddings model instance.

        Returns:
            Embeddings: MistralAIEmbeddings configured with settings.
        """
        return MistralAIEmbeddings(
            model=settings.MISTRAL_EMBEDDING_MODEL,
            api_key=settings.MISTRAL_API_KEY,
        )
