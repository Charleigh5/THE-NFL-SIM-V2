<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [DEP-007] Frontend Gridiron Heatmap Telemetry & Playwright E2E Suite

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** High-density sports management interfaces (Football Manager, Out of the Park Baseball, CAD/engineering dashboards) require live visual telemetry and automated E2E regression verification.
- **Related Ideas:** 2D canvas gridiron rendering, live heatmap overlays, Playwright headless browser orchestration.
- **Future Potential:** WebGL 3D physics rendering with real-time player telemetry particles and interactive instant replays.
- **Constraints:** Zero `any` types in TypeScript, zero purple-on-dark cliché tropes, 100% Playwright test reliability across user flows.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Only test backend APIs with unit tests and manually test the frontend UI in a browser window.

### Powerful Antithesis
Manual frontend testing misses broken route bindings, unhandled JSON parsing errors, missing CSS variables, and layout crashes across complex user flows (Draft Room, Medical Center, Roster Editor).

### The Superior Synthesis
1. Build high-density **Gridiron Turf Heatmap & Telemetry Canvas** in `frontend/src/components/GridironVisualizer.tsx` displaying 10x10 turf wear and player cognitive stress badges.
2. Build an automated **Playwright E2E Test Suite** in `tests/e2e/test_hyper_immersive_e2e.py` testing live browser flows with real FastAPI backend integration.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** React 19, Vite, TypeScript, TailwindCSS / Vanilla CSS Tokens, Playwright 1.55+
- **Language:** Strict TypeScript (zero `any`) / Python pytest-playwright
- **State Management:** Zustand Store + WebSocket Telemetry Stream

### 2. The Data Schema (Pre-Generation)
```typescript
export interface TurfWearOverlayData {
  zones: Array<{
    x: number;
    y: number;
    wearLevel: number; // 0.0 - 1.0
    color: string; // Dynamic green -> amber -> brown
  }>;
}

export interface PlayerTelemetryBadge {
  playerId: string;
  jerseyNumber: number;
  cognitiveState: 'RELAXED' | 'FOCUSED' | 'STRESSED' | 'PANICKED' | 'FLOW';
  visionConeAngle: number;
  s2LatencyMs: number;
}
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Configure `tests/e2e/conftest.py` with FastAPI test server background process fixture.
- [ ] **Step 2: Core Logic.** Build `GridironVisualizer.tsx` with 10x10 canvas wear grid and cognitive overlay.
- [ ] **Step 3: Interface.** Execute full Playwright test suite exercising:
  - Draft Room rookie selection flow
  - Medical Center injury rehabilitation flow
  - Live Simulation with turf wear progression.

### 4. Edge Cases & Error Handling
- **Case A: Slow WebSocket Telemetry** -> Implement interpolation and frame-smoothing buffer.
- **Case B: Headless CI Display Failure** -> Configure Playwright headless mode with `--no-sandbox` and explicit viewport size.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** TypeScript `tsc --noEmit` passes with zero errors and zero `any`.
- [ ] **Security:** Sanitized input fields and secure WebSocket connections.
- [ ] **Performance:** 60fps canvas rendering with < 5% CPU usage.
- [ ] **Self-Critique:** Ensure visual aesthetics avoid generic purple-on-dark tropes, using monograph CAD-grade typography and balanced whitespace.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Run `pytest tests/e2e -v` to confirm complete end-to-end integration.
</baton_handoff>
