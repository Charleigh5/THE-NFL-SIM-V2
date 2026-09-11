# Master System Architecture: 4-Core Requirements & 20-Feature Expansion Blueprint

**Document ID:** NFL-SIM-EXPANSION-2026-001  
**Project:** THE-NFL-SIM-V2 ("The Digital Gridiron")  
**Architect:** Antigravity Chief System Architect (Chris Weir Persona)  
**Status:** ARCHITECTURE_FROZEN  
**Standard:** 2025/2026 Production Standard (Strict Typing, Deterministic Logic, 3-Gate Security, Sub-100ms Latency)

---

## 🏛️ EXECUTIVE SUMMARY & SYSTEM TOPOLOGY

This document serves as the supreme architectural map extrapolating all core files and 20 modular feature expansions across the 4 foundational pillars of **THE-NFL-SIM-V2**:
1. **Module 1 (R1)**: Interactive Free Agency Market & Contract Bidding Hub (`TASK-010`)
2. **Module 2 (R2)**: Locker Room & Closed-Door Council UI (`TASK-011`)
3. **Module 3 (R3)**: Medical Center Live Roster & Surgical Triage Integration (`TASK-012`)
4. **Module 4 (R4)**: In-Game Play-Calling HUD during Live Sim (`TASK-013`)

```text
                                  +-------------------------------------------------------------+
                                  |                 THE NFL SIM ENGINE V2                       |
                                  |                 "The Digital Gridiron"                      |
                                  +-------------------------------------------------------------+
                                                                 |
              +--------------------------+-----------------------+-----------------------+--------------------------+
              |                          |                                               |                          |
              V                          V                                               V                          V
     +-----------------+        +-----------------+                             +-----------------+        +-----------------+
     |   MODULE 1      |        |   MODULE 2      |                             |   MODULE 3      |        |   MODULE 4      |
     |   Free Agency   |        |   Locker Room   |                             |   Medical Ctr   |        |   Live Sim HUD  |
     |   Bidding Hub   |        |   Council UI    |                             |   Live Triage   |        |   Play Calling  |
     +-----------------+        +-----------------+                             +-----------------+        +-----------------+
              |                          |                                               |                          |
     +--------+--------+        +--------+--------+                             +--------+--------+        +--------+--------+
     | 5 EXPANSIONS:   |        | 5 EXPANSIONS:   |                             | 5 EXPANSIONS:   |        | 5 EXPANSIONS:   |
     | 1.1 Void Years  |        | 2.1 Press Leaks |                             | 3.1 Orthobio    |        | 4.1 Baldwin EPA |
     | 1.2 Comp Picks  |        | 2.2 Cliques     |                             | 3.2 Turf Risk   |        | 4.2 Crowd Noise |
     | 1.3 State Taxes |        | 2.3 Captain Rep |                             | 3.3 IR Window   |        | 4.3 DC AI Buffs |
     | 1.4 Tag Tenders |        | 2.4 Hot Seat    |                             | 3.4 Toradol Inj |        | 4.4 2-Min Tempo |
     | 1.5 Post-June 1 |        | 2.5 Holdouts    |                             | 3.5 Trauma Brd  |        | 4.5 Ref Review  |
     +-----------------+        +-----------------+                             +-----------------+        +-----------------+
```

---

## 📋 COMPLETE 20-FEATURE TAXONOMY & FILE MATRIX

