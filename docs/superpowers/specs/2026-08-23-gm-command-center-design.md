# GM COMMAND CENTER — 3D NFL Front Office Development War Room

**Document:** `GM-COMMAND-CENTER-DESIGN-001`  
**Date:** 2026-08-23  
**Status:** `APPROVED_DESIGN / IMPLEMENTATION_NOT_STARTED`  
**Repository:** `Charleigh5/THE-NFL-SIM-V2`  
**Branch:** `design/gm-command-center`  
**Target architecture:** Existing React/Vite/TypeScript frontend + FastAPI/SQLAlchemy/PostgreSQL backend  
**Primary route:** `/gm-command-center`  

---

## 1. Purpose

Build a persistent, interactive **NFL General Manager development war room** inside THE-NFL-SIM-V2. The interface should resemble a professional football front-office draft board rather than a generic software Kanban page.

The user sees the application’s features, work items, issues, blockers, and evidence as physical-looking sticky notes pinned to a spatial whiteboard. Notes can be dragged between workflow lanes, clicked for full details, attached to an AI chat context tray, created or updated through natural-language commands, and animated in real time when state changes occur.

The board is not merely a visualization. It is the application’s **development command surface** over repository evidence, implementation state, and user-owned workflow state.

### Core user outcomes

The user must be able to:

1. See the major features of THE-NFL-SIM-V2 as movable board cards.
2. Distinguish **what the repository appears to implement** from **what the user considers done**.
3. Drag a card from `NOT_STARTED` / `READY` into `IN_PROCESS`, `REVIEW`, `BLOCKED`, or `COMPLETE`.
4. Click any card and inspect its description, progress, files, tests, commits, dependencies, blockers, and history.
5. Select cards/files as context for a GM-style chat interface.
6. Ask natural-language questions such as:
   - “What are we working on?”
   - “Why is Live Sim not complete?”
   - “Show everything related to player development.”
   - “What files support Draft AI?”
7. Issue natural-language board mutations such as:
   - “Move the trade engine back to in process; AI valuation still needs work.”
   - “Create a high-priority feature for compensatory draft picks.”
   - “Add the draft regression tests to context.”
8. Watch affected sticky notes animate to their new board location in real time.
9. Reverse or inspect prior board mutations through an append-only event history.
10. Let the system locate candidate repository files relevant to a card or chat request without treating inferred file matches as verified implementation facts.

---

## 2. Existing-system alignment

This subsystem must extend the existing application rather than create a second app.

Observed repository architecture already includes:

- React + Vite + TypeScript frontend.
- FastAPI backend.
- SQLAlchemy/PostgreSQL persistence.
- REST + WebSocket communication.
- A simulation orchestrator and domain services.
- Existing Draft Room, Front Office, Depth Chart, Trade Center, Trophy Room, Live Sim, Medical Center, Playbook, Training, Skills, Season, and Offseason routes.
- Existing AI-oriented concepts including Draft Assistant, GM Agent, and MCP integration.
- Existing frontend dependencies suited to the experience: React Three Fiber, Drei, Three.js, `dnd-kit`, Framer Motion, Zustand, React Query, Playwright, and gesture utilities.

The existing `.agent/rules/app-master.md` defines the UI as the user’s Front Office over a detailed simulated football world. GM Command Center therefore acts as a **development-facing extension of that same front-office metaphor**.

It must not replace the existing gameplay `DraftRoom` or `FrontOffice` in the first implementation. It is a new development/management route that can later be linked from global navigation.

---

## 3. Design principles

### 3.1 Board state is not repository truth

Never collapse “code exists” and “feature is complete” into one boolean.

Maintain two orthogonal state systems:

```text
REPOSITORY / EVIDENCE STATE
UNKNOWN
CANDIDATE
OBSERVED
PARTIAL
IMPLEMENTED
TESTED
CONFLICT

WORKFLOW STATE
BACKLOG
READY
IN_PROCESS
REVIEW
BLOCKED
COMPLETE
```

