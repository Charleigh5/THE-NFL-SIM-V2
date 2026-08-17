#!/usr/bin/env python3
"""
Codex Pipeline Runner - THE-NFL-SIM-V2
=======================================
Automates the 6-Stage Cognitive Lifecycle:
1. Research (Scout) -> 2. Synthesize (Architect) -> 3. Write (Engineer)
-> 4. Review (Auditor) -> 5. Critique (Tester) -> 6. Advance (Compounding)

Generates strict task specifications conforming to .agent/rules/task-list-template.md
and updates living dossiers and feature matrices.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

TASK_TEMPLATE = """<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: {task_title}

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** {historical_origins}
- **Related Ideas:** {related_ideas}
- **Future Potential:** {future_potential}
- **Constraints:** {constraints}
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
{primary_thesis}

### Powerful Antithesis
{powerful_antithesis}

### The Superior Synthesis
{superior_synthesis}
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** Python 3.12-3.14+, FastAPI, Pydantic v2, SQLAlchemy 2.0 / React 19, Vite, TypeScript
- **Language:** Strict typing (zero `any`, 100% annotations)
- **State Management:** Zustand, immutable state dataclasses, HMAC-SHA256 deterministic RNG

### 2. The Data Schema (Pre-Generation)
```python
{data_schema}
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** {step_1_scaffolding}
- [ ] **Step 2: Core Logic.** {step_2_core_logic}
- [ ] **Step 3: Interface.** {step_3_interface}

### 4. Edge Cases & Error Handling
- **Edge Case 1:** {edge_case_1}
- **Edge Case 2:** {edge_case_2}
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** No `any` types, pyright static typing verified.
- [ ] **Security:** RLS, JWT, HMAC seed verification, input sanitization checked.
- [ ] **Performance:** Deterministic 60Hz tick budget (<16ms) maintained.
- [ ] **Self-Critique:** {self_critique}
</final_audit>

---

<baton_handoff>
Next Immediate Step: {next_immediate_step}
</baton_handoff>
"""

def generate_task_spec(
    task_id: str,
    task_title: str,
    output_dir: Path,
    **kwargs
) -> Path:
    """Generate a task markdown file following task-list-template.md."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{task_id}_{task_title.lower().replace(' ', '_')}.md"
    file_path = output_dir / filename
    
    content = TASK_TEMPLATE.format(
        task_title=f"[{task_id}] {task_title}",
        historical_origins=kwargs.get("historical_origins", "NFL simulation mechanics and sports physics modeling."),
        related_ideas=kwargs.get("related_ideas", "NextGenStats, nflfastR, EPA/CPOE models, Box2D physics."),
        future_potential=kwargs.get("future_potential", "Real-time 3D telemetry rendering and distributed multi-agent franchise simulation."),
        constraints=kwargs.get("constraints", "Deterministic execution, <16ms tick latency, zero animation dictatorship, strict typing."),
        primary_thesis=kwargs.get("primary_thesis", "Standard statistical lookups with randomized threshold checks."),
        powerful_antithesis=kwargs.get("powerful_antithesis", "Pre-baked outcome trees ignore player cognitive load, turf fatigue, and physics momentum, leading to scripted gameplay."),
        superior_synthesis=kwargs.get("superior_synthesis", "Deterministic 60Hz physics & cognitive latency pipeline combining player biomechanics, turf wear, and AI key recognition."),
        data_schema=kwargs.get("data_schema", "# Defined in domain schemas"),
        step_1_scaffolding=kwargs.get("step_1_scaffolding", f"Create {task_id} module and unit test scaffold."),
        step_2_core_logic=kwargs.get("step_2_core_logic", "Implement core deterministic physics/logic functions."),
        step_3_interface=kwargs.get("step_3_interface", "Expose API endpoint and connect to React frontend UI."),
        edge_case_1=kwargs.get("edge_case_1", "Null/Zero division in probability calculations -> clamp to defined safe minimums."),
        edge_case_2=kwargs.get("edge_case_2", "Extreme weather/turf conditions -> apply graceful saturation bounds."),
        self_critique=kwargs.get("self_critique", "Verify that statistical distributions match real NFL benchmarks (sack rate ~6.5%, YPC ~4.2)."),
        next_immediate_step=kwargs.get("next_immediate_step", f"Run pytest on tests/unit/test_{task_id.lower()}.py and verify calibration.")
    )
    
    file_path.write_text(content, encoding="utf-8")
    print(f"[CODEX PIPELINE] Created task specification: {file_path}")
    return file_path

def main():
    parser = argparse.ArgumentParser(description="Codex Pipeline Task Generator")
    parser.add_argument("--id", required=True, help="Task ID (e.g. GAME-008, GEN-002)")
    parser.add_argument("--title", required=True, help="Task Title")
    parser.add_argument("--output", default="docs/tasks", help="Output directory")
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    generate_task_spec(args.id, args.title, output_dir)

if __name__ == "__main__":
    main()
