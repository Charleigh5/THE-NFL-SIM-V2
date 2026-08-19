# BROADCAST PHASE BOARD
Status legend: TODO | DOING | DONE | BLOCKED | NEEDS_DECISION
Rule: one PHASE_ID per agent turn. One TASK_ID per implementation burst.

## Active
- PHASE_ID: A
- TASK_ID: A1
- BLOCKED_BY: none

## Phase A — Cutscene System Scaffold
Goal: inspectable state machine + typed contracts. No hero art. No full clips.
Gate: a play can enter PRE_PLAY → PLAY_EXEC → POST_PLAY → REPLAY → BETWEEN_DOWNS
      and emit a ClipCue JSON without crashing LiveGameVisualizer.

| ID | Subtask | Depends | Files | DoD | Status |
|----|---------|---------|-------|-----|--------|
| A1 | Create board files and schema types | — | docs/tasks/BROADCAST_PHASE_BOARD.md, docs/tasks/broadcast_phase_board.json, frontend/src/types/broadcast.ts | files exist; types compile | DONE |
| A2 | Define BroadcastPhase enum + transition table | A1 | frontend/src/types/broadcast.ts, backend/app/schemas/broadcast.py | illegal transitions throw; 7 legal states documented | DONE |
| A3 | ClipCue / CameraShot / OverlayCue Pydantic+TS twins | A2 | backend/app/schemas/broadcast.py, frontend/src/types/broadcast.ts | field names match 1:1; no ORM types | DONE |
| A4 | Zustand broadcast slice | A3 | frontend/src/store/useBroadcastStore.ts | phase, activeClip, camera, overlays, reduce(event) | TODO |
| A5 | CutsceneDirector class (no React) | A4 | frontend/src/broadcast/CutsceneDirector.ts | given PlayResult, returns ordered ClipCue[] | TODO |
| A6 | Wire director into LiveGameVisualizer behind flag | A5 | LiveGameVisualizer.tsx | `enableBroadcast=false` default; no visual change when false | TODO |
| A7 | Backend GET /api/live/game/{id}/broadcast/{play_id} | A3 | live_visualization.py | returns ClipCue[]; Session never in response_model | TODO |
| A8 | Unit tests for transitions + cue schema | A5,A7 | frontend + backend tests | illegal transition fails; cue roundtrips JSON | TODO |
| A9 | Phase A evidence packet | A8 | docs/tasks/evidence/A_SCAFFOLD.md | screenshot or log of state walk; star audit | TODO |

## Phase B — Pre-Play Cinematics
Goal: before the snap, show formation, matchup, down/distance. 4–7 seconds.
Gate: user can see formation sweep + HUD cards using real roster data.

| ID | Subtask | Depends | Files | DoD | Status |
|----|---------|---------|-------|-----|--------|
| B1 | PrePlayClip catalog (formation_sweep, matchup_card, situation_lower_third) | A9 | frontend/src/broadcast/clips/preplay.ts | 3 clip ids, durations, camera paths | TODO |
| B2 | CameraPath interpolator | B1 | frontend/src/broadcast/camera/CameraRig.ts | lerp/slerp a shot list at 60fps | TODO |
| B3 | Down/distance + play-clock lower third | B1 | frontend/src/components/broadcast/SituationBar.tsx | 8px grid, text inside container, AAA contrast | TODO |
| B4 | MatchupCard (one O vs one D from roster) | B3 | frontend/src/components/broadcast/MatchupCard.tsx | uses VisualPlayer; jersey + position + rating | TODO |
| B5 | FormationSweep: camera trucks LOS, players hold stance | B2 | LiveGameVisualizer + EnhancedPlayerCharacter | 22 players visible; no clip through turf | TODO |
| B6 | Pre-play audio cue stubs (no licensed music) | B1 | frontend/src/broadcast/audio/preplay.ts | play/stop functions; silent if file missing | TODO |
| B7 | Skip / reduced-motion path | B5 | useBroadcastStore | skip jumps to PLAY_EXEC; reduced-motion skips truck | TODO |
| B8 | Bind to formation endpoint | B5,A7 | useLiveVisualizationStore | uses /formation/{play_id}; fallback to last roster | TODO |
| B9 | 5-star visual audit + evidence | B7,B8 | docs/tasks/evidence/B_PREPLAY.md | all 3 clips 5/5 or listed FAIL+patch | TODO |

## Phase C — Play Execution Animations
Goal: replace PlayAnimator setTimeout with a clip timeline driven by PlayResult.
Gate: pass, run, sack, punt, FG each play a distinct motion using existing meshes.