A repository scanner may determine that files or tests exist. It may not automatically move a card to `COMPLETE`.

### 3.2 User workflow state is authoritative

The user can explicitly move a card between workflow states. That mutation is persisted with provenance and can be reversed.

### 3.3 Every important claim has evidence

Cards should link to evidence such as:

- source files;
- routes;
- API endpoints;
- backend modules;
- tests;
- documentation;
- commits;
- repository scanner observations.

An inferred relationship is labeled `CANDIDATE` until verified.

### 3.4 Natural language becomes structured intent

Chat never directly mutates arbitrary application state from unconstrained prose. Natural-language requests become typed commands first.

### 3.5 Motion communicates state

Animation is functional:

- `lift` = selected/grabbed;
- `move` = workflow transition;
- `pin` = persisted/confirmed;
- `shake/pulse` = rejected or blocked mutation.

Avoid continuous decorative movement that interferes with board comprehension.

### 3.6 3D is a spatial shell, not a readability tax

The room and board use Three.js/R3F for depth, lighting, camera, parallax, and atmosphere. Sticky-note text, chat, forms, details, context chips, and control surfaces remain structured DOM for accessibility, text clarity, testing, and deterministic drag behavior.

---

## 4. Information model

The board uses three primary object types.

### 4.1 FEATURE

A capability the application offers or intends to offer.

Examples:

- Draft System
- Free Agency
- Trade Engine
- Salary Cap
- Live Simulation
- Player Progression

### 4.2 WORK_ITEM

A concrete implementation, verification, UX, research, or refactoring unit linked to a feature.

Examples:

- Add compensatory draft picks
- Add Draft Room E2E coverage
- Implement contract negotiation history

### 4.3 ISSUE

A defect, blocker, regression, data gap, or architectural risk.

Examples:

- Duplicate AI draft pick bug
- Trade valuation confidence mismatch
- Missing API integration coverage

A FEATURE may own many WORK_ITEM and ISSUE cards.

---

## 5. Core data contracts

### 5.1 `BoardCard`

```ts
export type BoardCardType = "FEATURE" | "WORK_ITEM" | "ISSUE";

export type WorkflowStatus =
  | "BACKLOG"
  | "READY"
  | "IN_PROCESS"
  | "REVIEW"
  | "BLOCKED"
  | "COMPLETE";

export type EvidenceState =
  | "UNKNOWN"
  | "CANDIDATE"
  | "OBSERVED"
  | "PARTIAL"
  | "IMPLEMENTED"
  | "TESTED"
  | "CONFLICT";

export interface BoardCard {
  id: string;
  type: BoardCardType;
  title: string;
  slug: string;
  summary: string;
  description?: string;

  workflowStatus: WorkflowStatus;
  evidenceState: EvidenceState;

  category: string;
  tags: string[];
  priority: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  completionPercent?: number;
  confidence?: number;

  parentFeatureId?: string;
  dependencyIds: string[];
  relatedCardIds: string[];

  implemented: string[];
  inProgress: string[];
  missing: string[];
  blockers: string[];

  evidenceRefs: EvidenceRef[];
  boardPosition: BoardPosition;

  createdAt: string;
  updatedAt: string;
  createdBy: ActorRef;
  lastUpdatedBy: ActorRef;
  version: number;
}
```

### 5.2 `EvidenceRef`

```ts
export interface EvidenceRef {
  id: string;
  kind:
    | "FILE"
    | "ROUTE"
    | "API_ENDPOINT"
    | "TEST"
    | "COMMIT"
    | "DOC"
    | "SCAN_OBSERVATION";
  locator: string;
  label: string;
  state: "CONFIRMED" | "CANDIDATE" | "CONFLICT" | "UNKNOWN";
  confidence?: number;
  excerpt?: string;
  observedAt?: string;
}
```

### 5.3 `BoardPosition`

