<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK_015_LOCKER_ROOM_SOCIAL_GRAPH_AND_MEDIA_LEAKS_ENGINE

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - An NFL locker room is a complex sociological ecosystem of 53 to 70 high-performing athletes divided into positional sub-cultures, seniority hierarchies, and competing personality factions.
  - Sociological research (e.g., Coleman social capital, Festinger social comparison theory) demonstrates that cohesion and tension are not uniform scalar values, but networked phenomena. Subgroups ("cliques") form around position rooms (e.g., Offensive Line vs. Defensive Backs), draft cohorts, and shared psychological traits (Alpha Competitors, Mercenaries, Leaders, Quiet Workhorses).
  - When closed-door council events occur (disciplining a star, benching a struggling quarterback, or restructuring contracts), friction does not remain sealed within four walls—it leaks to prominent national insiders (e.g., Schefter, Rapoport) and vocal local beat writers.
  - In `THE-NFL-SIM-V2`, the Locker Room Council (`TASK-011`) implemented deterministic Tier 1 differential equations and event-driven narrative synthesis. However, the UI currently presents aggregate team cohesion percentages and isolated player cards without revealing the underlying social graph or the external media fallout.

- **Related Ideas & Industry Parallels:**
  - *D3-Force / Cytoscape Graph Topologies*: Spring-embedded force simulation calculating node repulsion, link elasticity, and cluster modularity for social networks.
  - *Crusader Kings III Character Court & Relationship Graph*: Visualizing rivalries, friendships, mentorships, and internal court factions with dynamic opinion modifiers.
  - *Football Manager Social Groups & Dynamics Hierarchy*: Hierarchy pyramids (Team Leaders, Highly Influential, Other Players) and Core Social Groups with influence propagation.

- **Future Potential (2026/2027):**
  - Player trade demands with public holdout boycotts, coaching staff mutinies, locker room fistfights, and agent-driven whisper campaigns influencing free agency appeal.

- **Constraints:**
  - **Latency Ceiling:** $<2$ms for social graph node/edge calculations; 60 FPS hardware-accelerated canvas/SVG rendering for 53 nodes.
  - **Type Safety:** 0 `any` types across backend schemas and frontend graph components.
  - **Deterministic Social Physics:** Reproducible graph clustering seeded by franchise team state.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Use a heavy third-party graph visualization library (like Cytoscape or full D3) inside `LockerRoomCouncil.tsx` to render all 53 players as draggable nodes with physics simulation running continuously on the main thread, and post random pre-written tweets into a news feed when a council event finishes.

### Powerful Antithesis
- **Performance Collapse & Thermal Throttling**: Running continuous iterative force-directed physics for 53 nodes and ~150 edges on the React main thread will drop frame rates below 30 FPS, causing severe UI jank during council navigation.
- **Narrative Disconnect**: Generic pre-written tweets feel hollow and repetitive. If a GM benches a 94 OVR quarterback, the leaked tweet must accurately quote the quarterback's camp, reference the locker room divide, and name specific beat reporters.
- **Visual Clutter**: A 53-node raw hairball graph is unreadable on mobile screens and cluttered on desktop. Users cannot discern key cliques or toxic instigators without clustering and focal filtering.

### The Superior Synthesis
Architect a **Hierarchical Social Graph & Contextual Media Leaks Pipeline**:
1. **Clustered Social Graph Engine**: Backend calculates network edges based on 3 deterministic relational dimensions:
   - *Position Room Affinity* ($W_{\text{pos}} = 0.60$)
   - *Draft Class / Age Proximity* ($W_{\text{tenure}} = 0.25$)
   - *Personality Trait Resonance & Trust Scores* ($W_{\text{trait}} = 0.15$)
   Nodes are partitioned into 4 distinct modularity cliques (Offensive Leaders, Defensive Core, Veteran Faction, Disgruntled Rebels).
