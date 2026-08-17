<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [DEP-001] Operator Decision Register & Codex Skill Ingestion

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** Antigravity and Codex multi-agent architectures require persistent operator preference registries to align autonomous cognitive loops with human engineering directives.
- **Related Ideas:** Mem0 persistent memory graphs, Model Context Protocol (MCP) tool registrations, `.codex/AGENTS.md` operating contracts.
- **Future Potential:** Enables zero-drift multi-agent swarm development where all background subagents and Codex instances operate under synchronized governance contracts.
- **Constraints:** Zero mutation of raw credentials/secrets, immutable accepted decisions vs. candidate learning separation, strict JSON schema validation.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Manually prompt each subagent or rely on default system prompts to recall operator preferences and skill configurations on each turn.

### Powerful Antithesis
Prompt-based recall leads to context drift, hallucinated operating boundaries, inconsistent safety classifications, and forgotten project rules across distributed subagent executions.

### The Superior Synthesis
Formally register `nfl-sim-architect` as an authoritative skill in `~/.codex/skills/cweir-operator-preferences/references/operator-decision-register.json` and sync it with `.agent/rules/app-master.md`. This locks the 6-stage lifecycle into persistent global memory with deterministic validation.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** Codex Customization System, Antigravity 2.0 Skill Kernel
- **Language:** Strict JSON Schema / Markdown
- **State Management:** SQLite Memory DB (`~/.codex/sqlite/memories_1.sqlite`) + Local JSON Decision Register

### 2. The Data Schema (Pre-Generation)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "OperatorDecisionRecord",
  "type": "object",
  "required": ["decision_id", "skill_name", "category", "status", "rules"],
  "properties": {
    "decision_id": { "type": "string" },
    "skill_name": { "type": "string" },
    "category": { "type": "string" },
    "status": { "type": "string", "enum": ["ACCEPTED", "CANDIDATE", "SUPERSEDED"] },
    "rules": { "type": "array", "items": { "type": "string" } }
  }
}
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Inspect `~/.codex/skills/cweir-operator-preferences/references/operator-decision-register.json`.
- [ ] **Step 2: Core Logic.** Register the `nfl-sim-architect` skill entry with rule constraints, verification gates, and 6-stage lifecycle directives.
- [ ] **Step 3: Interface.** Validate load order and test skill discovery via Antigravity/Codex kernel.

### 4. Edge Cases & Error Handling
- **Case A: Corrupted JSON Register** -> Validate syntax with strict parser before saving; create `.bak` timestamped snapshot.
- **Case B: Conflicting Decision Rules** -> Explicitly prioritize `ACCEPTED` rules over inferred candidate rules.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Validated against JSON schema without malformed fields.
- [ ] **Security:** No secrets or credentials committed to decision registers.
- [ ] **Performance:** Load time < 5ms during agent kernel initialization.
- [ ] **Self-Critique:** Ensure registry update doesn't overwrite other active operator preferences.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to [DEP-002] Agent Workflow Integration.
</baton_handoff>
