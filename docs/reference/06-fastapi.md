# FastAPI Async & Streaming

## Application de Base

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

@app.post("/chat")
async def chat(request: ChatRequest):
    response = await agent.ainvoke({"messages": [request.message]})
    return {"response": response}
```

## Lifespan Events

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.agent = get_agent()
    yield
    # Shutdown (cleanup)

app = FastAPI(lifespan=lifespan)
```

## CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Server-Sent Events (SSE)

```python
from fastapi.responses import StreamingResponse
import json

def format_sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"

async def sse_stream(message: str):
    async for chunk in agent.astream({"messages": [message]}):
        yield format_sse({"token": chunk})
    yield format_sse({"done": True})

@app.get("/chat/stream")
async def chat_stream(message: str):
    return StreamingResponse(
        sse_stream(message),
        media_type="text/event-stream"
    )
```

## Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

@app.exception_handler(Exception)
async def general_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal error"})
```

## Static Files

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Health Check

```python
@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
```
