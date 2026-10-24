# Contextual "SportsCenter" Narrator (`TASK-NARRATOR-001`) Implementation Plan

> **For Hermes / Antigravity:** Execute this plan task-by-task using strict Test-Driven Development (Red -> Green -> Refactor) with mandatory terminal verification after every step.

**Goal:** Build a context-aware, hallucination-free "SportsCenter" Broadcast Narrator subsystem (`TASK-NARRATOR-001`) that synthesizes grounded franchise/game/player facts into network-styled anchor scripts (`ESPN`, `CBS`, `FOX`, `NFL_NETWORK`) and speaks them via an optional loopback VoiceStudio (`k2-fsa/OmniVoice`) sidecar or resilient browser `speechSynthesis` fallback with background soundtrack ducking.

**Architecture:** A 4-stage backend pipeline (`FactPacket` builder -> Grounded AI/Template `NarratorScriptService` -> Single-Flight `0600` SHA-256 `NarratorCacheService` -> Loopback-only `VoiceStudioTTSService`) exposed via rate-limited `/api/broadcast/*` endpoints, paired with a React/Zustand HUD (`NarratorBar.tsx`), `AudioContext` volume ducking, and a chunked Web Speech / HTML5 Audio driver (`narratorAudioDriver.ts`).

**Tech Stack:** Python 3.12+, FastAPI, SQLAlchemy 2.0 (`Session` / `AsyncSession`), Pydantic V2, `google-genai` (`aio`), `httpx`, React 19, TypeScript, Zustand, Howler.js, Web Speech API, Playwright.

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking + Deterministic Offline Fallback)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: `TASK-NARRATOR-001` — Contextual "SportsCenter" Narrator

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Classic sports broadcast presentation (ESPN *SportsCenter*, NFL Films, *NFL 2K5* Chris Berman Halftime/Weekly Wrap-up) where the desk anchor contextualizes franchise momentum, last game results, championship pedigree, and individual player storylines as the GM navigates the front office.
- **Related Ideas:** Fact-grounded RAG pipelines, single-flight content-addressed audio caching, OpenAI-compatible TTS sidecar architecture (`debpalash/VoiceStudio` running `k2-fsa/OmniVoice`), and Web Audio / Howler volume ducking.
- **Future Potential:** Extensible to multi-anchor banter, post-playoff documentary retrospectives, and live draft pick desk reactions in 2026/2027 without modifying the core `FactPacket` or caching contracts.
- **Constraints:**
  - **License & Process Boundary:** `debpalash/VoiceStudio` is `AGPL-3.0-only` and `k2-fsa/OmniVoice` weights are `CC-BY-NC` (non-commercial). Never copy VoiceStudio code into this repository; communicate strictly over literal loopback HTTP (`http://127.0.0.1:3900` or `::1`).
  - **SSRF & Security Gate:** Reject non-loopback hosts and hostname strings (including `"localhost"`) via `ipaddress.ip_address(host).is_loopback`; enforce `trust_env=False, follow_redirects=False` and `"x-voicestudio-csrf": "1"`.
  - **Zero Hallucination Gate:** Every `facts_used` ID must exist in `FactPacket.facts` and 100% of numeric `\d+` tokens in the generated script must appear in the serialized `FactPacket`, otherwise degrade immediately to deterministic network templates.
  - **Restricted Cache Permissions:** Disk MP3 cache files must be written atomically with `0o600` permissions and validated via `^[a-f0-9]{64}$`.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Query the database inside `/api/broadcast/narrate`, pass raw ORM objects to `GoogleGenAIProvider` to write an anchor script, send the text to VoiceStudio's `/v1/audio/speech`, and play the returned audio in the browser.

### Powerful Antithesis

1. **Event Loop Blocking:** `GoogleGenAIProvider.generate_text` and `generate_structured` currently call synchronous `self._client.models.generate_content(...)` inside `async def`, blocking the FastAPI event loop.
2. **Hallucination & Prompt Injection:** Unsanitized player backstories or custom names could inject prompt instructions or cause the LLM to invent scores, records, or Super Bowl titles.
3. **Thundering Herd & Cold-Start Timeouts:** First-time `OmniVoice` synthesis lazy-downloads weights (up to 60s), and rapid route changes in React (`MainLayout`) will trigger overlapping TTS calls, audio overlap, and stale playback.
4. **Browser Autoplay & Chromium Web Speech Bugs:** Unmuted `HTMLAudioElement.play()` throws `NotAllowedError` before user interaction; Chromium's `speechSynthesis` silently stops after ~15 seconds or garbage-collects local `SpeechSynthesisUtterance` instances.

