# Comprehensive Frontend Architecture & Component Survey
## NFL Sim Engine: The Digital Gridiron (THE-NFL-SIM-V2)
**Date:** 2026-08-23 | **Scope:** `frontend/src/` (Components, Pages, Loaders, Routing, Services, Types)

---

## 1. Executive Summary & Inventory Metrics

| Metric | Count | Details |
|---|---|---|
| **Total Frontend TS/TSX Files** | 214 | Analyzed across components, pages, services, types, hooks, stores |
| **Total Page Views** | 18 | 15 actively routed in React Router v7, 3 unmounted legacy pages |
| **Total UI Components** | 129 | Located under `frontend/src/components/` and subdirectories |
| **Mounted Components** | 93 | Actively rendered in the route hierarchy |
| **Unmounted / Orphaned Components** | 36 | Unreachable from `App.tsx` / `router.tsx` route tree |
| **Navigation Links** | 14 | Configured in sidebar `Navigation.tsx` |
| **Core 13 Views Coverage** | 13/13 (100%) | All 13 core views have active routing / page components |
| **Files with Mock / Fallback Data** | 16 | Identified across router loaders, services, and UI components |

---

## 2. The 13 Core Application Views: Mount & Route Matrix
The 13 mandatory application views specified in the architectural blueprint (`ORIGINAL_REQUEST.md`) are mapped below to their respective routes, page components, and mount status:

| # | View Specification | Route Path(s) | Primary Page Component | Mounted Subcomponents | Mock / Placeholder Status |
|---|---|---|---|---|---|
| 1 | **Franchise War Room / Dynasty Hub** | `/`, `/dashboard` | `pages/Dashboard.tsx` | Inline Dashboard Cards, Theme Glow | Hardcoded opponent fallback on week transition |
| 2 | **Tactical Live Sim Chalkboard & Field Radar** | `/live-sim` | `pages/LiveSim.tsx` | `ScoreBoard`, `GameClock`, `FieldCanvas`, `PlayByPlayFeed`, `LiveGameVisualizer`, `GridironVisualizer`, `WeatherWidget`, `CoachingWidget`, `CrowdNoiseMeter` | Mock ball trajectory fallback in page & visualizer |
| 3 | **Offseason Draft Room & Scouting Fog of War** | `/offseason/draft`, `/draft` | `pages/DraftRoom.tsx` | `DraftBoard`, `DraftTicker`, `TradeModal`, `DraftAssistant`, `WarRoomTicker`, `TradePhone`, `ParallaxScene`, `BroadcastPanel` | `router.tsx` loader uses mock teams/picks fallback |
| 4 | **Coaching Dynasty Tree & Staff Matrix** | `/playbook` (Coaching Tree tab) | `pages/Playbook.tsx` | `CoachingTree`, `CoachingDynastyTree`, `GameplanDashboard`, `FamiliarityBar` | Mock familiarity formula for demo in GameplanDashboard |
| 5 | **Medical Trauma Center & Orthopedic Triage** | `/medical-center`, `/medical` | `pages/MedicalCenter.tsx` | `BodyMap`, `GenesisBiometricCard`, `FatigueMonitor`, `OrthopedicTriageModal` | Biometrics fallback defaults when loading |
| 6 | **Depth Chart & Positional Hierarchy** | `/empire/depth-chart`, `/depth-chart` | `pages/DepthChart.tsx` | `ChemistryBadge`, Framer Motion `Reorder` | Live endpoint `api.getTeamChemistry`, `api.updateDepthChart` |
| 7 | **Roster Management & Capology Contracts** | `/empire/front-office`, `/roster` | `pages/FrontOffice.tsx` | `DraggableCard`, `PlayerCard`, `CoachSettings`, `ArchetypeBadge` | Live endpoint `api.getTeamRoster`, `api.getTeam` |
| 8 | **Season Schedule & Week Simulator** | `/season` (Schedule tab), `/season-dashboard` | `pages/SeasonDashboard.tsx` | `ScheduleView`, `SeasonSummaryCard`, `QuickActions`, `NewsFeed` | Live endpoint `seasonApi.getSchedule`, `seasonApi.advanceWeek` |
| 9 | **League Standings & Playoff Bracket** | `/season` (Standings & Playoffs tabs) | `pages/SeasonDashboard.tsx` | `StandingsTable`, `PlayoffBracket`, `LeagueLeaders`, `PlayerModal` | Live endpoint `seasonApi.getStandings`, `seasonApi.getPlayoffBracket` |
| 10 | **Player Profile & Biometric/S2 Cognition Card** | `/players/:playerId/skills`, `/skills` | `pages/SkillsPage.tsx` | `SkillTreeCanvas`, `SkillsOverlay`, `AbilityUnlockTree`, `TraitBadgeGrid`, `ArchetypeBadge` | Unmounted `EnhancedPlayerProfile.tsx`; mock trait data in overlay |
| 11 | **Front Office GM Trades & Valuation Matrix** | `/empire/trade-center`, `/trades` | `pages/TradeCenterPage.tsx` | `TradeNegotiator`, `TradeBlock`, `PendingOffers`, `DroppableZone`, `DraggableAsset`, `TradeAnalyzer` | `tradeApi.ts` has mock fallback generators for offers |
| 12 | **Cryptographic Replay Telemetry** | `/live-sim` (3D/2D Telemetry) | `pages/LiveSim.tsx` | `LiveGameVisualizer`, `FieldCanvas`, `GridironVisualizer` | Replay scrubber and animator exist in codebase but are unmounted |
| 13 | **League Settings & Weather Simulation Config** | `/settings` | `pages/Settings.tsx` | Form controls connected to `useSettingsStore` | Persisted to localStorage / Zustand store |

---

## 3. Application Shell & Route Mount Hierarchy

```text
App.tsx
└── RouterProvider (router.tsx)
    └── MainLayout.tsx
        ├── components/Navigation.tsx (Fixed 14-link Sidebar)
        ├── components/common/FeedbackWidget.tsx
        │   ├── AnnotationPopover.tsx
        │   ├── ElementInspector.tsx
        │   ├── RegionSelector.tsx
        │   ├── ScreenshotEditor.tsx
        │   └── TaskListPanel.tsx
        ├── components/audio/SoundtrackPlayer.tsx
        └── Outlet (Active Route View)
            ├── Route: /                     -> Dashboard.tsx
            ├── Route: /season               -> SeasonDashboard.tsx
            │   ├── ParallaxScene.tsx
            │   ├── RibbonTicker.tsx
            │   ├── BroadcastPanel.tsx
            │   ├── SeasonSummaryCard.tsx -> QuickActions.tsx
            │   ├── StandingsTable.tsx
            │   ├── ScheduleView.tsx
            │   ├── PlayoffBracket.tsx
            │   ├── LeagueLeaders.tsx -> PlayerModal.tsx
            │   └── NewsFeed.tsx
            ├── Route: /offseason            -> OffseasonDashboard.tsx
            │   ├── ParallaxScene.tsx
            │   ├── BroadcastPanel.tsx
            │   ├── OffseasonTimeline.tsx
            │   ├── SalaryCapWidget.tsx
            │   ├── TeamNeeds.tsx
            │   ├── DraftBoard.tsx
            │   │   ├── ScoutIntelligenceLens.tsx
            │   │   ├── GenesisReveal.tsx
            │   │   ├── GpsSpeedViz.tsx
            │   │   └── ScoutingReportModal.tsx
            │   ├── PlayerProgression.tsx
            │   └── NewsFeed.tsx
            ├── Route: /offseason/draft       -> DraftRoom.tsx
            │   ├── ParallaxScene.tsx
            │   ├── RibbonTicker.tsx
            │   ├── BroadcastPanel.tsx
            │   ├── DraftAssistant.tsx -> FeedbackCollector.tsx
            │   ├── WarRoomTicker.tsx
            │   ├── TradePhone.tsx
            │   ├── DraftBoard.tsx (with Scout Lens, Genesis Reveal, GPS Speed Viz)
            │   ├── DraftTicker.tsx
            │   └── TradeModal.tsx -> TradeAnalyzer.tsx
            ├── Route: /empire/front-office  -> FrontOffice.tsx
            │   ├── DraggableCard.tsx -> PlayerCard.tsx -> ArchetypeBadge.tsx, PlayerBackstoryModal.tsx
            │   └── CoachSettings.tsx -> Card.tsx
            ├── Route: /empire/depth-chart   -> DepthChart.tsx
            │   └── ChemistryBadge.tsx
            ├── Route: /empire/trade-center  -> TradeCenterPage.tsx
            │   ├── TradeNegotiator.tsx
            │   │   ├── DroppableZone.tsx -> DraggableAsset.tsx
            │   │   ├── TradeAnalyzer.tsx -> FeedbackCollector.tsx
            │   │   └── DraggableAsset.tsx
            │   ├── TradeBlock.tsx
            │   └── PendingOffers.tsx
            ├── Route: /empire/trophy-room   -> TrophyRoom.tsx
            │   └── TrophyCaseScene.tsx -> TrophyAssets.tsx (Lombardi, MVP, Division trophies)
            ├── Route: /live-sim             -> LiveSim.tsx
            │   ├── ScoreBoard.tsx -> MomentumIndicator.tsx
            │   ├── GameClock.tsx
            │   ├── FieldCanvas.tsx -> GameCanvas.tsx, PlayerSprite.tsx
            │   ├── PlayByPlayFeed.tsx -> InteractionTimeline.tsx -> InteractionBadge.tsx
            │   ├── PhysicsDebugOverlay.tsx -> FieldCanvas.tsx
            │   ├── WeatherWidget.tsx
            │   ├── GameStats.tsx
            │   ├── CoachingWidget.tsx -> Card.tsx
            │   ├── MomentumIndicator.tsx
            │   ├── CrowdNoiseMeter.tsx
            │   ├── GridironVisualizer.tsx
            │   └── LiveGameVisualizer.tsx -> EnhancedFieldVisualizer.tsx, EnhancedPlayerCharacter.tsx
            ├── Route: /medical-center       -> MedicalCenter.tsx
            │   ├── BodyMap.tsx
            │   ├── GenesisBiometricCard.tsx
            │   ├── FatigueMonitor.tsx
            │   └── OrthopedicTriageModal.tsx
            ├── Route: /playbook             -> Playbook.tsx
            │   ├── GameplanDashboard.tsx -> FamiliarityBar.tsx
            │   ├── CoachingTree.tsx -> CoachingDynastyTree.tsx
            │   └── Telestrator.tsx
            ├── Route: /training             -> TrainingCenter.tsx
            │   ├── StarfieldBackground.tsx
            │   ├── DrillSelector.tsx -> DrillCard3D.tsx
            │   ├── CoachingStyleDial.tsx
            │   ├── WeeklyScheduleTimeline.tsx
            │   └── TrainingSessionResult.tsx
            ├── Route: /skills               -> SkillsPage.tsx
            │   ├── SkillTreeCanvas.tsx -> SkillNode3D.tsx, ConnectionLine.tsx, StarfieldBackground.tsx
            │   ├── SkillsOverlay.tsx
            │   ├── AbilityUnlockTree.tsx
            │   ├── TraitBadgeGrid.tsx
            │   └── ArchetypeBadge.tsx
            ├── Route: /team-selection       -> TeamSelection.tsx
            │   ├── ParallaxScene.tsx
            │   ├── TiltCard.tsx
            │   └── RibbonTicker.tsx
            ├── Route: /settings             -> Settings.tsx
            └── Catch-all: *                 -> NotFound.tsx
```

