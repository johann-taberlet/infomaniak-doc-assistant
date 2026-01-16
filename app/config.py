from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation constraints."""

    # LLM Provider - constrained to supported values
    LLM_PROVIDER: Literal["ollama", "mistral", "qwen", "openrouter"] = "ollama"

    # Ollama Configuration
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_CHAT_MODEL: str = "qwen3:8b"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    # Qwen API Configuration
    QWEN_API_KEY: str = ""
    QWEN_API_BASE: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    QWEN_CHAT_MODEL: str = "qwen-turbo"
    QWEN_EMBEDDING_MODEL: str = "text-embedding-v3"

    # Mistral API Configuration
    MISTRAL_API_KEY: str = ""
    MISTRAL_CHAT_MODEL: str = "mistral-large-latest"
    MISTRAL_EMBEDDING_MODEL: str = "mistral-embed"

    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_CHAT_MODEL: str = "mistralai/ministral-8b"
    OPENROUTER_EMBEDDING_MODEL: str = "qwen/qwen3-embedding-8b"
    OPENROUTER_SITE_URL: str = "https://infomaniak-doc-assistant.demo"
    OPENROUTER_SITE_NAME: str = "Infomaniak Doc Assistant"

    # Qdrant Configuration
    QDRANT_HOST: str = "http://localhost:6333"
    QDRANT_COLLECTION_BASE: str = Field(default="infomaniak_docs", min_length=1)

    @property
    def QDRANT_COLLECTION(self) -> str:
        """Collection name with version and strategy suffix for A/B testing."""
        return f"{self.QDRANT_COLLECTION_BASE}_{self.RAG_ARCHITECTURE_VERSION}_{self.RAG_CHUNK_STRATEGY}"

    def get_embedding_model(self) -> str:
        """Get embedding model based on architecture version."""
        if self.RAG_ARCHITECTURE_VERSION == "v2":
            return "baai/bge-m3"  # BGE-M3 for v2
        return self.OPENROUTER_EMBEDDING_MODEL  # v1 default (qwen3-embedding-8b)

    def get_vector_dimension(self) -> int:
        """Get vector dimension based on architecture version."""
        if self.RAG_ARCHITECTURE_VERSION == "v2":
            return 1024  # BGE-M3 dimension
        return self.RAG_VECTOR_DIMENSION  # v1 default (4096)

    # Application Configuration
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = Field(default=8000, ge=1, le=65535)
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # Observability
    LANGFUSE_ENABLED: bool = False
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    # RAG Architecture Version (for A/B testing)
    RAG_ARCHITECTURE_VERSION: Literal["v1", "v2"] = "v1"

    # RAG Configuration
    RAG_CHUNK_STRATEGY: Literal["split", "document"] = "split"  # "split" or "document" (whole FAQ)
    RAG_CHUNK_SIZE: int = Field(default=1500, gt=0)  # For "split" strategy only
    RAG_CHUNK_OVERLAP: int = Field(default=200, ge=0)  # For "split" strategy only
    RAG_TOP_K: int = Field(default=10, gt=0)  # More candidates for hybrid search
    RAG_SIMILARITY_THRESHOLD: float = Field(default=0.7, ge=0.0, le=1.0)
    RAG_VECTOR_DIMENSION: int = Field(default=4096, gt=0)  # 768 for nomic, 4096 for Qwen3

    # Hybrid Search Configuration
    RAG_HYBRID_ENABLED: bool = True  # Enable BM25 + vector hybrid search
    RAG_BM25_K: int = Field(default=60, gt=0)  # RRF constant (higher = more equal weighting)

    # Reranking Configuration (v2 architecture)
    RAG_RERANK_ENABLED: bool = False  # Enable cross-encoder reranking
    RAG_RERANK_MODEL: str = "BAAI/bge-reranker-v2-m3"  # Open-source multilingual reranker
    RAG_RERANK_TOP_N: int = Field(default=5, gt=0)  # Final docs after reranking

    # Contextual Retrieval (v2 architecture)
    RAG_CONTEXTUAL_ENABLED: bool = False  # Prepend context to chunks before embedding

    # Jina API
    JINA_API_KEY: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
