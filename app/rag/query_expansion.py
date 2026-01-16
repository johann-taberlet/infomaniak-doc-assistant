"""Query expansion with synonyms for improved retrieval."""

import re

# Synonym mappings for common term mismatches
# Format: "search_term": ["synonym1", "synonym2", ...]
SYNONYMS = {
    # kMeet terms
    "livestream": ["broadcast", "live streaming", "stream", "video streaming"],
    "live stream": ["broadcast", "live streaming", "video streaming"],
    "breakout room": ["side room"],
    "breakout rooms": ["side rooms"],
    "record": ["recording", "save meeting", "save video"],
    "recording": ["record", "save meeting"],
    # kDrive terms
    "dropbox": ["drop box"],
    "drop box": ["dropbox", "deposit files"],
    "share a file": ["sharing", "share data", "share link", "public link"],
    "share file": ["sharing", "share data", "share link", "public link"],
    "sharing": ["share", "share link", "public link"],
    # kChat terms
    "webhook": ["integration", "external application", "incoming webhook", "outgoing webhook"],
    "external application": ["webhook", "integration", "connect"],
    "euria": ["ai assistant", "bot", "artificial intelligence", "conversational agent"],
    "ai assistant": ["euria", "bot", "conversational agent"],
    "bot": ["euria", "ai assistant", "conversational agent"],
    # General
    "sync": ["synchronize", "synchronization"],
    "synchronize": ["sync", "synchronization"],
    "install": ["installation", "setup"],
    "create": ["creating", "add", "new"],
}


def expand_query(query: str) -> str:
    """Expand query with synonyms to improve retrieval.

    Detects known terms in the query and appends their synonyms
    to help BM25 match documents using different terminology.

    Args:
        query: The original search query.

    Returns:
        Expanded query with synonyms appended.
    """
    query_lower = query.lower()
    expansions = []

    for term, synonyms in SYNONYMS.items():
        # Check if term appears in query (word boundary aware)
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, query_lower):
            expansions.extend(synonyms)

    if expansions:
        # Append unique synonyms to query
        unique_expansions = list(dict.fromkeys(expansions))
        return query + " " + " ".join(unique_expansions)

    return query
