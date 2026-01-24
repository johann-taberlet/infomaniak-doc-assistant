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

### A2: Low-Level Primitives ⏳ NEXT
- [ ] `backend/app/agents/primitives.py`
- [ ] `updateState(path, value)` - Modify React app state
- [ ] `queryDB(collection, filter)` - Search fake database
- [ ] `showPanel(panelId, props)` - Display UI component
- [ ] `navigate(route)` - Change current view
- [ ] `toast(message, type)` - Show notification
- [ ] Pydantic schemas for each primitive
- [ ] Unit tests

### A3: Skill Loader
- [ ] `backend/app/agents/skills.py`
- [ ] `skills/` directory structure
- [ ] YAML frontmatter parsing
- [ ] `SkillLoader.list_skills()`
- [ ] `SkillLoader.load_skill(name)`
- [ ] `SkillLoader.match_skill(query, intent)`

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

### C1: Skill Files
- [ ] `skills/kmeet/start-meeting.md`
- [ ] `skills/kdrive/share-file.md`
- [ ] `skills/kchat/send-message.md`

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
| A: Foundation | 🟡 In Progress | 1/3 done |
| B: RAG Generative UI | ⚪ Not Started | 0/3 done |
| C: Action Execution | ⚪ Not Started | 0/3 done |
| D: Fake Apps | ⚪ Not Started | 0/5 done |
| E: Integration | ⚪ Not Started | 0/3 done |

**Overall: ~6% complete (1/17 tasks)**

---

## Next Step

**A2: Low-Level Primitives**

Create `backend/app/agents/primitives.py` with 5 tools:
1. `updateState` - Modify frontend state via stream
2. `queryDB` - Query fake database (frontend-side)
3. `showPanel` - Trigger UI panel display
4. `navigate` - Change app route
5. `toast` - Show notification

These primitives will emit events that the frontend consumes to update the fake apps.
