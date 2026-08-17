<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: Update Player System Master Dossier

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** The Player System Dossier was created on 2025-12-11 as a living reference document. Since then, the simulation engine has undergone massive expansion: decomposed player models (6 satellite tables), a 12-type attribute interaction engine, 25+ traits with rarity tiers, 7 RPG abilities, 7 player archetypes, Skyrim-style use-based progression, 50+ training drills, and a 4-compartment fatigue model. The dossier fell out of sync with the codebase.
- **Related Ideas:** Sports simulation documentation patterns from Football Manager (SI Games) and OOTP Baseball — living design documents that map every attribute to game mechanics. Dwarf Fortress' design documents as a model for emergent narrative simulation docs.
- **Future Potential:** Must scale to support: new positions (EDGE, SLOT), expanded GENESIS biometrics, coaching tree skill trees, morale/chemistry systems, and potential multiplayer league features. Document structure uses modular sections that can be independently updated.
- **Constraints:**
  - Documentation only — zero code changes permitted
  - Must accurately reflect current codebase (no aspirational features)
  - Must follow existing markdown conventions
  - Must include source file linkages for every documented system
  - All formulas must match source code exactly (verified via research subagents)

</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Incrementally patch the existing `PLAYER_SYSTEM_DOSSIER.md` — add missing sections, update outdated ones, leave stable sections alone. This preserves git history and minimizes diff noise.

### Powerful Antithesis

The existing dossier is 817 lines and was written when the system had a monolithic Player model. Since then:
1. **Architecture changed fundamentally** — The monolithic model was decomposed into 6 satellite tables. Every section referencing "Player" fields is now incorrect.
2. **13 major systems were added** — Attribute interactions, training camps, coaching trees, archetype effects, fatigue compartments, use-based XP, GENESIS biometrics. These aren't "patches" — they're entirely new domains.
3. **Formula accuracy** — Many formulas were simplified or changed during implementation. Patching risks leaving stale formulas next to new ones.
4. **Cross-reference integrity** — A patched doc would have broken internal links and inconsistent section numbering.

The attack conclusion: Incremental patches would create a Frankenstein document with mixed old/new patterns, broken cross-references, and structural inconsistency. The maintenance cost exceeds a full rewrite.

### The Superior Synthesis

**Full authoritative rewrite** with the following safeguards:
1. **Research-first** — 3 parallel research subagents extracted every constant, formula, and data structure from 40+ source files before writing began.
2. **Parallel writing** — 2 writer subagents produce the document in halves, then merged by the orchestrator with cross-reference validation.
3. **Structure preservation** — The document retains the original section numbering (1-14) for backward compatibility with any external references.
4. **Source verification** — Every formula includes its source file and function name for future auditors.
5. **Mermaid diagrams** — Architecture, play flow, and file linkage visualized for rapid comprehension.

This approach is definitive because it produces a single-pass, consistent, fully verified document rather than a patchwork.

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** Python 3.11+ / SQLAlchemy 2.0 (Mapped[T] syntax) / FastAPI / Pydantic v2
- **Language:** Python with strict typing (Mapped annotations, dataclass, BaseModel)
- **State Management:** SQLAlchemy ORM session-based, deterministic RNG for reproducibility

### 2. The Data Schema (Pre-Generation)

Target file: `docs/player-system/PLAYER_SYSTEM_DOSSIER.md`

Document structure (14 sections):
1. Core Player Model (satellite architecture, 14 positions, 60+ attributes)
2. Offense Positions (QB, RB, WR/TE, OL with physics configs)
3. Defense Positions (DL, LB, DB with physics configs)
4. Special Teams (K, P, returners)
5. Play Triggers & Attribute Interaction Engine (12 matchup types)
6. Progression & Regression (age curves, offseason formulas, use-based XP)
7. Training System (50+ drills, coaching philosophy, camps)
8. Trait System (25+ traits, rarity tiers, resolver)
9. RPG Abilities & Archetypes (7 abilities, 7 archetypes)
10. Contracts & Salary Cap (free agency market valuation)
11. Injury System & GENESIS (4-compartment fatigue, biometrics)
12. Rookie Generation (draft class creation, narratives)
13. File Linkage Map (40+ source files)
14. Changelog

### 3. Step-by-Step Execution

- [x] **Step 1: Research.** 3 parallel subagents read 40+ source files, extracted all constants, formulas, enums.
- [x] **Step 2: Write Part 1.** Dossier Writer subagent produces Sections 1-7 (Core Model through Training).
- [x] **Step 3: Write Part 2.** Dossier Writer subagent produces Sections 8-14 (Traits through Changelog).
- [x] **Step 4: Merge.** Orchestrator combines parts into final `PLAYER_SYSTEM_DOSSIER.md`.
- [x] **Step 5: Verify.** Markdown lint check, cross-reference validation, line count verification.
- [x] **Step 6: Archive.** Save task execution reference to `docs/task-references/`.

### 4. Edge Cases & Error Handling

- [Case A: Missing source file] -> Research subagent falls back to grep_search for alternate paths
- [Case B: Conflicting constants between files] -> Source closest to runtime (engine > service > model) wins
- [Case C: Undocumented system] -> Marked with `> [!NOTE] Implementation exists but details are incomplete` alert

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Accuracy:** All formulas verified against source code via 3 research subagents reading 40+ files.
- [x] **Completeness:** All 14 sections populated. No placeholder content.
- [x] **Cross-References:** Internal links verified between sections. File linkage map covers all 40+ source files.
- [x] **Formatting:** Consistent markdown: `##` sections, `###` subsections, properly aligned tables, fenced code blocks with language hints.
- [x] **Self-Critique:** If I were a senior reviewer at Google, I would flag:
  1. ✅ The document is very long — but this is intentional for a "single source of truth" design document.
  2. ✅ Some formulas use simplified notation — but they match the source code exactly.
  3. ✅ Mermaid diagrams may not render in all markdown viewers — but they render in GitHub and the project's tooling.

</final_audit>

---

<baton_handoff>
Next Immediate Step: The updated `PLAYER_SYSTEM_DOSSIER.md` is now the authoritative reference. When any player-related system changes, run `/update-player-dossier` to re-sync this document. No user action required at this time.
</baton_handoff>
