# Pydantic Validation

## Modèles de Base

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
```

## Field Validator

```python
from pydantic import BaseModel, field_validator

class UserQuery(BaseModel):
    query: str

    @field_validator('query')
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()
```

## Model Validator (Cross-field)

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode='after')
    def check_dates_order(self) -> 'DateRange':
        if self.start_date > self.end_date:
            raise ValueError('start_date must be before end_date')
        return self
```

## Validation JSON

```python
from pydantic import ValidationError

try:
    request = ChatRequest.model_validate_json(raw_json)
except ValidationError as e:
    for error in e.errors():
        print(f"Erreur: {error['loc']} - {error['msg']}")
```

## Méthodes Principales

| Méthode | Description |
|---------|-------------|
| `Model.model_validate(data)` | Valide un dict |
| `model.model_dump()` | Sérialise en dict |
| `model.model_dump_json()` | Sérialise en JSON |
| `Model.model_validate_json(json)` | Valide depuis JSON |
