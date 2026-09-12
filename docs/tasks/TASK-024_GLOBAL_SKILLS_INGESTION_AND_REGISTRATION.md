<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: GLOBAL_SKILLS_INGESTION_AND_REGISTRATION

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Antigravity and agentic AI systems employ on-demand skills (progressive disclosure) defined via `SKILL.md` bundles containing prompt directives, executable scripts, and reference documents. Previously, numerous specialized skills existed scattered across repositories in the DevOps workspace (`hermes-agent`, `antigravity-kit`, `AionUi`, `Mem0`, `holaOS`, `codex`, `taste-skill`, `agentmemory`, `THE-NFL-SIM-V2`).
- **Related Ideas:** Model Context Protocol (MCP), dynamic plugin manifests, Unix hierarchy, hierarchical configuration inheritance (`workspace` -> `declared` -> `global` -> `builtin`).
- **Future Potential:** Establishing a comprehensive global skills library in `~/.gemini/config/skills` equips any future project, agentic session, or subagent with immediate access to 384+ specialized tools across AI/ML training, full-stack app building, game development, modding, document automation, finance, and security.
- **Constraints:**
  - Preserve all 11 pre-existing global skills intact without corruption.
  - Ignore ephemeral build caches, `.webpack`, `.repos`, `node_modules`, `venv`, and binary artifacts.
  - Copy entire companion bundles (`scripts/`, `references/`, `templates/`, `assets/`) alongside `SKILL.md`.
  - Validate 100% YAML frontmatter compliance (`name:` and `description:`).
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Directly copy all discovered `SKILL.md` files into `C:\Users\cweir\.gemini\config\skills\<name>\` flatly using a simple filesystem copy script.

### Powerful Antithesis

A naive file copy creates severe failure modes:
1. It copies `SKILL.md` without companion scripts, templates, or references, rendering scripts referenced in the doc broken (`FileNotFoundError`).
2. It inadvertently traverses `.webpack`, `.pnpm`, `t3code`, and nested `node_modules`, ballooning the filesystem with 50,000+ unnecessary files and hitting Windows path length (`MAX_PATH`) locks.
3. Mirror duplicates across repos (`Mem0/skills` vs `hermes-agent/skills`) cause race conditions or partial overwrites.
4. Unescaped YAML syntax in raw skills (such as unquoted colons in `description`) crashes agent frontmatter parsers.

### The Superior Synthesis

Execute an adversarial 4-stage transfer pipeline:
1. **Deduplication & Canonical Scoring**: Scan and filter build artifacts, selecting the most complete source repository for each unique skill name.
2. **Exclusion-Hardened Transfer**: Copy directory trees with an explicit ignore pattern covering `node_modules`, `venv`, `.git`, `.repos`, and cache directories.
3. **Robocopy Mirror Sanitization**: Purge any deep node_modules trees that hit path length locks.
4. **Comprehensive Automated Verification**: Run a full AST/YAML parser against all 394 target directories, confirming valid frontmatter, directory naming, and retention of original global skills.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** Python 3.13 (`os`, `shutil`, `re`, `json`, `yaml`), Windows PowerShell 7, Robocopy.
- **Language:** Python, Markdown, YAML.
- **Target Location:** `C:\Users\cweir\.gemini\config\skills`

### 2. The Data Schema (Pre-Generation)

```yaml
---
name: string (kebab-case, alphanumeric, dashes)
description: string (non-empty summary loaded in progressive disclosure)
allowed-tools: array (optional list of tool capabilities)
---
```

### 3. Step-by-Step Execution

- [x] **Step 1: Scaffolding & Discovery.** Scanned `C:\Users\cweir\OneDrive\Desktop\DevOps` recursively, detecting 651 `SKILL.md` candidates across 12 projects. Filtered build artifacts to identify 384 unique skills.
- [x] **Step 2: Transfer Execution.** Ran `execute_skills_transfer.py` with exclusion patterns to transfer 383 new skills, preserving all 11 existing global skills.
- [x] **Step 3: Edge Case Remediation.** Purged nested node_modules in `digital-gridiron-os` via Robocopy mirror, fixed YAML parsing in `lint-and-validate`, `docs-writer`, and `pr-creator`.
- [x] **Step 4: Full Audit.** Verified all 394 skill directories.

### 4. Edge Cases & Error Handling

- [Case A: Windows MAX_PATH in node_modules] -> [Resolved via Robocopy /MIR purge]
- [Case B: YAML unquoted colon syntax error] -> [Resolved by wrapping in quotes / block scalar]
- [Case C: Name formatting e.g. `here.now`] -> [Sanitized to `here-now`]

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type & Schema Check:** All 394 skills verified with valid `SKILL.md` and readable YAML frontmatter.
- [x] **Integrity:** Zero collisions or corruptions of the original 11 global skills.
- [x] **Completeness:** Companion scripts, references, and templates preserved.
- [x] **Verification Script:** `verify_all_global_skills.py` passed with 0 issues.
</final_audit>

---

<baton_handoff>
Next Immediate Step: All 394 skills are fully active in `C:\Users\cweir\.gemini\config\skills` and available across all workspaces and conversations.
</baton_handoff>