### The Superior Synthesis

1. **True Async GenAI + Strict Fact Grounding:** Upgrade `GoogleGenAIProvider` to `await self._client.aio.models.generate_content(...)` with `HttpOptions(api_version="v1", timeout=10_000)`. Strip control characters and cap free-text fields at 160 chars in `FactPacket`. Verify 100% of `facts_used` and numeric tokens against `FactPacket` before accepting AI output; fall back to deterministic network templates (`degraded=True`) on any mismatch.
2. **Single-Flight `0600` Disk Cache & Loopback TTS Client:** Use per-key `asyncio.Lock` keyed by `sha256(f"{model}:{voice}:{seed}:{script}")` with atomic `0o600` writes and 128-file LRU eviction. Use a 60s timeout until the first successful synthesis, then 10s thereafter.
3. **Abortion, Ducking & Chunked Speech Driver:** Track a monotonically increasing `requestId` and `AbortController` in `useNarratorStore`, attenuate `Howl` background music to 20% during narration via `duckVolume()`, retain a module-scoped `activeUtterance` reference, and split browser TTS into `<=180`-character sentence chunks.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** FastAPI, SQLAlchemy 2.0, Pydantic V2, React 19, Vite, Zustand, Playwright
- **Language:** Python 3.12+ (strict `mypy` typing), TypeScript 5.x (zero `any`)
- **State Management:** Zustand (`useNarratorStore`) with `localStorage` persistence (`nfl-sim-narrator-prefs`) + React Context (`AudioContext`)

### 2. The Data Schema (Pre-Generation)

- **Backend Schema:** `backend/app/schemas/narrator.py` (`PageRouteKey`, `NarrationContextRequest`, `FactItem`, `FactPacket`, `StructuredAnchorScript`, `NarrationResponse`)
- **Frontend Types:** `frontend/src/types/narrator.ts` (`PageRouteKey`, `BroadcastStyle`, `NarrationContextRequest`, `NarrationResponse`)

### 3. Step-by-Step Execution

- [x] **Step 1: Config & Schema Scaffolding**
  - Modify: `backend/app/core/config.py`
  - Create: `backend/app/schemas/narrator.py`
  - Create: `frontend/src/types/narrator.ts`
  - Verify: `pytest backend/tests -k "not e2e" --collect-only` and `npm --prefix frontend run build`

- [x] **Step 2A: FactPacket Builder (Team, Last Game, Season & Franchise History)**
  - Create Test: `backend/tests/services/test_narrator_facts_team.py`
  - Create: `backend/app/services/narrator_facts_service.py`
  - Verify: `pytest backend/tests/services/test_narrator_facts_team.py -v`

- [x] **Step 2B: FactPacket Builder (Player Bio, RPG Traits & Backstory Sanitization)**
  - Create Test: `backend/tests/services/test_narrator_facts_player.py`
  - Modify: `backend/app/services/narrator_facts_service.py`
  - Verify: `pytest backend/tests/services/test_narrator_facts_player.py -v`

- [x] **Step 3: Grounded Script Generator & Async `GoogleGenAIProvider` Fix**
  - Create Test: `backend/tests/services/test_narrator_script.py`
  - Modify: `backend/app/services/ai/ai_provider.py`
  - Create: `backend/app/services/narrator_script_service.py`
  - Verify: `pytest backend/tests/services/test_narrator_script.py -v`

- [x] **Step 4: Loopback-Hardened VoiceStudio `httpx` Client**
  - Create Test: `backend/tests/services/test_voicestudio_tts.py`
  - Create: `backend/app/services/voicestudio_tts_service.py`
  - Verify: `pytest backend/tests/services/test_voicestudio_tts.py -v`