Board positions are deterministic UI data, not hidden inside canvas state.

```ts
export interface BoardPosition {
  lane: WorkflowStatus;
  rank: number;
  x?: number;
  y?: number;
  rotationDeg?: number;
}
```

`lane` + `rank` are authoritative ordering. `x`, `y`, and `rotationDeg` are visual preferences.

### 5.4 `BoardEvent`

Every mutation produces an append-only event.

```ts
export interface BoardEvent {
  id: string;
  eventType:
    | "CARD_CREATED"
    | "CARD_UPDATED"
    | "CARD_MOVED"
    | "CARD_LINKED"
    | "CARD_UNLINKED"
    | "EVIDENCE_ATTACHED"
    | "EVIDENCE_REMOVED"
    | "EVENT_REVERTED";

  cardId: string;
  actor: ActorRef;
  source: "DRAG" | "DETAIL_EDITOR" | "CHAT" | "SYSTEM";

  before?: Record<string, unknown>;
  after?: Record<string, unknown>;
  reason?: string;

  causedByEventId?: string;
  createdAt: string;
}
```

### 5.5 `ContextAttachment`

```ts
export interface ContextAttachment {
  id: string;
  kind: "CARD" | "FILE" | "TEST" | "COMMIT" | "DOC";
  locator: string;
  label: string;
  evidenceState: EvidenceState;
}
```

The chat context tray displays these explicitly before a question is sent.

---

## 6. Visual architecture

### 6.1 Page layout

```text
┌─────────────────────────────────────────────────────────────────────┐
│ GM COMMAND CENTER    filters / search / scan status / board stats   │
├───────────────────────────────────────────────────────┬─────────────┤
│                                                       │             │
│  3D FRONT-OFFICE ROOM / WHITEBOARD                   │ DETAILS /   │
│                                                       │ CONTEXT /   │
│  BACKLOG  READY  IN PROCESS  REVIEW BLOCKED COMPLETE │ CHAT        │
│                                                       │             │
│  [sticky] [sticky] [sticky]                           │             │
│  [sticky]          [sticky]                           │             │
│                                                       │             │
├───────────────────────────────────────────────────────┴─────────────┤
│ context tray / activity / undo                                        │
└─────────────────────────────────────────────────────────────────────┘
```

Desktop is the primary target. Tablet and mobile fall back to a flat, accessible lane view while preserving all data and actions.

### 6.2 Three-dimensional layer

`BoardScene3D` owns:

- room geometry;
- wall/board geometry;
- lighting;
- subtle depth/parallax;
- camera;
- environmental materials;
- optional shelves/screens/football-office props;
- reduced-motion behavior.

The room should evoke a professional NFL draft war room without copying proprietary broadcast packages or protected team branding.

### 6.3 DOM board layer

`BoardSurface` owns:

- status lanes;
- sticky notes;
- drag targets;
- sorting;
- keyboard drag controls;
- selection;
- multi-select;
- filters;
- accessibility semantics.

The DOM board visually inherits perspective from the 3D scene but remains testable without WebGL.

### 6.4 Sticky note visual grammar

Card color is semantic but not sole-state communication.

Suggested family:

- FEATURE — neutral cream/paper.
- WORK_ITEM — pale blue.
- ISSUE — pale red/pink.
- BLOCKED — striped/risk edge.
- COMPLETE — subdued green confirmation mark.

Each sticky shows only high-signal information:

```text
DRAFT AI
FEATURE
IN PROCESS
72%
3 files • 2 tests • 1 blocker
```

Full detail belongs in the inspector.

---

## 7. Interaction design

### 7.1 Drag-and-drop

Use `dnd-kit` for deterministic lane movement and sortable ordering.

On drag start:

- card lifts visually;
- source lane remains visible;
- valid target lanes highlight.

On drop:

1. optimistic UI moves the card;
2. API persists the mutation;
3. server emits a WebSocket event;
4. client reconciles authoritative state;
5. card pins into place.

