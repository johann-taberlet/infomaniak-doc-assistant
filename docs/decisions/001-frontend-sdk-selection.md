# ADR-001: Frontend SDK Selection for AI Chat & Agentic UI

**Status:** Proposed
**Date:** 2026-01-23
**Decision Makers:** Johann Taberlet

## Context

We are building a kSuite documentation assistant with two phases:
1. **Phase 1**: RAG-based chatbot for documentation Q&A
2. **Phase 2**: Agentic system that interacts with simulated kMeet/kDrive/kChat UIs

Tech stack: **FastAPI backend + Vite React frontend** (not Next.js)

## Options Evaluated

### 1. Vercel AI SDK (`@ai-sdk/react`)
- **Pros**: Production-ready, type-safe tool calling, streaming, works with Vite
- **Cons**: Generative UI (RSC) not available in Vite, Next.js-centric docs
- **Rating**: Excellent for our use case

### 2. CopilotKit + AG-UI Protocol
- **Pros**: Pre-built chat UI, `useCopilotReadable` for state exposure, AG-UI adoption
- **Cons**: API churn, opinionated patterns
- **Rating**: Excellent alternative

### 3. Vercel json-render
- **Pros**: Constrained generative UI, Zod schemas, streaming
- **Cons**: Token costs (JSONL verbose), component lock-in
- **Rating**: Good for specific UI components

### 4. Stately Agent (XState)
- **Pros**: State machine guardrails, visual debugging
- **Cons**: Requires upfront state modeling, overhead
- **Rating**: Good if strict state control needed

### 5. LangGraph + assistant-ui
- **Pros**: Graph-based orchestration, conversation branching
- **Cons**: Backend coupling, complexity
- **Rating**: Good for complex multi-agent flows

## Decision

**Primary: Vercel AI SDK** for streaming and tool calling
**Secondary: json-render** for structured generative UI components

### Rationale

1. **Vercel AI SDK** provides the cleanest abstraction for:
   - Streaming chat responses
   - Tool calling with typed schemas
   - Client-side tool execution (for simulated app actions)
   - Human-in-the-loop approval flows

2. **json-render** complements for:
   - Constrained UI generation (step guides, platform availability)
   - Schema-validated component rendering
   - Progressive streaming of UI elements

3. **Not using CopilotKit** because:
   - We want full control over UI design
   - AG-UI adds conceptual overhead
   - Vercel AI SDK covers our needs

## Implementation Notes

### FastAPI Backend Requirements
Must implement Vercel AI SDK stream protocol:
- Header: `x-vercel-ai-ui-message-stream: v1`
- SSE format with typed messages
- Consider `fastapi-ai-sdk` library

### Simulated App Architecture
```typescript
// Tool definitions for agent actions
const tools = {
  startMeeting: { params: z.object({ title: z.string() }) },
  shareFile: { params: z.object({ fileId: z.string() }) },
  sendMessage: { params: z.object({ channelId: z.string(), text: z.string() }) }
};

// Tool handler updates React state
onToolCall: async ({ toolCall }) => {
  if (toolCall.name === 'startMeeting') {
    setMeetingState({ status: 'active', title: toolCall.args.title });
  }
}
```

## References

- [Vercel AI SDK Docs](https://ai-sdk.dev/docs/introduction)
- [json-render GitHub](https://github.com/vercel-labs/json-render)
- [fastapi-ai-sdk](https://github.com/doganarif/fastapi-ai-sdk)