| Mod | Feature ID | Feature Name | Core Architectural Mechanism | Primary New / Modified Files |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | **R1-Core** | **Free Agency War Room & Bidding** | Real-time cap proration & AI GM multi-wave bidding | `free_agency.py` (API & Schemas), `FreeAgencyHub.tsx` |
| R1 | **1.1** | **Void Years & Option Bonus Restructuring** | Proration over $\min(5, \text{Years} + \text{Void})$; accelerated dead cap | `void_years_calculator.py`, `VoidYearToggle.tsx` |
| R1 | **1.2** | **Compensatory Draft Pick Formula (App. V)** | Net lost vs gained UFA percentiles & pick cancellation | `compensatory_pick_engine.py`, `CompPickWarningBadge.tsx` |
| R1 | **1.3** | **State Income Tax & Market Location Matrix** | Net take-home pay delta (0% FL/TX vs 13.3% CA) | `tax_adjusted_valuation.py`, `NetIncomeComparisonCard.tsx` |
| R1 | **1.4** | **Franchise Tag & Transition Tag Tenders** | Exclusive, non-exclusive top-5 positional averages | `tag_service.py`, `FranchiseTagModal.tsx` |
| R1 | **1.5** | **Post-June 1st Cut & Dead Cap Allocation** | 2-year split dead cap amortization simulator | `post_june_cut_service.py`, `CutPlayerCapPreviewModal.tsx` |
| **R2** | **R2-Core** | **Locker Room Hub & 3-Way Council UI** | Big-Six DNA math & 3-actor confrontation dialogues | `society.py`, `locker_room_agent.py`, `ClosedDoorCouncilModal.tsx` |
| R2 | **2.1** | **Anonymous Press Leaks ("Gridiron Insider")** | Probabilistic leaks to national media on high tension | `press_leak_generator.py`, `GridironInsiderTicker.tsx` |
| R2 | **2.2** | **Positional Group Cliques & Mentorship Tree** | Veteran captain traits accelerating rookie XP | `position_cliques.py`, `MentorshipAssignmentModal.tsx` |
| R2 | **2.3** | **Captain's Council Weekly Briefing & Vote** | Preseason player voting & weekly coach pulse meetings | `captain_election_service.py`, `CaptainBriefingCard.tsx` |
| R2 | **2.4** | **Owner Confidence Barometer & Hot Seat** | Multi-factor ownership patience & ultimatum mandates | `owner_confidence_engine.py`, `OwnerUltimatumModal.tsx` |
| R2 | **2.5** | **Contract Renegotiation Holdout Simulator** | Preseason camp holdouts, daily fines & rust decay | `holdout_service.py`, `HoldoutResolutionModal.tsx` |
| **R3** | **R3-Core** | **Medical Center Live Roster & 7-Zone Triage** | Real franchise DB binding & persistent orthopedic outcomes | `medical.py`, `MedicalCenter.tsx`, `BodyMap.tsx` |
| R3 | **3.1** | **Regenerative Orthobiologics vs Arthroscopy** | PRP / stem cell cartilage preservation vs surgery speed | `orthobiologics_service.py`, `BiologicsProtocolSelector.tsx` |
| R3 | **3.2** | **Turf vs Grass Biomechanical Load Engine** | Slit-film rotational traction multipliers on non-contact tears | `surface_injury_risk.py`, `TurfRiskAlertBanner.tsx` |
| R3 | **3.3** | **Injured Reserve (IR) 21-Day Window Tracker** | NFL 8-return quota & 21-day practice countdown clock | `ir_management_service.py`, `PracticeWindowClock.tsx` |
| R3 | **3.4** | **Gameday "Toradol" Pain Block Trade-off** | Gameday numbing vs post-game trauma escalation risk | `pain_management.py`, `GamedayInjectionModal.tsx` |
| R3 | **3.5** | **Career Trauma Review Board & Buyouts** | Concussion/spine medical retirement & CBA cap relief | `catastrophic_trauma_service.py`, `MedicalRetirementModal.tsx` |
| **R4** | **R4-Core** | **Sideline Play-Calling HUD during Live Sim** | Coach mode pause-and-call loop & tactical tray | `simulation.py`, `playcalling.py`, `PlayCallingHUD.tsx` |
| R4 | **4.1** | **Baldwin 4th-Down & 2-Pt Conversion Analytics** | Real-time Win Probability & Expected Points Added HUD | `baldwin_conversion_model.py`, `TwoPointConversionModal.tsx` |
| R4 | **4.2** | **Acoustic Decibel & Crowd Noise Interference** | Dynamic stadium noise causing audibles & false starts | `crowd_noise_engine.py`, `DecibelMeterWidget.tsx` |
| R4 | **4.3** | **DC AI Tendency Recognition & Counter Buffs** | Opponent coordinator predicting user play distribution | `coordinator_tendency_engine.py`, `CoordinatorTendencyBadge.tsx` |
| R4 | **4.4** | **Two-Minute Drill No-Huddle Clock Matrix** | Turbo tempo, chew clock, spike & intentional kneel | `tempo_controller.py`, `TwoMinuteHurryUpBar.tsx` |
| R4 | **4.5** | **Referee Challenge Flag & Booth Review** | High-tension toe-tap / spot reviews with audio ruling | `challenge_review_engine.py`, `ChallengePromptModal.tsx` |

---

## 🛠️ ARCHITECTURAL STANDARDS & CROSS-CUTTING CONCERNS

1. **Deterministic State Synchronization**:
   - All financial and psychological state transitions are governed by pure, deterministic equations before committing to the SQLAlchemy database.
   - Replay logs guarantee that any simulated bidding war, council confrontation, or injury recovery can be identically reproduced.
2. **Canonical 3-Gate Security Pattern**:
   - Gate 1: PII and user inputs redacted before logging or long-term vector storage.
   - Gate 2: Sensitive keys and secrets isolated behind opaque environment references.
   - Gate 3: All text feeds (press leaks, council dialogues, fan reactions) strictly treated as data to prevent model hijacking.
3. **Ultra-Low Latency & Non-Blocking Loops**:
   - Live sim pause/resume hooks execute in $< 50$ms over WebSocket connections.
   - Real-time capology and Baldwin 4th-down analytics execute in $< 10$ms synchronously in memory.

---
*Reference Detailed Specifications:*
- [`R1_FREE_AGENCY_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/specifications/extrapolated_systems/R1_FREE_AGENCY_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md)
- [`R2_LOCKER_ROOM_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/specifications/extrapolated_systems/R2_LOCKER_ROOM_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md)
- [`R3_MEDICAL_TRIAGE_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/specifications/extrapolated_systems/R3_MEDICAL_TRIAGE_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md)
- [`R4_PLAY_CALLING_HUD_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/docs/specifications/extrapolated_systems/R4_PLAY_CALLING_HUD_FILE_EXTRAPOLATION_AND_5_EXPANSIONS.md)