On rejected mutation:

- card returns to prior lane;
- UI shows a concise failure reason;
- no successful event is recorded.

### 7.2 Card detail inspector

Clicking a card opens a side panel with:

- title/type/status/priority;
- description;
- completion;
- repository evidence state;
- implemented/in-progress/missing/blockers;
- source files;
- tests;
- related commits;
- routes/endpoints;
- dependencies;
- related cards;
- event history;
- “Add to Chat Context”.

### 7.3 Context tray

The tray contains explicit chips such as:

```text
[ Draft AI × ]
[ DraftRoom.tsx × ]
[ draft_service.py × ]
[ regression test × ]
```

The user can remove any attachment before sending a prompt.

### 7.4 Board filtering

Minimum filters:

- card type;
- workflow status;
- category;
- priority;
- evidence state;
- tags;
- text search;
- “has blockers”;
- “has unknown evidence”.

Filtering should visually dim or hide cards without changing board data.

---

## 8. Repository intelligence subsystem

### 8.1 Objective

Create a read-only repository index that can answer:

- Which files are likely relevant to this feature?
- Which tests exercise it?
- Which routes/endpoints expose it?
- Which recent commits touched it?
- Where are unresolved TODO/FIXME markers?

This subsystem does **not** modify application source code.

### 8.2 Index sources

Initial index scope:

```text
frontend/src/pages/**
frontend/src/components/**
frontend/src/services/**
frontend/src/types/**
backend/app/api/**
backend/app/models/**
backend/app/schemas/**
backend/app/services/**
backend/app/orchestrator/**
backend/app/engine/**
backend/app/rpg/**
backend/tests/**
frontend/tests/**
docs/**
.agent/rules/**
```

Git metadata may additionally provide recent commit linkage.

### 8.3 File candidate resolution

Repository matches receive confidence and provenance.

```text
EXACT_EXPLICIT_LINK       -> CONFIRMED
KNOWN_ROUTE/SERVICE LINK  -> OBSERVED
NAME/SYMBOL MATCH         -> CANDIDATE
SEMANTIC MATCH ONLY       -> CANDIDATE
NO SUPPORT                -> UNKNOWN
```

A semantic match does not become `CONFIRMED` automatically.

### 8.4 Feature registry seeding

The first canonical feature registry should be generated as a candidate inventory from the actual repo, then reviewed.

Likely families to inspect include:

- Season / schedule / standings / playoffs / awards;
- roster / depth chart / contracts / salary cap;
- trade engine;
- draft / scouting / team needs;
- free agency;
- player progression / traits / training;
- coaching / play calling;
- game simulation / play resolver / physics / momentum;
- Live Sim;
- Medical Center;
- Trophy Room;
- Playbook;
- Skills;
- AI Draft Assistant / GM Agent;
- MCP integrations.

These are discovery targets, not automatic assertions that every item is complete.

---

## 9. Natural-language GM assistant

### 9.1 Scope

The first assistant is a **board and repository-context agent**, not an unrestricted code-writing agent.

Allowed first-slice capabilities:

- search board;
- filter/highlight board;
- explain current board state;
- inspect evidence;
- attach files/cards to context;
- create board cards;
- update board-card metadata;
- move cards;
- link dependencies;
- summarize blockers;
- request repository candidate files.

Source-code mutations remain outside this subsystem unless added later behind a separate implementation-agent boundary.

### 9.2 Intent schema

```ts
export type GMCommandIntent =
  | { type: "QUERY_BOARD"; query: BoardQuery }
  | { type: "SELECT_CARD"; cardId: string }
  | { type: "CREATE_CARD"; draft: CreateCardDraft }
  | { type: "UPDATE_CARD"; cardId: string; patch: CardPatch; reason?: string }
  | { type: "MOVE_CARD"; cardId: string; to: WorkflowStatus; reason?: string }
  | { type: "ADD_CONTEXT"; attachments: ContextAttachment[] }
  | { type: "FIND_REPO_CONTEXT"; cardId?: string; query: string }
  | { type: "LINK_CARDS"; fromId: string; toId: string; relation: string }
  | { type: "UNDO_EVENT"; eventId: string };
```

