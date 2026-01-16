# Plan d'Action - Revue de Code

> **Contexte**: Démo pour candidature AI Engineer chez Infomaniak
> Ce document trie les issues identifiées selon leur pertinence pour une démo de qualité professionnelle.

---

## Catégorie A - À Corriger (Impact Fonctionnel ou Qualité Code)

Ces issues affectent soit le fonctionnement de la démo, soit donnent une mauvaise impression du code.

### A1. Performance - QdrantRetriever recréé à chaque requête

**Fichier**: `app/agent/tools.py:18`

**Problème**: Nouvelle instance de QdrantRetriever à chaque appel du tool
```python
@tool(parse_docstring=True)
def search_docs(query: str) -> str:
    retriever = QdrantRetriever()  # Nouvelle connexion à chaque fois
```

**Impact**: Latence inutile, mauvaise pratique visible.

**Action**: Utiliser un singleton ou une instance module-level.

---

### A2. Path Hardcodé - Static Files

**Fichier**: `app/main.py:39`

**Problème**: Path relatif au CWD
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**Impact**: L'UI ne marche pas si on lance depuis un autre répertoire.

**Action**: Utiliser un path absolu basé sur `__file__`.

---

### A3. Type Hints Incomplets

**Fichiers**: `app/rag/chunker.py:7`, `app/main.py` (plusieurs endroits)

**Problème**: `metadata: dict` sans type précis, variables sans annotations.

**Impact**: Donne l'impression de code pas fini pour un poste d'AI Engineer.

**Action**: Compléter les type hints avec `dict[str, Any]`, `dict[str, str]`, etc.

---

### A4. Validation Settings Manquante

**Fichier**: `app/config.py`

**Problème**: Pas de validation sur les valeurs numériques
```python
RAG_CHUNK_SIZE: int = 500      # Devrait être > 0
RAG_CHUNK_OVERLAP: int = 50    # Devrait être < chunk_size
RAG_TOP_K: int = 5             # Devrait être > 0
```

**Impact**: Montre une maîtrise de Pydantic si on ajoute les validators.

**Action**: Ajouter `Field(gt=0)` et validators Pydantic v2.

---

### A5. Langfuse Non Intégré

**Fichier**: `app/agent/executor.py`

**Problème**: `get_langfuse_handler()` existe mais n'est jamais utilisé dans l'agent.

**Impact**: Feature d'observabilité mentionnée mais non fonctionnelle.

**Action**: Intégrer le handler dans `get_agent()` ou supprimer la feature.

---

## Catégorie B - À Documenter par Commentaires

Ces issues sont des préoccupations de production. Ajouter des commentaires `# PRODUCTION:` montre la maturité technique.

### B1. CORS Ouvert

**Fichier**: `app/main.py:31-36`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # PRODUCTION: Restreindre aux domaines autorisés
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### B2. Mémoire Partagée Entre Sessions

**Fichier**: `app/agent/executor.py:12`

```python
# PRODUCTION: Utiliser un checkpointer par session pour l'isolation des utilisateurs
# Options: Redis, PostgreSQL, ou per-request InMemorySaver
_checkpointer = InMemorySaver()
```

---

### B3. Metrics Non Thread-Safe

**Fichier**: `app/main.py:18-22`

```python
# PRODUCTION: Utiliser asyncio.Lock ou une lib de metrics (prometheus_client)
metrics = {
    "request_count": 0,
    "error_count": 0,
}
```

---

### B4. Pas de Rate Limiting

**Fichier**: `app/main.py` (en haut du fichier)

```python
# PRODUCTION: Ajouter rate limiting avec slowapi ou fastapi-limiter
# from slowapi import Limiter
# limiter = Limiter(key_func=get_remote_address)
```

---

### B5. Error Handling Streaming

**Fichier**: `app/main.py:119-135`

```python
async def sse_stream(message: str, session_id: str):
    """Generate SSE events from agent streaming response."""
    # PRODUCTION: Wrapper try/except pour envoyer un event d'erreur au client
    # en cas d'exception pendant le streaming
    agent = get_agent()
    ...
```

---

### B6. Connexion Qdrant Sans Retry

**Fichier**: `app/rag/retriever.py:17-18`

```python
def __init__(self) -> None:
    """Initialize the Qdrant client connection."""
    # PRODUCTION: Ajouter retry logic et health check
    # from tenacity import retry, stop_after_attempt
    self.client = QdrantClient(url=settings.QDRANT_HOST)
```

---

### B7. Validation API Keys

**Fichier**: `app/llm/mistral_provider.py`

```python
def get_chat_model(self) -> BaseChatModel:
    # PRODUCTION: Valider que MISTRAL_API_KEY est non-vide
    # if not settings.MISTRAL_API_KEY:
    #     raise ValueError("MISTRAL_API_KEY is required for Mistral provider")
    return ChatMistralAI(...)
```

---

## Catégorie C - À Ignorer (Non Pertinent pour Démo)

Ces issues ne sont pas pertinentes pour une démo de candidature.

| Issue | Raison d'ignorer |
|-------|------------------|
| Session timeout / memory leak | Démo courte durée |
| Accessibilité frontend (ARIA) | Pas le focus du poste |
| Path traversal ingest.py | Script interne, pas exposé |
| Tests exhaustifs | Quelques tests fonctionnels suffisent |
| Dependencies inutilisées | Nettoyage mineur |
| XSS frontend | Données contrôlées, pas d'input utilisateur malveillant |

---

## Résumé des Actions

### À Faire Maintenant

| # | Action | Fichier | Effort |
|---|--------|---------|--------|
| A1 | Singleton QdrantRetriever | app/agent/tools.py | 5 min |
| A2 | Absolute path static | app/main.py | 2 min |
| A3 | Compléter type hints | Plusieurs | 10 min |
| A4 | Validators Pydantic | app/config.py | 5 min |
| A5 | Intégrer Langfuse | app/agent/executor.py | 5 min |

### Commentaires à Ajouter

| # | Commentaire | Fichier |
|---|-------------|---------|
| B1 | CORS production | app/main.py |
| B2 | Session isolation | app/agent/executor.py |
| B3 | Thread-safe metrics | app/main.py |
| B4 | Rate limiting | app/main.py |
| B5 | Error handling stream | app/main.py |
| B6 | Retry Qdrant | app/rag/retriever.py |
| B7 | Validate API keys | app/llm/mistral_provider.py |

---

## Vérification Finale

Après corrections, vérifier que:

1. **La recherche fonctionne**: `curl -X POST localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"comment partager un fichier"}'`
2. **Les sources sont citées**: Réponse contient des URLs Infomaniak
3. **L'UI marche**: Ouvrir `localhost:8000/static/index.html`
4. **Le streaming fonctionne**: Réponse s'affiche progressivement
5. **Le code est propre**: `uv run ruff check app/`