| ID | Subtask | Depends | Files | DoD | Status |
|----|---------|---------|-------|-----|--------|
| C1 | Inventory PlayAnimator + PlayResult fields | A9 | PlayAnimator.tsx, types/simulation | write field map in board notes | TODO |
| C2 | TimelineClock (16.66ms tick, seek, pause) | C1 | frontend/src/broadcast/TimelineClock.ts | 60Hz; seek(ms); onComplete | TODO |
| C3 | PlayerPose track format | C2 | frontend/src/broadcast/tracks/PlayerPoseTrack.ts | {playerId, t, x, y, z, yaw, clip} | TODO |
| C4 | BallTrack format | C3 | frontend/src/broadcast/tracks/BallTrack.ts | snap → release → flight → catch/incomplete | TODO |
| C5 | Motion recipes: pass / run / sack / punt / FG | C4 | frontend/src/broadcast/recipes/*.ts | each recipe returns pose+ball tracks from PlayResult | TODO |
| C6 | Replace PlayAnimator timers with TimelineClock | C5 | PlayAnimator.tsx | no setTimeout animation; clock drives poses | TODO |
| C7 | EnhancedPlayerCharacter pose consumer | C6 | EnhancedPlayerCharacter.tsx | apply x,z,yaw; keep existing body/jersey logic | TODO |
| C8 | Position stance library (14 positions, idle+explode) | C7 | frontend/src/broadcast/stances.ts | QB drop, OL crouch, WR 2pt, K plant | TODO |
| C9 | Collision-safe yards: stay on field bounds | C7 | recipes | no player x outside [-60,60] or z outside hashes+sideline pad | TODO |
| C10 | Play type visual tells (pass vs run readable by 1s) | C8 | recipes + camera | blind user test note in evidence | TODO |
| C11 | 5-star motion audit + evidence | C10 | docs/tasks/evidence/C_PLAY.md | 5 play types recorded; 60fps claim measured | TODO |

## Phase D — Replay System
Goal: after a scoring play, turnover, or 15+ yard gain, optional replay.
Gate: 2 camera angles, 0.5x/1x, overlay telestrator stub, return to between-downs.

| ID | Subtask | Depends | Files | DoD | Status |
|----|---------|---------|-------|-----|--------|
| D1 | Replay trigger rules | C11 | frontend/src/broadcast/replay/triggers.ts | score, turnover, sack, 15+ yards, user request | TODO |
| D2 | Clip buffer: last N ms of pose+ball+camera | D1 | frontend/src/broadcast/replay/ReplayBuffer.ts | ring buffer; dump to ReplayTake | TODO |
| D3 | Angle set: all22, sideline, endzone, sky | D2 | CameraRig.ts | 4 named shots; no new meshes required | TODO |
| D4 | Transport UI: scrub, 0.5x, 1x, skip | D3 | frontend/src/components/broadcast/ReplayTransport.tsx | keyboard + click; text inside hit targets | TODO |
| D5 | Telestrator overlay stub (circle + arrow) | D4 | frontend/src/components/broadcast/Telestrator.tsx | SVG over canvas; 8px grid; hide on skip | TODO |
| D6 | Stats bug (yards, passer, tackler) | D5 | frontend/src/components/broadcast/ReplayBug.tsx | data from PlayResult only | TODO |
| D7 | Auto-exit to BETWEEN_DOWNS | D4 | CutsceneDirector | max 8s unless user holds replay | TODO |
| D8 | Backend optional persist replay take | D2 | live_visualization.py | POST optional; do not block UI if 404 | TODO |
| D9 | 5-star replay audit + evidence | D7 | docs/tasks/evidence/D_REPLAY.md | two angles + skip proven | TODO |

## Phase E — Visual Asset Pipeline
Goal: generate/assign team + position visual kits from roster data.
Gate: 2 sample teams render with correct colors, body types, logos; no new ORM columns.

| ID | Subtask | Depends | Files | DoD | Status |
|----|---------|---------|-------|-----|--------|
| E1 | Asset manifest schema | A9 | frontend/src/assets/visual/manifest.ts | kit ids, lod, license, path | TODO |
| E2 | TeamKit resolver from VisualTeam colors | E1 | frontend/src/assets/visual/teamKit.ts | primary/secondary/helmet/endzone | TODO |
| E3 | PositionKit: 14 position body+gear maps | E2 | frontend/src/assets/visual/positionKit.ts | uses existing body_type mapping | TODO |
| E4 | Logo loader from /logos/{ABBR}.png with fallback | E3 | frontend/src/assets/visual/logo.ts | missing file → abbreviation glyph | TODO |
| E5 | Jersey number decal on EnhancedPlayerCharacter | E3 | EnhancedPlayerCharacter.tsx | number readable at sideline cam | TODO |
| E6 | Helmet stripe + facemask from kit | E5 | EnhancedPlayerCharacter.tsx | no extra draw-call explosion on low LOD | TODO |
| E7 | Field endzone colors from home/away kits | E2 | EnhancedFieldVisualizer.tsx | home/away ends distinct | TODO |
| E8 | Procedural kit bake script (optional CLI) | E3 | scripts/bake_visual_kits.py | writes JSON kits; no binary blobs in git | TODO |
| E9 | License + provenance ledger | E1 | docs/tasks/ASSET_PROVENANCE.md | every path: authored / public / missing | TODO |
| E10 | 5-star kit audit + evidence | E7,E9 | docs/tasks/evidence/E_ASSETS.md | 2 teams, 14 positions sampled | TODO |

## Cross-phase rules
- A is the only phase that may run with no prior DONE rows.
- B and C both require A9 DONE.
- D requires C11 DONE.
- E may run after A9 (parallel to B/C) but must not edit PlayAnimator.
- Never mark a row DONE without proof in docs/tasks/evidence/.

## Notes
- Field coords: yardLine 0-100 maps to X = (yardLine/100)*120 - 60.
- Reuse existing live-vis files. Do not regenerate LiveGameVisualizer, EnhancedPlayerCharacter, roster endpoint, or Player ORM.
- No Session / AsyncSession / raw SQLAlchemy types in any response_model.
- No new npm/pip packages unless justified.
- No Madden/NFL licensed content. Author original broadcast language.