### 9.3 Read vs write behavior

Read-only intents execute immediately.

Board mutations follow:

```text
USER TEXT
   ↓
INTENT PARSER
   ↓
ENTITY RESOLUTION
   ↓
STRUCTURED MUTATION
   ↓
VALIDATION / CONFLICT CHECK
   ↓
PERSIST EVENT + STATE
   ↓
WEBSOCKET BROADCAST
   ↓
ANIMATED BOARD UPDATE
```

When entity resolution is ambiguous, the assistant does not guess silently. It returns candidates.

### 9.4 Example

User:

> Move the trade engine back to in process. The AI valuation still needs work.

Normalized command:

```json
{
  "type": "MOVE_CARD",
  "cardId": "feature-trade-engine",
  "to": "IN_PROCESS",
  "reason": "AI valuation still needs work"
}
```

Result:

- workflow state persists;
- event records old/new states and reason;
- affected card animates from its current lane to `IN_PROCESS`;
- detail history updates.

---

## 10. Backend architecture

### 10.1 New modules

```text
backend/app/
  api/
    gm_command_center.py
  models/
    gm_command_center.py
  schemas/
    gm_command_center.py
  services/
    gm_command_center/
      __init__.py
      board_service.py
      evidence_service.py
      repo_indexer.py
      repository_context_service.py
      command_parser.py
      command_executor.py
      websocket_hub.py
```

Tests:

```text
backend/tests/
  gm_command_center/
    test_board_service.py
    test_board_api.py
    test_command_parser.py
    test_command_executor.py
    test_repo_indexer.py
    test_event_reversal.py
    test_websocket_events.py
```

### 10.2 Database tables

Recommended relational tables:

- `gm_board_cards`
- `gm_board_card_relations`
- `gm_board_evidence_refs`
- `gm_board_events`
- `gm_context_sessions`
- `gm_context_attachments`
- optional `gm_repo_scan_runs`
- optional `gm_repo_scan_observations`

The event ledger is append-only. Reversal creates a new event rather than deleting history.

### 10.3 API surface

Initial endpoints:

```text
GET    /api/gm-command-center/board
GET    /api/gm-command-center/cards/{card_id}
POST   /api/gm-command-center/cards
PATCH  /api/gm-command-center/cards/{card_id}
POST   /api/gm-command-center/cards/{card_id}/move
GET    /api/gm-command-center/cards/{card_id}/events
POST   /api/gm-command-center/events/{event_id}/revert

GET    /api/gm-command-center/repository/search
GET    /api/gm-command-center/repository/context
POST   /api/gm-command-center/repository/scan

POST   /api/gm-command-center/chat/interpret
POST   /api/gm-command-center/chat/execute

WS     /ws/gm-command-center
```

`chat/interpret` returns structured intent and resolved targets without performing mutations. `chat/execute` accepts an already validated command and applies it.

This split makes command behavior testable and auditable.

### 10.4 WebSocket events

```ts
export type GMBoardSocketEvent =
  | { type: "CARD_CREATED"; card: BoardCard }
  | { type: "CARD_UPDATED"; card: BoardCard }
  | { type: "CARD_MOVED"; cardId: string; from: WorkflowStatus; to: WorkflowStatus }
  | { type: "EVIDENCE_UPDATED"; cardId: string; refs: EvidenceRef[] }
  | { type: "EVENT_REVERTED"; eventId: string; card: BoardCard }
  | { type: "SCAN_PROGRESS"; scanId: string; progress: number }
  | { type: "SCAN_COMPLETE"; scanId: string; candidateCount: number };
```

WebSocket events trigger UI synchronization and animation but are not the persistence authority. The backend database is authoritative.

