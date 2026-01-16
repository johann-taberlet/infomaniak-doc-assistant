from langfuse.langchain import CallbackHandler

from app.config import settings


def get_langfuse_handler() -> CallbackHandler | None:
    """Get Langfuse callback handler for LangChain observability.

    Returns:
        CallbackHandler if LANGFUSE_ENABLED is true, None otherwise.
    """
    if not settings.LANGFUSE_ENABLED:
        return None

    return CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_HOST,
    )
