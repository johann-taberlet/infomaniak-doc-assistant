# Infomaniak Doc Assistant - Frontend

React frontend for the Infomaniak Documentation AI Assistant.

## Tech Stack

- React 19
- TypeScript
- Vite
- ONNX Runtime Web (for TTS)

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

## Build

```bash
npm run build
```

## Features

- Server-Sent Events (SSE) streaming for real-time responses
- Rich UI components (step guides, source cards, quick actions)
- Text-to-Speech with WebGPU/WASM acceleration
- Markdown rendering with syntax highlighting

## Project Structure

```
src/
├── components/
│   ├── ui/                 # UI components
│   │   ├── Markdown.tsx    # Markdown renderer
│   │   ├── SourceCards.tsx # Source citations
│   │   ├── QuickActions.tsx
│   │   └── StreamingStepGuide.tsx
│   └── MessageRenderer.tsx # Message display
├── hooks/
│   ├── useSSEChat.ts       # SSE chat hook
│   └── useTTS.ts           # Text-to-speech hook
├── utils/
│   ├── tts.ts              # TTS utilities
│   └── text.ts             # Text utilities
└── types.ts                # TypeScript types
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run lint` | Run ESLint |
| `npm run preview` | Preview production build |