---

## 11. Frontend architecture

Recommended feature-oriented structure:

```text
frontend/src/features/gmCommandCenter/
  pages/
    GMCommandCenter.tsx

  components/
    BoardScene3D.tsx
    BoardSurface.tsx
    BoardLane.tsx
    StickyCard.tsx
    StickyDragOverlay.tsx
    BoardToolbar.tsx
    BoardStats.tsx
    CardDetailsDrawer.tsx
    ContextTray.tsx
    GMChatPanel.tsx
    CommandPreview.tsx
    EvidenceList.tsx
    DependencyGraph.tsx
    EventHistory.tsx
    RepoSearchPanel.tsx

  hooks/
    useBoardSocket.ts
    useBoardDrag.ts
    useReducedMotionPreference.ts

  stores/
    useGMBoardStore.ts

  services/
    gmCommandCenterApi.ts

  types/
    index.ts

  motion/
    boardMotion.ts
```

Add route:

```text
/gm-command-center
```

Keep route ownership separate from gameplay `/draft` and `/empire/front-office`.

---

## 12. Client state model

Use React Query for server state and Zustand only for transient UI state.

### React Query owns

- board cards;
- card details;
- event history;
- repository search results;
- evidence records;
- scan status.

### Zustand owns

- selected card IDs;
- open drawer/tab;
- local board filters;
- chat context tray;
- active drag item;
- camera/presentation mode;
- reduced visual density preference.

Do not duplicate persisted card records as an independent Zustand source of truth.

---

## 13. Concurrency and conflict handling

Each card carries a monotonically increasing `version`.

Mutation requests include the version the client last observed.

If the persisted version differs:

```text
HTTP 409 CARD_VERSION_CONFLICT
```

The UI refreshes and presents the conflict rather than overwriting newer state.

This is important once chat actions, drag actions, or multiple clients can mutate the same board.

---

## 14. Accessibility and fallback

3D presentation must never be required to operate the board.

Requirements:

- keyboard-accessible lane/card navigation;
- keyboard move action for cards;
- semantic headings and lists;
- visible focus states;
- sufficient contrast;
- no color-only status representation;
- reduced-motion support;
- `prefers-reduced-motion` respected;
- optional “Flat Board” mode;
- chat/context controls usable without WebGL;
- screen-reader label for card type/status/priority/progress.

If WebGL fails, the DOM board remains fully functional.

---

## 15. Performance constraints

The primary board should remain responsive with at least 150 visible cards.

Guidelines:

- do not create one heavy Three.js scene node per line of card text;
- cards remain DOM;
- memoize card components;
- virtualize large detail/evidence lists where necessary;
- lazy-load dependency graph and commit history;
- debounce repository search;
- stream repository scan progress;
- cap simultaneous decorative lights/shadows;
- disable expensive post-processing in reduced-performance mode.

The 3D shell must not block board interaction while loading.

---

## 16. Testing strategy

### 16.1 Backend unit tests

Must prove:

- card creation validates required fields;
- workflow transitions persist;
- card versions prevent lost updates;
- append-only events are written;
- event revert creates a compensating event;
- ambiguous NLP entity resolution does not silently mutate;
- repository indexer labels inferred matches as candidates;
- repository scanner does not write source files;
- chat execution applies only validated structured commands.

### 16.2 Frontend component tests / logic tests

Must prove:

- lane counts match state;
- drag drop updates target lane;
- failed mutation restores prior visual state;
- context tray add/remove works;
- detail drawer renders evidence and blockers;
- socket event reconciles a moved card;
- reduced-motion mode avoids fly animation.

### 16.3 Playwright E2E

Required paths:

#### E2E-01 — Drag lifecycle

1. Open GM Command Center.
2. Locate a seeded card in `READY`.
3. Drag to `IN_PROCESS`.
4. Confirm persisted state after reload.
5. Confirm history event exists.

#### E2E-02 — NLP mutation