---

## 4. Deep Catalog of All 129 Components

### 4.1 Folder: `components/components/` (129 Components)

#### `AbilityUnlockTree` (frontend/src/components/skills/AbilityUnlockTree.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SkillsPage.tsx`
- **JSX Rendered By:** `pages/SkillsPage.tsx`
- **Expected Props Interface:**
  ```typescript
  playerId: number;
  playerLevel: number;
  playerXp: number;
  playerPosition: string;
  abilityStatuses: Record<string, PlayerAbilityStatus>;
  onUnlockSuccess: (abilityKey: string, remainingXp?: number) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SkillsPage.tsx`: passed attributes `[playerId, playerLevel, playerXp, playerPosition, abilityStatuses, onUnlockSuccess]`

#### `AnnotationPopover` (frontend/src/components/common/AnnotationPopover.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/common/FeedbackWidget.tsx`
- **JSX Rendered By:** `components/common/FeedbackWidget.tsx`
- **Expected Props Interface:**
  ```typescript
  element: ElementMetadata | null;
  screenshot?: string | null;
  onSave: (note: string, researchRequested: boolean) => void;
  onCancel: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/common/FeedbackWidget.tsx`: passed attributes `[element, screenshot, onSave, onCancel]`

#### `ArchetypeBadge` (frontend/src/components/player/ArchetypeBadge.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/ui/PlayerCard.tsx`, `pages/SkillsPage.tsx`
- **JSX Rendered By:** `components/ui/PlayerCard.tsx`, `pages/SkillsPage.tsx`
- **Expected Props Interface:**
  ```typescript
  archetype: PlayerArchetype | string;
  size?: "sm" | "md" | "lg";
  showTooltip?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SkillsPage.tsx`: passed attributes `[archetype, size, showTooltip]`
  - In `components/ui/PlayerCard.tsx`: passed attributes `[archetype, size, showTooltip]`

#### `Badge` (frontend/src/components/ui/Badge.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

#### `BodyMap` (frontend/src/components/medical/BodyMap.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/MedicalCenter.tsx`
- **JSX Rendered By:** `pages/MedicalCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  id: BodyZoneKey;
  name: string;
  health: number;
  isSelected: boolean;
  onClick: (id: BodyZoneKey) => void;
  d: string;
  healthData: BodyMapHealthData;
  selectedZone?: BodyZoneKey | null;
  onZoneSelect: (zone: BodyZoneKey) => void;
  playerName?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/MedicalCenter.tsx`: passed attributes `[healthData, selectedZone, onZoneSelect, playerName]`

#### `BroadcastPanel` (frontend/src/components/immersive/BroadcastPanel.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`, `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`, `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  ```typescript
  title: string;
  isLive?: boolean;
  className?: string;
  children: React.ReactNode;
  "data-testid"?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/DraftRoom.tsx`: passed attributes `[title, Big, Board, Live, isLive]`
  - In `pages/DraftRoom.tsx`: passed attributes `[title, AI]`
  - In `pages/DraftRoom.tsx`: passed attributes `[title, Team]`

#### `CampSchedulePlanner` (frontend/src/components/training/CampSchedulePlanner.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  onScheduleChange?: (schedule: DaySchedule[]) => void;
  onSimulateCampWeek?: () => void;
  ```

#### `Card` (frontend/src/components/ui/Card.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/coaching/CoachSettings.tsx`, `components/game/CoachingWidget.tsx`
- **JSX Rendered By:** `components/game/CoachingWidget.tsx`, `components/coaching/CoachSettings.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `components/coaching/CoachSettings.tsx`: passed attributes `[variant]`
  - In `components/game/CoachingWidget.tsx`: passed attributes `[w-64, 60, backdrop-blur-md, variant]`

#### `ChemistryBadge` (frontend/src/components/ui/ChemistryBadge.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DepthChart.tsx`
- **JSX Rendered By:** `pages/DepthChart.tsx`
- **Expected Props Interface:**
  ```typescript
  level: number; // 0.0 to 1.0
  consecutiveGames: number;
  status: string; // "NONE", "DEVELOPING", "STRONG", "ELITE", "MAXIMUM"
  bonuses?: {
  pass_block: number;
  run_block: number;
  awareness: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/DepthChart.tsx`: passed attributes `[level, consecutiveGames, status, bonuses]`

#### `CoachCard` (frontend/src/components/coaching/CoachCard.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  name: string;
  role: string;
  tier: CoachTier | string;
  archetype: CoachArchetype | string;
  playbookOffense?: string;
  playbookDefense?: string;
  experience: number;
  ```

#### `CoachSettings` (frontend/src/components/coaching/CoachSettings.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/FrontOffice.tsx`
- **JSX Rendered By:** `pages/FrontOffice.tsx`
- **Expected Props Interface:**
  ```typescript
  teamId: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/FrontOffice.tsx`: passed attributes `[teamId]`

#### `CoachingDynastyTree` (frontend/src/components/coaching/CoachingDynastyTree.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/coaching/CoachingTree.tsx`
- **JSX Rendered By:** `components/coaching/CoachingTree.tsx`
- **Expected Props Interface:**
  ```typescript
  initialProfile?: CoachDynastyProfile;
  initialSynergy?: StaffSynergyBreakdown;
  onSkillUnlock?: (nodeId: string) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/coaching/CoachingTree.tsx`: passed attributes `[]`

#### `CoachingStyleDial` (frontend/src/components/training/CoachingStyleDial.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/TrainingCenter.tsx`
- **JSX Rendered By:** `pages/TrainingCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  styles: CoachingStyle[];
  selectedStyle?: string;
  onSelect: (styleName: string) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TrainingCenter.tsx`: passed attributes `[styles, selectedStyle, onSelect]`

#### `CoachingStylePicker` (frontend/src/components/training/CoachingStylePicker.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  currentStyle: CoachingStyleType;
  onStyleSelect: (style: CoachingStyleType) => void;
  ```

#### `CoachingTree` (frontend/src/components/coaching/CoachingTree.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/Playbook.tsx`
- **JSX Rendered By:** `pages/Playbook.tsx`
- **Expected Props Interface:**
  ```typescript
  name: string;
  role: string;
  specialty: string;
  color: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/Playbook.tsx`: passed attributes `[]`

#### `CoachingUnlockPanel` (frontend/src/components/coaching/CoachingUnlockPanel.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  playerId: number;
  availableTraits: Trait[];
  onUnlockComplete: () => void;
  ```

#### `CoachingWidget` (frontend/src/components/game/CoachingWidget.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[teamId]`

#### `ConnectionLine` (frontend/src/components/skills/ConnectionLine.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/skills/SkillTreeCanvas.tsx`
- **JSX Rendered By:** `components/skills/SkillTreeCanvas.tsx`
- **Expected Props Interface:**
  ```typescript
  start: [number, number, number];
  end: [number, number, number];
  isUnlocked: boolean;
  color?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/skills/SkillTreeCanvas.tsx`: passed attributes `[start, end, isUnlocked]`

#### `CrowdNoiseMeter` (frontend/src/components/game/CrowdNoiseMeter.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  ```typescript
  decibels: number; // 50 to 120
  stadiumName?: string;
  isAwayTeamOnOffense: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[decibels, 96, stadiumName, Lambeau, isAwayTeamOnOffense]`

#### `DraftAssistant` (frontend/src/components/draft/DraftAssistant.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`
- **JSX Rendered By:** `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  teamId: number;
  pickNumber: number;
  availablePlayers: number[];
  onPlayerSelect?: (prospect: Prospect) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/DraftRoom.tsx`: passed attributes `[seasonId, teamId, pickNumber, availablePlayers]`

