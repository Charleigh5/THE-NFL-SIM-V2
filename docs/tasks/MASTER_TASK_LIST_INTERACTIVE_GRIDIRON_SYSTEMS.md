# NFL Sim Engine: Master Task List — Interactive Gridiron Systems

**Document ID:** NFL-SIM-TASK-INDEX-001  
**Author:** Antigravity Architect (Chris Weir Persona)  
**Date:** September 2026  
**Reference Rule:** [`.agent/rules/task-list-template.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/.agent/rules/task-list-template.md)  

---

## Executive Overview

This master document links the four production-grade task specifications generated for **THE-NFL-SIM-V2 ("The Digital Gridiron")**. Each task follows the strict 4-Phase Cognitive Engineering Standard:
1. **Phase 1: Conceptual Exploration (The Scout)**
2. **Phase 2: Adversarial Synthesis (The Architect)**
3. **Phase 3: Actionable Blueprint (The Engineer)**
4. **Phase 4: The Auditor (Verification)**

---

## Detailed Task Index

### 1. Option 1: Interactive Free Agency Market & Contract Bidding Hub
- **File:** [`TASK-010_INTERACTIVE_FREE_AGENCY_MARKET_AND_CONTRACT_BIDDING_HUB.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/tasks/TASK-010_INTERACTIVE_FREE_AGENCY_MARKET_AND_CONTRACT_BIDDING_HUB.md)
- **Scope:**
  - Dynamic free agent market browser with multi-facet filtering (Position, OVR, Age, Scheme Fit).
  - Tactile Contract Offer Builder with real-time NFL capology (AAV, Signing Bonus proration over 5 years, Guaranteed Money, Rule of 51 checks).
  - Multi-round AI GM counter-bidding and player sentiment evaluation engine.
- **Key Subtasks:**
  - `Subtask 2.1`: Free Agent Query Engine (`get_free_agents_paginated`)
  - `Subtask 2.2`: NFL Capology & Proration Calculator
  - `Subtask 2.3`: Player Valuation & Agent Feedback Synthesizer
  - `Subtask 2.4`: Multi-Team AI Counter-Bidding Engine
  - `Subtask 2.5`: Atomic Contract Execution & Roster Signing
  - `Subtask 3.1`: Free Agency Market View (`FreeAgencyHub.tsx`)
  - `Subtask 3.2`: Contract Builder Studio Modal (`ContractBuilderModal.tsx`)
  - `Subtask 3.3`: Live Agent Sentiment & Interest Gauge
  - `Subtask 3.4`: Bidding War War-Room Feed (`BiddingWarTicker.tsx`)

---

### 2. Option 2: Locker Room & Closed-Door Council UI
- **File:** [`TASK-011_LOCKER_ROOM_AND_CLOSED_DOOR_COUNCIL_UI.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/tasks/TASK-011_LOCKER_ROOM_AND_CLOSED_DOOR_COUNCIL_UI.md)
- **Scope:**
  - Team Tension & Morale Command Center in Front Office/War Room.
  - Interactive 3-Way Closed-Door Confrontation Modal (Disgruntled Star, Head Coach, Team Captain) powered by the Tier 3 Society Engine.
  - Big-Six Psychological DNA Hexagon visualizer.
- **Key Subtasks:**
  - `Subtask 2.1`: Roster Tension & Chemistry Overview Aggregator
  - `Subtask 2.2`: Automated Weekly Evaluation Hook in Season Progression
  - `Subtask 2.3`: GM Action Resolution Pipeline (`resolve_action` commit)
  - `Subtask 3.1`: Locker Room Tab in Front Office (`LockerRoomHub.tsx`)
  - `Subtask 3.2`: Psychological DNA Radar Visualizer (`PsychologicalHexagon.tsx`)
  - `Subtask 3.3`: 3-Way Closed-Door Council Modal (`ClosedDoorCouncilModal.tsx`)
  - `Subtask 3.4`: Resolution Aftermath & News Ticker

---

### 3. Option 3: Medical Center Live Roster & Surgical Triage Integration
- **File:** [`TASK-012_MEDICAL_CENTER_LIVE_ROSTER_AND_SURGICAL_TRIAGE_INTEGRATION.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/tasks/TASK-012_MEDICAL_CENTER_LIVE_ROSTER_AND_SURGICAL_TRIAGE_INTEGRATION.md)
- **Scope:**
  - Complete eradication of static mock rosters in `MedicalCenter.tsx`.
  - Dynamic binding to active franchise's real injured roster via `useTeamStore`.
  - Full relational database persistence for 7-zone surgical triage and treatment decisions (`BodyHealth`, `Player.injury_status`, `weeks_to_recovery`).
- **Key Subtasks:**
  - `Subtask 2.1`: Live Injury Roster Aggregator (`GET /api/medical/team/{team_id}/injuries`)
  - `Subtask 2.2`: Orthopedic Triage DB Mutation Pipeline (`POST /api/medical/orthopedic/triage`)
  - `Subtask 2.3`: Preventative Maintenance Starters Query
  - `Subtask 3.1`: Clean Roster Ingestion in `MedicalCenter.tsx`
  - `Subtask 3.2`: Zero-Injury Preventive Maintenance View
  - `Subtask 3.3`: Interactive 7-Zone Click-to-Triage Flow
  - `Subtask 3.4`: Treatment Modal DB Action Dispatch & Cache Invalidation

---

### 4. Option 4: In-Game Play-Calling HUD during Live Sim
- **File:** [`TASK-013_IN_GAME_PLAY_CALLING_HUD_DURING_LIVE_SIM.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/tasks/TASK-013_IN_GAME_PLAY_CALLING_HUD_DURING_LIVE_SIM.md)
- **Scope:**
  - Real-time Play-Calling HUD in `LiveSim.tsx` for offensive concepts (Run/Pass) and defensive packages (Coverages/Blitzes).
  - High-leverage 4th-Down Analytics Prompt Modal (Go For It, Punt, Field Goal) driven by the Baldwin Win Probability model.
  - Sideline clock management controls (Timeouts, Hurry-Up, Chew Clock, Spike, Kneel).
- **Key Subtasks:**
  - `Subtask 2.1`: Live Engine Manual Play Injection over WebSocket / REST
  - `Subtask 2.2`: 4th-Down Analytics Engine (`fourth_down_calculator.py`)
  - `Subtask 2.3`: Timeout & Clock Stoppage Controller
  - `Subtask 3.1`: Mount `PlayCallingHUD.tsx` in `LiveSim.tsx`
  - `Subtask 3.2`: 4th Down High-Leverage Prompt Modal (`FourthDownModal.tsx`)
  - `Subtask 3.3`: Sideline Clock & Timeout Bar (`ClockManagementBar.tsx`)
  - `Subtask 3.4`: Coach Mode vs Spectator Mode Toggle