1. Open chat.
2. Send a deterministic test command.
3. Verify resolved target.
4. Execute command.
5. Observe card in new lane.
6. Reload and verify persistence.

#### E2E-03 — Context flow

1. Open a FEATURE.
2. Add card to context.
3. Add one linked FILE.
4. Ask a test query.
5. Verify request payload contains only selected context.

#### E2E-04 — Revert

1. Move a card.
2. Open event history.
3. Revert move.
4. Verify card returns to prior state.
5. Verify reversal event is appended.

#### E2E-05 — WebGL fallback

Disable WebGL or force flat mode and verify full board functionality.

---

## 17. Delivery slices

### SLICE 01 — Visual Board Kernel

Deliver:

- `/gm-command-center` route;
- 3D front-office shell;
- DOM whiteboard;
- workflow lanes;
- seeded local/mock cards;
- drag/drop;
- details drawer;
- context tray;
- deterministic animations;
- reduced-motion/flat fallback;
- Playwright smoke path.

No backend persistence or NLP required yet.

**Exit criterion:** the user can physically operate a convincing GM war-room board and inspect notes without any repository mutation.

### SLICE 02 — Persistent Board + Event Ledger

Deliver:

- database models + migration;
- board CRUD;
- status transitions;
- event history;
- event reversal;
- WebSocket sync;
- React Query integration;
- optimistic/reconciliation behavior.

**Exit criterion:** board state survives reload and every state-changing action has reversible history.

### SLICE 03 — Repository Evidence Index

Deliver:

- read-only repo index;
- file/test/route/commit candidate discovery;
- evidence attachments;
- repository search UI;
- candidate confidence/status;
- first reviewed feature-registry seed.

**Exit criterion:** a card can show exactly which repository evidence supports its current implementation assessment.

### SLICE 04 — NLP GM Assistant

Deliver:

- chat UI;
- command interpretation;
- entity resolution;
- context tray integration;
- board queries;
- create/update/move/link commands;
- repository-context lookup;
- audited mutation execution.

**Exit criterion:** the user can operate the board by natural language and see the same changes reflected visually and persistently.

### SLICE 05 — Automated Feature Reconnaissance

Deliver:

- governed repo scan;
- candidate feature discovery;
- candidate stale/missing evidence;
- dependency mapping;
- review queue;
- scan progress on board.

**Exit criterion:** repo changes can generate reviewable board intelligence without silently changing user workflow state.

---

## 18. Initial feature-registry strategy

Do not manually invent a large canonical list before scanning.

Use a two-step bootstrapping process:

### Step A — candidate extraction

Inspect route/page/service/model/test/documentation structures and create candidate FEATURE cards.

### Step B — human-reviewed promotion

For each candidate:

- verify title/scope;
- attach source evidence;
- resolve duplicate/overlapping cards;
- assign category;
- establish dependencies;
- explicitly choose workflow state.

Only then treat it as a canonical board card.

The repository’s existing roadmap checkboxes may seed evidence, but they do not independently prove current implementation completeness.

---

## 19. Security and mutation boundaries

The GM Command Center is permitted to mutate **its own board database records**.

It must not, in the initial architecture:

- modify arbitrary repository source files;
- commit code;
- create pull requests;
- run shell commands from chat;
- execute unbounded MCP tools;
- expose secrets;
- infer successful source-code implementation from board movement.

Repository scanning is read-only.

Future code-agent integration should be a separate explicit subsystem where a board WORK_ITEM can be handed to an implementation agent with independent permissions, tests, and execution receipts.

---

## 20. Error states

The UI needs explicit handling for:

- board API unavailable;
- WebSocket disconnected;
- mutation rejected;
- version conflict;
- repository scan unavailable;
- repository candidate unresolved;
- chat intent ambiguous;
- chat provider unavailable;
- WebGL unavailable;
- empty board;
- no evidence for selected card.

No error should destroy local context-tray selections.

---