#### `DraftBoard` (frontend/src/components/offseason/DraftBoard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`, `pages/OffseasonDashboard.tsx`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`, `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  ```typescript
  prospects: Prospect[];
  teamNeeds?: TeamNeed[];
  onProspectSelect?: (prospect: Prospect) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/DraftRoom.tsx`: passed attributes `[prospects, teamNeeds, onProspectSelect]`
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[prospects, teamNeeds]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 300: `playerId={String(scoutingReportProspect.id)} // Assuming prospect.id is number, mock service expects string`

#### `DraftTicker` (frontend/src/components/offseason/DraftTicker.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  ```typescript
  recentPicks: DraftPickSummary[];
  ```

#### `DraggableAsset` (frontend/src/components/trades/DraggableAsset.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/trades/DroppableZone.tsx`, `components/trades/TradeNegotiator.tsx`
- **JSX Rendered By:** `components/trades/DroppableZone.tsx`, `components/trades/TradeNegotiator.tsx`
- **Expected Props Interface:**
  ```typescript
  id: string;
  player: TradePlayer;
  disabled?: boolean;
  onClick?: () => void;
  showRemoveButton?: boolean;
  onRemove?: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/trades/DroppableZone.tsx`: passed attributes `[player, showRemoveButton, onRemove]`
  - In `components/trades/TradeNegotiator.tsx`: passed attributes `[player, onClick]`
  - In `components/trades/TradeNegotiator.tsx`: passed attributes `[player, onClick]`

#### `DraggableCard` (frontend/src/components/ui/DraggableCard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/FrontOffice.tsx`, `pages/FrontOffice_Baseline.tsx`
- **JSX Rendered By:** `pages/FrontOffice.tsx`, `pages/FrontOffice_Baseline.tsx`
- **Expected Props Interface:**
  ```typescript
  name: string;
  position: string;
  rating: number;
  team: string;
  jerseyNumber?: number;
  speed?: number;
  strength?: number;
  agility?: number;
  acceleration?: number;
  awareness?: number;
  devTrait?: "NORMAL" | "STAR" | "SUPERSTAR" | "XFACTOR";
  morale?: string;
  className?: string;
  traits?: string[];
  archetype?: PlayerArchetype | string;
  onClick?: () => void;
  testId?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/FrontOffice.tsx`: passed attributes `[name, position, rating, team, abbreviation, jerseyNumber, speed, speed, strength, strength, agility, agility, onClick]`
  - In `pages/FrontOffice_Baseline.tsx`: passed attributes `[name, position, rating, team]`
  - In `pages/FrontOffice_Baseline.tsx`: passed attributes `[name, position, rating, team]`

#### `DrillCard` (frontend/src/components/training/DrillCard.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  drill: Drill;
  isSelected?: boolean;
  onSelect?: (drill: Drill) => void;
  ```

#### `DrillCard3D` (frontend/src/components/training/DrillCard3D.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/training/DrillSelector.tsx`
- **JSX Rendered By:** `components/training/DrillSelector.tsx`
- **Expected Props Interface:**
  ```typescript
  drill: Drill;
  isSelected: boolean;
  isRecommended?: boolean;
  onSelect: (drill: Drill) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/training/DrillSelector.tsx`: passed attributes `[drill, isSelected, name, isRecommended, onSelect]`

#### `DrillSelector` (frontend/src/components/training/DrillSelector.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/TrainingCenter.tsx`
- **JSX Rendered By:** `pages/TrainingCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  position?: string;
  seasonPhase?: string;
  onDrillSelect: (drill: Drill) => void;
  selectedDrill?: Drill | null;
  playerWeaknesses?: string[]; // New prop for recommendations
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TrainingCenter.tsx`: passed attributes `[position, onDrillSelect, selectedDrill, playerWeaknesses]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 215: `className="w-full pl-10 pr-4 py-3 bg-gray-800/60 border border-gray-700/50 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"`

#### `DroppableZone` (frontend/src/components/trades/DroppableZone.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/trades/TradeNegotiator.tsx`
- **JSX Rendered By:** `components/trades/TradeNegotiator.tsx`
- **Expected Props Interface:**
  ```typescript
  id: string;
  title: string;
  players: TradePlayer[];
  onRemove: (playerId: number) => void;
  emptyMessage?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/trades/TradeNegotiator.tsx`: passed attributes `[title, You, players, onRemove, emptyMessage, Drag, your, players]`
  - In `components/trades/TradeNegotiator.tsx`: passed attributes `[title, You, players, onRemove, emptyMessage, Drag, their, players]`

#### `ElementInspector` (frontend/src/components/common/ElementInspector.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/common/FeedbackWidget.tsx`
- **JSX Rendered By:** `components/common/FeedbackWidget.tsx`
- **Expected Props Interface:**
  ```typescript
  isActive: boolean;
  onElementSelect: (metadata: ElementMetadata) => void;
  onDeactivate: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/common/FeedbackWidget.tsx`: passed attributes `[isActive, onElementSelect, onDeactivate]`

#### `EnhancedFieldVisualizer` (frontend/src/components/3d/EnhancedFieldVisualizer.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/3d/LiveGameVisualizer.tsx`
- **JSX Rendered By:** `components/3d/LiveGameVisualizer.tsx`
- **Expected Props Interface:**
  ```typescript
  gameId?: number;
  showPlayers?: boolean;
  detailLevel?: "low" | "medium" | "high";
  homeColor?: string;
  awayColor?: string;
  showYardLines?: boolean;
  showNumbers?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/3d/LiveGameVisualizer.tsx`: passed attributes `[homeColor, primary_color, awayColor, primary_color, showYardLines, showNumbers]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 170: `{/* Ball marker placeholder */}`

#### `EnhancedPlayerCharacter` (frontend/src/components/3d/EnhancedPlayerCharacter.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/3d/LiveGameVisualizer.tsx`
- **JSX Rendered By:** `components/3d/LiveGameVisualizer.tsx`
- **Expected Props Interface:**
  ```typescript
  playerData: PlayerVisualData;
  position: [number, number, number];
  isAnimating?: boolean;
  targetPosition?: [number, number, number];
  showNumber?: boolean;
  detailLevel?: "low" | "medium" | "high";
  ```
- **Sample Props Passed at Call Site:**
  - In `components/3d/LiveGameVisualizer.tsx`: passed attributes `[playerData, position, isAnimating, detailLevel, showNumber]`

#### `EnhancedPlayerProfile` (frontend/src/components/ui/EnhancedPlayerProfile.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  playerId: number;
  onClose: () => void;
  ```

#### `ErrorBoundary` (frontend/src/components/ErrorBoundary.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  /** Child components to wrap */
  children: ReactNode;
  /** Custom fallback UI to render on error */
  fallback?: ReactNode | ((props: FallbackProps) => ReactNode);
  /** Callback when an error is caught */
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  /** Callback when user clicks retry */
  onRetry?: () => void;
  /** Maximum number of retry attempts before giving up */
  maxRetries?: number;
  /** Whether to show error details in non-production */
  showDetails?: boolean;
  /** Custom error boundary name for logging context */
  name?: string;
  error: Error | null;
  errorInfo: ErrorInfo | null;
  resetError: () => void;
  retryCount: number;
  isRetrying: boolean;
  ```

#### `FamiliarityBar` (frontend/src/components/playbook/FamiliarityBar.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/coaching/GameplanDashboard.tsx`
- **JSX Rendered By:** `components/coaching/GameplanDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  score: number; // 0.0 to 1.0
  showLabel?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/coaching/GameplanDashboard.tsx`: passed attributes `[score, showLabel]`
  - In `components/coaching/GameplanDashboard.tsx`: passed attributes `[score, showLabel]`

#### `FatigueIndicator` (frontend/src/components/game/FatigueIndicator.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  fatigue: number; // 0.0 to 1.0 (0% to 100%)
  showLabel?: boolean;
  ```

#### `FatigueMonitor` (frontend/src/components/medical/FatigueMonitor.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/MedicalCenter.tsx`
- **JSX Rendered By:** `pages/MedicalCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  fatigue?: FatigueState | null;
  currentWearLevel?: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/MedicalCenter.tsx`: passed attributes `[fatigue, currentWearLevel]`

#### `FeedbackCollector` (frontend/src/components/draft/FeedbackCollector.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/draft/DraftAssistant.tsx`, `components/trades/TradeAnalyzer.tsx`, `components/trades/TradeCenter.tsx`, `components/trades/TradeNegotiator.tsx`
- **JSX Rendered By:** `components/trades/TradeAnalyzer.tsx`, `components/trades/TradeCenter.tsx`, `components/draft/DraftAssistant.tsx`, `components/trades/TradeNegotiator.tsx`
- **Expected Props Interface:**
  ```typescript
  contextId: string; // ID of the recommendation (e.g., draft pick ID or trade ID)
  contextType: "draft" | "trade";
  onFeedbackSubmit?: (feedback: FeedbackData) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/draft/DraftAssistant.tsx`: passed attributes `[contextId, contextType]`
  - In `components/trades/TradeAnalyzer.tsx`: passed attributes `[contextId, targetTeamId, contextType]`
  - In `components/trades/TradeCenter.tsx`: passed attributes `[contextId, contextType]`

#### `FeedbackWidget` (frontend/src/components/common/FeedbackWidget.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `layouts/MainLayout.tsx`
- **JSX Rendered By:** `layouts/MainLayout.tsx`
- **Expected Props Interface:**
  ```typescript
  currentPage?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `layouts/MainLayout.tsx`: passed attributes `[currentPage]`

#### `FieldCanvas` (frontend/src/components/game/FieldCanvas.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/debug/PhysicsDebugOverlay.tsx`, `components/game/ReplayScrubber.tsx`, `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  ```typescript
  currentPlay?: PlayTrajectory;
  isPlaying: boolean;
  onPlayComplete?: () => void;
  playbackSpeed?: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[isPlaying, currentPlay, playbackSpeed, onPlayComplete]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 205: `color={p.player_id < 11 ? 0xff0000 : 0x0000ff} // Mock Offense/Defense based on ID`

