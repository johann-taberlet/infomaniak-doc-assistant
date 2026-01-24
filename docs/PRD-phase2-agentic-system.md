# PRD: Phase 2 - Agentic kSuite Assistant

**Version:** 1.0
**Author:** Johann Taberlet
**Date:** 2026-01-24
**Status:** Draft

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Goals & Success Criteria](#2-goals--success-criteria)
3. [Architecture Overview](#3-architecture-overview)
4. [Technical Specifications](#4-technical-specifications)
5. [Implementation Phases](#5-implementation-phases)
6. [Fake App Specifications](#6-fake-app-specifications)
7. [Skills Catalog](#7-skills-catalog)
8. [Testing Strategy](#8-testing-strategy)
9. [Risks & Mitigations](#9-risks--mitigations)

---

## 1. Executive Summary

### 1.1 Context

Phase 1 of the kSuite Documentation Assistant is complete:
- RAG chatbot achieving 76.5% correctness, ~2.8s latency, $0.00009/query
- Hybrid retrieval (dense + BM25) with Qdrant
- Streaming chat with Vercel AI SDK protocol
- Docker one-command deployment

### 1.2 Phase 2 Vision

Transform the assistant from a documentation Q&A bot into an **intelligent agent** that can:

1. **Answer documentation questions** with rich, structured UI components (tables, step guides, cards)
2. **Execute actions** on simulated kSuite apps (kMeet, kDrive, kChat) with visible UI feedback

### 1.3 Key Innovation: Skills Architecture

Instead of implementing many high-level tools, we use a **skills-based approach** inspired by Claude Code:

- **5 low-level primitives**: `updateState`, `queryDB`, `showPanel`, `navigate`, `toast`
- **Skills as markdown files**: Describe how to accomplish complex actions using primitives
- **Agent reads and applies**: LLM loads relevant skill, then executes with judgment

This approach is:
- **Scalable**: Add new actions by writing markdown, not code
- **Debuggable**: Read the skill to understand what agent should do
- **Explainable**: Skills ARE the documentation

---

## 2. Goals & Success Criteria

### 2.1 Functional Goals

| Goal | Description |
|------|-------------|
| **G1** | User can ask documentation questions and receive rich UI responses |
| **G2** | User can request actions and see fake apps respond in real-time |
| **G3** | Chat shows agent "thinking" during action execution |
| **G4** | System correctly routes between RAG and action modes |

### 2.2 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| RAG correctness | >76% (maintain Phase 1) | Evaluation dataset |
| Action success rate | >80% | Manual testing on defined scenarios |
| Intent routing accuracy | >90% | Classification test set |
| End-to-end latency | <5s for actions | Manual timing |
| Error rate | <5% unhandled errors | Error monitoring |

### 2.3 Demo Scenarios

The following scenarios MUST work flawlessly for the recruitment demo:

**RAG Scenarios:**
1. "How do I share a file in kDrive?" → Step-by-step guide with UI
2. "What's the difference between kDrive folder types?" → Comparison table
3. "Can I use kMeet without an account?" → Info card with answer

**Action Scenarios:**
1. "Start a meeting with John" → Opens kMeet, searches contacts, creates meeting
2. "Share my budget.xlsx with the marketing team" → Opens kDrive, finds file, shares it
3. "Send a message to Sarah about the meeting" → Opens kChat, sends message

---

## 3. Architecture Overview

### 3.1 High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER QUERY                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTENT ROUTER (LLM)                                 │
│                    classifyIntent() → "rag" | "action"                       │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                                     │
        ┌───────────┘                                     └───────────┐
        ▼                                                             ▼
┌───────────────────────────────┐                 ┌─────────────────────────────┐
│         RAG PATH              │                 │       ACTION PATH           │
│                               │                 │                             │
│  1. Hybrid retrieval          │                 │  1. Match skill             │
│  2. Generate JSON answer      │                 │  2. Load SKILL.md           │
│     (json-render catalog)     │                 │  3. Execute with primitives │
│  3. Stream → components       │                 │  4. Stream status to chat   │
└───────────────────────────────┘                 └─────────────────────────────┘
        │                                                             │
        ▼                                                             ▼
┌───────────────────────────────┐                 ┌─────────────────────────────┐
│   CHAT: Rich UI Components    │                 │  CHAT: Agent Status         │
│   (Tables, Steps, Cards)      │                 │  + APP PANEL: Fake kSuite   │
└───────────────────────────────┘                 └─────────────────────────────┘
```

### 3.2 Frontend Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              HEADER: kSuite Assistant                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐   │
│  │         CHAT PANEL              │  │         APP PANEL               │   │
│  │                                 │  │                                 │   │
│  │  User: How do I share a file?  │  │  (Hidden when RAG mode)         │   │
│  │                                 │  │                                 │   │
│  │  Assistant:                     │  │  ┌─────────────────────────┐   │   │
│  │  ┌─────────────────────────┐   │  │  │      FAKE kMeet         │   │   │
│  │  │ Step 1: Open kDrive     │   │  │  │                         │   │   │
│  │  │ Step 2: Right-click     │   │  │  │  Meeting: Team Sync     │   │   │
│  │  │ Step 3: Click Share     │   │  │  │  Participants:          │   │   │
│  │  └─────────────────────────┘   │  │  │  • John (connected)     │   │   │
│  │                                 │  │  │  • David (invited)      │   │   │
│  │  OR (action mode):              │  │  │                         │   │   │
│  │                                 │  │  │  [End Meeting]          │   │   │
│  │  🔄 Starting kMeet...           │  │  └─────────────────────────┘   │   │
│  │  🔍 Searching contacts...       │  │                                 │   │
│  │  ✓ Found: John                  │  │                                 │   │
│  │  📞 Creating meeting...         │  │                                 │   │
│  │  ✓ Meeting started!             │  │                                 │   │
│  │                                 │  │                                 │   │
│  └─────────────────────────────────┘  └─────────────────────────────────┘   │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Type your message...]                                            [Send]   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Component Interaction

```
Frontend (React)                    Backend (FastAPI)
─────────────────                   ─────────────────
     │                                    │
     │  POST /api/chat                    │
     │  {messages: [...]}                 │
     │ ──────────────────────────────────>│
     │                                    │
     │                              ┌─────┴─────┐
     │                              │  Router   │
     │                              │  (LLM)    │
     │                              └─────┬─────┘
     │                                    │
     │                         ┌──────────┴──────────┐
     │                         │                     │
     │                    ┌────┴────┐          ┌─────┴─────┐
     │                    │   RAG   │          │  Action   │
     │                    │ Pipeline│          │ Executor  │
     │                    └────┬────┘          └─────┬─────┘
     │                         │                     │
     │   SSE: json chunks      │                     │
     │ <───────────────────────│                     │
     │                         │                     │
     │   SSE: tool status      │                     │
     │ <─────────────────────────────────────────────│
     │                                               │
     │   SSE: state update     │                     │
     │ <─────────────────────────────────────────────│
     │                                               │
  ┌──┴──┐                                            │
  │Render│                                           │
  │ JSON │                                           │
  └──┬──┘                                            │
     │                                               │
  ┌──┴──┐                                            │
  │Update│ <─────── state delta ─────────────────────│
  │ App  │                                           │
  │State │                                           │
  └─────┘
```

---

## 4. Technical Specifications

### 4.1 Low-Level Primitives (5 Tools)

| Tool | Signature | Purpose |
|------|-----------|---------|
| `updateState` | `(path: string, value: any)` | Modify React app state |
| `queryDB` | `(collection: string, filter: object) → results[]` | Search fake database |
| `showPanel` | `(panelId: string, props?: object)` | Display UI component |
| `navigate` | `(route: string)` | Change current view |
| `toast` | `(message: string, type: "info"\|"success"\|"error")` | Show notification |

### 4.2 Stream Protocol

The backend streams events using the Vercel AI SDK Data Stream Protocol with extensions:

```typescript
// Text chunk (standard)
0:"text content"\n

// Tool call start
9:{"toolCallId":"tc_1","toolName":"queryDB","args":{"collection":"contacts"}}\n

// Tool result
a:{"toolCallId":"tc_1","result":{"contacts":[...]}}\n

// Custom: Tool status (for UI feedback)
2:["tool-status",{"tool":"queryDB","status":"executing","message":"Searching contacts..."}]\n

// Custom: State update (for app panel)
2:["state-update",{"path":"kmeet.currentMeeting","value":{...}}]\n

// Done
d:{"finishReason":"stop"}\n
```

### 4.3 json-render Catalog (RAG Mode)

**Implementation:** `frontend/src/lib/catalog.ts` uses Zod schemas for runtime validation.

```typescript
// Actual implementation uses Zod for schema validation
import { z } from 'zod';
import { createCatalog } from '@json-render/core';

const docsCatalog = createCatalog({
  components: {
    // Container for structured answers
    Answer: { props: z.object({ summary: z.string().optional() }), hasChildren: true },

    // Step-by-step procedures
    Steps: { props: z.object({ title: z.string().optional() }), hasChildren: true },
    Step: { props: z.object({
      number: z.number().int().min(1),  // Validated: positive integer
      title: z.string(),
      description: z.string()
    }) },

    // Information cards
    Card: {
      props: z.object({
        title: z.string(),
        type: z.enum(['info', 'warning', 'tip', 'important'])
      }),
      hasChildren: true
    },

    // Data tables
    Table: { props: z.object({ headers: z.array(z.string()), rows: z.array(z.array(z.string())) }) },

    // Feature comparisons
    Comparison: { props: z.object({
      features: z.array(z.string()),
      items: z.array(z.object({ name: z.string(), values: z.array(z.boolean()) }))
    }) },

    // Code blocks
    CodeBlock: { props: z.object({ language: z.string().optional(), code: z.string() }) },

    // Links to related actions (action constrained to catalog actions)
    ActionSuggestion: { props: z.object({
      label: z.string(),
      action: z.enum(['navigate', 'copy', 'openApp']),  // Type-safe action names
      params: z.record(z.string(), z.unknown()).optional()
    }) },

    // Platform availability
    PlatformBadges: { props: z.object({
      platforms: z.array(z.enum(['web', 'ios', 'android', 'macos', 'windows', 'linux']))
    }) },

    // Plain text content (added for flexibility)
    Text: { props: z.object({ content: z.string() }) },
  },
  actions: {
    navigate: z.object({ path: z.string() }),
    copy: z.object({ text: z.string() }),
    openApp: z.object({
      app: z.enum(['kdrive', 'kmeet', 'kchat']),
      action: z.string().optional()
    }),
  },
  validation: 'strict',
});
```

**Design Decisions:**
- **Zod schemas**: Runtime validation prevents malformed JSON from crashing the UI
- **Error boundaries**: `JsonRenderer` wraps content in error boundary for graceful degradation
- **Text component**: Added for simple text content within containers
- **Action type safety**: `ActionSuggestion.action` constrained to defined catalog actions
- **CSS variables**: Infomaniak Design System uses `--ik-*` CSS variables for theming

### 4.4 Fake Database Schema

```typescript
interface FakeDB {
  contacts: Contact[];
  files: File[];
  folders: Folder[];
  meetings: Meeting[];
  channels: Channel[];
  messages: Message[];
}

interface Contact {
  id: string;
  name: string;
  email: string;
  avatar: string;
  status: "online" | "offline" | "busy" | "dnd";
}

interface File {
  id: string;
  name: string;
  type: "document" | "spreadsheet" | "presentation" | "image" | "pdf" | "other";
  folderId: string;
  size: number;
  modifiedAt: string;
  sharedWith: string[]; // contact IDs
}

interface Folder {
  id: string;
  name: string;
  parentId: string | null;
  type: "personal" | "shared" | "common";
}

interface Meeting {
  id: string;
  name: string;
  participants: { contactId: string; status: "invited" | "joined" | "declined" }[];
  status: "scheduled" | "active" | "ended";
  startedAt?: string;
}

interface Channel {
  id: string;
  name: string;
  type: "public" | "private" | "direct";
  members: string[]; // contact IDs
}

interface Message {
  id: string;
  channelId: string;
  senderId: string;
  content: string;
  sentAt: string;
}
```

### 4.5 App State Schema

```typescript
interface AppState {
  // Current view
  activeApp: "none" | "kmeet" | "kdrive" | "kchat";

  // kMeet state
  kmeet: {
    currentMeeting: Meeting | null;
    isJoining: boolean;
  };

  // kDrive state
  kdrive: {
    currentFolder: string; // folder ID
    selectedFiles: string[]; // file IDs
    shareModal: { open: boolean; fileId?: string } | null;
  };

  // kChat state
  kchat: {
    currentChannel: string | null;
    composingMessage: string;
  };
}
```

---

## 5. Implementation Phases

### Overview

```
Phase A: Foundation (Backend)
├── A1: Intent Router
├── A2: Low-Level Primitives
└── A3: Skill Loader

Phase B: RAG Generative UI
├── B1: json-render Setup
├── B2: RAG JSON Generation
└── B3: Component Library

Phase C: Action Execution
├── C1: Skill Files
├── C2: Agent Executor
└── C3: Status Streaming

Phase D: Fake Apps
├── D1: State Management
├── D2: Fake Database
├── D3: kMeet UI
├── D4: kDrive UI
└── D5: kChat UI

Phase E: Integration & Polish
├── E1: Layout Integration
├── E2: Error Handling
└── E3: Demo Scenarios
```

---

### Phase A: Foundation (Backend)

#### A1: Intent Router

**Goal:** Classify user queries as "rag" (documentation question) or "action" (do something).

**Deliverables:**
- `backend/app/agents/router.py` - Intent classification
- Classification prompt
- Test cases

**Implementation:**
```python
class IntentRouter:
    async def classify(self, query: str, history: list[Message]) -> Intent:
        """
        Returns:
        - Intent(type="rag", confidence=0.95)
        - Intent(type="action", skill="start-meeting", confidence=0.87)
        """
```

**Test Cases:**
| Query | Expected Intent | Expected Skill |
|-------|-----------------|----------------|
| "How do I share a file?" | rag | - |
| "What is kMeet?" | rag | - |
| "Start a meeting with John" | action | start-meeting |
| "Share budget.xlsx with Sarah" | action | share-file |
| "Send a message to the team" | action | send-message |

**Acceptance Criteria:**
- [ ] Router correctly classifies 10 test queries
- [ ] Returns confidence score
- [ ] Identifies relevant skill for actions
- [ ] Latency < 500ms

---

#### A2: Low-Level Primitives

**Goal:** Implement 5 tools that the agent uses to interact with the frontend.

**Deliverables:**
- `backend/app/agents/primitives.py` - Tool definitions
- Tool schemas (Pydantic)
- Mock implementations for testing

**Implementation:**
```python
class Primitives:
    async def update_state(self, path: str, value: Any) -> ToolResult
    async def query_db(self, collection: str, filter: dict) -> ToolResult
    async def show_panel(self, panel_id: str, props: dict = None) -> ToolResult
    async def navigate(self, route: str) -> ToolResult
    async def toast(self, message: str, type: str = "info") -> ToolResult
```

**Acceptance Criteria:**
- [ ] All 5 primitives implemented
- [ ] Each returns structured ToolResult
- [ ] State updates emit events for streaming
- [ ] Unit tests pass

---

#### A3: Skill Loader

**Goal:** Load and parse skill markdown files.

**Deliverables:**
- `backend/app/agents/skills.py` - Skill loading logic
- `skills/` directory structure
- Example skill file

**Implementation:**
```python
class SkillLoader:
    def list_skills(self) -> list[SkillMetadata]
    def load_skill(self, skill_name: str) -> Skill
    def match_skill(self, query: str, intent: Intent) -> Skill | None

@dataclass
class SkillMetadata:
    name: str
    description: str
    allowed_tools: list[str]

@dataclass
class Skill:
    metadata: SkillMetadata
    content: str  # Full markdown content
```

**Acceptance Criteria:**
- [ ] Loads skills from `skills/` directory
- [ ] Parses YAML frontmatter
- [ ] Returns skill content for agent context
- [ ] Handles missing skills gracefully

---

### Phase B: RAG Generative UI

#### B1: json-render Setup ✅ COMPLETE

**Goal:** Set up json-render in the frontend.

**Deliverables:**
- Install `@json-render/core` and `@json-render/react`
- `frontend/src/lib/catalog.ts` - Zod-based component catalog with strict validation
- `frontend/src/lib/registry.tsx` - React component registry with Infomaniak Design System
- `frontend/src/lib/JsonRenderer.tsx` - Wrapper with error boundary and action handlers
- `frontend/src/lib/JsonRendererDemo.tsx` - Demo page exercising all components
- `frontend/src/components/ThemeToggle.tsx` - Light/dark/system theme toggle
- Tailwind CSS v4 migration with CSS variables

**Acceptance Criteria:**
- [x] Packages installed (React 19, Tailwind v4, json-render)
- [x] Catalog defined with all components + Text component
- [x] Basic renderer working with test JSON
- [x] Error boundaries prevent crashes from malformed data
- [x] Theme toggle with localStorage persistence (safe for private browsing)
- [x] All components styled with Infomaniak Design System

---

#### B2: RAG JSON Generation

**Goal:** Modify RAG pipeline to generate JSON instead of plain text.

**Deliverables:**
- Updated generation prompt for JSON output
- JSON validation against catalog schema
- Fallback to plain text if JSON invalid

**Implementation:**
```python
class JSONAnswerGenerator:
    async def generate(
        self,
        question: str,
        context: str,
        catalog_schema: dict
    ) -> dict | str:
        """
        Returns JSON tree matching catalog schema,
        or plain text string as fallback.
        """
```

**Acceptance Criteria:**
- [ ] Generates valid JSON for 80%+ of queries
- [ ] JSON matches catalog schema
- [ ] Graceful fallback to text
- [ ] Maintains answer quality (>70% correctness)

---

#### B3: Component Library ✅ COMPLETE

**Goal:** Build React components for json-render catalog.

**Deliverables:**
- `frontend/src/lib/registry.tsx` - All components in single registry file
- Styling with Infomaniak Design System CSS variables
- Demo page for visual testing

**Components:**
| Component | Priority | Status | Notes |
|-----------|----------|--------|-------|
| Answer | P0 | ✅ | Container with optional summary |
| Steps + Step | P0 | ✅ | Animated step-by-step guides |
| Card | P0 | ✅ | 4 variants: info, warning, tip, important |
| Table | P0 | ✅ | Responsive with hover states |
| Comparison | P1 | ✅ | Feature matrix with checkmarks |
| CodeBlock | P1 | ✅ | Dark theme code display |
| ActionSuggestion | P1 | ✅ | Pill buttons, disabled when no handler |
| PlatformBadges | P2 | ✅ | Grid of platform icons |
| Text | P1 | ✅ | Added for flexible text content |

**Acceptance Criteria:**
- [x] All P0 components implemented
- [x] All P1/P2 components implemented
- [x] Components render correctly from JSON
- [x] Styling matches Infomaniak Design System
- [x] Dark mode support via CSS variables
- [x] Console warnings for unknown types (graceful degradation)

---

### Phase C: Action Execution

#### C1: Skill Files

**Goal:** Write skill files for demo scenarios.

**Deliverables:**
- `skills/kmeet/start-meeting.md`
- `skills/kdrive/share-file.md`
- `skills/kchat/send-message.md`

**Skill Template:**
```markdown
---
name: skill-name
description: Use when user asks to "...", "...", or wants to "..."
allowed-tools: updateState, queryDB, showPanel, navigate, toast
---

# Skill Title

## Goal
Brief description of what this accomplishes.

## Procedure

### 1. Step Name
Description of what to do.
```tool
toolName(args)
```

### 2. Step Name
...

## Edge Cases
- Case 1 → How to handle
- Case 2 → How to handle
```

**Acceptance Criteria:**
- [ ] 3 skills written
- [ ] Skills follow template
- [ ] Skills tested manually with mock execution

---

#### C2: Agent Executor

**Goal:** Execute skills by reading them and calling primitives.

**Deliverables:**
- `backend/app/agents/executor.py` - Agent loop
- Integration with primitives
- Streaming support

**Implementation:**
```python
class AgentExecutor:
    async def execute(
        self,
        skill: Skill,
        user_query: str,
        context: dict
    ) -> AsyncIterator[AgentEvent]:
        """
        Yields events:
        - ToolStatusEvent (for chat)
        - StateUpdateEvent (for app)
        - TextEvent (for final message)
        """
```

**Acceptance Criteria:**
- [ ] Reads skill and executes with LLM
- [ ] Calls primitives correctly
- [ ] Streams status events
- [ ] Handles errors gracefully
- [ ] Max 10 tool calls (prevent infinite loops)

---

#### C3: Status Streaming

**Goal:** Stream tool execution status to chat.

**Deliverables:**
- Updated stream protocol with tool-status events
- Frontend component to render status
- Status icons and styling

**Status Component:**
```tsx
function ToolStatus({ status }: { status: ToolStatusEvent }) {
  const icons = {
    starting: "🔄",
    "in-progress": "🔍",
    success: "✓",
    error: "✗"
  };

  return (
    <div className={`tool-status ${status.status}`}>
      <span>{icons[status.status]}</span>
      <span>{status.message}</span>
    </div>
  );
}
```

**Acceptance Criteria:**
- [ ] Status events stream correctly
- [ ] UI renders status in real-time
- [ ] Different styling for each status type
- [ ] Error states displayed clearly

---

### Phase D: Fake Apps

#### D1: State Management

**Goal:** Set up global state for app panel.

**Deliverables:**
- `frontend/src/stores/appStore.ts` - Zustand store
- State update handling from stream
- State persistence (optional)

**Implementation:**
```typescript
const useAppStore = create<AppState>((set) => ({
  activeApp: "none",
  kmeet: { currentMeeting: null, isJoining: false },
  kdrive: { currentFolder: "root", selectedFiles: [], shareModal: null },
  kchat: { currentChannel: null, composingMessage: "" },

  // Actions
  updateState: (path, value) => set(produce((state) => {
    lodashSet(state, path, value);
  })),
}));
```

**Acceptance Criteria:**
- [ ] Store created with full schema
- [ ] `updateState` works with dot-notation paths
- [ ] State updates trigger re-renders
- [ ] DevTools integration (optional)

---

#### D2: Fake Database

**Goal:** Create seed data for fake apps.

**Deliverables:**
- `frontend/src/data/seed.ts` - Seed data
- `frontend/src/stores/dbStore.ts` - Query logic
- Realistic sample data

**Seed Data:**
```typescript
const seedData: FakeDB = {
  contacts: [
    { id: "1", name: "John Smith", email: "john@company.com", status: "online" },
    { id: "2", name: "Sarah Johnson", email: "sarah@company.com", status: "busy" },
    { id: "3", name: "David Chen", email: "david@company.com", status: "offline" },
    { id: "4", name: "Marie Dubois", email: "marie@company.com", status: "online" },
    { id: "5", name: "Marketing Team", email: "marketing@company.com", status: "online" },
  ],
  files: [
    { id: "f1", name: "budget.xlsx", type: "spreadsheet", folderId: "root", ... },
    { id: "f2", name: "presentation.pptx", type: "presentation", folderId: "root", ... },
    { id: "f3", name: "report.pdf", type: "pdf", folderId: "shared", ... },
  ],
  // ... more seed data
};
```

**Acceptance Criteria:**
- [ ] 5+ contacts with varied statuses
- [ ] 5+ files in different folders
- [ ] 2+ channels with messages
- [ ] Query functions work (filter by name, etc.)

---

#### D3: kMeet UI

**Goal:** Build fake kMeet interface.

**Deliverables:**
- `frontend/src/components/apps/KMeet.tsx`
- Meeting room view
- Participant list

**States to Handle:**
1. **Idle**: No active meeting (show "No active meeting")
2. **Joining**: Creating/joining meeting (show spinner)
3. **Active**: In meeting (show room with participants)

**Acceptance Criteria:**
- [ ] Renders based on state
- [ ] Shows participant list
- [ ] Animated transitions between states
- [ ] "End Meeting" button works

---

#### D4: kDrive UI

**Goal:** Build fake kDrive file browser.

**Deliverables:**
- `frontend/src/components/apps/KDrive.tsx`
- File list view
- Share modal

**States to Handle:**
1. **Browse**: Show files/folders
2. **Selected**: File(s) selected (highlight)
3. **Share Modal**: Show sharing dialog

**Acceptance Criteria:**
- [ ] Renders file list from state
- [ ] Folder navigation works
- [ ] Selection highlights files
- [ ] Share modal appears when triggered

---

#### D5: kChat UI

**Goal:** Build fake kChat messaging interface.

**Deliverables:**
- `frontend/src/components/apps/KChat.tsx`
- Channel list sidebar
- Message view

**States to Handle:**
1. **Channel List**: Show available channels
2. **Active Channel**: Show messages
3. **Composing**: Show typing indicator when sending

**Acceptance Criteria:**
- [ ] Renders channels and messages
- [ ] Switching channels works
- [ ] New messages appear with animation
- [ ] Typing indicator shows during send

---

### Phase E: Integration & Polish

#### E1: Layout Integration

**Goal:** Integrate chat and app panels with sliding animation.

**Deliverables:**
- `frontend/src/components/Layout.tsx`
- Responsive layout
- Slide animation for app panel

**Behavior:**
- RAG mode: Chat full width, app panel hidden
- Action mode: Chat slides left, app panel slides in from right
- Smooth animation (300ms ease-out)

**Acceptance Criteria:**
- [ ] Layout responds to activeApp state
- [ ] Animations are smooth
- [ ] Works on mobile (stacked, not side-by-side)
- [ ] Accessible (no motion for prefers-reduced-motion)

---

#### E2: Error Handling

**Goal:** Graceful error handling throughout.

**Deliverables:**
- Error boundaries for app components
- User-friendly error messages
- Retry mechanisms

**Error Cases:**
| Error | User Message | Recovery |
|-------|--------------|----------|
| LLM timeout | "Taking longer than expected..." | Auto-retry once |
| Skill not found | "I don't know how to do that yet" | Suggest alternatives |
| Tool failure | "Something went wrong with [action]" | Show what was attempted |
| Network error | "Connection lost. Retrying..." | Auto-retry with backoff |

**Acceptance Criteria:**
- [ ] No unhandled exceptions visible to user
- [ ] All errors have user-friendly messages
- [ ] Critical errors logged to console
- [ ] Recovery options where applicable

---

#### E3: Demo Scenarios

**Goal:** Polish and test all demo scenarios.

**Test Script:**

**Scenario 1: Documentation Question**
```
User: "How do I share a file in kDrive?"
Expected:
- Intent classified as "rag"
- JSON generated with Steps component
- Rich UI renders in chat
- No app panel
```

**Scenario 2: Start Meeting**
```
User: "Start a meeting with John and Sarah"
Expected:
- Intent classified as "action", skill "start-meeting"
- Chat shows: "🔄 Starting kMeet...", "🔍 Searching contacts...", etc.
- App panel slides in with kMeet
- kMeet shows "Joining..." then active meeting with John, Sarah
- Final chat message confirms meeting started
```

**Scenario 3: Share File**
```
User: "Share budget.xlsx with the marketing team"
Expected:
- Intent classified as "action", skill "share-file"
- Chat shows: "📂 Opening kDrive...", "🔍 Finding budget.xlsx...", etc.
- App panel shows kDrive with file selected
- Share modal appears
- Final chat message confirms sharing
```

**Scenario 4: Send Message**
```
User: "Send a message to David about tomorrow's meeting"
Expected:
- Intent classified as "action", skill "send-message"
- Chat shows: "💬 Opening kChat...", "🔍 Finding David...", etc.
- App panel shows kChat with David's DM
- Message appears in chat
- Final chat message confirms sent
```

**Acceptance Criteria:**
- [ ] All 4 scenarios work end-to-end
- [ ] Response time <5s for actions
- [ ] No visual glitches
- [ ] Works in Chrome, Firefox, Safari

---

## 6. Fake App Specifications

### 6.1 kMeet

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  kMeet           [End Meeting]          │
├─────────────────────────────────────────┤
│                                         │
│        ┌─────────────────────┐          │
│        │                     │          │
│        │    📹 Video Area    │          │
│        │    (placeholder)    │          │
│        │                     │          │
│        └─────────────────────┘          │
│                                         │
├─────────────────────────────────────────┤
│  Participants:                          │
│  ┌──────┐ ┌──────┐ ┌──────┐            │
│  │ John │ │Sarah │ │ You  │            │
│  │  ✓   │ │  ✓   │ │  ✓   │            │
│  └──────┘ └──────┘ └──────┘            │
└─────────────────────────────────────────┘
```

**States:**
- `idle`: "No active meeting" message
- `joining`: Spinner + "Creating meeting..."
- `active`: Full meeting UI

### 6.2 kDrive

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  kDrive  📁 My Files                    │
├─────────────────────────────────────────┤
│  ← Back   /Personal/Documents           │
├─────────────────────────────────────────┤
│  📁 Projects                            │
│  📁 Archive                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  📊 budget.xlsx          ← selected     │
│  📄 report.pdf                          │
│  📽️ presentation.pptx                  │
└─────────────────────────────────────────┘

Share Modal:
┌─────────────────────────────────────────┐
│  Share "budget.xlsx"              [×]   │
├─────────────────────────────────────────┤
│  Share with:                            │
│  ┌─────────────────────────────────┐    │
│  │ Marketing Team           [Add] │    │
│  └─────────────────────────────────┘    │
│                                         │
│  Shared with:                           │
│  • Marketing Team (pending)             │
│                                         │
│            [Cancel]  [Share]            │
└─────────────────────────────────────────┘
```

### 6.3 kChat

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  kChat                                  │
├───────────┬─────────────────────────────┤
│ Channels  │  #general                   │
│           │─────────────────────────────│
│ #general  │  John: Hey team!            │
│ #random   │  Sarah: Hi everyone         │
│ ───────── │  You: Hello!                │
│ Direct    │                             │
│ @David    │─────────────────────────────│
│ @Sarah    │  [Type a message...]        │
└───────────┴─────────────────────────────┘
```

---

## 7. Skills Catalog

### 7.1 kMeet Skills

| Skill | Trigger Phrases | Actions |
|-------|-----------------|---------|
| `start-meeting` | "start a meeting", "call someone", "video chat with" | queryDB contacts → showPanel kmeet → updateState meeting → toast success |

### 7.2 kDrive Skills

| Skill | Trigger Phrases | Actions |
|-------|-----------------|---------|
| `share-file` | "share a file", "share with", "give access to" | showPanel kdrive → queryDB files → updateState selection → showPanel shareModal → toast success |

### 7.3 kChat Skills

| Skill | Trigger Phrases | Actions |
|-------|-----------------|---------|
| `send-message` | "send a message", "message someone", "tell them" | showPanel kchat → queryDB contacts → navigate channel → updateState message → toast success |

---

## 8. Testing Strategy

### 8.1 Unit Tests

| Component | Test File | Coverage Target |
|-----------|-----------|-----------------|
| Intent Router | `test_router.py` | >90% |
| Primitives | `test_primitives.py` | >90% |
| Skill Loader | `test_skills.py` | >80% |
| Agent Executor | `test_executor.py` | >80% |

### 8.2 Integration Tests

| Test | Description |
|------|-------------|
| RAG E2E | Query → Retrieval → JSON Generation → Valid output |
| Action E2E | Query → Routing → Skill → Primitives → State updates |
| Stream E2E | Full stream protocol validation |

### 8.3 Manual Test Checklist

- [ ] RAG: "How do I share a file?"
- [ ] RAG: "What's the difference between kDrive folder types?"
- [ ] RAG: "Can I use kMeet without an account?"
- [ ] Action: "Start a meeting with John"
- [ ] Action: "Share budget.xlsx with marketing"
- [ ] Action: "Send a message to Sarah"
- [ ] Error: "Start a meeting with NonexistentPerson"
- [ ] Error: "Share nonexistent.txt"
- [ ] Edge: Very long query
- [ ] Edge: Query in French

---

## 9. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| LLM generates invalid JSON | High | Medium | Fallback to plain text, JSON schema validation |
| Intent misclassification | Medium | Medium | High-confidence threshold, fallback to RAG |
| Skill execution loops | High | Low | Max tool calls limit (10) |
| State sync issues | Medium | Medium | Single source of truth, event-driven updates |
| Demo scenario failure | Critical | Low | Extensive manual testing, fallback flows |

---

## Appendix A: File Structure

```
backend/
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── router.py        # A1: Intent Router
│   │   ├── primitives.py    # A2: Low-Level Primitives
│   │   ├── skills.py        # A3: Skill Loader
│   │   └── executor.py      # C2: Agent Executor
│   ├── api/
│   │   └── chat.py          # Updated for dual-mode streaming
│   └── rag/
│       └── json_generator.py # B2: JSON Answer Generator

skills/
├── kmeet/
│   └── start-meeting.md     # C1
├── kdrive/
│   └── share-file.md        # C1
└── kchat/
    └── send-message.md      # C1

frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   └── ToolStatus.tsx    # C3 (planned)
│   │   ├── apps/
│   │   │   ├── KMeet.tsx         # D3 (planned)
│   │   │   ├── KDrive.tsx        # D4 (planned)
│   │   │   └── KChat.tsx         # D5 (planned)
│   │   ├── ThemeToggle.tsx       # B1 ✅
│   │   └── Layout.tsx            # E1 (planned)
│   ├── stores/
│   │   ├── appStore.ts           # D1 (planned)
│   │   └── dbStore.ts            # D2 (planned)
│   ├── data/
│   │   └── seed.ts               # D2 (planned)
│   ├── lib/
│   │   ├── catalog.ts            # B1 ✅ Zod schemas
│   │   ├── registry.tsx          # B1+B3 ✅ All components
│   │   ├── JsonRenderer.tsx      # B1 ✅ Error boundary wrapper
│   │   └── JsonRendererDemo.tsx  # B1 ✅ Demo page
│   ├── App.tsx                   # Updated with demo route
│   └── index.css                 # Infomaniak Design System
```

---

## Appendix B: Implementation Order Recommendation

For maximum testability at each step:

```
Week 1 (Foundation):
├── Day 1: A1 (Router) + A2 (Primitives) + A3 (Skills)
└── Day 2: C1 (Skill Files) + C2 (Executor) - backend complete

Week 2 (Frontend):
├── Day 3: D1 (State) + D2 (DB) + B1 (json-render)
├── Day 4: D3 (kMeet) + D4 (kDrive) + D5 (kChat)
└── Day 5: B2 (JSON Gen) + B3 (Components)

Week 3 (Integration):
├── Day 6: C3 (Status Streaming) + E1 (Layout)
├── Day 7: E2 (Error Handling) + E3 (Demo Scenarios)
└── Day 8: Polish + Documentation
```

---

*End of PRD*
