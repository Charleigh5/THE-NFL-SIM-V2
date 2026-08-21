<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [UI-001] Madden and NCAA 25 Gridiron Visual Redesign

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** EA Sports Madden NFL franchise (Madden 24/25/26), EA Sports College Football 25 (CFB 25) Dynasty Hub, and modern sports television broadcast packages (Fox Sports, ESPN, CBS, Prime Video Thursday Night Football).
- **Related Ideas:** Next Gen Stats AWS telemetry, Frostbite Engine HUD aesthetic, tactile sports card collection mechanics (Ultimate Team, Dynasty Big Board), Web Audio API stadium sound design.
- **Future Potential:** 3D WebGPU dynamic player card holograms, live multi-angle broadcast replay camera views, real-time AI coach video press conferences.
- **Constraints:** Must maintain 100% backward compatibility with existing React Router v7 routes, data loaders, backend API contracts, and Playwright E2E test IDs (`data-testid`). Strict TypeScript typing (zero `any`), responsive across desktop & mobile.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Apply a generic CSS dark-mode skin with neon accents and static sports icon badges.

### Powerful Antithesis
A surface-level skin does not solve the user's core dissatisfaction. Modern sports games like Madden 25 and College Football 25 evoke emotional immersion through **Dynamic Team Identity** (the entire UI bleeds the colors, stadium atmosphere, and logo of the managed franchise), **Authentic Broadcast Graphics** (official Fox/ESPN style scorebugs with down-and-distance laser pills, possession footballs, and timeout dots), **Tactile Player Presentation Cards** (99 Club gold shields, dev traits, attribute polygons), and **Chalkboard Play Art** with real football route trees.

### The Superior Synthesis
Engineer a comprehensive **Dynasty & Franchise Design System** built on:
1. Dynamic franchise color injection (Primary/Secondary/Accent HSL tokens with real NFL vector logos).
2. Broadcast HUD package with authentic scorebug, momentum meter, and home-field crowd noise decibel meter.
3. Ultimate/Dynasty Player Cards featuring metallic OVR shields (99 Club gold, 90+ elite, 80+ gold, 70+ silver), dev trait badges (Normal, Star, Superstar, X-Factor), and athletic attribute bars.
4. Franchise War Room Command Center with Matchup of the Week clash banner, 53-man roster health breakdown, salary cap room meter, and breaking media wire feed.
5. Interactive chalkboard playbook with animated route stems and defensive coverage shells.
6. Synthesized stadium sound design (whistle, crowd roar, horn, snap).
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** React 19, Vite, Tailwind CSS v4, Framer Motion, Lucide React, Web Audio API
- **Language:** Strict TypeScript 5.9+ (zero `any`, full interfaces)
- **State Management:** Zustand (`useSettingsStore`, `useSimulationStore`), ThemeProvider (`ThemeContext`)

### 2. The Data Schema (Pre-Generation)
```typescript
export interface FranchiseTheme {
  teamId: number;
  abbreviation: string;
  name: string;
  city: string;
  conference: "AFC" | "NFC";
  division: "North" | "South" | "East" | "West";
  colors: {
    primary: string;
    secondary: string;
    accent: string;
  };
  stadium: string;
  established: number;
}

export interface PlayerCardPresentation {
  id: number;
  name: string;
  jerseyNumber: number;
  position: string;
  overallRating: number;
  archetype: string;
  devTrait: "NORMAL" | "STAR" | "SUPERSTAR" | "XFACTOR";
  morale: "Ecstatic" | "Happy" | "Content" | "Unhappy" | "Disgruntled";
  keyAttributes: {
    speed: number;
    acceleration: number;
    strength: number;
    agility: number;
    awareness: number;
  };
}
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Design Tokens & Styling Core.** Enhance `frontend/src/index.css` with football stadium textures, OVR tier shields, turf lines, and broadcast scorebug tokens.
- [ ] **Step 2: Audio & Atmosphere Engine.** Create `frontend/src/services/soundEffects.ts` with Web Audio API stadium whistles, buzzers, crowd roars, and card snaps.
- [ ] **Step 3: Dynamic Navigation & Header.** Redesign `frontend/src/components/Navigation.tsx` into a high-impact Dynasty Franchise Navigation Hub with live franchise record and cap space.
- [ ] **Step 4: Franchise War Room Dashboard.** Redesign `frontend/src/pages/Dashboard.tsx` with Matchup of the Week banner, Roster Health breakdown, Media Wire, and tactical action tiles.
- [ ] **Step 5: Ultimate/Dynasty Player Cards.** Overhaul `frontend/src/components/ui/PlayerCard.tsx`, `PlayerCard.css`, and `DraggableCard.tsx` with metallic OVR shields, dev trait flames, and attribute bars.
- [ ] **Step 6: Broadcast Scorebug & Live Sim.** Elevate `frontend/src/components/ScoreBoard.tsx` and `frontend/src/pages/LiveSim.tsx` with TV broadcast scorebug, possession pill, timeout dots, and crowd decibel meter.
- [ ] **Step 7: Franchise Roster Central.** Enhance `frontend/src/pages/FrontOffice.tsx` with position group tabs, sort filters, and comprehensive player comparison.
- [ ] **Step 8: Chalkboard Playbook & Strategy.** Upgrade `frontend/src/pages/Playbook.tsx` with formation personnel sets and route tree diagrams.
- [ ] **Step 9: Stadium Tunnel Franchise Selector.** Polish `frontend/src/pages/TeamSelection.tsx` with division groupings, team ratings, and instant live theme switching.

### 4. Edge Cases & Error Handling
- **Edge Case 1: Logo image load failure** -> Fall back gracefully to high-contrast team abbreviation on colored badge.
- **Edge Case 2: Audio disabled / blocked by browser autoplay policy** -> Silently catch Web Audio context resume errors without blocking user interaction.
- **Edge Case 3: Missing player attributes or stats** -> Default to calculated position-specific positional baseline ratings.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** No `any` types allowed, strict TypeScript build verified via `npm run build`.
- [ ] **Security:** Client-side audio generation sanitized, zero external CDN scripts.
- [ ] **Performance:** 60fps GPU-accelerated CSS animations and canvas rendering maintained.
- [ ] **Self-Critique:** Verified all existing `data-testid` attributes and route loaders remain 100% intact for automated test suites.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to implementation phase upon approval.
</baton_handoff>
