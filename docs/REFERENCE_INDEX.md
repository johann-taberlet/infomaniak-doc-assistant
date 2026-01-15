# Technical Reference Index

Ce fichier liste toutes les références techniques disponibles.
**Lis uniquement les fichiers dont tu as besoin pour la tâche en cours.**

## Références Disponibles

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| `docs/reference/01-langchain-agents.md` | Création d'agents LangChain, @tool decorator, create_react_agent, LCEL | Tâches agent-* |
| `docs/reference/02-rag-pipeline.md` | Chunking, recherche hybride, query expansion | Tâches rag-* |
| `docs/reference/03-qdrant.md` | Client Qdrant, collections, upsert, search | Tâches rag-*, ingest-* |
| `docs/reference/04-ollama.md` | ChatOllama, OllamaEmbeddings, configuration | Tâches llm-*, config-* |
| `docs/reference/05-pydantic.md` | BaseModel, field_validator, model_validator | Tâches models-* |
| `docs/reference/06-fastapi.md` | Endpoints, SSE streaming, middleware, exception handlers | Tâches api-* |
| `docs/reference/07-langfuse.md` | Observabilité, CallbackHandler, @observe | Tâches obs-* |
| `docs/reference/08-embeddings.md` | Modèles d'embeddings, dimensions | Tâches rag-* |
| `docs/reference/09-memory.md` | InMemorySaver, conversation memory, thread_id | Tâches agent-* |
| `docs/reference/10-error-handling.md` | Retry, fallback, health checks | Toutes tâches |
| `docs/reference/11-pydantic-settings.md` | BaseSettings, configuration .env | Tâches config-* |

## Autres Documents

| Fichier | Description |
|---------|-------------|
| `docs/prd.md` | Product Requirements Document - architecture et spécifications |
| `.env.example` | Variables d'environnement disponibles |

## Comment Utiliser

1. Identifie la tâche (ex: `llm-002`)
2. Regarde le préfixe (ex: `llm`)
3. Lis le(s) fichier(s) correspondant(s) dans la colonne "Quand l'utiliser"
4. Implémente en suivant les patterns du fichier