2. **Pre-Computed Lightweight Canvas/SVG Renderer**: Instead of continuous browser physics, execute 100 iterations of spring force layout on data load or via a Web Worker, freeze coordinates into normalized viewport coordinates $[0, 1000] \times [0, 600]$, and render with lightweight SVG nodes and animated glowing edges.
3. **Beat Writer & National Insider Leaks Dispatcher**: Following any Closed-Door Council resolution, if team tension exceeds $65.0$ or any player's individual tension exceeds $80.0$, a deterministic media leak generator creates high-fidelity social media dispatches (formatted with verified checkmarks, timestamp, source attribution, and fallout sentiment).
4. **Contract Holdout & Mutiny Gating**: If a player's tension reaches $\ge 90.0$ and their contract value is below market top-15, trigger an explicit `HOLDOUT_DECLARED` status, preventing game day dressing and displaying a red flame aura on the graph.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Backend:** FastAPI, Pydantic V2, NetworkX / native graph algorithms in Python.
- **Frontend:** React 19, TypeScript 5.x, SVG with Framer Motion, Lucide Icons.
- **State Management:** `useLockerRoomStore.ts` synchronized with active team roster.
- **Styling:** Cyber-gridiron dark theme (`#080d1a`), neon node glow (Leadership `#10b981`, Neutral `#3b82f6`, Toxic/High Tension `#ef4444`).

### 2. The Data Schema (Pre-Generation)

#### Backend Schemas (`backend/app/schemas/social_graph.py`)
```python
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field, ConfigDict

class GraphNode(BaseModel):
    id: int
    name: str
    position: str
    overall_rating: int
    tension_score: float
    trust_in_coach: int
    clique_id: str = Field(description="E.g. 'OFF_LEADERS', 'DEF_CORE', 'VETERANS', 'REBELS'")
    role: Literal["CAPTAIN", "MENTOR", "STUBBORN_VET", "DISRUPTOR", "NEUTRAL"]
    x: float
    y: float
    is_holding_out: bool = False

class GraphEdge(BaseModel):
    source: int
    target: int
    weight: float = Field(ge=0.0, le=1.0)
    relationship_type: Literal["BOND", "RIVALRY", "MENTORSHIP", "FRICTION"]

class MediaLeakPost(BaseModel):
    id: str
    author_name: str
    author_handle: str
    author_avatar: str
    outlet: Literal["ESPN", "NFL_NETWORK", "THE_ATHLETIC", "LOCAL_BEAT"]
    timestamp_str: str
    headline: str
    content: str
    sentiment: Literal["NEGATIVE", "NEUTRAL", "POSITIVE", "SCANDAL"]
    referenced_player_ids: List[int]
    leak_source: Literal["ANONYMOUS_PLAYER", "AGENT", "COACHING_STAFF", "FRONT_OFFICE"]

class LockerRoomSocialNetworkResponse(BaseModel):
    team_id: int
    cliques: Dict[str, str]
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    active_leaks: List[MediaLeakPost]
    team_morale_index: float
    model_config = ConfigDict(from_attributes=True)
```

#### Frontend TypeScript Contracts (`frontend/src/types/socialGraph.ts`)
```typescript
export type SocialRole = "CAPTAIN" | "MENTOR" | "STUBBORN_VET" | "DISRUPTOR" | "NEUTRAL";
export type RelationshipType = "BOND" | "RIVALRY" | "MENTORSHIP" | "FRICTION";
export type LeakOutlet = "ESPN" | "NFL_NETWORK" | "THE_ATHLETIC" | "LOCAL_BEAT";

export interface GraphNode {
  id: number;
  name: string;
  position: string;
  overallRating: number;
  tensionScore: number;
  trustInCoach: number;
  cliqueId: string;
  role: SocialRole;
  x: number;
  y: number;
  isHoldingOut: boolean;
}

export interface GraphEdge {
  source: number;
  target: number;
  weight: number;
  relationshipType: RelationshipType;
}

export interface MediaLeakPost {
  id: string;
  authorName: string;
  authorHandle: string;
  authorAvatar: string;
  outlet: LeakOutlet;
  timestampStr: string;
  headline: string;
  content: string;
  sentiment: "NEGATIVE" | "NEUTRAL" | "POSITIVE" | "SCANDAL";
  referencedPlayerIds: number[];
  leakSource: string;
}

export interface LockerRoomSocialNetworkResponse {
  teamId: number;
  cliques: Record<string, string>;
  nodes: GraphNode[];
  edges: GraphEdge[];
  activeLeaks: MediaLeakPost[];
  teamMoraleIndex: number;
}
```

