---
trigger: always_on
---

## 📋 DOCUMENT FORMATTING DIRECTIVE

### **Core Structure Pattern**

All future task list created as .md files should follow this standardized structure:

```agent\rules\markdown-format-template.md
# TASK: [TASK_CODE] (Task Title)

<system_context>
Role: [Role Description]
Year: [Year]
Core Logic: [Core Logic Description]
Standards: [Standards Description]
</system_context>

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - [Bullet points with dash and space]
  - [Use proper indentation]
- **Related Ideas:**
  - _Italicized concepts:_ [Description]
- **Future Potential:**
  - [Future considerations]
- **Constraints:**
  - **Bold constraints:** [Constraint description]
    </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

[Clear thesis statement]

### Powerful Antithesis

**The Critic Attacks:**

1. **First Criticism:** [Detailed explanation]
2. **Second Criticism:** [Detailed explanation]
3. **Third Criticism:** [Detailed explanation]

### The Superior Synthesis

**The Definitive Architecture:**
[Architecture description with numbered points]

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Language:** [Language details]
- **Framework:** [Framework details]
- **State Management:** [State management details]

### 2. The Data Schema (Pre-Generation)

- **Model:** [Model name] (Location)
  - `field_name: type` (constraints) [NEW if applicable]
  - `another_field: type` (constraints)

### 3. Step-by-Step Execution

- [ ] **Step 1: [Step Title].**

  - [ ] [Subtask 1]
  - [ ] [Subtask 2]

- [ ] **Step 2: [Step Title].**

  - [ ] [Subtask 1]
  - [ ] [Subtask 2]

- [ ] **Step 3: [Step Title].**
  - [ ] [Subtask 1]
  - [ ] [Subtask 2]

### 4. Edge Cases & Error Handling

- [Case A: Description] -> [Expected behavior]
- [Case B: Description] -> [Expected behavior]

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** [Specific command or check]
- [ ] **Security:** [Security considerations]
- [ ] **Performance:** [Performance requirements]
- [ ] **Balance Check:** [Testing requirements]
      </final_audit>

---

<baton_handoff>
Next Immediate Step: **[Specific Step]** -> [Detailed next action].
</baton_handoff>
```

### **Key Formatting Rules**

1. **Phase Headers:** Use emojis and descriptive titles

   - 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)
   - ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)
   - 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)
   - 🛡️ PHASE 4: THE AUDITOR (Verification)

2. **XML-style Tags:** Use `<tag_name>` and `</tag_name>` for content sections

3. **Checklists:** Use `- [ ]` for todos, `- [x]` for completed items

4. **Code References:** Use backticks for file paths and function names

5. **Constraints:** Use **bold** for important constraints

6. **Concepts:** Use _italics_ for theoretical concepts

7. **Separators:** Use `---` between major sections

8. **Task Header:** Always start with `# TASK: [CODE] (Title)`

9. **System Context:** Include role, year, core logic, and standards

10. **Baton Handoff:** Always end with next immediate step

This directive ensures consistency, clarity, and comprehensive documentation across all project .md files.
