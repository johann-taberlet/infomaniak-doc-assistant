"""
Query processing for enhanced retrieval.

Provides:
- BM25 vocabulary normalization for kSuite terms
- HyDE (Hypothetical Document Embeddings) query expansion
"""

import re

from langfuse import observe

from backend.app.core.config import settings


# kSuite vocabulary normalization patterns
# BM25 tokenizers split on camelCase/special chars, so "kDrive" becomes separate tokens
# We normalize to space-separated form for better BM25 matching
KSUITE_NORMALIZATIONS = {
    # Products
    r"\bkDrive\b": "k Drive",
    r"\bkMeet\b": "k Meet",
    r"\bkChat\b": "k Chat",
    r"\bkSuite\b": "k Suite",
    r"\bkMail\b": "k Mail",
    r"\bkCalendar\b": "k Calendar",
    r"\bInfomaniak\b": "Infomaniak",
    # Common terms
    r"\bSwissTransfer\b": "Swiss Transfer",
    r"\bWebDAV\b": "Web DAV",
}


class QueryProcessor:
    """
    Processes queries for improved retrieval.

    Supports:
    - BM25-friendly vocabulary normalization
    - HyDE hypothetical document generation
    """

    def __init__(
        self,
        hyde_model: str | None = None,
        enable_hyde: bool = False,
        enable_normalization: bool = False,
    ):
        """
        Initialize query processor.

        Args:
            hyde_model: Model for HyDE generation (defaults to settings.hyde_model)
            enable_hyde: Whether to generate hypothetical documents
            enable_normalization: Whether to normalize queries for BM25
        """
        self.hyde_model = hyde_model or settings.hyde_model
        self.enable_hyde = enable_hyde
        self.enable_normalization = enable_normalization
        self._llm = None

    def _get_llm(self):
        """Lazy-load LLM for HyDE generation."""
        if self._llm is None:
            from langchain_openai import ChatOpenAI

            self._llm = ChatOpenAI(
                api_key=settings.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
                model=self.hyde_model,
                temperature=0.7,
                max_tokens=300,
            )
        return self._llm

    @observe(name="normalize_for_bm25")
    def normalize_for_bm25(self, text: str) -> str:
        """
        Normalize text for better BM25 matching.

        Transforms kSuite compound words into space-separated tokens
        that BM25 tokenizers can match properly.

        Args:
            text: Input text (query or document)

        Returns:
            Normalized text with split compound words

        Example:
            "kDrive sync" -> "k Drive sync"
        """
        result = text
        for pattern, replacement in KSUITE_NORMALIZATIONS.items():
            result = re.sub(pattern, replacement, result)
        return result

    @observe(name="generate_hyde_document")
    def generate_hyde_document(self, query: str) -> str:
        """
        Generate a hypothetical document that answers the query.

        HyDE (Hypothetical Document Embeddings) improves retrieval by
        embedding a synthetic answer that contains relevant vocabulary,
        rather than the short query text.

        Args:
            query: User's question

        Returns:
            Hypothetical document text

        Reference:
            https://arxiv.org/abs/2212.10496
        """
        llm = self._get_llm()

        prompt = f"""You are a technical documentation writer for Infomaniak's kSuite products (kDrive, kMeet, kChat).

Given the following question, write a short technical documentation passage that would answer it.
Use the exact terminology found in kSuite documentation (kDrive, sync, share, collaboration, etc.).
Keep the response under 150 words and factual.

Question: {query}

Documentation passage:"""

        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    @observe(name="process_query")
    def process_query(self, query: str) -> dict[str, str]:
        """
        Process a query for retrieval.

        Returns different query representations based on enabled features:
        - original: The original query
        - normalized: BM25-normalized query (if enabled)
        - hyde: Hypothetical document (if enabled)

        Args:
            query: User's question

        Returns:
            Dictionary with query variants
        """
        result = {"original": query}

        if self.enable_normalization:
            result["normalized"] = self.normalize_for_bm25(query)

        if self.enable_hyde:
            result["hyde"] = self.generate_hyde_document(query)

        return result

    def get_search_query(self, query: str, for_sparse: bool = False) -> str:
        """
        Get the appropriate query text for search.

        Args:
            query: Original user query
            for_sparse: If True, return normalized query for BM25

        Returns:
            Query text to use for embedding/search
        """
        if self.enable_hyde:
            # HyDE document is used for dense search
            if not for_sparse:
                return self.generate_hyde_document(query)

        if for_sparse and self.enable_normalization:
            return self.normalize_for_bm25(query)

        return query