### 3. Step-by-Step Execution

#### Step 1: Scaffolding
- [ ] Create backend schema: `backend/app/schemas/social_graph.py`.
- [ ] Create backend service: `backend/app/services/social_graph_engine.py`.
- [ ] Create backend router: `backend/app/api/endpoints/social_graph.py` and register in `backend/app/core/setup.py`.
- [ ] Create frontend types: `frontend/src/types/socialGraph.ts`.
- [ ] Create frontend API client: `frontend/src/services/socialGraphApi.ts`.
- [ ] Create frontend components: `frontend/src/components/social/LockerRoomGraphCanvas.tsx` and `frontend/src/components/social/MediaLeaksFeed.tsx`.

#### Step 2: Core Logic Implementation
- [ ] Implement `SocialGraphEngine.build_team_social_graph(team_id)`:
  - Query all players on roster with attributes, tension, trust, and psychological DNA.
  - Calculate pair-wise affinity matrix using position affinity, age deltas, and trait compatibility.
  - Assign clique clusters via community detection algorithm (Greedy Modularity).
  - Execute deterministic 2D spring-embedding layout (Fruchterman-Reingold) scaled to $[100, 900] \times [100, 500]$.
- [ ] Implement `SocialGraphEngine.generate_media_leaks(team_id, event_outcome)`:
  - If event increases tension above threshold ($\ge 65.0$), sample a beat reporter personality (e.g. "Ian Rapoport", "Adam Schefter", "Local Beat Writer").
  - Dynamically construct leak text citing anonymous locker room discontent, contract dispute, or leadership endorsement.
- [ ] Implement holdout trigger: Flag players with `tension_score >= 90.0` as `is_holding_out = True`.

#### Step 3: Interface & UX Integration
- [ ] Build `LockerRoomGraphCanvas.tsx`:
  - Interactive SVG canvas with smooth zoom/pan controls.
  - Node rendering: Colored circles by clique with player initials, rating badge, and pulsating tension aura if $>75.0$.
  - Edge rendering: Connecting lines with animated dashed strokes for friction and solid lines for mentorship bonds.
  - Hover card displaying player backstory, personality archetype, trust bars, and relationship links.
- [ ] Build `MediaLeaksFeed.tsx`:
  - Authentic social feed widget styled like verified NFL insider posts.
  - Sound effect or flashing "BREAKING LEAK" banner when new leak arrives.
  - Filter toggle: "All News", "Beat Leaks", "Holdout Alerts".

### 4. Edge Cases & Error Handling
- [Case A: Player Has No Connections (Isolated Node)] -> Ensure default gravity pulls isolated players into the general perimeter rather than flying offscreen.
- [Case B: All Players Have Low Tension (<20.0)] -> Media feed renders positive culture beats ("Veteran leadership praised inside team facility").
- [Case C: Star Player Holdout Declared] -> UI renders high-priority warning banner in Roster and Depth Chart pages showing player inactive due to holdout.
- [Case D: Mobile Screen Viewport (<640px)] -> Graph switches to list-based "Locker Room Factions" breakdown for touch-friendly accessibility.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** 0 `any` types across backend schemas and frontend components. Verified with `tsc --noEmit` and `pyright`.
- [ ] **Security:** Team ID validation prevents accessing opponent locker room telemetry in competitive game modes.
- [ ] **Performance:** Graph calculation executes in $<2$ms in Python backend; SVG canvas runs at a locked 60 FPS with zero re-layout lag.
- [ ] **Self-Critique:** Is the layout deterministic? Yes, random number generator is seeded with `team_id + season_year`, guaranteeing identical node coordinates across reloads unless locker room state mutates.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Scaffold `backend/app/schemas/social_graph.py` and implement `backend/app/services/social_graph_engine.py`.
</baton_handoff>
