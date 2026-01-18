# Claude Code Instructions

## Development Tools

- Use `pyright-lsp` for Python type checking
- Use `npm run lint` for frontend linting
- Run `uv run pytest` for backend tests

## Code Conventions

### Python (Backend)

- Use type hints for all function signatures
- Follow PEP 8 style guide
- Use `pydantic` for data validation
- Configuration via `app/config.py` with environment variables

### TypeScript (Frontend)

- Strict TypeScript mode enabled
- Use functional components with hooks
- Export types from dedicated `types.ts` file
- Use CSS modules or dedicated CSS files per component

## Architecture Patterns

### Backend

- LLM providers implement `LLMProvider` base class
- RAG search via `app/agent/tools.py`
- SSE streaming for real-time responses
- Langfuse integration for observability (optional)

### Frontend

- Custom hooks for stateful logic (`useSSEChat`, `useTTS`)
- Streaming UI updates via SSE events
- Component-based UI with dedicated CSS files

## Testing

```bash
# Backend
uv run pytest

# Frontend
cd frontend && npm run build && npm run lint
```
