"""
Tests for configuration defaults.

These tests ensure our configuration matches the evaluation-optimized values.
If any of these fail, it means someone changed defaults that were carefully
selected through benchmarking.
"""

from backend.app.core.config import ChunkingStrategy, Settings


class TestEvaluationDefaults:
    """Verify config defaults match evaluation results."""

    def test_generation_model_is_mistral_nemo(self):
        """
        Evaluation showed Mistral Nemo is the best quality/cost ratio.
        See: docs/evaluations/003-llm-model-evaluation.md
        """
        settings = Settings()
        assert settings.generation_model == "mistralai/mistral-nemo"

    def test_fallback_model_is_mistral_large(self):
        """
        Mistral Large is the flagship fallback for complex queries.
        See: docs/evaluations/003-llm-model-evaluation.md
        """
        settings = Settings()
        assert settings.fallback_model == "mistralai/mistral-large"

    def test_chunking_strategy_is_full_document(self):
        """
        Evaluation showed full_document beats recursive chunking for FAQs.
        See: docs/evaluations/002-chunking-strategy-evaluation.md
        """
        settings = Settings()
        assert settings.chunking_strategy == ChunkingStrategy.FULL_DOCUMENT

    def test_dataset_is_no_images(self):
        """
        Evaluation showed cleaned_no_images gives cleaner retrieval.
        See: docs/evaluations/001-data-cleaning-evaluation.md
        """
        settings = Settings()
        assert settings.dataset_path == "cleaned_no_images"

    def test_vector_dimension_matches_embedding_model(self):
        """
        qwen/qwen3-embedding-4b outputs 2560 dimensions.
        Using wrong dimension would cause Qdrant errors.
        """
        settings = Settings()
        assert settings.rag_vector_dimension == 2560
        assert settings.openrouter_embedding_model == "qwen/qwen3-embedding-4b"

    def test_collection_name_matches_best_config(self):
        """
        Default collection should be the hybrid full_doc collection
        that won in retrieval evaluation.
        See: docs/evaluations/005-retrieval-enhancement-evaluation.md
        """
        settings = Settings()
        assert settings.qdrant_collection == "infomaniak_hybrid_full_doc_no_images"


class TestCollectionNameGeneration:
    """Test collection name generation logic."""

    def test_full_document_no_images(self):
        """Full document strategy should not include chunk size."""
        settings = Settings()
        name = settings.get_collection_name(
            strategy=ChunkingStrategy.FULL_DOCUMENT,
            dataset="cleaned_no_images",
        )
        assert name == "infomaniak_full_doc_no_images"

    def test_full_document_with_images(self):
        """Should use 'images' suffix for cleaned dataset."""
        settings = Settings()
        name = settings.get_collection_name(
            strategy=ChunkingStrategy.FULL_DOCUMENT,
            dataset="cleaned",
        )
        assert name == "infomaniak_full_doc_images"

    def test_recursive_includes_chunk_size(self):
        """Recursive strategy should include chunk size in name."""
        settings = Settings()
        name = settings.get_collection_name(
            strategy=ChunkingStrategy.RECURSIVE,
            chunk_size=1500,
            dataset="cleaned_no_images",
        )
        assert name == "infomaniak_recursive_1500_no_images"