#### `FieldView` (frontend/src/components/FieldView.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 7: `// For Phase 1, we just render static placeholders.`

#### `FieldVisualizer` (frontend/src/components/3d/FieldVisualizer.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **JSX Rendered By:** `components/3d/SceneContainer.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

#### `GameCanvas` (frontend/src/components/game/GameCanvas.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/FieldView.tsx`, `components/game/FieldCanvas.tsx`
- **JSX Rendered By:** `components/FieldView.tsx`, `components/game/FieldCanvas.tsx`
- **Expected Props Interface:**
  ```typescript
  width?: number;
  height?: number;
  children?: React.ReactNode;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/FieldView.tsx`: passed attributes `[width, height]`
  - In `components/game/FieldCanvas.tsx`: passed attributes `[width, height]`

#### `GameClock` (frontend/src/components/GameClock.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[]`

#### `GameStats` (frontend/src/components/game/GameStats.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 141: `<StatRow label="First Downs" value="--" /> {/* Placeholder */}`

#### `GameplanDashboard` (frontend/src/components/coaching/GameplanDashboard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/Playbook.tsx`
- **JSX Rendered By:** `pages/Playbook.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/Playbook.tsx`: passed attributes `[]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 47: `// Mock familiarity depending on strategy for demo`
  - Line 87: `// Mock familiarity depending on strategy for demo`

#### `GenesisBiometricCard` (frontend/src/components/medical/GenesisBiometricCard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/MedicalCenter.tsx`
- **JSX Rendered By:** `pages/MedicalCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  biometrics?: BioMetrics | null;
  playerName?: string;
  position?: string;
  isScoutedInitially?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/MedicalCenter.tsx`: passed attributes `[biometrics, playerName, position]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 23: `// Defaults derived or mocked if backend biometrics are loading`

#### `GenesisReveal` (frontend/src/components/draft/GenesisReveal.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/offseason/DraftBoard.tsx`
- **JSX Rendered By:** `components/offseason/DraftBoard.tsx`
- **Expected Props Interface:**
  ```typescript
  prospectName: string;
  data: CombineResult;
  onClose: () => void;
  onReveal: () => void;
  isRevealed: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/offseason/DraftBoard.tsx`: passed attributes `[prospectName, data, isRevealed, onClose]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 140: `for now we render placeholders if missing or just what we have)`

#### `GpsSpeedViz` (frontend/src/components/draft/GpsSpeedViz.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/offseason/DraftBoard.tsx`
- **JSX Rendered By:** `components/offseason/DraftBoard.tsx`
- **Expected Props Interface:**
  ```typescript
  speedMph: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/offseason/DraftBoard.tsx`: passed attributes `[speedMph]`
  - In `components/offseason/DraftBoard.tsx`: passed attributes `[speedMph]`

