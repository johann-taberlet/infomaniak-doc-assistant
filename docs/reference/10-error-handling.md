# Error Handling & Resilience

## Retry avec Tenacity

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_llm(messages):
    return llm.invoke(messages)
```

## LangChain with_retry

```python
llm_with_retry = llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
```

## Fallback avec Modèle Alternatif

```python
primary_llm = ChatOllama(model="qwen3:8b")
fallback_llm = ChatOllama(model="qwen3:4b")

llm_with_fallback = primary_llm.with_fallbacks([fallback_llm])
```

## Health Check Ollama

```python
import httpx

def check_ollama_health(base_url: str = "http://localhost:11434") -> bool:
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False
```

## Input Validation

```python
from pydantic import BaseModel, field_validator

class ChatInput(BaseModel):
    message: str

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Message cannot be empty')
        if len(v) > 5000:
            raise ValueError('Message too long')
        return v
```