## 21. Observability

Log structured events for:

- card create/update/move/revert;
- command interpretation result;
- command execution result;
- entity resolution ambiguity;
- repo scan start/progress/end;
- WebSocket connect/disconnect;
- version conflicts;
- repository evidence promotion/demotion.

Do not log secrets or full sensitive file contents by default.

---

## 22. Success criteria

The subsystem is successful when all of the following are true:

1. It visually reads as a football GM war room rather than a generic SaaS Kanban board.
2. The board remains usable with 3D disabled.
3. Cards can be dragged and reordered accessibly.
4. Workflow status and evidence status are never conflated.
5. Clicking a card exposes detailed implementation/evidence context.
6. Cards/files/tests can be explicitly attached to chat context.
7. Natural-language board operations resolve to typed commands.
8. Ambiguous commands fail closed rather than guessing.
9. Card changes persist and synchronize in real time.
10. Every mutation is recorded and reversible.
11. Repository scanning remains read-only.
12. Candidate repository matches retain confidence/provenance.
13. The initial feature inventory is source-grounded and reviewable.
14. Playwright covers drag, NLP mutation, context, rollback, and no-WebGL operation.
15. Existing Draft Room and Front Office gameplay routes continue to work unchanged unless intentionally integrated later.

---

## 23. Explicit non-goals for the first implementation

Do not include in the first proof build:

- autonomous code editing from GM chat;
- GitHub write operations from the browser;
- multi-repository orchestration;
- production collaboration/permissions;
- full project-management replacement;
- elaborate avatar agents;
- voice control;
- mobile-first 3D;
- proprietary NFL/team visual assets without approved provenance.

These can be layered on after the board kernel, evidence model, and command architecture prove reliable.

---

## 24. Recommended implementation order

```text
1. GM route + visual shell
2. typed board/card contracts
3. static seeded cards
4. drag/drop + details + context tray
5. flat/reduced-motion fallback
6. Playwright smoke test
7. backend persistence
8. append-only event ledger + revert
9. WebSocket synchronization
10. repository read-only index
11. evidence attachment model
12. reviewed feature seed
13. NLP interpretation
14. NLP mutation execution
15. repo reconnaissance + review queue
```

This preserves a vertical-slice learning loop: the user gets the spatial board early, then each following layer adds real evidence and control without forcing the entire architecture to be perfect before it can be tested.

---

## 25. Design self-review

### Placeholder scan

No required implementation behavior is left as `TBD`. Optional future integrations are explicitly labeled non-goals or later slices.

### Internal consistency

- Existing React/FastAPI architecture is preserved.
- Three.js is restricted to spatial presentation while DOM owns readable interactive content.
- React Query owns server state; Zustand owns transient UI state.
- Repository evidence and workflow state remain separate across UI, API, persistence, and NLP.
- Chat mutation flows through typed commands and validation.
- Event history is append-only and reversible.

### Scope check

The complete subsystem is architectural, but delivery is decomposed into five independently testable vertical slices. Implementation planning should begin with **SLICE 01 only**, while preserving the contracts needed by later slices.

### Ambiguity check

The following decisions are intentionally locked:

- New route is `/gm-command-center`.
- Existing gameplay Front Office/Draft Room are not replaced in Slice 01.
- Workflow lanes are `BACKLOG`, `READY`, `IN_PROCESS`, `REVIEW`, `BLOCKED`, `COMPLETE`.
- Card types are `FEATURE`, `WORK_ITEM`, `ISSUE`.
- Repository scanning is read-only.
- Board mutations are persisted and audited only after Slice 02.
- Natural-language mutations are typed/validated and begin in Slice 04.
- Source code editing is not part of this subsystem.

---

## 26. Next gate

After user review of this design specification, create the implementation plan for **SLICE 01 — Visual Board Kernel** using the project’s existing frontend stack and test conventions.

Do not begin implementation until that plan is reviewed under the project’s normal implementation workflow.
