# Phase 2 Progress Tracker

Based on [PRD-phase2-agentic-system.md](./PRD-phase2-agentic-system.md)

---

## Phase A: Foundation (Backend)

### A1: Intent Router ✅ DONE
- [x] `backend/app/agents/router.py` - Intent classification
- [x] Classification prompt with few-shot examples
- [x] `IntentType` enum (rag, action)
- [x] `Intent` dataclass with confidence score
- [x] `SkillInfo` for available skills
- [x] Integration in `chat.py` (routes to RAG or action stub)
- [x] Proper error handling (`IntentClassificationError`)
- [x] Logging instead of print statements
- [x] Unit tests (27 passing)
- [x] Config: `router_model`, `router_confidence_threshold`

### A2: Low-Level Primitives ✅ DONE
- [x] `backend/app/agents/primitives.py` - Core primitive implementations
- [x] `backend/app/agents/events.py` - Stream event types (Vercel AI SDK format)
- [x] `backend/app/agents/fakedb.py` - Seed data for agent queries
- [x] `backend/app/agents/tools.py` - OpenAI-format tool definitions
- [x] `updateState(path, value)` - Modify React app state
- [x] `queryDB(collection, filter)` - Search fake database
- [x] `showPanel(panelId, props)` - Display UI component
- [x] `navigate(route)` - Change current view
- [x] `toast(message, type)` - Show notification
- [x] `ToastType` enum for type safety
- [x] Event emission with `2:` prefix (Vercel AI SDK protocol)
- [x] Unit tests (76 tests for primitives, events, fakedb, tools)

### A3: Skill Loader ✅ DONE
- [x] `backend/app/agents/skills.py` - Skill loading and parsing
- [x] `skills/` directory structure (kmeet/, kdrive/, kchat/)
- [x] YAML frontmatter parsing with `pyyaml`
- [x] `SkillLoader.list_skills()` - List all available skills
- [x] `SkillLoader.load_skill(name)` - Load a skill by name
- [x] `SkillLoader.get_skill(name)` - Get skill or None
- [x] `SkillMetadata` and `Skill` dataclasses with validation
- [x] Custom exceptions: `SkillNotFoundError`, `SkillParseError`
- [x] Proper error handling and logging (no silent failures)
- [x] I/O error handling (PermissionError, UnicodeDecodeError, OSError)
- [x] Unit tests (36 passing)
- [x] Config: `skills_dir` setting

---

## Phase B: RAG Generative UI

### B1: json-render Setup
- [ ] Install `@json-render/core` and `@json-render/react`
- [ ] `frontend/src/lib/catalog.ts`
- [ ] `frontend/src/lib/registry.tsx`
- [ ] Basic renderer working

### B2: RAG JSON Generation
- [ ] `backend/app/rag/json_generator.py`
- [ ] Updated generation prompt for JSON output
- [ ] JSON validation against catalog schema
- [ ] Fallback to plain text

### B3: Component Library
- [ ] `Answer` component
- [ ] `Steps` + `Step` components
- [ ] `Card` component
- [ ] `Table` component
- [ ] `Comparison` component
- [ ] `CodeBlock` component
- [ ] `ActionSuggestion` component
- [ ] `PlatformBadges` component

---

## Phase C: Action Execution

### C1: Skill Files ✅ DONE (moved to A3)
- [x] `skills/kmeet/start-meeting.md`
- [x] `skills/kdrive/share-file.md`
- [x] `skills/kchat/send-message.md`

### C2: Agent Executor
- [ ] `backend/app/agents/executor.py`
- [ ] Agent loop with LLM
- [ ] Primitive invocation
- [ ] Max 10 tool calls limit
- [ ] Streaming support

### C3: Status Streaming
- [ ] Tool-status events in stream protocol
- [ ] `ToolStatus` React component
- [ ] Status icons (🔄 🔍 ✓ ✗)

---

## Phase D: Fake Apps

### D1: State Management
- [ ] `frontend/src/stores/appStore.ts` (Zustand)
- [ ] State update from stream events
- [ ] `activeApp` switching

### D2: Fake Database
- [ ] `frontend/src/data/seed.ts`
- [ ] `frontend/src/stores/dbStore.ts`
- [ ] 5+ contacts, 5+ files, 2+ channels

### D3: kMeet UI
- [ ] `frontend/src/components/apps/KMeet.tsx`
- [ ] Idle, Joining, Active states
- [ ] Participant list
- [ ] End Meeting button

### D4: kDrive UI
- [ ] `frontend/src/components/apps/KDrive.tsx`
- [ ] File browser view
- [ ] File selection
- [ ] Share modal

### D5: kChat UI
- [ ] `frontend/src/components/apps/KChat.tsx`
- [ ] Channel list
- [ ] Message view
- [ ] Composing state

---

## Phase E: Integration & Polish

### E1: Layout Integration
- [ ] `frontend/src/components/Layout.tsx`
- [ ] Chat + App panel side-by-side
- [ ] Slide animation for app panel
- [ ] Mobile responsive (stacked)

### E2: Error Handling
- [ ] Error boundaries
- [ ] User-friendly error messages
- [ ] Retry mechanisms

### E3: Demo Scenarios
- [ ] "How do I share a file?" → Rich UI
- [ ] "Start a meeting with John" → kMeet opens
- [ ] "Share budget.xlsx with marketing" → kDrive opens
- [ ] "Send a message to David" → kChat opens

---

## Summary

| Phase | Status | Progress |
|-------|--------|----------|
| A: Foundation | ✅ Complete | 3/3 done |
| B: RAG Generative UI | ⚪ Not Started | 0/3 done |
| C: Action Execution | 🟡 In Progress | 1/3 done |
| D: Fake Apps | ⚪ Not Started | 0/5 done |
| E: Integration | ⚪ Not Started | 0/3 done |

**Overall: ~24% complete (4/17 tasks)**

---

## Next Step

**B1: json-render Setup**

Set up the json-render library for constrained generative UI:
1. Install `@json-render/core` and `@json-render/react`
2. Create `frontend/src/lib/catalog.ts` with component definitions
3. Create `frontend/src/lib/registry.tsx` with React component mappings
4. Basic renderer working with test components

This enables the RAG system to output structured JSON that renders as rich UI.
