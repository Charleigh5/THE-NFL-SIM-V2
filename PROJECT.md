# Project: THE-NFL-SIM-V2 UI/UX Tactical Gridiron Overhaul (TASK-041)

## Architecture
- **Design Token & Style Engine**: Tailwind CSS v4.1.18 CSS-first configuration (`frontend/src/index.css`), zero-blur hard shadows (`--shadow-hard-md: 3px 3px 0px #000000`, `--shadow-hard-primary`, `--shadow-hard-pressed: 1px 1px 0px #000000`), tactile corner radius ceiling (`--radius-tactile-sm: 2px` [`rounded-[2px]`], `--radius-tactile-md: 4px` [`rounded-sm`]).
- **Optical Vector Icon Grammar**: Domain-authentic gridiron SVG vector icons in `frontend/src/components/icons` (`BlitzBoltIcon`, `GridironIcon`, `YardHashesIcon`, `ChalkboardRouteIcon`, `HelmetIcon`, `PlayClockIcon`, etc.), purging 100% of generic AI sparkles (`Sparkles` from `lucide-react`).
- **Interactive Playoff Tournament Bracket**: `frontend/src/components/season/PlayoffBracket.tsx` re-architected with responsive SVG cubic bezier splines, deterministic 15-slot bracket geometry (CLS = 0), franchise seed and helmet badges, retiring legacy `PlayoffBracket.css`.
- **Interactive SVG Playbook Route Tree Diagrammer**: `frontend/src/components/playbook/RouteDiagrammer.tsx` and `frontend/src/pages/Playbook.tsx` replacing placeholder compass with animated SVG stems, route breaks, cuts, defensive coverage drops, and interactive player tokens for installed plays (Go, Slant, Mesh, Dig, Zone).
- **Gridiron Telemetry Loader & 12-State Interactive Matrix**: `frontend/src/components/ui/LoadingSpinner.tsx` transformed into a 25-second digital play-clock radar sweep with sweep telemetry, accompanied by full 12-state interactive matrix coverage (`idle`, `hover`, `pressed`, `focused`, `dragging`, `drop-target`, `selected`, `disabled`, `loading`, `success`, `warning`, `error`).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Anti-Template Firewall Radius Ceiling | Purge all instances of rounded-xl, rounded-2xl, rounded-3xl, and pill rounded-full across core pages, modals, HUD cards in favor of rounded-[2px] / rounded-sm | M1 | Survey / R1 |
| 2 | Zero-Blur Hard Shadows | Replace soft blurry shadows (shadow-2xl, shadow-xl, shadow-lg) with directional zero-blur hard shadows (shadow-hard-md, shadow-hard-primary, shadow-hard-pressed) | M1 | Survey / R1 |
| 3 | Optical Vector Symbol Grammar Migration | Purge 100% of generic `Sparkles` from `lucide-react` across 17 files, replacing with authentic gridiron vector icons (`BlitzBoltIcon`, `GridironIcon`, `YardHashesIcon`, `ChalkboardRouteIcon`, etc.) | M1 | Survey / R2 |
| 4 | Connected SVG Playoff Bracket Engine | Re-architect `PlayoffBracket.tsx` with responsive SVG cubic bezier connector lines, seeds, helmets, zero layout shifting (CLS = 0) | M2 | Survey / R3 |
| 5 | Legacy PlayoffBracket.css Retirement | Delete unstyled/legacy `PlayoffBracket.css` and migrate all styles to Tailwind v4 / SVG presentation attributes | M2 | Survey / R3 |
| 6 | Interactive SVG Playbook Route Diagrammer | Replace placeholder compass in `Playbook.tsx` with dynamic SVG chalkboard diagrammer rendering stems, breaks, cuts, defensive drops, and player tokens | M3 | Survey / R4 |
| 7 | Gridiron Telemetry Loader Upgrade | Transform `LoadingSpinner.tsx` into a digital 25-second play-clock radar sweep with telemetry readouts and zero horizontal overflow | M4 | Survey / R5 |
| 8 | 12-State Interactive Matrix Support | Provide complete 12-state interactive coverage (`idle` through `error`) across tactile interactive components and buttons | M4 | Survey / R5 |
| 9 | Verification & Build Assurance Gate | Full TypeScript compilation (`npm run build`), lint check (`npm run lint`), regression check, and independent forensic integrity audit | M5 | Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Anti-Template Firewall & Vector Symbol Migration | Enforce 0-4px radius ceiling, hard shadows, purge Sparkles from lucide-react across all 17 files | none | PLANNED |
| M2 | Connected SVG Playoff Tournament Bracket | Rebuild PlayoffBracket.tsx with bezier connectors & seeds; retire PlayoffBracket.css | none | PLANNED |
| M3 | Interactive SVG Playbook Route Tree Diagrammer | Implement RouteDiagrammer.tsx and integrate into Playbook.tsx replacing compass | none | PLANNED |
| M4 | Gridiron Telemetry Loader & 12-State Matrix | Modernize LoadingSpinner.tsx into play-clock radar sweep & complete 12-state matrix | none | PLANNED |
| M5 | Full Verification, Build Assurance & Forensic Audit | Run TypeScript build, lint, visual verification, and Forensic Audit veto check | M1, M2, M3, M4 | PLANNED |

## Code Layout
- `frontend/src/index.css`: Tactile token definitions and utilities
- `frontend/src/components/icons/`: Domain-authentic football vector icons
- `frontend/src/components/season/PlayoffBracket.tsx`: Connected SVG playoff tournament bracket
- `frontend/src/components/playbook/RouteDiagrammer.tsx`: Interactive SVG route tree physics diagrammer
- `frontend/src/pages/Playbook.tsx`: Playbook film room and chalkboard host
- `frontend/src/components/ui/LoadingSpinner.tsx`: 25s play-clock radar sweep loader
- `frontend/src/components/tactile/`: 12-state tactile matrix primitives
- `frontend/src/pages/`: Core application viewports
