<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [DEP-002] Agent Workflow Integration & Task Dispatcher

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** Antigravity slash commands and workflow scripts automate standard developer tasks, reducing cognitive overhead and manual CLI invocations.
- **Related Ideas:** GitHub Actions dispatchers, Makefiles, Justfiles, Antigravity `/workflows`.
- **Future Potential:** Full end-to-end task execution triggered directly from chat UI with automatic branch isolation and receipt generation.
- **Constraints:** Must use standard Markdown workflow format, execute in non-interactive mode, enforce `task-list-template.md`.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Rely on developers remembering CLI parameters to execute `scripts/codex_pipeline_runner.py` manually in terminals.

### Powerful Antithesis
Manual invocation leads to omitted flags, missed verification passes, unformatted output markdown files, and neglected living dossier synchronization.

### The Superior Synthesis
Create `.agent/workflows/codex-pipeline.md` integrating the `/codex-pipeline` slash command. This standardizes execution, automates task generation, enforces test running, and guarantees living dossier updates on every cycle.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** Antigravity Workflow Engine, Python 3.14 CLI
- **Language:** Markdown / Python 3.14
- **State Management:** Git Worktrees, Task Spec Markdown Files

### 2. The Data Schema (Pre-Generation)
```markdown
# Workflow Definition Schema
- command: /codex-pipeline
- description: "Automated 6-stage engineering lifecycle runner"
- parameters: [task_id, task_title, output_dir]
- steps: [Research, Synthesize, Scaffold, Test, Sync]
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Create `.agent/workflows/codex-pipeline.md`.
- [ ] **Step 2: Core Logic.** Define step-by-step workflow instructions invoking `scripts/codex_pipeline_runner.py`.
- [ ] **Step 3: Interface.** Link workflow in `.agent/workflows/README.md` and verify slash command discovery.

### 4. Edge Cases & Error Handling
- **Case A: Missing Task ID argument** -> Prompt user with clear syntax guide and interactive defaults.
- **Case B: Non-zero test exit code** -> Halt workflow, capture stack trace in `debug_output.txt`, and trigger auto-remediation.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Verified workflow markdown syntax and Python argument parsing.
- [ ] **Security:** Workflow only runs local read/write within repository boundaries.
- [ ] **Performance:** Workflow initialization overhead < 50ms.
- [ ] **Self-Critique:** Ensure workflow operates seamlessly across both Windows PowerShell and Linux bash shells.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to [DEP-003] S2 Cognitive Latency & Vision Cone Injection.
</baton_handoff>
