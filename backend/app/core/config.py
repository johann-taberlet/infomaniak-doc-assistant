"""
Application configuration using Pydantic Settings.

All configuration is loaded from environment variables with sensible defaults.
"""

from enum import Enum
from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChunkingStrategy(str, Enum):
    """Available chunking strategies."""

    FULL_DOCUMENT = "full_document"
    RECURSIVE = "recursive"
    SEMANTIC = "semantic"
    SENTENCE_WINDOW = "sentence_window"


class LLMProvider(str, Enum):
    """Available LLM providers."""

    OLLAMA = "ollama"
    OPENROUTER = "openrouter"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # =========================================================================
    # LLM Provider Configuration
    # =========================================================================
    llm_provider: LLMProvider = Field(default=LLMProvider.OPENROUTER)
    llm_temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    # Ollama Configuration
    ollama_host: str = Field(default="http://localhost:11434")
    ollama_chat_model: str = Field(default="qwen3:8b")
    ollama_embedding_model: str = Field(default="nomic-embed-text")

    # OpenRouter Configuration
    openrouter_api_key: str = Field(default="")
    openrouter_chat_model: str = Field(default="qwen/qwen3-8b")
    openrouter_embedding_model: str = Field(default="qwen/qwen3-embedding-4b")
    openrouter_site_url: str = Field(default="https://infomaniak-doc-assistant.demo")
    openrouter_site_name: str = Field(default="Infomaniak Doc Assistant")

    # Judge LLM (for evaluation) - uses a fast, cheap model
    judge_model: str = Field(default="google/gemini-3-flash-preview")

    # Intent Router (for classifying queries as RAG or Action)
    router_model: str = Field(default="mistralai/mistral-nemo")
    router_confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)

    # Generation model for RAG answer generation (evaluation winner: best quality/cost)
    generation_model: str = Field(default="mistralai/mistral-nemo")

    # Fallback model for complex queries (flagship quality)
    fallback_model: str = Field(default="mistralai/mistral-large")

    # =========================================================================
    # Vector Database Configuration
    # =========================================================================
    qdrant_host: str = Field(default="http://localhost:6333")
    qdrant_api_key: str = Field(default="")
    qdrant_collection: str = Field(default="infomaniak_hybrid_full_doc_no_images")

    # =========================================================================
    # RAG Configuration
    # =========================================================================
    chunking_strategy: ChunkingStrategy = Field(default=ChunkingStrategy.FULL_DOCUMENT)
    chunk_size: int = Field(default=1500, ge=100, le=10000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000)
    dataset_path: Literal["cleaned", "cleaned_no_images"] = Field(default="cleaned_no_images")

    # Retrieval settings
    rag_top_k: int = Field(default=5, ge=1, le=50)
    rag_similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    rag_vector_dimension: int = Field(default=2560)  # qwen/qwen3-embedding-4b

    # Sentence window specific settings
    sentence_window_size: int = Field(default=3, ge=1, le=10)

    # =========================================================================
    # Hybrid Search Configuration
    # =========================================================================
    bm25_model: str = Field(default="Qdrant/bm25")
    hyde_model: str = Field(default="mistralai/mistral-nemo")
    hybrid_rrf_k: int = Field(default=60, ge=1, le=200)

    # =========================================================================
    # Observability (Langfuse)
    # =========================================================================
    langfuse_enabled: bool = Field(default=False)
    langfuse_public_key: str = Field(default="")
    langfuse_secret_key: str = Field(default="")
    langfuse_host: str = Field(default="https://cloud.langfuse.com")

    # =========================================================================
    # Application Configuration
    # =========================================================================
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    log_level: str = Field(default="INFO")

    # =========================================================================
    # Skills Configuration
    # =========================================================================
    skills_dir: str = Field(default="skills")

    # =========================================================================
    # Computed Properties
    # =========================================================================
    @computed_field
    @property
    def data_dir(self) -> str:
        """Path to data directory."""
        return "data"

    @computed_field
    @property
    def dataset_full_path(self) -> str:
        """Full path to the selected dataset."""
        return f"{self.data_dir}/{self.dataset_path}"

    def get_collection_name(
        self,
        strategy: ChunkingStrategy | None = None,
        chunk_size: int | None = None,
        dataset: str | None = None,
    ) -> str:
        """
        Generate a collection name based on experiment parameters.

        Format: infomaniak_{strategy}_{chunk_size}_{dataset_suffix}
        """
        strategy = strategy or self.chunking_strategy
        chunk_size = chunk_size or self.chunk_size
        dataset = dataset or self.dataset_path

        # Determine dataset suffix
        dataset_suffix = "images" if dataset == "cleaned" else "no_images"

        # Full document strategy doesn't use chunk size
        if strategy == ChunkingStrategy.FULL_DOCUMENT:
            return f"infomaniak_full_doc_{dataset_suffix}"

        # Semantic strategy doesn't use chunk size
        if strategy == ChunkingStrategy.SEMANTIC:
            return f"infomaniak_semantic_{dataset_suffix}"

        return f"infomaniak_{strategy.value}_{chunk_size}_{dataset_suffix}"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()


# Model pricing (per million tokens) - OpenRouter prices as of Jan 2025
MODEL_PRICING: dict[str, dict[str, float]] = {
    # Budget models
    "mistralai/mistral-nemo": {"input": 0.02, "output": 0.04},
    "qwen/qwen3-8b": {"input": 0.04, "output": 0.14},
    "z-ai/glm-4.7-flash": {"input": 0.07, "output": 0.40},
    # Flagship models
    "mistralai/mistral-large": {"input": 2.00, "output": 6.00},
}