- [x] **Step 5: Single-Flight Disk Audio Cache (`0600` Permissions)**
  - Create Test: `backend/tests/services/test_narrator_cache.py`
  - Create: `backend/app/services/narrator_cache_service.py`
  - Verify: `pytest backend/tests/services/test_narrator_cache.py -v`

- [x] **Step 6: Broadcast Narrator Endpoints (`/api/broadcast/*`)**
  - Create Test: `backend/tests/api/test_broadcast_narrator.py`
  - Modify: `backend/app/api/endpoints/broadcast.py`
  - Verify: `pytest backend/tests/api/test_broadcast_narrator.py -v`

- [x] **Step 7: Frontend Audio Ducking, Narrator API Service & Zustand Store**
  - Modify: `frontend/src/context/AudioTypes.ts`
  - Modify: `frontend/src/context/AudioContext.tsx`
  - Create: `frontend/src/services/narrator.ts`
  - Create: `frontend/src/store/useNarratorStore.ts`
  - Verify: `npm --prefix frontend run build`

- [x] **Step 8: Audio Driver (`speechSynthesis` Chunking) & `NarratorBar.tsx` HUD**
  - Create: `frontend/src/services/narratorAudioDriver.ts`
  - Create: `frontend/src/components/audio/NarratorBar.tsx`
  - Modify: `frontend/src/layouts/MainLayout.tsx`
  - Verify: `npm --prefix frontend run lint` and `npm --prefix frontend run build`

- [x] **Step 9: End-to-End Playwright Verification & Final Audit**
  - Create: `frontend/e2e/narrator.spec.ts`
  - Verify:
    - `pytest backend/tests/services/test_narrator_*.py backend/tests/services/test_voicestudio_tts.py backend/tests/api/test_broadcast_narrator.py -v`
    - `mypy backend/app/schemas/narrator.py backend/app/services/narrator_facts_service.py backend/app/services/narrator_script_service.py backend/app/services/voicestudio_tts_service.py backend/app/services/narrator_cache_service.py`
    - `npm --prefix frontend run build`
    - `npx --prefix frontend playwright test e2e/narrator.spec.ts`

### 4. Edge Cases & Error Handling

- **Preseason / Week 1 (No Played Games):** Emits valid `FactPacket` with `0-0` record and season opener storyline without raising `NoResultFound`.
- **Hallucinated Numbers / Invalid Fact IDs:** Rejected by `NarratorScriptService` post-validation; seamlessly degrades to deterministic network-specific template (`degraded=True`).
- **VoiceStudio Offline / `409` Ambiguous Voice / Timeout:** Returns `audio_url=None, voice_source="browser", degraded=True`; frontend plays chunked Web Speech synthesis and displays `Browser Voice` badge.
- **SSRF / Non-Loopback URL:** `VoiceStudioTTSService` rejects any non-loopback IP or hostname (including `"localhost"`) before opening a socket.
- **Browser Autoplay Blocked (`NotAllowedError`):** Caught cleanly by `narratorAudioDriver.ts`, sets `needsUserGesture = true`, and restores soundtrack volume.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** Zero `any` types in TypeScript (`npm --prefix frontend run build` & `lint`) and clean `mypy` check on all new backend modules.
- [x] **Security:** Loopback IP enforcement (`127.0.0.1` / `::1`), prompt-injection sanitization (control-char stripping + 160-char cap), path traversal prevention (`^[a-f0-9]{64}$`), and `0o600` cache file permissions verified.
- [x] **Performance:** True async `self._client.aio.models.generate_content`, single-flight per-key `asyncio.Lock`, 128-file LRU cache eviction, and `AbortController` cancellation on route change.
- [x] **Self-Critique:** Ensure soundtrack ducking always restores volume in `finally` / `onended` / `onerror` / `stop()` paths so background audio never remains stuck at 20% volume.
</final_audit>

---

<baton_handoff>
Next Immediate Step: All 9 TDD steps and Phase 4 audit checks for `TASK-NARRATOR-001` are verified and complete. Optionally launch a local VoiceStudio sidecar on `http://127.0.0.1:3900` to switch from `Browser Voice` fallback to neural `OmniVoice` MP3 synthesis.
</baton_handoff>
