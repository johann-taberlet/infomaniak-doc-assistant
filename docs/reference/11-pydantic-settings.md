# Pydantic Settings

## Configuration avec BaseSettings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM Provider
    LLM_PROVIDER: str = "ollama"

    # Ollama
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_CHAT_MODEL: str = "qwen3:8b"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    # Qdrant
    QDRANT_HOST: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "infomaniak_docs"

    # App
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

settings = Settings()
```

## Utilisation

```python
from app.config import settings

print(settings.OLLAMA_HOST)
print(settings.LLM_PROVIDER)
```

## Validation Custom

```python
from pydantic import field_validator

class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"

    @field_validator('LOG_LEVEL')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()
```