#### `GridironVisualizer` (frontend/src/components/GridironVisualizer.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  ```typescript
  turfData?: TurfGridData;
  players?: PlayerCognitiveTelemetry[];
  ballPosition?: { x: number; y: number
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[]`

#### `InteractionBadge` (frontend/src/components/game/InteractionBadge.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/game/InteractionTimeline.tsx`
- **JSX Rendered By:** `components/game/InteractionTimeline.tsx`
- **Expected Props Interface:**
  ```typescript
  outcome: InteractionOutcome;
  showLabel?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/game/InteractionTimeline.tsx`: passed attributes `[outcome]`

#### `InteractionTimeline` (frontend/src/components/game/InteractionTimeline.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/PlayByPlayFeed.tsx`
- **JSX Rendered By:** `components/PlayByPlayFeed.tsx`
- **Expected Props Interface:**
  ```typescript
  interactions: InteractionResult[];
  ```
- **Sample Props Passed at Call Site:**
  - In `components/PlayByPlayFeed.tsx`: passed attributes `[interactions]`

#### `LeagueLeaders` (frontend/src/components/season/LeagueLeaders.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SeasonDashboard.tsx`
- **JSX Rendered By:** `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  leaders: LeagueLeadersType | null;
  loading: boolean;
  teams: Team[];
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SeasonDashboard.tsx`: passed attributes `[leaders, loading, teams]`

#### `LiveGameVisualizer` (frontend/src/components/3d/LiveGameVisualizer.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  ```typescript
  gameId: number;
  apiUrl?: string;
  autoConnect?: boolean;
  enableBroadcast?: boolean;
  showControls?: boolean;
  detailLevel?: "low" | "medium" | "high";
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[gameId, enableBroadcast]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 105: `const mockPlayResult: BroadcastPlayResult = {`
  - Line 118: `dispatchBroadcast({ type: "PLAY_CALLED", playResult: mockPlayResult });`
  - Line 120: `const clips = director.generateClipSequence(mockPlayResult, BroadcastPhase.PRE_PLAY);`
  - Line 129: `dispatchBroadcast({ type: "WHISTLE", playResult: mockPlayResult });`
  - Line 131: `const nextPhase = director.determineNextPhase(BroadcastPhase.POST_PLAY, mockPlayResult);`

#### `LoadingSpinner` (frontend/src/components/ui/LoadingSpinner.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/season/LeagueLeaders.tsx`, `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`, `pages/TradeCenterPage.tsx`
- **JSX Rendered By:** `pages/TradeCenterPage.tsx`, `pages/OffseasonDashboard.tsx`, `components/season/LeagueLeaders.tsx`, `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  size?: "small" | "medium" | "large";
  color?: string;
  text?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[text, Loading, offseason, size]`
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[text, size, color]`
  - In `pages/SeasonDashboard.tsx`: passed attributes `[text, Loading, season, size]`

#### `LogoTimeline` (frontend/src/components/history/LogoTimeline.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 5: `const MOCK_HISTORY = [`
  - Line 28: `{MOCK_HISTORY.map((era, i) => (`
  - Line 38: `<div className="logo-timeline__logo-placeholder" />`

#### `LombardiTrophy` (frontend/src/components/trophy/TrophyAssets.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/trophy/TrophyCaseScene.tsx`
- **JSX Rendered By:** `components/trophy/TrophyCaseScene.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `components/trophy/TrophyCaseScene.tsx`: passed attributes `[position]`

#### `MomentumIndicator` (frontend/src/components/game/MomentumIndicator.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/ScoreBoard.tsx`, `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`, `components/ScoreBoard.tsx`
- **Expected Props Interface:**
  ```typescript
  label?: string;
  state: MomentumState;
  align?: "left" | "right";
  size?: "sm" | "md";
  ```
- **Sample Props Passed at Call Site:**
  - In `components/ScoreBoard.tsx`: passed attributes `[state, size]`
  - In `components/ScoreBoard.tsx`: passed attributes `[state, size, align]`
  - In `pages/LiveSim.tsx`: passed attributes `[label, Home, state, align]`

#### `Navigation` (frontend/src/components/Navigation.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `layouts/MainLayout.tsx`
- **JSX Rendered By:** `layouts/MainLayout.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `layouts/MainLayout.tsx`: passed attributes `[]`

#### `NewsFeed` (frontend/src/components/season/NewsFeed.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  /** Filter news by team name */
  teamFilter?: string;
  /** Maximum items to display */
  maxItems?: number;
  /** Enable compact mode for sidebar */
  compact?: boolean;
  /** Auto-refresh interval in seconds (0 to disable) */
  refreshInterval?: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[maxItems, compact, refreshInterval]`
  - In `pages/SeasonDashboard.tsx`: passed attributes `[maxItems, compact, refreshInterval]`

#### `NewsFeed` (frontend/src/components/common/NewsFeed.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  limit?: number;
  showRefresh?: boolean;
  compact?: boolean;
  ```

#### `NewsFeedWidget` (frontend/src/components/news/NewsFeedWidget.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  week?: number;
  maxItems?: number;
  ```

#### `NotFound` (frontend/src/components/NotFound.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `router.tsx`
- **JSX Rendered By:** `router.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `router.tsx`: passed attributes `[]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 6: `<div className="page-placeholder">`

#### `OffseasonTimeline` (frontend/src/components/offseason/OffseasonTimeline.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/OffseasonDashboard.tsx`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  currentPhase: string;
  phaseStats?: {
  [key: string]: PhaseStat;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[currentPhase, phaseStats]`

#### `OrthopedicTriageModal` (frontend/src/components/medical/OrthopedicTriageModal.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/MedicalCenter.tsx`
- **JSX Rendered By:** `pages/MedicalCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  isOpen: boolean;
  playerId?: number;
  playerName?: string;
  zoneKey: string;
  zoneName: string;
  currentIntegrity: number;
  baselineWeeks?: number;
  onClose: () => void;
  onConfirmProtocol: (protocol: MedicalProtocolType) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/MedicalCenter.tsx`: passed attributes `[isOpen, playerId, playerName, zoneKey, selectedPart, zoneName, selectedPart, ANATOMICAL, currentIntegrity, selectedPart, baselineWeeks, onClose]`

#### `PageTransition` (frontend/src/components/transitions/PageTransition.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  children: React.ReactNode;
  ```

#### `ParallaxScene` (frontend/src/components/immersive/ParallaxScene.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`, `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`, `pages/TeamSelection.tsx`
- **JSX Rendered By:** `pages/TeamSelection.tsx`, `pages/OffseasonDashboard.tsx`, `pages/SeasonDashboard.tsx`, `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  ```typescript
  className?: string;
  children: React.ReactNode;
  rain?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/DraftRoom.tsx`: passed attributes `[]`
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[]`
  - In `pages/SeasonDashboard.tsx`: passed attributes `[]`

#### `PendingOffers` (frontend/src/components/trades/PendingOffers.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/trades/TradeCenter.tsx`, `pages/TradeCenterPage.tsx`
- **JSX Rendered By:** `pages/TradeCenterPage.tsx`, `components/trades/TradeCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  teamId: number;
  onCounter?: (offer: TradeOffer) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TradeCenterPage.tsx`: passed attributes `[teamId, onCounter]`
  - In `components/trades/TradeCenter.tsx`: passed attributes `[teamId]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 25: `// Silent error for now, mock data fallback handles it`

#### `PhysicsDebugOverlay` (frontend/src/components/debug/PhysicsDebugOverlay.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  ```typescript
  play: PlayTrajectory;
  canvasRef: React.RefObject<FieldCanvasRef | null>;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[play, canvasRef]`

#### `PlayAnimator` (frontend/src/components/3d/PlayAnimator.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  onAnimationComplete?: () => void;
  ```

#### `PlayByPlayFeed` (frontend/src/components/PlayByPlayFeed.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[]`

#### `PlayerBackstoryModal` (frontend/src/components/player/PlayerBackstoryModal.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/ui/PlayerCard.tsx`
- **JSX Rendered By:** `components/ui/PlayerCard.tsx`
- **Expected Props Interface:**
  ```typescript
  playerId: string;
  playerName: string;
  isOpen: boolean;
  onClose: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/ui/PlayerCard.tsx`: passed attributes `[playerId, playerName, isOpen, onClose]`

#### `PlayerCard` (frontend/src/components/ui/PlayerCard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/ui/DraggableCard.tsx`
- **JSX Rendered By:** `components/ui/DraggableCard.tsx`
- **Expected Props Interface:**
  ```typescript
  name: string;
  position: string;
  rating: number;
  team: string;
  jerseyNumber?: number;
  speed?: number;
  strength?: number;
  agility?: number;
  acceleration?: number;
  awareness?: number;
  devTrait?: "NORMAL" | "STAR" | "SUPERSTAR" | "XFACTOR";
  morale?: string;
  className?: string;
  traits?: string[];
  archetype?: PlayerArchetype | string;
  onClick?: () => void;
  testId?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/ui/DraggableCard.tsx`: passed attributes `[testId]`

#### `PlayerCharacter` (frontend/src/components/3d/PlayerCharacter.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **JSX Rendered By:** `components/3d/FieldVisualizer.tsx`
- **Expected Props Interface:**
  ```typescript
  position: [number, number, number];
  team: "offense" | "defense";
  playerNumber?: number;
  isAnimating?: boolean;
  targetPosition?: [number, number, number];
  ```

#### `PlayerModal` (frontend/src/components/ui/PlayerModal.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/season/LeagueLeaders.tsx`
- **JSX Rendered By:** `components/season/LeagueLeaders.tsx`
- **Expected Props Interface:**
  ```typescript
  playerId: number;
  onClose: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/season/LeagueLeaders.tsx`: passed attributes `[playerId, onClose]`

#### `PlayerProgressChart` (frontend/src/components/training/PlayerProgressChart.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  playerId: number;
  playerName: string;
  position: string;
  stats: StatProgress[];
  weeklyXP?: number[];
  ```

#### `PlayerProgression` (frontend/src/components/offseason/PlayerProgression.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/OffseasonDashboard.tsx`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  progressionData: ProgressionData[];
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[progressionData]`

#### `PlayerSprite` (frontend/src/components/game/PlayerSprite.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/FieldView.tsx`, `components/game/FieldCanvas.tsx`
- **JSX Rendered By:** `components/FieldView.tsx`, `components/game/FieldCanvas.tsx`
- **Expected Props Interface:**
  ```typescript
  /** Player ID - required for dynamic position updates via dataSource */
  id?: number;
  /** Static X position (used when dataSource not provided) */
  x: number;
  /** Static Y position (used when dataSource not provided) */
  y: number;
  /** Fill color for the player sprite */
  color: number;
  /** Whether player is on offense (affects direction indicator) */
  isOffense?: boolean;
  /** Dynamic position source - when provided with id, sprite updates position from this ref */
  dataSource?: React.MutableRefObject<Map<number, { x: number; y: number
  ```
- **Sample Props Passed at Call Site:**
  - In `components/FieldView.tsx`: passed attributes `[x, y, color, isOffense]`
  - In `components/FieldView.tsx`: passed attributes `[x, losX, y, color, isOffense]`
  - In `components/FieldView.tsx`: passed attributes `[x, losX, y, color, isOffense]`

#### `PlayoffBracket` (frontend/src/components/season/PlayoffBracket.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SeasonDashboard.tsx`
- **JSX Rendered By:** `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  /** List of all playoff matchups to display in the bracket. */
  matchups: PlayoffMatchup[];
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SeasonDashboard.tsx`: passed attributes `[matchups]`

#### `PrimeCard` (frontend/src/components/ui/PrimeCard.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  children: ReactNode;
  className?: string;
  title?: string;
  icon?: ReactNode;
  variant?: "default" | "danger" | "glass";
  delay?: number;
  ```

#### `QuickActions` (frontend/src/components/season/QuickActions.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/season/SeasonSummaryCard.tsx`
- **JSX Rendered By:** `components/season/SeasonSummaryCard.tsx`
- **Expected Props Interface:**
  ```typescript
  actions: Action[];
  ```
- **Sample Props Passed at Call Site:**
  - In `components/season/SeasonSummaryCard.tsx`: passed attributes `[actions]`

#### `RegionSelector` (frontend/src/components/common/RegionSelector.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/common/FeedbackWidget.tsx`
- **JSX Rendered By:** `components/common/FeedbackWidget.tsx`
- **Expected Props Interface:**
  ```typescript
  isActive: boolean;
  onCapture: (imageData: string, rect: DOMRect) => void;
  onCancel: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/common/FeedbackWidget.tsx`: passed attributes `[isActive, onCapture, onCancel]`

#### `ReplayScrubber` (frontend/src/components/game/ReplayScrubber.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  canvasRef: React.RefObject<FieldCanvasRef>;
  duration: number;
  ```

#### `RibbonTicker` (frontend/src/components/immersive/RibbonTicker.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`, `pages/SeasonDashboard.tsx`, `pages/TeamSelection.tsx`
- **JSX Rendered By:** `pages/TeamSelection.tsx`, `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  items: Array<string>;
  speedSec?: number;
  "data-testid"?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SeasonDashboard.tsx`: passed attributes `[items, Season, Broadcast, League, speedSec]`
  - In `pages/TeamSelection.tsx`: passed attributes `[items, Tunnel, Choose, Your, 32, NFL, Dynasty, Mode, speedSec]`

#### `RootErrorBoundary` (frontend/src/components/RootErrorBoundary.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `router.tsx`
- **JSX Rendered By:** `router.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `router.tsx`: passed attributes `[]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 6: `<div className="page-placeholder">`

#### `RouteErrorBoundary` (frontend/src/components/RouteErrorBoundary.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `router.tsx`
- **JSX Rendered By:** `router.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `router.tsx`: passed attributes `[]`
  - In `router.tsx`: passed attributes `[]`
  - In `router.tsx`: passed attributes `[]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 15: `<div className="page-placeholder">`
  - Line 26: `<div className="page-placeholder">`
  - Line 39: `<div className="page-placeholder">`

#### `SalaryCapWidget` (frontend/src/components/offseason/SalaryCapWidget.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/OffseasonDashboard.tsx`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  data: SalaryCapData;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[data]`

#### `SceneContainer` (frontend/src/components/3d/SceneContainer.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 36: `/* Placeholder Content (The "Hive" Core) - Only show on Dashboard/others */`

#### `ScheduleView` (frontend/src/components/season/ScheduleView.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SeasonDashboard.tsx`
- **JSX Rendered By:** `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  /** List of games to display for the selected week. */
  games: Game[];
  /** List of all teams, used for looking up names and logos. */
  teams: Team[];
  /** The currently active week in the season. */
  currentWeek: number;
  /** Total number of weeks in the season. */
  totalWeeks: number;
  /** Callback triggered when the user selects a different week. */
  onWeekChange: (week: number) => void;
  /** Callback triggered when the user wants to simulate a specific game. */
  onSimulateGame?: (gameId: number) => void;
  /** Whether the schedule data is loading. */
  loading?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SeasonDashboard.tsx`: passed attributes `[games, teams, currentWeek, totalWeeks, total_weeks, Approx, playoff, weeks, onWeekChange, onSimulateGame]`

#### `ScoreBoard` (frontend/src/components/ScoreBoard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[]`

#### `ScoutIntelligenceLens` (frontend/src/components/offseason/ScoutIntelligenceLens.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/offseason/DraftBoard.tsx`
- **JSX Rendered By:** `components/offseason/DraftBoard.tsx`
- **Expected Props Interface:**
  ```typescript
  currentLens: ScoutBiasLens;
  onLensChange: (lens: ScoutBiasLens) => void;
  selectedProspect?: ProspectIntelligence | null;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/offseason/DraftBoard.tsx`: passed attributes `[currentLens, onLensChange]`

#### `ScoutingReportModal` (frontend/src/components/scouting/ScoutingReportModal.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/offseason/DraftBoard.tsx`
- **JSX Rendered By:** `components/offseason/DraftBoard.tsx`
- **Expected Props Interface:**
  ```typescript
  playerId: string;
  playerName: string;
  position: string;
  isOpen: boolean;
  onClose: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/offseason/DraftBoard.tsx`: passed attributes `[playerId, Assuming, is, mock, service, expects, string, playerName, position, isOpen, onClose]`

#### `ScreenshotEditor` (frontend/src/components/common/ScreenshotEditor.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/common/FeedbackWidget.tsx`
- **JSX Rendered By:** `components/common/FeedbackWidget.tsx`
- **Expected Props Interface:**
  ```typescript
  annotation: Annotation;
  onSave: (updatedAnnotation: Annotation) => void;
  onClose: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/common/FeedbackWidget.tsx`: passed attributes `[annotation, onSave, onClose]`

#### `SeasonSummaryCard` (frontend/src/components/season/SeasonSummaryCard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SeasonDashboard.tsx`
- **JSX Rendered By:** `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  season: Season;
  progress: number;
  actions: Action[];
  champion?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SeasonDashboard.tsx`: passed attributes `[season, progress, actions, champion]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 121: `<span className="stat-value">--</span> {/* Placeholder */}`

#### `Sidebar` (frontend/src/components/ui/Sidebar.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

#### `SkillNode3D` (frontend/src/components/skills/SkillNode3D.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/skills/SkillTreeCanvas.tsx`
- **JSX Rendered By:** `components/skills/SkillTreeCanvas.tsx`
- **Expected Props Interface:**
  ```typescript
  id: string;
  position: [number, number, number];
  iconType: string;
  isUnlocked: boolean;
  isEquipped: boolean;
  tier: string;
  label: string;
  onClick: (id: string) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/skills/SkillTreeCanvas.tsx`: passed attributes `[position, iconType, It, is, unlocked, if, s, in, the, list, isUnlocked, isEquipped, tier, Read, from, actual, trait, data, if, defaulting, for, visual, demo, label, onClick]`

#### `SkillTreeCanvas` (frontend/src/components/skills/SkillTreeCanvas.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SkillsPage.tsx`
- **JSX Rendered By:** `pages/SkillsPage.tsx`
- **Expected Props Interface:**
  ```typescript
  layout: SkillTreeLayout;
  unlockedTraits: string[]; // List of trait IDs
  equippedTraits: string[]; // List of trait IDs
  onNodeClick: (traitId: string) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SkillsPage.tsx`: passed attributes `[layout, unlockedTraits, equippedTraits, onNodeClick]`

#### `SkillsOverlay` (frontend/src/components/skills/SkillsOverlay.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SkillsPage.tsx`
- **JSX Rendered By:** `pages/SkillsPage.tsx`
- **Expected Props Interface:**
  ```typescript
  selectedTraitId: string | null;
  selectedTraitDetails: Trait | null;
  onCloseDetail: () => void;
  onEquip: (traitId: string) => void;
  playerPoints: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SkillsPage.tsx`: passed attributes `[selectedTraitId, selectedTraitDetails, selectedTraitId, Active, NFL, SIM, Trait, as, null, playerPoints, onCloseDetail]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 83: `{/* Mock data for now, would come from real trait */}`

#### `SoundtrackPlayer` (frontend/src/components/audio/SoundtrackPlayer.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `layouts/MainLayout.tsx`
- **JSX Rendered By:** `layouts/MainLayout.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `layouts/MainLayout.tsx`: passed attributes `[]`

#### `SpotlightButton` (frontend/src/components/immersive/SpotlightButton.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

#### `StandingsTable` (frontend/src/components/season/StandingsTable.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SeasonDashboard.tsx`
- **JSX Rendered By:** `pages/SeasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  /** List of team standings to display. */
  standings: TeamStanding[];
  /** Whether the data is currently loading. */
  loading?: boolean;
  /** Whether to show a compact version of the table. */
  compact?: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SeasonDashboard.tsx`: passed attributes `[standings, compact]`
  - In `pages/SeasonDashboard.tsx`: passed attributes `[standings]`

#### `StarfieldBackground` (frontend/src/components/skills/StarfieldBackground.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/skills/SkillTreeCanvas.tsx`, `pages/TrainingCenter.tsx`
- **JSX Rendered By:** `pages/TrainingCenter.tsx`, `components/skills/SkillTreeCanvas.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/TrainingCenter.tsx`: passed attributes `[]`
  - In `components/skills/SkillTreeCanvas.tsx`: passed attributes `[]`

#### `StorylineTracker` (frontend/src/components/news/StorylineTracker.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  teamId?: number;
  ```

#### `TaskListPanel` (frontend/src/components/common/TaskListPanel.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/common/FeedbackWidget.tsx`
- **JSX Rendered By:** `components/common/FeedbackWidget.tsx`
- **Expected Props Interface:**
  ```typescript
  annotations: Annotation[];
  onEdit: (annotation: Annotation) => void;
  onRemove: (id: string) => void;
  onClose: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `components/common/FeedbackWidget.tsx`: passed attributes `[annotations, onEdit, onRemove, onClose]`

#### `TeamNeeds` (frontend/src/components/offseason/TeamNeeds.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/OffseasonDashboard.tsx`
- **JSX Rendered By:** `pages/OffseasonDashboard.tsx`
- **Expected Props Interface:**
  ```typescript
  needs: TeamNeed[];
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/OffseasonDashboard.tsx`: passed attributes `[needs]`

#### `Telestrator` (frontend/src/components/ui/Telestrator.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/Playbook.tsx`
- **JSX Rendered By:** `pages/Playbook.tsx`
- **Expected Props Interface:**
  ```typescript
  isActive: boolean;
  onClose: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/Playbook.tsx`: passed attributes `[isActive, onClose]`

#### `TiltCard` (frontend/src/components/immersive/TiltCard.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/TeamSelection.tsx`
- **JSX Rendered By:** `pages/TeamSelection.tsx`
- **Expected Props Interface:**
  ```typescript
  className?: string;
  children: React.ReactNode;
  intensity?: number; // degrees
  glow?: boolean;
  onClick?: React.MouseEventHandler<HTMLDivElement>;
  "data-testid"?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TeamSelection.tsx`: passed attributes `[team-card, broadcast-glass, group, relative, overflow-hidden, rounded-2xl, border, transition-all, duration-300, isSelected, border-yellow-400, ring-2, 50, 10, onClick]`

#### `TradeAnalyzer` (frontend/src/components/trades/TradeAnalyzer.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/offseason/TradeModal.tsx`, `components/trades/TradeNegotiator.tsx`, `components/trades/index.ts`
- **JSX Rendered By:** `components/offseason/TradeModal.tsx`, `components/trades/TradeNegotiator.tsx`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  teamId: number;
  targetTeamId?: number | null;
  offeredAssets: number[]; // Player IDs
  requestedAssets: number[]; // Player IDs
  ```
- **Sample Props Passed at Call Site:**
  - In `components/offseason/TradeModal.tsx`: passed attributes `[seasonId, teamId, offeredAssets, In, this, simple, modal, we, are, trading, the, current, pick, which, d, need, ID, For, ll, just, simulate, it, by, passing, empty, arrays, as, the, backend, handles, logic, based, on, context, or, we, need, to, pass, pick, ID, the, backend, endpoint, expects, offered_ids, and, Since, this, modal, is, Trade, Current, we, should, ideally, pass, the, pick, the, current, TradeModal, t, have, the, pick, ID, ll, assume, for, this, MVP, integration, we, just, pass, empty, to, trigger, the, general, check, or, mock, A, better, approach, is, to, pass, a, dummy, ID, or, update, s, pass, empty, for, now, and, let, the, frontend, handle, it, gracefully, or, just, show, the, requestedAssets]`
  - In `components/trades/TradeNegotiator.tsx`: passed attributes `[seasonId, teamId, targetTeamId, offeredAssets]`

#### `TradeBlock` (frontend/src/components/trades/TradeBlock.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `components/trades/index.ts`, `pages/TradeCenterPage.tsx`
- **JSX Rendered By:** `pages/TradeCenterPage.tsx`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  userTeamId: number;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TradeCenterPage.tsx`: passed attributes `[seasonId, userTeamId]`

#### `TradeCenter` (frontend/src/components/trades/TradeCenter.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  userTeamId: number;
  userTeam: Team;
  ```
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 318: `className="trade-drop-zone-placeholder"`
  - Line 374: `placeholder="Search players..."`
  - Line 478: `className="trade-drop-zone-placeholder"`
  - Line 534: `placeholder="Search players..."`
  - Line 605: `<div className="trade-drop-zone-placeholder">`

#### `TradeModal` (frontend/src/components/offseason/TradeModal.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`
- **JSX Rendered By:** `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  currentTeamId: number;
  onClose: () => void;
  onTrade: (targetTeamId: number) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/DraftRoom.tsx`: passed attributes `[seasonId, currentTeamId, onClose]`
- ⚠️ **Mock Data / Fallback Hits:**
  - Line 72: `// We'll assume for this MVP integration we just pass empty to trigger the "general fairness" check or mock it.`
  - Line 73: `// A better approach is to pass a dummy ID or update props.`

#### `TradeNegotiator` (frontend/src/components/trades/TradeNegotiator.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/TradeCenterPage.tsx`
- **JSX Rendered By:** `pages/TradeCenterPage.tsx`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  userTeamId: number;
  initialOffer?: TradeOffer | null; // Support for counter-offers
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TradeCenterPage.tsx`: passed attributes `[seasonId, userTeamId, initialOffer]`

#### `TradePhone` (frontend/src/components/draft/TradePhone.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`
- **JSX Rendered By:** `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  ```typescript
  onAnswer: () => void;
  hasOffer: boolean;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/DraftRoom.tsx`: passed attributes `[hasOffer, Simulate, offer, when, modal, is, open, for, or, add, specific, state, onAnswer]`

#### `TrainingSessionResult` (frontend/src/components/training/TrainingSessionResult.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/TrainingCenter.tsx`
- **JSX Rendered By:** `pages/TrainingCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  result: TrainingResult;
  onClose: () => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TrainingCenter.tsx`: passed attributes `[result, onClose]`

#### `TraitBadge` (frontend/src/components/common/TraitBadge.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **JSX Rendered By:** `components/coaching/CoachingUnlockPanel.tsx`
- **Expected Props Interface:**
  ```typescript
  trait: Trait;
  showTooltip?: boolean;
  ```

#### `TraitBadge` (frontend/src/components/shared/TraitBadge.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **JSX Rendered By:** `components/coaching/CoachingUnlockPanel.tsx`
- **Expected Props Interface:**
  ```typescript
  name: string;
  tier: "GOLD" | "SILVER" | "BRONZE" | "COMMON";
  description?: string;
  iconUrl?: string;
  ```

#### `TraitBadgeGrid` (frontend/src/components/skills/TraitBadgeGrid.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/SkillsPage.tsx`
- **JSX Rendered By:** `pages/SkillsPage.tsx`
- **Expected Props Interface:**
  ```typescript
  unlockedTraits: string[];
  allTraits?: Trait[];
  onTraitClick?: (traitName: string) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/SkillsPage.tsx`: passed attributes `[unlockedTraits, onTraitClick]`

#### `TraitManager` (frontend/src/components/dev/TraitManager.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  playerId: number;
  playerName?: string;
  ```

#### `TraitNotification` (frontend/src/components/ui/TraitNotification.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  traitName: string;
  playerName: string;
  type?: "UNLOCK" | "UPGRADE" | "LOST";
  duration?: number;
  onDismiss?: () => void;
  ```

#### `TraitTooltip` (frontend/src/components/common/TraitTooltip.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **JSX Rendered By:** `components/common/TraitBadge.tsx`
- **Expected Props Interface:**
  ```typescript
  trait: Trait;
  ```

#### `TreatmentModal` (frontend/src/components/medical/TreatmentModal.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  isOpen: boolean;
  playerId?: number;
  playerName?: string;
  partName: string;
  currentHealth: number;
  injurySeverity?: number;
  weeksRemaining?: number;
  onClose: () => void;
  onConfirm: (treatment: TreatmentType) => void;
  ```

#### `TrophyCaseScene` (frontend/src/components/trophy/TrophyCaseScene.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/TrophyRoom.tsx`
- **JSX Rendered By:** `pages/TrophyRoom.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/TrophyRoom.tsx`: passed attributes `[]`

#### `WarRoomTicker` (frontend/src/components/draft/WarRoomTicker.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/DraftRoom.tsx`
- **JSX Rendered By:** `pages/DraftRoom.tsx`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*
- **Sample Props Passed at Call Site:**
  - In `pages/DraftRoom.tsx`: passed attributes `[]`

#### `WeatherWidget` (frontend/src/components/game/WeatherWidget.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/LiveSim.tsx`
- **JSX Rendered By:** `pages/LiveSim.tsx`
- **Expected Props Interface:**
  ```typescript
  weather: GameWeather;
  location?: string;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/LiveSim.tsx`: passed attributes `[weather, location, Lambeau]`

#### `WeeklyRecapModal` (frontend/src/components/news/WeeklyRecapModal.tsx) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  ```typescript
  seasonId: number;
  week: number;
  isOpen: boolean;
  onClose: () => void;
  ```

#### `WeeklyScheduleTimeline` (frontend/src/components/training/WeeklyScheduleTimeline.tsx) — 🟢 MOUNTED
- **Mount Status:** `MOUNTED`
- **Mounted In (Parent Files):** `pages/TrainingCenter.tsx`
- **JSX Rendered By:** `pages/TrainingCenter.tsx`
- **Expected Props Interface:**
  ```typescript
  selectedDay?: string;
  onSelectDay: (day: string) => void;
  ```
- **Sample Props Passed at Call Site:**
  - In `pages/TrainingCenter.tsx`: passed attributes `[selectedDay, onSelectDay]`

#### `index` (frontend/src/components/news/index.ts) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

#### `index` (frontend/src/components/trades/index.ts) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

#### `index` (frontend/src/components/transitions/index.ts) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

#### `staggerChildVariants` (frontend/src/components/transitions/transitionVariants.ts) — 🔴 UNMOUNTED / ORPHANED
- **Mount Status:** `UNMOUNTED / ORPHANED`
- **Expected Props Interface:**
  *No required props (standalone / context consumer)*

---

## 5. Catalog of Unmounted & Orphaned Components (36 Components + 3 Legacy Pages)
The following components exist in the repository but have 0 incoming render calls in the active application tree:

| Component Name | File Path | Original Purpose & Why Orphaned | Remediation Recommendation |
|---|---|---|---|
| `DraftLegacy` | `frontend/src/pages/DraftLegacy.tsx` | Old table-based draft room | Safe to archive / remove |
| `FrontOffice_Baseline` | `frontend/src/pages/FrontOffice_Baseline.tsx` | Static baseline roster screen | Retain for visual baseline tests or archive |
| `SeasonDashboardLegacy` | `frontend/src/pages/SeasonDashboardLegacy.tsx` | Early season dashboard prototype | Safe to archive / remove |
| `FieldVisualizer` | `frontend/src/components/3d/FieldVisualizer.tsx` | Early Three.js field renderer | Superseded by `EnhancedFieldVisualizer.tsx` |
| `PlayAnimator` | `frontend/src/components/3d/PlayAnimator.tsx` | 3D play trajectory animator | Integrate into `LiveGameVisualizer.tsx` for replay mode |
| `PlayerCharacter` | `frontend/src/components/3d/PlayerCharacter.tsx` | Early player 3D mesh | Superseded by `EnhancedPlayerCharacter.tsx` |
| `SceneContainer` | `frontend/src/components/3d/SceneContainer.tsx` | Canvas wrapper for early 3D view | Superseded by `LiveGameVisualizer.tsx` |
| `ErrorBoundary` | `frontend/src/components/ErrorBoundary.tsx` | Generic class error boundary | Router uses `RootErrorBoundary` and `RouteErrorBoundary` |
| `FieldView` | `frontend/src/components/FieldView.tsx` | Phase 1 static 2D formation diagram | Superseded by `FieldCanvas.tsx` & `GridironVisualizer.tsx` |
| `CoachCard` | `frontend/src/components/coaching/CoachCard.tsx` | Styled-component coach profile card | Mount inside `CoachSettings.tsx` or `CoachingTree.tsx` |
| `CoachingUnlockPanel` | `frontend/src/components/coaching/CoachingUnlockPanel.tsx` | Modal to unlock traits with coaching points | Mount in `CoachingTree.tsx` or `SkillsPage.tsx` |
| `NewsFeed` | `frontend/src/components/common/NewsFeed.tsx` | Standalone category-filtered news feed | Deduplicate with `components/season/NewsFeed.tsx` |
| `TraitBadge` | `frontend/src/components/common/TraitBadge.tsx` | Badge atom for player traits with tooltip | Deduplicate with `components/skills/TraitBadgeGrid.tsx` |
| `TraitTooltip` | `frontend/src/components/common/TraitTooltip.tsx` | Tooltip popup for trait tier details | Deduplicate with skills tooltip |
| `TraitManager` | `frontend/src/components/dev/TraitManager.tsx` | Dev panel to manually assign/remove traits | Mount as dev modal in `Settings.tsx` or `SkillsPage.tsx` |
| `FatigueIndicator` | `frontend/src/components/game/FatigueIndicator.tsx` | Circular energy/fatigue gauge | Integrate into `GameStats.tsx` / `ScoreBoard.tsx` in `LiveSim.tsx` |
| `ReplayScrubber` | `frontend/src/components/game/ReplayScrubber.tsx` | Play scrubber timeline for canvas replay | Mount below `FieldCanvas.tsx` in `LiveSim.tsx` |
| `LogoTimeline` | `frontend/src/components/history/LogoTimeline.tsx` | Historical franchise era logos | Mount inside `TrophyRoom.tsx` or `TeamSelection.tsx` |
| `SpotlightButton` | `frontend/src/components/immersive/SpotlightButton.tsx` | Radial cursor glow motion button atom | Reusable button atom; integrate into War Room buttons |
| `TreatmentModal` | `frontend/src/components/medical/TreatmentModal.tsx` | Modal for selecting 4 injury treatments | Mount inside `MedicalCenter.tsx` on body part click |
| `NewsFeedWidget` | `frontend/src/components/news/NewsFeedWidget.tsx` | Sidebar widget for living news | Mount in `Dashboard.tsx` or `SeasonDashboard.tsx` sidebar |
| `StorylineTracker` | `frontend/src/components/news/StorylineTracker.tsx` | Multi-week narrative arc tracker | Mount in `Dashboard.tsx` or `SeasonDashboard.tsx` |
| `WeeklyRecapModal` | `frontend/src/components/news/WeeklyRecapModal.tsx` | Modal summarizing completed week games | Mount in `SeasonDashboard.tsx` post-simulation |
| `news/index.ts` | `frontend/src/components/news/index.ts` | Barrel export for news components | Unreferenced barrel |
| `TraitBadge` | `frontend/src/components/shared/TraitBadge.tsx` | Duplicate shared trait badge | Deduplicate / merge |
| `TradeCenter` | `frontend/src/components/trades/TradeCenter.tsx` | Monolithic trade room container | Refactored into `TradeCenterPage.tsx` subcomponents |
| `trades/index.ts` | `frontend/src/components/trades/index.ts` | Barrel export for trade components | Unreferenced barrel |
| `CampSchedulePlanner` | `frontend/src/components/training/CampSchedulePlanner.tsx`| Training schedule calendar planner | Mount inside `TrainingCenter.tsx` |
| `CoachingStylePicker` | `frontend/src/components/training/CoachingStylePicker.tsx`| Card-based coaching style picker | Superseded by 3D `CoachingStyleDial.tsx` |
| `DrillCard` | `frontend/src/components/training/DrillCard.tsx` | 2D drill card item | Superseded by `DrillCard3D.tsx` |
| `PlayerProgressChart` | `frontend/src/components/training/PlayerProgressChart.tsx`| Progress line chart for training gains | Mount in `TrainingCenter.tsx` after session results |
| `PageTransition` | `frontend/src/components/transitions/PageTransition.tsx` | Wrapper for animated route transitions | `MainLayout.tsx` handles transitions directly |
| `transitions/index.ts` | `frontend/src/components/transitions/index.ts` | Barrel export for transitions | Unreferenced barrel |
| `transitionVariants.ts`| `frontend/src/components/transitions/transitionVariants.ts`| Framer motion variant definitions | Merged into `styles/motion.ts` |
| `Badge` | `frontend/src/components/ui/Badge.tsx` | Atom badge component | Reusable atom |
| `EnhancedPlayerProfile`| `frontend/src/components/ui/EnhancedPlayerProfile.tsx` | Tabbed full-card player modal | Mount on player click in `FrontOffice.tsx` / `DepthChart.tsx` |
| `PrimeCard` | `frontend/src/components/ui/PrimeCard.tsx` | Neon bordered card container | Reusable container |
| `Sidebar` | `frontend/src/components/ui/Sidebar.tsx` | Early sidebar navigation prototype | Superseded by `components/Navigation.tsx` |
| `TraitNotification` | `frontend/src/components/ui/TraitNotification.tsx` | Floating toast for unlocked traits | Mount in `MainLayout.tsx` or `SkillsPage.tsx` |

---

## 6. Comprehensive Mock & Fallback Data Audit

### 6.1 Services Layer Mock Data
1. **`frontend/src/services/scouting.ts`**
   - `MOCK_SCOUTING_REPORT`: Hardcoded scouting report object containing traits, college stats, and physical ratings.
   - `MOCK_BACKSHIORY`: Hardcoded player backstory narrative.
   - **Remediation:** Wire `getScoutingReport(prospectId)` and `getPlayerBackstory(prospectId)` to FastAPI backend `/api/draft/prospects/{id}/report` and `/api/draft/prospects/{id}/backstory`.

2. **`frontend/src/services/tradeApi.ts`**
   - `generateMockIncomingOffers(teamId)`: Procedurally generates synthetic trade offers when API fails.
   - `respondToOffer()`: Contains mock fallback simulation of offer acceptance/rejection.
   - `getTradeBlock()`: Falls back to mock tradeable assets if endpoint fails.
   - **Remediation:** Ensure backend `/api/trades/offers` and `/api/trades/respond` endpoints are fully implemented and remove client mock generators.

3. **`frontend/src/services/ImageGenService.ts`**
   - `mockImages`: Array of 5 unsplash stock photos returned as random mock images.
   - **Remediation:** Wire to backend generative image endpoint or SVG avatar generator.

### 6.2 Router Loaders Mock Data
1. **`frontend/src/router.tsx` (`draftRoomLoader`)**
   - Lines 148-205: Defines `mockTeams`, `mockSeason`, and `mockCurrentPick` directly in the loader.
   - **Remediation:** Replace mock loader data with live `api.getTeams()`, `seasonApi.getCurrentSeason()`, and `seasonApi.getCurrentPick()` calls.

### 6.3 Components & Pages Inline Mock / Fallback Logic
1. **`pages/Dashboard.tsx` (Line 89)**: Calculates a simulated opponent string based on current week number instead of querying backend match schedule.
2. **`pages/LiveSim.tsx` (Line 64)**: Uses mock ball trajectory formula when websocket or simulation physics data is pending.
3. **`components/3d/LiveGameVisualizer.tsx` (Lines 116-126)**: Inlines `mockPlayResult` object with hardcoded yards gained and outcome.
4. **`components/coaching/GameplanDashboard.tsx` (Lines 47, 87)**: Uses hardcoded familiarity percentages (`85%`, `70%`) for offensive and defensive scheme execution.
5. **`components/game/FieldCanvas.tsx` (Line 205)**: Distinguishes offense vs defense by checking `player_id < 11`.
6. **`components/skills/SkillTreeCanvas.tsx` (Line 89)**: Defaults tier to `GOLD` for visual demonstration.
7. **`components/skills/SkillsOverlay.tsx` (Line 83)**: Inlines static perk description text.
8. **`components/history/LogoTimeline.tsx` (Line 5)**: Inlines `MOCK_HISTORY` array with 3 static era descriptions.

---

## 7. Navigation Completeness & View Gap Analysis

### 7.1 Sidebar Navigation Coverage
`components/Navigation.tsx` exposes 14 navigation links:
1. `WAR ROOM` (`/`) -> `Dashboard.tsx`
2. `SEASON` (`/season`) -> `SeasonDashboard.tsx`
3. `ROSTER` (`/empire/front-office`) -> `FrontOffice.tsx`
4. `DEPTH CHART` (`/empire/depth-chart`) -> `DepthChart.tsx`
5. `PLAYBOOK` (`/playbook`) -> `Playbook.tsx`
6. `GAME DAY` (`/live-sim`) -> `LiveSim.tsx`
7. `MEDICAL` (`/medical-center`) -> `MedicalCenter.tsx`
8. `TRADE DESK` (`/empire/trade-center`) -> `TradeCenterPage.tsx`
9. `OFFSEASON` (`/offseason`) -> `OffseasonDashboard.tsx`
10. `DRAFT ROOM` (`/offseason/draft`) -> `DraftRoom.tsx`
11. `TROPHY ROOM` (`/empire/trophy-room`) -> `TrophyRoom.tsx`
12. `TRAINING` (`/training`) -> `TrainingCenter.tsx`
13. `MY FRANCHISE` (`/team-selection`) -> `TeamSelection.tsx`
14. `SETTINGS` (`/settings`) -> `Settings.tsx`

### 7.2 Routing & Navigation Gaps Identified
1. **Skills Tree Page Discovery:** `SkillsPage.tsx` is mounted at `/players/:playerId/skills` and `/skills`, but lacks a direct menu entry in `Navigation.tsx`. Users currently navigate via player cards, but a standalone 'SKILLS & TRAITS' link or direct player profile modal transition is recommended.
2. **Player Detail Modal Integration:** `EnhancedPlayerProfile.tsx` provides a high-fidelity tabbed profile (Attributes, Contracts, Traits, Injury History) but is unmounted. `FrontOffice.tsx` and `DepthChart.tsx` currently only show basic cards or open player modals with partial data.
3. **Medical Treatment Action:** `MedicalCenter.tsx` displays `OrthopedicTriageModal.tsx`, while `TreatmentModal.tsx` contains 4 specific surgical/injection treatment pathways. Merging or mounting `TreatmentModal.tsx` on body part triage unlocks the 5-pathway orthopedic triage requirement.
4. **Live Replay Scrubber:** `ReplayScrubber.tsx` exists and controls `FieldCanvasRef`, but is unmounted in `LiveSim.tsx`. Mounting it enables instant replay and telemetry scrubbing.
5. **Living World News & Storylines:** `NewsFeedWidget.tsx` and `StorylineTracker.tsx` in `components/news/` are unmounted. Integrating them into `Dashboard.tsx` and `SeasonDashboard.tsx` activates emergent storyline tracking.

---

## 8. Prioritized Remediation Action Plan

### Phase 1: High-Priority UI Component Mounts
1. **Mount `ReplayScrubber.tsx` into `LiveSim.tsx`** to fulfill cryptographic replay telemetry verification.
2. **Mount `TreatmentModal.tsx` into `MedicalCenter.tsx`** to fulfill the 5-pathway orthopedic triage requirement.
3. **Mount `EnhancedPlayerProfile.tsx` in `FrontOffice.tsx` and `DepthChart.tsx`** when clicking any player row or card.
4. **Mount `NewsFeedWidget.tsx` / `StorylineTracker.tsx` in `Dashboard.tsx`** for live franchise narrative generation.
5. **Mount `LogoTimeline.tsx` in `TrophyRoom.tsx`** to display franchise championship history.

### Phase 2: Live Backend Endpoint Wiring & Mock Data Elimination
1. Replace `router.tsx` `draftRoomLoader` mock objects with live API fetches.
2. Wire `services/scouting.ts` to backend `/api/draft/prospects/{id}/report` and backstory endpoints.
3. Wire `services/tradeApi.ts` to live trade evaluation and incoming offers endpoints, eliminating `generateMockIncomingOffers()`.
4. Replace hardcoded familiarity calculations in `GameplanDashboard.tsx` with coach scheme ratings from backend.

### Phase 3: Dead Code & Orphan Cleanup
1. Safely remove or archive legacy prototypes (`DraftLegacy.tsx`, `FrontOffice_Baseline.tsx`, `SeasonDashboardLegacy.tsx`, `FieldView.tsx`, `components/3d/FieldVisualizer.tsx`, `components/3d/PlayerCharacter.tsx`).
2. Clean up redundant barrel files (`components/news/index.ts`, `components/trades/index.ts`, `components/transitions/index.ts`).
3. Deduplicate `TraitBadge` between `components/common/`, `components/shared/`, and `components/skills/`.
