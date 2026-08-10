To: cweir45@gmail.com
Subject: Comprehensive Codebase Review Report

# Code Review Report
This report contains a comprehensive review of the codebase for bugs, errors, TypeScript issues, and missing documentation.

## Missing Files and Documentation Issues

Based on repository conventions and best practices, the following structural and documentation issues were identified:

### File/Dir: `docs/architecture`
**Error:** Missing File or Directory. Crucial for system design documentation.
**Solve:**
```bash
# Proposed Fix
Create `mkdir -p docs/architecture` and add initial architectural diagrams.
```

---

### File/Dir: `docs/data`
**Error:** Missing File or Directory. Crucial for data models documentation.
**Solve:**
```bash
# Proposed Fix
Create `mkdir -p docs/data` and document schemas.
```

---

### File/Dir: `AGENTS.md`
**Error:** Missing File or Directory. Required for LLM agent instructions in this repo.
**Solve:**
```bash
# Proposed Fix
Create `AGENTS.md` in the root with development instructions.
```

---

### File/Dir: `scripts/check_docs.py`
**Error:** Missing File or Directory. Missing documentation validation script.
**Solve:**
```bash
# Proposed Fix
Create a Python script to verify all modules have docstrings.
```

---

## Frontend ESLint Issues

## Backend Mypy Issues

### File: `backend/app/services/training/coaching_tree.py`
**Lines of Code:** 126
**Error:** Argument "category" to "CoachSkill" has incompatible type "str"; expected "SkillCategory"  [arg-type]
**Solve:**
```python
# Original Code:
                id=sid,
                name=data["name"],
                category=data["category"],
                max_rank=3,
                description=data["desc"]

# Proposed Fix:
                category=SkillCategory(data["category"]),
```


---

### File: `backend/app/services/training/coaching_tree.py`
**Lines of Code:** 171
**Error:** Need type annotation for "bonuses" (hint: "bonuses: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        Coordinator bonuses stack with Head Coach.
        """
        bonuses = {}
        for coach in staff:
            for skill in coach.skills.values():

# Proposed Fix:
        bonuses: dict[str, float] = {}
```


---

### File: `backend/app/services/society/social_graph.py`
**Lines of Code:** 149
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
                total_rels += 1
                if r.is_positive:
                    positive_rels += r.strength
                elif r.type == RelationshipType.ENEMY:
                    negative_rels += r.strength

# Proposed Fix:
                    positive_rels = int(positive_rels + r.strength)
```


---

### File: `backend/app/services/society/social_graph.py`
**Lines of Code:** 151
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
                    positive_rels += r.strength
                elif r.type == RelationshipType.ENEMY:
                    negative_rels += r.strength

        # Base chemistry from morale

# Proposed Fix:
                    negative_rels = int(negative_rels + r.strength)
```


---

### File: `backend/app/engine/rb_tribes.py`
**Lines of Code:** 145
**Error:** Dict entry 0 has incompatible type "str": "str"; expected "str": "float"  [dict-item]
**Solve:**
```python
# Original Code:

    return {
        "tribe": tribe.value,
        "base_yards": profile.base_yards,
        "std_dev": profile.std_dev,

# Proposed Fix:
    # FIX: Dict entry 0 has incompatible type "str": "str"; expected "str": "float"  [dict-item]
        "tribe": tribe.value,
```


---

### File: `backend/app/engine/rb_tribes.py`
**Lines of Code:** 150
**Error:** Dict entry 5 has incompatible type "str": "str"; expected "str": "float"  [dict-item]
**Solve:**
```python
# Original Code:
        "breakaway_mult": profile.breakaway_multiplier,
        "fumble_mult": profile.fumble_multiplier,
        "description": profile.description
    }

# Proposed Fix:
    # FIX: Dict entry 5 has incompatible type "str": "str"; expected "str": "float"  [dict-item]
        "description": profile.description
```


---

### File: `backend/app/data/special_jerseys.py`
**Lines of Code:** 124
**Error:** Incompatible default for argument "year" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:
# ============================================================================

def get_thanksgiving_jersey(team_abbr: str, year: int = None) -> Dict[str, Any]:
    """
    Get the Thanksgiving jersey for a team.

# Proposed Fix:
    # FIX: Incompatible default for argument "year" (default has type "None", argument has type "int")  [assignment]
def get_thanksgiving_jersey(team_abbr: str, year: int = None) -> Dict[str, Any]:
```


---

### File: `backend/app/data/special_jerseys.py`
**Lines of Code:** 137
**Error:** Incompatible return value type (got "None", expected "dict[str, Any]")  [return-value]
**Solve:**
```python
# Original Code:
    if team_abbr in THANKSGIVING_JERSEYS:
        return THANKSGIVING_JERSEYS[team_abbr]
    return None



# Proposed Fix:
    # FIX: Incompatible return value type (got "None", expected "dict[str, Any]")  [return-value]
    return None
```


---

### File: `backend/app/data/special_jerseys.py`
**Lines of Code:** 148
**Error:** Incompatible return value type (got "object", expected "float")  [return-value]
**Solve:**
```python
# Original Code:
    """Get the extra home field boost for Thanksgiving hosts."""
    if team_abbr in THANKSGIVING_HOSTS:
        return THANKSGIVING_HOSTS[team_abbr]["home_field_boost"]
    return 0.0

# Proposed Fix:
        return float(THANKSGIVING_HOSTS[team_abbr]["home_field_boost"])
```


---

### File: `backend/app/services/validation/calibrator.py`
**Lines of Code:** 94
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
                target.current_value += adjustment
                adjustments[name] = adjustment
                total_error += target.error_pct

            avg_error = total_error / len(self.targets) if self.targets else 0

# Proposed Fix:
                total_error = int(total_error + target.error_pct)
```


---

### File: `backend/app/services/empire/gm_ai.py`
**Lines of Code:** 254
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
                base_value *= min(1.2, 1 + contract_years * 0.05)

            return max(0, base_value)

        return 0

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
            return max(0, base_value)
```


---

### File: `backend/app/services/empire/gm_ai.py`
**Lines of Code:** 289
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
                base -= 2

            return base

        return sorted(prospects, key=score_prospect, reverse=True)

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
            return base
```


---

### File: `backend/app/engine/genesis/biometrics.py`
**Lines of Code:** 314
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
        base = rng.next_float()
        biased = base * (1 - talent_level * 0.5) + talent_level * 0.5
        return low + (high - low) * biased

    # Generate base biometrics

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
        return low + (high - low) * biased
```


---

### File: `backend/app/engine/offensive_line_ai.py`
**Lines of Code:** 34
**Error:** Returning Any from function declared to return "int"  [no-any-return]
**Solve:**
```python
# Original Code:
        """
        if player_id in self.active_debuffs:
            return self.active_debuffs[player_id]["pass_block_modifier"]
        return 0


# Proposed Fix:
    # FIX: Returning Any from function declared to return "int"  [no-any-return]
            return self.active_debuffs[player_id]["pass_block_modifier"]
```


---

### File: `backend/app/engine/venue_effects.py`
**Lines of Code:** 45
**Error:** Unsupported operand types for + ("float" and "object")  [operator]
**Solve:**
```python
# Original Code:
        # Thanksgiving host bonus
        if self.game_type == "THANKSGIVING" and is_thanksgiving_host(self.home_team):
            modifier += THANKSGIVING_HOSTS[self.home_team]["home_field_boost"]

        # Playoff intensity

# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "object")  [operator]
            modifier += THANKSGIVING_HOSTS[self.home_team]["home_field_boost"]
```


---

### File: `backend/app/engine/venue_effects.py`
**Lines of Code:** 115
**Error:** Incompatible types in assignment (expression has type "object", target has type "float")  [assignment]
**Solve:**
```python
# Original Code:
    if home_team in THANKSGIVING_HOSTS:
        host_data = THANKSGIVING_HOSTS[home_team]
        atmosphere["tradition_started"] = host_data["tradition_started"]
        atmosphere["game_slot"] = host_data["game_slot"]


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "object", target has type "float")  [assignment]
        atmosphere["tradition_started"] = host_data["tradition_started"]
```


---

### File: `backend/app/engine/venue_effects.py`
**Lines of Code:** 116
**Error:** Incompatible types in assignment (expression has type "object", target has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        host_data = THANKSGIVING_HOSTS[home_team]
        atmosphere["tradition_started"] = host_data["tradition_started"]
        atmosphere["game_slot"] = host_data["game_slot"]

    return atmosphere

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "object", target has type "float")  [assignment]
        atmosphere["game_slot"] = host_data["game_slot"]
```


---

### File: `backend/app/rpg/traits.py`
**Lines of Code:** 54
**Error:** Incompatible return value type (got "Collection[str]", expected "dict[Any, Any]")  [return-value]
**Solve:**
```python
# Original Code:
            stacklevel=2
        )
        return TraitSystem.TRAITS.get(trait_name, {}).get("effect", {})


# Proposed Fix:
    # FIX: Incompatible return value type (got "Collection[str]", expected "dict[Any, Any]")  [return-value]
        return TraitSystem.TRAITS.get(trait_name, {}).get("effect", {})
```


---

### File: `backend/app/engine/position_physics/running_back.py`
**Lines of Code:** 325
**Error:** Returning Any from function declared to return "bool"  [no-any-return]
**Solve:**
```python
# Original Code:

        roll = rng.next_float() if rng else __import__('random').random()
        return roll < fumble_prob

    def execute_cut_move(

# Proposed Fix:
    # FIX: Returning Any from function declared to return "bool"  [no-any-return]
        return roll < fumble_prob
```


---

### File: `backend/app/engine/position_physics/pass_rush.py`
**Lines of Code:** 174
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
        cumulative = 0
        for move, weight in options:
            cumulative += weight
            if roll <= cumulative:
                return move

# Proposed Fix:
            cumulative = int(cumulative + weight)
```


---

### File: `backend/app/engine/position_physics/offensive_line.py`
**Lines of Code:** 177
**Error:** Need type annotation for "assignments" (hint: "assignments: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
            Dict of blocker_id -> rusher_id assignments
        """
        assignments = {}
        available_rushers = set(r[0] for r in rushers)


# Proposed Fix:
        assignments: dict[str, float] = {}
```


---

### File: `backend/app/engine/position_physics/offensive_line.py`
**Lines of Code:** 185
**Error:** Incompatible types in assignment (expression has type "None", target has type "str")  [assignment]
**Solve:**
```python
# Original Code:
        for blocker_id, blocker_pos in sorted_blockers:
            if not available_rushers:
                assignments[blocker_id] = None
                continue


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "None", target has type "str")  [assignment]
                assignments[blocker_id] = None
```


---

### File: `backend/app/engine/position_physics/offensive_line.py`
**Lines of Code:** 205
**Error:** Incompatible types in assignment (expression has type "None", target has type "str")  [assignment]
**Solve:**
```python
# Original Code:
                available_rushers.remove(best_rusher)
            else:
                assignments[blocker_id] = None

        return assignments

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "None", target has type "str")  [assignment]
                assignments[blocker_id] = None
```


---

### File: `backend/app/engine/position_physics/offensive_line.py`
**Lines of Code:** 207
**Error:** Incompatible return value type (got "dict[str, str]", expected "dict[str, str | None]")  [return-value]
**Solve:**
```python
# Original Code:
                assignments[blocker_id] = None

        return assignments

    def calculate_pocket_contour(

# Proposed Fix:
    # FIX: Incompatible return value type (got "dict[str, str]", expected "dict[str, str | None]")  [return-value]
        return assignments
```


---

### File: `backend/app/engine/position_physics/offensive_line.py`
**Lines of Code:** 267
**Error:** Returning Any from function declared to return "bool"  [no-any-return]
**Solve:**
```python
# Original Code:

        roll = rng.next_float() if rng else __import__('random').random()
        return roll < prob

# Proposed Fix:
    # FIX: Returning Any from function declared to return "bool"  [no-any-return]
        return roll < prob
```


---

### File: `backend/app/services/database/optimizer.py`
**Lines of Code:** 81
**Error:** Incompatible default for argument "pattern" (default has type "None", argument has type "str")  [assignment]
**Solve:**
```python
# Original Code:
        )

    def invalidate(self, pattern: str = None):
        """
        Invalidate cache entries.

# Proposed Fix:
    # FIX: Incompatible default for argument "pattern" (default has type "None", argument has type "str")  [assignment]
    def invalidate(self, pattern: str = None):
```


---

### File: `backend/app/services/database/optimizer.py`
**Lines of Code:** 88
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        """
        if pattern is None:
            self.cache.clear()
        else:
            # Would use pattern matching

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            self.cache.clear()
```


---

### File: `backend/app/services/broadcasting_service.py`
**Lines of Code:** 194
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:
    """

    def __init__(self, style: BroadcastStyle = BroadcastStyle.ESPN, seed: int = None):
        self.style = style
        self.rng = random.Random(seed)

# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, style: BroadcastStyle = BroadcastStyle.ESPN, seed: int = None):
```


---

### File: `backend/app/services/scouting/scout.py`
**Lines of Code:** 194
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        if specialty == ScoutSpecialty.TRENCHES: return attribute in ["run_block", "pass_block", "power_moves"]
        if specialty == ScoutSpecialty.SKILL_POS: return attribute in ["catching", "route_running", "man_coverage"]
        return False

    def format_for_display(self, report: ScoutingReport) -> Dict[str, str]:

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
        return False
```


---

### File: `backend/app/rpg/narrative.py`
**Lines of Code:** 37
**Error:** Incompatible return value type (got "None", expected "dict[Any, Any]")  [return-value]
**Solve:**
```python
# Original Code:
            return random.choice(NarrativeEngine.EVENTS)

        return None

# Proposed Fix:
    # FIX: Incompatible return value type (got "None", expected "dict[Any, Any]")  [return-value]
        return None
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 311
**Error:** Need type annotation for "gains" (hint: "gains: list[<type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        """
        context = context or {}
        gains = []

        # Get base XP awards for this action

# Proposed Fix:
        gains: list[Any] = []
```


---

### File: `backend/app/services/ratings_generator.py`
**Lines of Code:** 42
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
    """
    if value is None:
        return 50  # Default average
    if high == low:
        return 70

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
        return 50  # Default average
```


---

### File: `backend/app/services/ratings_generator.py`
**Lines of Code:** 54
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
    """
    if value is None:
        return 50
    if high == low:
        return 70

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
        return 50
```


---

### File: `backend/app/services/data_sync_service.py`
**Lines of Code:** 31
**Error:** Unused "type: ignore" comment  [unused-ignore]
**Solve:**
```python
# Original Code:
# Check for nflreadpy availability
try:
    import nflreadpy  # type: ignore[import-not-found]
    HAS_NFLVERSE = True
except ImportError:

# Proposed Fix:
    # FIX: Unused "type: ignore" comment  [unused-ignore]
    import nflreadpy  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/data_sync_service.py`
**Lines of Code:** 31
**Error:** Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker  [import-untyped]
**Solve:**
```python
# Original Code:
# Check for nflreadpy availability
try:
    import nflreadpy  # type: ignore[import-not-found]
    HAS_NFLVERSE = True
except ImportError:

# Proposed Fix:
    # FIX: Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker  [import-untyped]
    import nflreadpy  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/data_sync_service.py`
**Lines of Code:** 321
**Error:** Unsupported target for indexed assignment ("object")  [index]
**Solve:**
```python
# Original Code:
            needs_update = self.should_update(source)

            report["sources"][source.value] = {
                "last_updated": last.isoformat() if last else None,
                "update_frequency": config.frequency.value,

# Proposed Fix:
    # FIX: Unsupported target for indexed assignment ("object")  [index]
            report["sources"][source.value] = {
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 141
**Error:** Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
            if re.search(pattern, description_lower):
                return ResearchResult(
                    summary=research["summary"],
                    recommended_approach=research["approach"],
                    code_examples=research.get("examples", []),

# Proposed Fix:
                    summary=str(research["summary"]),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 142
**Error:** Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
                return ResearchResult(
                    summary=research["summary"],
                    recommended_approach=research["approach"],
                    code_examples=research.get("examples", []),
                    complexity=research["complexity"],

# Proposed Fix:
                    recommended_approach=str(research["approach"]),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 143
**Error:** Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  [arg-type]
**Solve:**
```python
# Original Code:
                    summary=research["summary"],
                    recommended_approach=research["approach"],
                    code_examples=research.get("examples", []),
                    complexity=research["complexity"],
                    sources=research.get("sources", []),

# Proposed Fix:
                    code_examples=list(research.get("examples"), []),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 144
**Error:** Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"  [arg-type]
**Solve:**
```python
# Original Code:
                    recommended_approach=research["approach"],
                    code_examples=research.get("examples", []),
                    complexity=research["complexity"],
                    sources=research.get("sources", []),
                    related_docs=[]

# Proposed Fix:
                    complexity=TaskComplexity(research["complexity"]),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 145
**Error:** Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  [arg-type]
**Solve:**
```python
# Original Code:
                    code_examples=research.get("examples", []),
                    complexity=research["complexity"],
                    sources=research.get("sources", []),
                    related_docs=[]
                )

# Proposed Fix:
                    sources=list(research.get("sources"), []),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 151
**Error:** Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
        # Default fallback
        return ResearchResult(
            summary=self.DEFAULT_RESEARCH["summary"],
            recommended_approach=self.DEFAULT_RESEARCH["approach"],
            code_examples=self.DEFAULT_RESEARCH["examples"],

# Proposed Fix:
            summary=str(self.DEFAULT_RESEARCH["summary"]),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 152
**Error:** Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
        return ResearchResult(
            summary=self.DEFAULT_RESEARCH["summary"],
            recommended_approach=self.DEFAULT_RESEARCH["approach"],
            code_examples=self.DEFAULT_RESEARCH["examples"],
            complexity=self.DEFAULT_RESEARCH["complexity"],

# Proposed Fix:
            recommended_approach=str(self.DEFAULT_RESEARCH["approach"]),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 153
**Error:** Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  [arg-type]
**Solve:**
```python
# Original Code:
            summary=self.DEFAULT_RESEARCH["summary"],
            recommended_approach=self.DEFAULT_RESEARCH["approach"],
            code_examples=self.DEFAULT_RESEARCH["examples"],
            complexity=self.DEFAULT_RESEARCH["complexity"],
            sources=self.DEFAULT_RESEARCH["sources"],

# Proposed Fix:
            code_examples=list(self.DEFAULT_RESEARCH["examples"]),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 154
**Error:** Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"  [arg-type]
**Solve:**
```python
# Original Code:
            recommended_approach=self.DEFAULT_RESEARCH["approach"],
            code_examples=self.DEFAULT_RESEARCH["examples"],
            complexity=self.DEFAULT_RESEARCH["complexity"],
            sources=self.DEFAULT_RESEARCH["sources"],
            related_docs=[]

# Proposed Fix:
            complexity=TaskComplexity(self.DEFAULT_RESEARCH["complexity"]),
```


---

### File: `backend/app/services/ai_research_service.py`
**Lines of Code:** 155
**Error:** Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  [arg-type]
**Solve:**
```python
# Original Code:
            code_examples=self.DEFAULT_RESEARCH["examples"],
            complexity=self.DEFAULT_RESEARCH["complexity"],
            sources=self.DEFAULT_RESEARCH["sources"],
            related_docs=[]
        )

# Proposed Fix:
            sources=list(self.DEFAULT_RESEARCH["sources"]),
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 671
**Error:** Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
            if f"{{{pos}}}" in narrative.lower():
                if pos in ["qb", "wr", "te", "rb", "ol", "bc"]:
                    narrative = narrative.replace(f"{{{pos}}}", attacker_name)
                else:
                    narrative = narrative.replace(f"{{{pos}}}", defender_name)

# Proposed Fix:
    # FIX: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
                    narrative = narrative.replace(f"{{{pos}}}", attacker_name)
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 673
**Error:** Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
                    narrative = narrative.replace(f"{{{pos}}}", attacker_name)
                else:
                    narrative = narrative.replace(f"{{{pos}}}", defender_name)

        # Generic replacements

# Proposed Fix:
    # FIX: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
                    narrative = narrative.replace(f"{{{pos}}}", defender_name)
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 676
**Error:** Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

        # Generic replacements
        narrative = narrative.replace("{attacker}", attacker_name)
        narrative = narrative.replace("{defender}", defender_name)


# Proposed Fix:
    # FIX: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
        narrative = narrative.replace("{attacker}", attacker_name)
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 677
**Error:** Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
        # Generic replacements
        narrative = narrative.replace("{attacker}", attacker_name)
        narrative = narrative.replace("{defender}", defender_name)

        return narrative

# Proposed Fix:
    # FIX: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"  [arg-type]
        narrative = narrative.replace("{defender}", defender_name)
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 810
**Error:** Unsupported operand types for + ("object" and "float")  [operator]
**Solve:**
```python
# Original Code:
        if result.outcome in [InteractionOutcome.DOMINANT_WIN, InteractionOutcome.WIN,
                              InteractionOutcome.SLIGHT_WIN]:
            aggregate["total_offense_boost"] += result.winner_boost
        elif result.outcome in [InteractionOutcome.DOMINANT_LOSS, InteractionOutcome.LOSS,
                                InteractionOutcome.SLIGHT_LOSS]:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("object" and "float")  [operator]
            aggregate["total_offense_boost"] += result.winner_boost
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 813
**Error:** Unsupported operand types for + ("object" and "float")  [operator]
**Solve:**
```python
# Original Code:
        elif result.outcome in [InteractionOutcome.DOMINANT_LOSS, InteractionOutcome.LOSS,
                                InteractionOutcome.SLIGHT_LOSS]:
            aggregate["total_defense_boost"] += result.loser_penalty

        aggregate["narratives"].append(result.narrative)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("object" and "float")  [operator]
            aggregate["total_defense_boost"] += result.loser_penalty
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 815
**Error:** "object" has no attribute "append"  [attr-defined]
**Solve:**
```python
# Original Code:
            aggregate["total_defense_boost"] += result.loser_penalty

        aggregate["narratives"].append(result.narrative)
        aggregate["all_events"].append(result.to_dict())


# Proposed Fix:
    # FIX: "object" has no attribute "append"  [attr-defined]
        aggregate["narratives"].append(result.narrative)
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 816
**Error:** "object" has no attribute "append"  [attr-defined]
**Solve:**
```python
# Original Code:

        aggregate["narratives"].append(result.narrative)
        aggregate["all_events"].append(result.to_dict())

        if result.outcome in [InteractionOutcome.DOMINANT_WIN, InteractionOutcome.DOMINANT_LOSS]:

# Proposed Fix:
    # FIX: "object" has no attribute "append"  [attr-defined]
        aggregate["all_events"].append(result.to_dict())
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 819
**Error:** "object" has no attribute "append"  [attr-defined]
**Solve:**
```python
# Original Code:

        if result.outcome in [InteractionOutcome.DOMINANT_WIN, InteractionOutcome.DOMINANT_LOSS]:
            aggregate["dominant_events"].append(result.to_dict())

    return aggregate

# Proposed Fix:
    # FIX: "object" has no attribute "append"  [attr-defined]
            aggregate["dominant_events"].append(result.to_dict())
```


---

### File: `backend/app/services/scouting/draft_board.py`
**Lines of Code:** 59
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
            # Need multiplier
            if p.position in needs:
                score *= 1.15 # 15% boost for need

            # Scheme fit? (Placeholder)

# Proposed Fix:
                score = int(score * 1.15 # 15% boost for need)
```


---

### File: `backend/app/services/training/training_programs.py`
**Lines of Code:** 169
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:
    """

    def __init__(self, season_phase: SeasonPhase = SeasonPhase.REGULAR, seed: int = None):
        self.season_phase = season_phase
        self.phase_config = PHASE_CONFIGS[season_phase]

# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, season_phase: SeasonPhase = SeasonPhase.REGULAR, seed: int = None):
```


---

### File: `backend/app/engine/physics.py`
**Lines of Code:** 55
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:

            # Update Position
            x += vx * dt
            y += vy * dt


# Proposed Fix:
            x = int(x + vx * dt)
```


---

### File: `backend/app/engine/physics.py`
**Lines of Code:** 56
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
            # Update Position
            x += vx * dt
            y += vy * dt

            t += dt

# Proposed Fix:
            y = int(y + vy * dt)
```


---

### File: `backend/app/engine/physics.py`
**Lines of Code:** 58
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
            y += vy * dt

            t += dt
            trajectory.append({"t": round(t, 2), "x": round(x, 2), "y": round(y, 2)})


# Proposed Fix:
            t = int(t + dt)
```


---

### File: `backend/app/engine/defense.py`
**Lines of Code:** 70
**Error:** Returning Any from function declared to return "bool"  [no-any-return]
**Solve:**
```python
# Original Code:
        if in_zone:
            # Reaction check
            return rng.randint(0, 100) < awareness
        return False

# Proposed Fix:
    # FIX: Returning Any from function declared to return "bool"  [no-any-return]
            return rng.randint(0, 100) < awareness
```


---

### File: `backend/app/kernels/society/social_graph.py`
**Lines of Code:** 4
**Error:** Library stubs not installed for "networkx"  [import-untyped]
**Solve:**
```python
# Original Code:
from typing import Dict, List, Tuple
from pydantic import Field
import networkx as nx

class TrustGraph(Component):

# Proposed Fix:
    # FIX: Library stubs not installed for "networkx"  [import-untyped]
import networkx as nx
```


---

### File: `backend/app/kernels/society/social_graph.py`
**Lines of Code:** 20
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
    def get_trust(self, p1: str, p2: str) -> float:
        if self.graph.has_edge(p1, p2):
            return self.graph[p1][p2]['weight']
        return 0.5 # Default neutral


# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
            return self.graph[p1][p2]['weight']
```


---

### File: `backend/app/kernels/hive/weather.py`
**Lines of Code:** 39
**Error:** Missing return statement  [empty-body]
**Solve:**
```python
# Original Code:
        return 0.0

    def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
        """
        Directive 5: Sun Glare.

# Proposed Fix:
    # FIX: Missing return statement  [empty-body]
    def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
```


---

### File: `backend/app/kernels/hive/weather.py`
**Lines of Code:** 63
**Error:** Name "get_ballistic_modifiers" already defined on line 20  [no-redef]
**Solve:**
```python
# Original Code:
            self.temperature_f = 75.0

    def get_ballistic_modifiers(self) -> Tuple[float, float, float]:
        """
        Directive 6: Ballistics Trajectory.

# Proposed Fix:
    # FIX: Name "get_ballistic_modifiers" already defined on line 20  [no-redef]
    def get_ballistic_modifiers(self) -> Tuple[float, float, float]:
```


---

### File: `backend/app/kernels/hive/weather.py`
**Lines of Code:** 78
**Error:** Name "get_visibility_penalty" already defined on line 31  [no-redef]
**Solve:**
```python
# Original Code:
        return (altitude_boost, self.wind_speed_mph * 0.5, weight_multiplier)

    def get_visibility_penalty(self) -> float:
        """
        Directive 12: Snowfall & Fog Obscuration.

# Proposed Fix:
    # FIX: Name "get_visibility_penalty" already defined on line 31  [no-redef]
    def get_visibility_penalty(self) -> float:
```


---

### File: `backend/app/kernels/hive/weather.py`
**Lines of Code:** 91
**Error:** Name "get_sun_glare_vector" already defined on line 39  [no-redef]
**Solve:**
```python
# Original Code:
        return min(0.9, penalty)

    def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
        """
        Directive 5: Sun Glare.

# Proposed Fix:
    # FIX: Name "get_sun_glare_vector" already defined on line 39  [no-redef]
    def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
```


---

### File: `backend/app/kernels/genesis/trauma_center.py`
**Lines of Code:** 21
**Error:** Name "AnatomyModel" is not defined  [name-defined]
**Solve:**
```python
# Original Code:
        return []

    def administer_shot(self, anatomy: 'AnatomyModel'):
        """
        Directive 9: The Shot.

# Proposed Fix:
    # FIX: Name "AnatomyModel" is not defined  [name-defined]
    def administer_shot(self, anatomy: 'AnatomyModel'):
```


---

### File: `backend/app/kernels/empire/econ_dynamics.py`
**Lines of Code:** 11
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
        # Accelerate all remaining signing bonus
        bonus_per_year = contract.get("signing_bonus", 0) / contract.get("length", 1)
        return bonus_per_year * years_remaining

class MarketInflator(Component):

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
        return bonus_per_year * years_remaining
```


---

### File: `backend/app/kernels/cortex/coverage_net.py`
**Lines of Code:** 29
**Error:** Incompatible return value type (got "Any | None", expected "str")  [return-value]
**Solve:**
```python
# Original Code:
                closest_defender = defender['id']

        return closest_defender

    def identify_matchups(self, receivers: List[Dict], defenders: List[Dict]) -> Dict[str, str]:

# Proposed Fix:
        return str(closest_defender)
```


---

### File: `backend/app/kernels/cortex/behavior_tree.py`
**Lines of Code:** 16
**Error:** Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
    def __init__(self, root_node: BehaviorNode):
        self.root = root_node
        self.context = {}

    def update(self):

# Proposed Fix:
        self.context: dict[str, float] = {}
```


---

### File: `backend/app/kernels/cortex/behavior_tree.py`
**Lines of Code:** 29
**Error:** Returning Any from function declared to return "NodeStatus"  [no-any-return]
**Solve:**
```python
# Original Code:
            status = child.tick(context)
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE


# Proposed Fix:
    # FIX: Returning Any from function declared to return "NodeStatus"  [no-any-return]
                return status
```


---

### File: `backend/app/kernels/cortex/behavior_tree.py`
**Lines of Code:** 40
**Error:** Returning Any from function declared to return "NodeStatus"  [no-any-return]
**Solve:**
```python
# Original Code:
            status = child.tick(context)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS

# Proposed Fix:
    # FIX: Returning Any from function declared to return "NodeStatus"  [no-any-return]
                return status
```


---

### File: `backend/app/kernels/core/sim_engine.py`
**Lines of Code:** 17
**Error:** Incompatible return value type (got "Component | None", expected "Component")  [return-value]
**Solve:**
```python
# Original Code:

    def get_component(self, entity_id: str, comp_type: str) -> Component:
        return self.components.get(comp_type, {}).get(entity_id)

class SimEngine:

# Proposed Fix:
    # FIX: Incompatible return value type (got "Component | None", expected "Component")  [return-value]
        return self.components.get(comp_type, {}).get(entity_id)
```


---

### File: `backend/app/kernels/core/sim_engine.py`
**Lines of Code:** 25
**Error:** Name "PhysicsKernel" is not defined  [name-defined]
**Solve:**
```python
# Original Code:

    # Directive 9: Decoupled Physics/AI Kernels
    physics_kernel: 'PhysicsKernel' = None
    ai_kernel: 'AIKernel' = None


# Proposed Fix:
    # FIX: Name "PhysicsKernel" is not defined  [name-defined]
    physics_kernel: 'PhysicsKernel' = None
```


---

### File: `backend/app/kernels/core/sim_engine.py`
**Lines of Code:** 26
**Error:** Name "AIKernel" is not defined  [name-defined]
**Solve:**
```python
# Original Code:
    # Directive 9: Decoupled Physics/AI Kernels
    physics_kernel: 'PhysicsKernel' = None
    ai_kernel: 'AIKernel' = None

    def run_loop(self, duration_seconds: float):

# Proposed Fix:
    # FIX: Name "AIKernel" is not defined  [name-defined]
    ai_kernel: 'AIKernel' = None
```


---

### File: `backend/app/orchestrator/kernels/genesis_kernel.py`
**Lines of Code:** 30
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
        state = self.player_states[player_id]["fatigue"]
        state.update_fatigue(exertion, temperature)
        return state.lactic_acid

    def get_current_fatigue(self, player_id: int) -> float:

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
        return state.lactic_acid
```


---

### File: `backend/app/orchestrator/kernels/genesis_kernel.py`
**Lines of Code:** 41
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:

        state = self.player_states[player_id]["fatigue"]
        return state.lactic_acid

    def check_injury_risk(self, player_id: int, impact_force: float, body_part: str) -> Dict[str, Any]:

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
        return state.lactic_acid
```


---

### File: `backend/app/services/playbook/clock_management.py`
**Lines of Code:** 240
**Error:** "GameSituation" has no attribute "yards_to_goal"  [attr-defined]
**Solve:**
```python
# Original Code:
        if timeouts_remaining > 0 and urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]:
            # In FG range with ~20 seconds, save for potential ice or FG setup
            if situation.yards_to_goal <= 35 and situation.time_remaining < 25:
                context.timeout_recommended = False  # Save for FG
            elif situation.time_remaining < 40 and situation.down >= 2:

# Proposed Fix:
    # FIX: "GameSituation" has no attribute "yards_to_goal"  [attr-defined]
            if situation.yards_to_goal <= 35 and situation.time_remaining < 25:
```


---

### File: `backend/app/services/issue_logger.py`
**Lines of Code:** 42
**Error:** Item "None" of "datetime | None" has no attribute "strftime"  [union-attr]
**Solve:**
```python
# Original Code:
    Context7 Best Practice: Pure function for formatting.
    """
    timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    page_info = f" ({entry.page})" if entry.page else ""


# Proposed Fix:
    # FIX: Item "None" of "datetime | None" has no attribute "strftime"  [union-attr]
    timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
```


---

### File: `backend/app/services/issue_logger.py`
**Lines of Code:** 109
**Error:** Library stubs not installed for "aiofiles"  [import-untyped]
**Solve:**
```python
# Original Code:
        """
        try:
            import aiofiles

            self._ensure_file_header()

# Proposed Fix:
    # FIX: Library stubs not installed for "aiofiles"  [import-untyped]
            import aiofiles
```


---

### File: `backend/app/engine/core/enhanced_event_bus.py`
**Lines of Code:** 249
**Error:** Argument 1 to "create_task" of "AbstractEventLoop" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"  [arg-type]
**Solve:**
```python
# Original Code:
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(reg.handler(event))
                    except RuntimeError:
                        continue

# Proposed Fix:
    # FIX: Argument 1 to "create_task" of "AbstractEventLoop" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"  [arg-type]
                        loop.create_task(reg.handler(event))
```


---

### File: `backend/app/engine/core/enhanced_event_bus.py`
**Lines of Code:** 290
**Error:** Need type annotation for "task"  [var-annotated]
**Solve:**
```python
# Original Code:
            try:
                if reg.is_async:
                    task = asyncio.create_task(reg.handler(event))
                    tasks.append(task)
                else:

# Proposed Fix:
                    task: Any = asyncio.create_task(reg.handler(event))
```


---

### File: `backend/app/engine/core/enhanced_event_bus.py`
**Lines of Code:** 290
**Error:** Argument 1 to "create_task" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"  [arg-type]
**Solve:**
```python
# Original Code:
            try:
                if reg.is_async:
                    task = asyncio.create_task(reg.handler(event))
                    tasks.append(task)
                else:

# Proposed Fix:
    # FIX: Argument 1 to "create_task" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"  [arg-type]
                    task = asyncio.create_task(reg.handler(event))
```


---

### File: `backend/app/models/base.py`
**Lines of Code:** 7
**Error:** Cannot override class variable (previously declared on base class "DeclarativeBase") with instance variable  [misc]
**Solve:**
```python
# Original Code:
    """Base class for all database models."""
    id: Any
    __name__: str

    # Generate __tablename__ automatically

# Proposed Fix:
    # FIX: Cannot override class variable (previously declared on base class "DeclarativeBase") with instance variable  [misc]
    __name__: str
```


---

### File: `backend/app/models/trait.py`
**Lines of Code:** 63
**Error:** Name "Player" is not defined  [name-defined]
**Solve:**
```python
# Original Code:

    # Relationships
    player: Mapped["Player"] = relationship(back_populates="player_traits")
    trait: Mapped["Trait"] = relationship(back_populates="players")


# Proposed Fix:
    # FIX: Name "Player" is not defined  [name-defined]
    player: Mapped["Player"] = relationship(back_populates="player_traits")
```


---

### File: `backend/app/models/trade_offer.py`
**Lines of Code:** 45
**Error:** Need type annotation for "status"  [var-annotated]
**Solve:**
```python
# Original Code:

    # Status
    status = Column(
        Enum(TradeOfferStatus),
        default=TradeOfferStatus.PENDING,

# Proposed Fix:
    status: Any = Column(
```


---

### File: `backend/app/models/trade_offer.py`
**Lines of Code:** 82
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        """Check if the offer has expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            return False
```


---

### File: `backend/app/models/trade_offer.py`
**Lines of Code:** 83
**Error:** Incompatible return value type (got "ColumnElement[bool]", expected "bool")  [return-value]
**Solve:**
```python
# Original Code:
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

# Proposed Fix:
        return bool(datetime.utcnow() > self.expires_at)
```


---

### File: `backend/app/models/season.py`
**Lines of Code:** 26
**Error:** Need type annotation for "status"  [var-annotated]
**Solve:**
```python
# Original Code:
    current_week = Column(Integer, default=1)
    is_active = Column(Boolean, default=False, index=True)
    status = Column(SQLEnum(SeasonStatus), default=SeasonStatus.REGULAR_SEASON, nullable=False)

    # Configuration

# Proposed Fix:
    status: Any = Column(SQLEnum(SeasonStatus), default=SeasonStatus.REGULAR_SEASON, nullable=False)
```


---

### File: `backend/app/models/playoff.py`
**Lines of Code:** 27
**Error:** Need type annotation for "round"  [var-annotated]
**Solve:**
```python
# Original Code:

    # Bracket Info
    round = Column(SQLEnum(PlayoffRound), nullable=False)
    conference = Column(SQLEnum(PlayoffConference), nullable=False)
    matchup_code = Column(String, nullable=False) # e.g., "NFC_WC_1", "SB"

# Proposed Fix:
    round: Any = Column(SQLEnum(PlayoffRound), nullable=False)
```


---

### File: `backend/app/models/playoff.py`
**Lines of Code:** 28
**Error:** Need type annotation for "conference"  [var-annotated]
**Solve:**
```python
# Original Code:
    # Bracket Info
    round = Column(SQLEnum(PlayoffRound), nullable=False)
    conference = Column(SQLEnum(PlayoffConference), nullable=False)
    matchup_code = Column(String, nullable=False) # e.g., "NFC_WC_1", "SB"


# Proposed Fix:
    conference: Any = Column(SQLEnum(PlayoffConference), nullable=False)
```


---

### File: `backend/app/models/player_game_starts.py`
**Lines of Code:** 27
**Error:** Name "Player" is not defined  [name-defined]
**Solve:**
```python
# Original Code:

    # Relationships
    player: Mapped["Player"] = relationship(back_populates="game_starts")
    game: Mapped["Game"] = relationship(back_populates="player_starts")


# Proposed Fix:
    # FIX: Name "Player" is not defined  [name-defined]
    player: Mapped["Player"] = relationship(back_populates="game_starts")
```


---

### File: `backend/app/models/player_game_starts.py`
**Lines of Code:** 28
**Error:** Name "Game" is not defined  [name-defined]
**Solve:**
```python
# Original Code:
    # Relationships
    player: Mapped["Player"] = relationship(back_populates="game_starts")
    game: Mapped["Game"] = relationship(back_populates="player_starts")

    __table_args__ = (

# Proposed Fix:
    # FIX: Name "Game" is not defined  [name-defined]
    game: Mapped["Game"] = relationship(back_populates="player_starts")
```


---

### File: `backend/app/models/game.py`
**Lines of Code:** 33
**Error:** Need type annotation for "game_type"  [var-annotated]
**Solve:**
```python
# Original Code:
    is_playoff = Column(Boolean, default=False)
    is_preseason = Column(Boolean, default=False)  # Flag for preseason games
    game_type = Column(SQLEnum(GameType), default=GameType.REGULAR, nullable=False)

    # Teams

# Proposed Fix:
    game_type: Any = Column(SQLEnum(GameType), default=GameType.REGULAR, nullable=False)
```


---

### File: `backend/app/models/coach.py`
**Lines of Code:** 21
**Error:** Need type annotation for "tier"  [var-annotated]
**Solve:**
```python
# Original Code:

    # Tier system
    tier = Column(SQLEnum(CoachTier), default=CoachTier.DEVELOPING, nullable=False)

    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)

# Proposed Fix:
    tier: Any = Column(SQLEnum(CoachTier), default=CoachTier.DEVELOPING, nullable=False)
```


---

### File: `backend/app/engine/weather_effects.py`
**Lines of Code:** 35
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        if self.weather.wind_speed and self.weather.wind_speed > 10:
            wind_over = self.weather.wind_speed - 10
            accuracy -= wind_over * 0.008   # -0.8% per mph over 10 (calibrated)
            distance -= wind_over * 0.005   # -0.5% per mph over 10


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
            accuracy -= wind_over * 0.008   # -0.8% per mph over 10 (calibrated)
```


---

### File: `backend/app/engine/weather_effects.py`
**Lines of Code:** 36
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
            wind_over = self.weather.wind_speed - 10
            accuracy -= wind_over * 0.008   # -0.8% per mph over 10 (calibrated)
            distance -= wind_over * 0.005   # -0.5% per mph over 10

        # Precipitation (NFL: ~12% reduction in rain)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
            distance -= wind_over * 0.005   # -0.5% per mph over 10
```


---

### File: `backend/app/engine/weather_effects.py`
**Lines of Code:** 66
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        if self.weather.wind_speed and self.weather.wind_speed > 5:
            wind_over = self.weather.wind_speed - 5
            accuracy -= wind_over * 0.015   # -1.5% per mph over 5
            distance -= wind_over * 0.008   # -0.8% per mph over 5


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
            accuracy -= wind_over * 0.015   # -1.5% per mph over 5
```


---

### File: `backend/app/engine/weather_effects.py`
**Lines of Code:** 67
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
            wind_over = self.weather.wind_speed - 5
            accuracy -= wind_over * 0.015   # -1.5% per mph over 5
            distance -= wind_over * 0.008   # -0.8% per mph over 5

        # Temperature (Dense cold air reduces distance)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
            distance -= wind_over * 0.008   # -0.8% per mph over 5
```


---

### File: `backend/app/engine/weather_effects.py`
**Lines of Code:** 71
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        # Temperature (Dense cold air reduces distance)
        if self.weather.temperature and self.weather.temperature < 40:
            distance -= (40 - self.weather.temperature) * 0.004  # -0.4% per degree under 40

        return max(0.5, accuracy), max(0.6, distance)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
            distance -= (40 - self.weather.temperature) * 0.004  # -0.4% per degree under 40
```


---

### File: `backend/app/engine/weather_effects.py`
**Lines of Code:** 106
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        # Heat
        if self.weather.temperature and self.weather.temperature > 85:
            multiplier += (self.weather.temperature - 85) * 0.02

        # Humidity

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
            multiplier += (self.weather.temperature - 85) * 0.02
```


---

### File: `backend/app/engine/weather_effects.py`
**Lines of Code:** 110
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        # Humidity
        if self.weather.humidity and self.weather.humidity > 0.7:
            multiplier += (self.weather.humidity - 0.7) * 0.5

        # Heavy field

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")  [assignment]
            multiplier += (self.weather.humidity - 0.7) * 0.5
```


---

### File: `backend/app/services/elo_service.py`
**Lines of Code:** 84
**Error:** Incompatible default for argument "k_factor" (default has type "None", argument has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        point_diff: int,
        is_tie: bool = False,
        k_factor: float = None,
    ) -> tuple[float, float]:
        """

# Proposed Fix:
    # FIX: Incompatible default for argument "k_factor" (default has type "None", argument has type "float")  [assignment]
        k_factor: float = None,
```


---

### File: `backend/app/services/elo_service.py`
**Lines of Code:** 152
**Error:** Argument "winner_elo" to "update_ratings" of "EloService" has incompatible type "Column[float] | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:

        new_winner_elo, new_loser_elo = cls.update_ratings(
            winner_elo=winner.elo_rating or 1500.0,
            loser_elo=loser.elo_rating or 1500.0,
            point_diff=abs(point_diff),

# Proposed Fix:
            winner_elo=float(winner.elo_rating) or 1500.0,
```


---

### File: `backend/app/services/elo_service.py`
**Lines of Code:** 153
**Error:** Argument "loser_elo" to "update_ratings" of "EloService" has incompatible type "Column[float] | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
        new_winner_elo, new_loser_elo = cls.update_ratings(
            winner_elo=winner.elo_rating or 1500.0,
            loser_elo=loser.elo_rating or 1500.0,
            point_diff=abs(point_diff),
            is_tie=is_tie,

# Proposed Fix:
            loser_elo=float(loser.elo_rating) or 1500.0,
```


---

### File: `backend/app/services/elo_service.py`
**Lines of Code:** 159
**Error:** Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
**Solve:**
```python
# Original Code:

        # Update the team objects
        winner.elo_rating = new_winner_elo
        loser.elo_rating = new_loser_elo


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
        winner.elo_rating = new_winner_elo
```


---

### File: `backend/app/services/elo_service.py`
**Lines of Code:** 160
**Error:** Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
**Solve:**
```python
# Original Code:
        # Update the team objects
        winner.elo_rating = new_winner_elo
        loser.elo_rating = new_loser_elo

        # Commit changes

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
        loser.elo_rating = new_loser_elo
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 28
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
TEAM_SCOUTS: List[ScoutData] = [
    # AFC EAST
    ScoutData("BUF", "Marcus Williamson", Region.EAST, ScoutBias.ANALYTICS, None, 75, 70, 65),
    ScoutData("BUF", "Tom Polley", Region.MIDWEST, ScoutBias.OLD_SCHOOL, "OL", 80, 60, 70),
    ScoutData("BUF", "Derek Sharpley", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 60),

# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("BUF", "Marcus Williamson", Region.EAST, ScoutBias.ANALYTICS, None, 75, 70, 65),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 30
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    ScoutData("BUF", "Marcus Williamson", Region.EAST, ScoutBias.ANALYTICS, None, 75, 70, 65),
    ScoutData("BUF", "Tom Polley", Region.MIDWEST, ScoutBias.OLD_SCHOOL, "OL", 80, 60, 70),
    ScoutData("BUF", "Derek Sharpley", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 60),

    ScoutData("MIA", "Carlos Diaz", Region.SOUTH, ScoutBias.RAS_LOVER, "WR", 85, 65, 75),

# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("BUF", "Derek Sharpley", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 60),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 33
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("MIA", "Carlos Diaz", Region.SOUTH, ScoutBias.RAS_LOVER, "WR", 85, 65, 75),
    ScoutData("MIA", "Frank Johnson", Region.NATIONAL, ScoutBias.NEUTRAL, None, 72, 78, 68),
    ScoutData("MIA", "David Chen", Region.WEST, ScoutBias.ANALYTICS, "DB", 78, 70, 65),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("MIA", "Frank Johnson", Region.NATIONAL, ScoutBias.NEUTRAL, None, 72, 78, 68),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 36
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    ScoutData("MIA", "David Chen", Region.WEST, ScoutBias.ANALYTICS, "DB", 78, 70, 65),

    ScoutData("NE", "Bill Langford", Region.EAST, ScoutBias.CHARACTER, None, 88, 55, 85),
    ScoutData("NE", "James McCarthy", Region.NATIONAL, ScoutBias.TECHNICIAN, "LB", 82, 68, 78),
    ScoutData("NE", "Robert Hall", Region.SOUTH, ScoutBias.OLD_SCHOOL, "OL", 75, 72, 70),

# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("NE", "Bill Langford", Region.EAST, ScoutBias.CHARACTER, None, 88, 55, 85),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 41
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("NYJ", "Mike Tannenbaum Jr", Region.EAST, ScoutBias.ANALYTICS, "QB", 80, 70, 72),
    ScoutData("NYJ", "Sam Decker", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 65),
    ScoutData("NYJ", "Chris Patterson", Region.MIDWEST, ScoutBias.RAS_LOVER, "DL", 76, 68, 68),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("NYJ", "Sam Decker", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 65),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 46
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    # AFC NORTH
    ScoutData("BAL", "Ozzie Newsome III", Region.EAST, ScoutBias.OLD_SCHOOL, "DL", 90, 60, 88),
    ScoutData("BAL", "Eric DeCosta Jr", Region.SOUTH, ScoutBias.ANALYTICS, None, 85, 72, 82),
    ScoutData("BAL", "Keith Williams", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 75),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("BAL", "Eric DeCosta Jr", Region.SOUTH, ScoutBias.ANALYTICS, None, 85, 72, 82),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 47
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    ScoutData("BAL", "Ozzie Newsome III", Region.EAST, ScoutBias.OLD_SCHOOL, "DL", 90, 60, 88),
    ScoutData("BAL", "Eric DeCosta Jr", Region.SOUTH, ScoutBias.ANALYTICS, None, 85, 72, 82),
    ScoutData("BAL", "Keith Williams", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 75),

    ScoutData("CIN", "Duke Tobin II", Region.MIDWEST, ScoutBias.TECHNICIAN, "WR", 82, 68, 75),

# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("BAL", "Keith Williams", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 75),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 50
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("CIN", "Duke Tobin II", Region.MIDWEST, ScoutBias.TECHNICIAN, "WR", 82, 68, 75),
    ScoutData("CIN", "Paul Brown IV", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
    ScoutData("CIN", "Marcus King", Region.SOUTH, ScoutBias.RAS_LOVER, "RB", 78, 70, 68),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("CIN", "Paul Brown IV", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 54
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("CLE", "Andrew Berry II", Region.MIDWEST, ScoutBias.ANALYTICS, "DB", 88, 75, 80),
    ScoutData("CLE", "Kevin Stefanski Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 72),
    ScoutData("CLE", "Tony Fields", Region.SOUTH, ScoutBias.OLD_SCHOOL, "OL", 80, 65, 75),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("CLE", "Kevin Stefanski Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 72),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 58
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("PIT", "Kevin Colbert III", Region.EAST, ScoutBias.CHARACTER, "LB", 85, 60, 85),
    ScoutData("PIT", "Omar Khan Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 78),
    ScoutData("PIT", "Mike Mularkey", Region.MIDWEST, ScoutBias.OLD_SCHOOL, "OL", 76, 68, 72),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("PIT", "Omar Khan Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 78),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 63
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    # AFC SOUTH
    ScoutData("HOU", "Nick Caserio Jr", Region.SOUTH, ScoutBias.ANALYTICS, "WR", 82, 75, 78),
    ScoutData("HOU", "Devon Still", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 70),
    ScoutData("HOU", "Marcus Peters", Region.WEST, ScoutBias.RAS_LOVER, "DB", 80, 68, 72),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("HOU", "Devon Still", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 70),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 67
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("IND", "Chris Ballard II", Region.MIDWEST, ScoutBias.CHARACTER, "OL", 85, 65, 80),
    ScoutData("IND", "Ed Dodds Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 75),
    ScoutData("IND", "Sam Houston", Region.SOUTH, ScoutBias.TECHNICIAN, "QB", 78, 70, 72),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("IND", "Ed Dodds Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 75),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 71
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("JAX", "Trent Baalke III", Region.SOUTH, ScoutBias.RAS_LOVER, "DL", 78, 70, 70),
    ScoutData("JAX", "Tony Khan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 75, 75, 72),
    ScoutData("JAX", "Marcus Allen", Region.WEST, ScoutBias.OLD_SCHOOL, "RB", 76, 68, 68),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("JAX", "Tony Khan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 75, 75, 72),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 76
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    ScoutData("TEN", "Ran Carthon Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "OL", 80, 65, 75),
    ScoutData("TEN", "Mike Vrabel Jr", Region.NATIONAL, ScoutBias.CHARACTER, "LB", 82, 68, 78),
    ScoutData("TEN", "David Caldwell", Region.EAST, ScoutBias.NEUTRAL, None, 75, 75, 70),

    # AFC WEST

# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("TEN", "David Caldwell", Region.EAST, ScoutBias.NEUTRAL, None, 75, 75, 70),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 80
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    # AFC WEST
    ScoutData("DEN", "George Paton Jr", Region.WEST, ScoutBias.ANALYTICS, "QB", 82, 72, 78),
    ScoutData("DEN", "John Elway III", Region.NATIONAL, ScoutBias.CHARACTER, None, 78, 68, 82),
    ScoutData("DEN", "Marcus Thompson", Region.MIDWEST, ScoutBias.RAS_LOVER, "WR", 76, 70, 70),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("DEN", "John Elway III", Region.NATIONAL, ScoutBias.CHARACTER, None, 78, 68, 82),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 84
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("KC", "Brett Veach Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "WR", 90, 75, 88),
    ScoutData("KC", "Clark Hunt III", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 80),
    ScoutData("KC", "Deron Cherry Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "DB", 82, 68, 78),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("KC", "Clark Hunt III", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 80),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 92
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("LAC", "Tom Telesco Jr", Region.WEST, ScoutBias.ANALYTICS, "OL", 82, 72, 78),
    ScoutData("LAC", "John Spanos", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 72),
    ScoutData("LAC", "Eric Weddle Jr", Region.SOUTH, ScoutBias.TECHNICIAN, "DB", 80, 68, 75),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("LAC", "John Spanos", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 72),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 97
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    # NFC EAST
    ScoutData("DAL", "Will McClay Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "DL", 88, 65, 85),
    ScoutData("DAL", "Jerry Jones IV", Region.NATIONAL, ScoutBias.RAS_LOVER, None, 70, 75, 78),
    ScoutData("DAL", "Tony Romo Jr", Region.MIDWEST, ScoutBias.TECHNICIAN, "QB", 82, 70, 80),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("DAL", "Jerry Jones IV", Region.NATIONAL, ScoutBias.RAS_LOVER, None, 70, 75, 78),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 101
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("NYG", "Joe Schoen Jr", Region.EAST, ScoutBias.ANALYTICS, "OL", 82, 72, 78),
    ScoutData("NYG", "Brian Daboll Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 75, 75),
    ScoutData("NYG", "Chris Mara", Region.SOUTH, ScoutBias.CHARACTER, "LB", 76, 68, 72),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("NYG", "Brian Daboll Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 75, 75),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 105
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("PHI", "Howie Roseman Jr", Region.EAST, ScoutBias.ANALYTICS, "DL", 90, 78, 88),
    ScoutData("PHI", "Nick Sirianni Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
    ScoutData("PHI", "Brian Dawkins Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "DB", 82, 68, 78),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("PHI", "Nick Sirianni Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 109
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("WAS", "Martin Mayhew Jr", Region.EAST, ScoutBias.CHARACTER, "WR", 78, 70, 72),
    ScoutData("WAS", "Adam Peters Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 80, 75, 75),
    ScoutData("WAS", "Dan Quinn Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "LB", 76, 68, 70),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("WAS", "Adam Peters Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 80, 75, 75),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 118
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("DET", "Brad Holmes Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "DL", 88, 78, 85),
    ScoutData("DET", "Dan Campbell Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 72, 82),
    ScoutData("DET", "Barry Sanders Jr", Region.SOUTH, ScoutBias.RAS_LOVER, "RB", 85, 70, 80),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("DET", "Dan Campbell Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 72, 82),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 122
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("GB", "Brian Gutekunst Jr", Region.MIDWEST, ScoutBias.TECHNICIAN, "WR", 85, 72, 82),
    ScoutData("GB", "Matt LaFleur Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
    ScoutData("GB", "Aaron Rodgers Jr", Region.WEST, ScoutBias.ANALYTICS, "QB", 78, 68, 85),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("GB", "Matt LaFleur Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 126
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("MIN", "Kwesi Adofo-Mensah Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "DB", 85, 78, 80),
    ScoutData("MIN", "Kevin O'Connell Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
    ScoutData("MIN", "Randy Moss Jr", Region.SOUTH, ScoutBias.RAS_LOVER, "WR", 82, 70, 82),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("MIN", "Kevin O'Connell Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 135
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("CAR", "Dan Morgan Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "LB", 80, 68, 75),
    ScoutData("CAR", "Dave Canales Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
    ScoutData("CAR", "Luke Kuechly Jr", Region.EAST, ScoutBias.TECHNICIAN, "LB", 85, 70, 80),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("CAR", "Dave Canales Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 139
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("NO", "Mickey Loomis Jr", Region.SOUTH, ScoutBias.CHARACTER, "OL", 82, 68, 78),
    ScoutData("NO", "Dennis Allen Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 75),
    ScoutData("NO", "Drew Brees Jr", Region.MIDWEST, ScoutBias.TECHNICIAN, "QB", 85, 70, 85),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("NO", "Dennis Allen Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 75),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 152
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("LAR", "Les Snead Jr", Region.WEST, ScoutBias.ANALYTICS, "OL", 85, 78, 82),
    ScoutData("LAR", "Sean McVay Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
    ScoutData("LAR", "Aaron Donald Jr", Region.MIDWEST, ScoutBias.OLD_SCHOOL, "DL", 82, 68, 88),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("LAR", "Sean McVay Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 156
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("SF", "John Lynch Jr", Region.WEST, ScoutBias.CHARACTER, "DB", 88, 72, 88),
    ScoutData("SF", "Kyle Shanahan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 85, 78, 85),
    ScoutData("SF", "Jerry Rice Jr", Region.SOUTH, ScoutBias.TECHNICIAN, "WR", 82, 68, 88),


# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("SF", "Kyle Shanahan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 85, 78, 85),
```


---

### File: `backend/app/data/scouts.py`
**Lines of Code:** 160
**Error:** Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:

    ScoutData("SEA", "John Schneider Jr", Region.WEST, ScoutBias.RAS_LOVER, "DL", 85, 75, 82),
    ScoutData("SEA", "Pete Carroll Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 70, 85),
    ScoutData("SEA", "Russell Wilson Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "QB", 78, 72, 78),
]

# Proposed Fix:
    # FIX: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  [arg-type]
    ScoutData("SEA", "Pete Carroll Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 70, 85),
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 73
**Error:** Name "Team" is not defined  [name-defined]
**Solve:**
```python
# Original Code:
    # Team Relationship
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("team.id"), nullable=True, index=True)
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="players")

    # --- RPG Attributes (Proxied to PlayerAttributes) ---

# Proposed Fix:
    # FIX: Name "Team" is not defined  [name-defined]
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="players")
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 79
**Error:** Name "speed" already defined on line 76  [no-redef]
**Solve:**
```python
# Original Code:
    def speed(self) -> int:
        return self.attributes.speed if self.attributes else 50
    @speed.setter
    def speed(self, value):
        if self.attributes: self.attributes.speed = value

# Proposed Fix:
    # FIX: Name "speed" already defined on line 76  [no-redef]
    @speed.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 86
**Error:** Name "acceleration" already defined on line 83  [no-redef]
**Solve:**
```python
# Original Code:
    def acceleration(self) -> int:
        return self.attributes.acceleration if self.attributes else 50
    @acceleration.setter
    def acceleration(self, value):
        if self.attributes: self.attributes.acceleration = value

# Proposed Fix:
    # FIX: Name "acceleration" already defined on line 83  [no-redef]
    @acceleration.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 93
**Error:** Name "strength" already defined on line 90  [no-redef]
**Solve:**
```python
# Original Code:
    def strength(self) -> int:
        return self.attributes.strength if self.attributes else 50
    @strength.setter
    def strength(self, value):
        if self.attributes: self.attributes.strength = value

# Proposed Fix:
    # FIX: Name "strength" already defined on line 90  [no-redef]
    @strength.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 100
**Error:** Name "agility" already defined on line 97  [no-redef]
**Solve:**
```python
# Original Code:
    def agility(self) -> int:
        return self.attributes.agility if self.attributes else 50
    @agility.setter
    def agility(self, value):
        if self.attributes: self.attributes.agility = value

# Proposed Fix:
    # FIX: Name "agility" already defined on line 97  [no-redef]
    @agility.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 107
**Error:** Name "awareness" already defined on line 104  [no-redef]
**Solve:**
```python
# Original Code:
    def awareness(self) -> int:
        return self.attributes.awareness if self.attributes else 50
    @awareness.setter
    def awareness(self, value):
        if self.attributes: self.attributes.awareness = value

# Proposed Fix:
    # FIX: Name "awareness" already defined on line 104  [no-redef]
    @awareness.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 114
**Error:** Name "stamina" already defined on line 111  [no-redef]
**Solve:**
```python
# Original Code:
    def stamina(self) -> int:
        return self.attributes.stamina if self.attributes else 80
    @stamina.setter
    def stamina(self, value):
        if self.attributes: self.attributes.stamina = value

# Proposed Fix:
    # FIX: Name "stamina" already defined on line 111  [no-redef]
    @stamina.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 121
**Error:** Name "injury_resistance" already defined on line 118  [no-redef]
**Solve:**
```python
# Original Code:
    def injury_resistance(self) -> int:
        return self.attributes.injury_resistance if self.attributes else 80
    @injury_resistance.setter
    def injury_resistance(self, value):
        if self.attributes: self.attributes.injury_resistance = value

# Proposed Fix:
    # FIX: Name "injury_resistance" already defined on line 118  [no-redef]
    @injury_resistance.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 129
**Error:** Name "forty_yard_dash" already defined on line 126  [no-redef]
**Solve:**
```python
# Original Code:
    def forty_yard_dash(self) -> Optional[float]:
        return self.attributes.forty_yard_dash if self.attributes else None
    @forty_yard_dash.setter
    def forty_yard_dash(self, value):
        if self.attributes: self.attributes.forty_yard_dash = value

# Proposed Fix:
    # FIX: Name "forty_yard_dash" already defined on line 126  [no-redef]
    @forty_yard_dash.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 136
**Error:** Name "bench_press" already defined on line 133  [no-redef]
**Solve:**
```python
# Original Code:
    def bench_press(self) -> Optional[int]:
        return self.attributes.bench_press if self.attributes else None
    @bench_press.setter
    def bench_press(self, value):
        if self.attributes: self.attributes.bench_press = value

# Proposed Fix:
    # FIX: Name "bench_press" already defined on line 133  [no-redef]
    @bench_press.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 143
**Error:** Name "vertical_jump" already defined on line 140  [no-redef]
**Solve:**
```python
# Original Code:
    def vertical_jump(self) -> Optional[float]:
        return self.attributes.vertical_jump if self.attributes else None
    @vertical_jump.setter
    def vertical_jump(self, value):
        if self.attributes: self.attributes.vertical_jump = value

# Proposed Fix:
    # FIX: Name "vertical_jump" already defined on line 140  [no-redef]
    @vertical_jump.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 150
**Error:** Name "broad_jump" already defined on line 147  [no-redef]
**Solve:**
```python
# Original Code:
    def broad_jump(self) -> Optional[int]:
        return self.attributes.broad_jump if self.attributes else None
    @broad_jump.setter
    def broad_jump(self, value):
        if self.attributes: self.attributes.broad_jump = value

# Proposed Fix:
    # FIX: Name "broad_jump" already defined on line 147  [no-redef]
    @broad_jump.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 157
**Error:** Name "three_cone_drill" already defined on line 154  [no-redef]
**Solve:**
```python
# Original Code:
    def three_cone_drill(self) -> Optional[float]:
        return self.attributes.three_cone_drill if self.attributes else None
    @three_cone_drill.setter
    def three_cone_drill(self, value):
        if self.attributes: self.attributes.three_cone_drill = value

# Proposed Fix:
    # FIX: Name "three_cone_drill" already defined on line 154  [no-redef]
    @three_cone_drill.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 164
**Error:** Name "twenty_yard_shuttle" already defined on line 161  [no-redef]
**Solve:**
```python
# Original Code:
    def twenty_yard_shuttle(self) -> Optional[float]:
        return self.attributes.twenty_yard_shuttle if self.attributes else None
    @twenty_yard_shuttle.setter
    def twenty_yard_shuttle(self, value):
        if self.attributes: self.attributes.twenty_yard_shuttle = value

# Proposed Fix:
    # FIX: Name "twenty_yard_shuttle" already defined on line 161  [no-redef]
    @twenty_yard_shuttle.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 172
**Error:** Name "power_clean_max" already defined on line 169  [no-redef]
**Solve:**
```python
# Original Code:
    def power_clean_max(self) -> Optional[int]:
        return self.attributes.power_clean_max if self.attributes else None
    @power_clean_max.setter
    def power_clean_max(self, value):
        if self.attributes: self.attributes.power_clean_max = value

# Proposed Fix:
    # FIX: Name "power_clean_max" already defined on line 169  [no-redef]
    @power_clean_max.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 179
**Error:** Name "gps_speed_max" already defined on line 176  [no-redef]
**Solve:**
```python
# Original Code:
    def gps_speed_max(self) -> Optional[float]:
        return self.attributes.gps_speed_max if self.attributes else None
    @gps_speed_max.setter
    def gps_speed_max(self, value):
        if self.attributes: self.attributes.gps_speed_max = value

# Proposed Fix:
    # FIX: Name "gps_speed_max" already defined on line 176  [no-redef]
    @gps_speed_max.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 186
**Error:** Name "s2_cognition_score" already defined on line 183  [no-redef]
**Solve:**
```python
# Original Code:
    def s2_cognition_score(self) -> Optional[int]:
        return self.attributes.s2_cognition_score if self.attributes else None
    @s2_cognition_score.setter
    def s2_cognition_score(self, value):
        if self.attributes: self.attributes.s2_cognition_score = value

# Proposed Fix:
    # FIX: Name "s2_cognition_score" already defined on line 183  [no-redef]
    @s2_cognition_score.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 193
**Error:** Name "medical_flags" already defined on line 190  [no-redef]
**Solve:**
```python
# Original Code:
    def medical_flags(self) -> Optional[dict]:
        return self.injury.medical_flags if self.injury else None
    @medical_flags.setter
    def medical_flags(self, value):
        if self.injury: self.injury.medical_flags = value

# Proposed Fix:
    # FIX: Name "medical_flags" already defined on line 190  [no-redef]
    @medical_flags.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 200
**Error:** Name "genesis_revealed" already defined on line 197  [no-redef]
**Solve:**
```python
# Original Code:
    def genesis_revealed(self) -> bool:
        return self.injury.genesis_revealed if self.injury else False
    @genesis_revealed.setter
    def genesis_revealed(self, value):
        if self.injury: self.injury.genesis_revealed = value

# Proposed Fix:
    # FIX: Name "genesis_revealed" already defined on line 197  [no-redef]
    @genesis_revealed.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 208
**Error:** Name "throw_power" already defined on line 205  [no-redef]
**Solve:**
```python
# Original Code:
    def throw_power(self) -> int:
        return self.attributes.throw_power if self.attributes else 50
    @throw_power.setter
    def throw_power(self, value):
        if self.attributes: self.attributes.throw_power = value

# Proposed Fix:
    # FIX: Name "throw_power" already defined on line 205  [no-redef]
    @throw_power.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 215
**Error:** Name "throw_accuracy_short" already defined on line 212  [no-redef]
**Solve:**
```python
# Original Code:
    def throw_accuracy_short(self) -> int:
        return self.attributes.throw_accuracy_short if self.attributes else 50
    @throw_accuracy_short.setter
    def throw_accuracy_short(self, value):
        if self.attributes: self.attributes.throw_accuracy_short = value

# Proposed Fix:
    # FIX: Name "throw_accuracy_short" already defined on line 212  [no-redef]
    @throw_accuracy_short.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 222
**Error:** Name "throw_accuracy_mid" already defined on line 219  [no-redef]
**Solve:**
```python
# Original Code:
    def throw_accuracy_mid(self) -> int:
        return self.attributes.throw_accuracy_mid if self.attributes else 50
    @throw_accuracy_mid.setter
    def throw_accuracy_mid(self, value):
        if self.attributes: self.attributes.throw_accuracy_mid = value

# Proposed Fix:
    # FIX: Name "throw_accuracy_mid" already defined on line 219  [no-redef]
    @throw_accuracy_mid.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 229
**Error:** Name "throw_accuracy_deep" already defined on line 226  [no-redef]
**Solve:**
```python
# Original Code:
    def throw_accuracy_deep(self) -> int:
        return self.attributes.throw_accuracy_deep if self.attributes else 50
    @throw_accuracy_deep.setter
    def throw_accuracy_deep(self, value):
        if self.attributes: self.attributes.throw_accuracy_deep = value

# Proposed Fix:
    # FIX: Name "throw_accuracy_deep" already defined on line 226  [no-redef]
    @throw_accuracy_deep.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 236
**Error:** Name "catching" already defined on line 233  [no-redef]
**Solve:**
```python
# Original Code:
    def catching(self) -> int:
        return self.attributes.catching if self.attributes else 50
    @catching.setter
    def catching(self, value):
        if self.attributes: self.attributes.catching = value

# Proposed Fix:
    # FIX: Name "catching" already defined on line 233  [no-redef]
    @catching.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 243
**Error:** Name "route_running" already defined on line 240  [no-redef]
**Solve:**
```python
# Original Code:
    def route_running(self) -> int:
        return self.attributes.route_running if self.attributes else 50
    @route_running.setter
    def route_running(self, value):
        if self.attributes: self.attributes.route_running = value

# Proposed Fix:
    # FIX: Name "route_running" already defined on line 240  [no-redef]
    @route_running.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 250
**Error:** Name "pass_block" already defined on line 247  [no-redef]
**Solve:**
```python
# Original Code:
    def pass_block(self) -> int:
        return self.attributes.pass_block if self.attributes else 50
    @pass_block.setter
    def pass_block(self, value):
        if self.attributes: self.attributes.pass_block = value

# Proposed Fix:
    # FIX: Name "pass_block" already defined on line 247  [no-redef]
    @pass_block.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 257
**Error:** Name "run_block" already defined on line 254  [no-redef]
**Solve:**
```python
# Original Code:
    def run_block(self) -> int:
        return self.attributes.run_block if self.attributes else 50
    @run_block.setter
    def run_block(self, value):
        if self.attributes: self.attributes.run_block = value

# Proposed Fix:
    # FIX: Name "run_block" already defined on line 254  [no-redef]
    @run_block.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 264
**Error:** Name "tackle" already defined on line 261  [no-redef]
**Solve:**
```python
# Original Code:
    def tackle(self) -> int:
        return self.attributes.tackle if self.attributes else 50
    @tackle.setter
    def tackle(self, value):
        if self.attributes: self.attributes.tackle = value

# Proposed Fix:
    # FIX: Name "tackle" already defined on line 261  [no-redef]
    @tackle.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 271
**Error:** Name "hit_power" already defined on line 268  [no-redef]
**Solve:**
```python
# Original Code:
    def hit_power(self) -> int:
        return self.attributes.hit_power if self.attributes else 50
    @hit_power.setter
    def hit_power(self, value):
        if self.attributes: self.attributes.hit_power = value

# Proposed Fix:
    # FIX: Name "hit_power" already defined on line 268  [no-redef]
    @hit_power.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 278
**Error:** Name "block_shed" already defined on line 275  [no-redef]
**Solve:**
```python
# Original Code:
    def block_shed(self) -> int:
        return self.attributes.block_shed if self.attributes else 50
    @block_shed.setter
    def block_shed(self, value):
        if self.attributes: self.attributes.block_shed = value

# Proposed Fix:
    # FIX: Name "block_shed" already defined on line 275  [no-redef]
    @block_shed.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 285
**Error:** Name "man_coverage" already defined on line 282  [no-redef]
**Solve:**
```python
# Original Code:
    def man_coverage(self) -> int:
        return self.attributes.man_coverage if self.attributes else 50
    @man_coverage.setter
    def man_coverage(self, value):
        if self.attributes: self.attributes.man_coverage = value

# Proposed Fix:
    # FIX: Name "man_coverage" already defined on line 282  [no-redef]
    @man_coverage.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 292
**Error:** Name "zone_coverage" already defined on line 289  [no-redef]
**Solve:**
```python
# Original Code:
    def zone_coverage(self) -> int:
        return self.attributes.zone_coverage if self.attributes else 50
    @zone_coverage.setter
    def zone_coverage(self, value):
        if self.attributes: self.attributes.zone_coverage = value

# Proposed Fix:
    # FIX: Name "zone_coverage" already defined on line 289  [no-redef]
    @zone_coverage.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 299
**Error:** Name "pass_rush_power" already defined on line 296  [no-redef]
**Solve:**
```python
# Original Code:
    def pass_rush_power(self) -> int:
        return self.attributes.pass_rush_power if self.attributes else 50
    @pass_rush_power.setter
    def pass_rush_power(self, value):
        if self.attributes: self.attributes.pass_rush_power = value

# Proposed Fix:
    # FIX: Name "pass_rush_power" already defined on line 296  [no-redef]
    @pass_rush_power.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 306
**Error:** Name "pass_rush_finesse" already defined on line 303  [no-redef]
**Solve:**
```python
# Original Code:
    def pass_rush_finesse(self) -> int:
        return self.attributes.pass_rush_finesse if self.attributes else 50
    @pass_rush_finesse.setter
    def pass_rush_finesse(self, value):
        if self.attributes: self.attributes.pass_rush_finesse = value

# Proposed Fix:
    # FIX: Name "pass_rush_finesse" already defined on line 303  [no-redef]
    @pass_rush_finesse.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 313
**Error:** Name "play_recognition" already defined on line 310  [no-redef]
**Solve:**
```python
# Original Code:
    def play_recognition(self) -> int:
        return self.attributes.play_recognition if self.attributes else 50
    @play_recognition.setter
    def play_recognition(self, value):
        if self.attributes: self.attributes.play_recognition = value

# Proposed Fix:
    # FIX: Name "play_recognition" already defined on line 310  [no-redef]
    @play_recognition.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 320
**Error:** Name "kick_power" already defined on line 317  [no-redef]
**Solve:**
```python
# Original Code:
    def kick_power(self) -> int:
        return self.attributes.kick_power if self.attributes else 50
    @kick_power.setter
    def kick_power(self, value):
        if self.attributes: self.attributes.kick_power = value

# Proposed Fix:
    # FIX: Name "kick_power" already defined on line 317  [no-redef]
    @kick_power.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 327
**Error:** Name "kick_accuracy" already defined on line 324  [no-redef]
**Solve:**
```python
# Original Code:
    def kick_accuracy(self) -> int:
        return self.attributes.kick_accuracy if self.attributes else 50
    @kick_accuracy.setter
    def kick_accuracy(self, value):
        if self.attributes: self.attributes.kick_accuracy = value

# Proposed Fix:
    # FIX: Name "kick_accuracy" already defined on line 324  [no-redef]
    @kick_accuracy.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 335
**Error:** Name "pocket_presence" already defined on line 332  [no-redef]
**Solve:**
```python
# Original Code:
    def pocket_presence(self) -> int:
        return self.attributes.pocket_presence if self.attributes else 50
    @pocket_presence.setter
    def pocket_presence(self, value):
        if self.attributes: self.attributes.pocket_presence = value

# Proposed Fix:
    # FIX: Name "pocket_presence" already defined on line 332  [no-redef]
    @pocket_presence.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 342
**Error:** Name "quick_release" already defined on line 339  [no-redef]
**Solve:**
```python
# Original Code:
    def quick_release(self) -> int:
        return self.attributes.quick_release if self.attributes else 50
    @quick_release.setter
    def quick_release(self, value):
        if self.attributes: self.attributes.quick_release = value

# Proposed Fix:
    # FIX: Name "quick_release" already defined on line 339  [no-redef]
    @quick_release.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 349
**Error:** Name "scramble_willingness" already defined on line 346  [no-redef]
**Solve:**
```python
# Original Code:
    def scramble_willingness(self) -> int:
        return self.attributes.scramble_willingness if self.attributes else 50
    @scramble_willingness.setter
    def scramble_willingness(self, value):
        if self.attributes: self.attributes.scramble_willingness = value

# Proposed Fix:
    # FIX: Name "scramble_willingness" already defined on line 346  [no-redef]
    @scramble_willingness.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 356
**Error:** Name "throw_on_run" already defined on line 353  [no-redef]
**Solve:**
```python
# Original Code:
    def throw_on_run(self) -> int:
        return self.attributes.throw_on_run if self.attributes else 50
    @throw_on_run.setter
    def throw_on_run(self, value):
        if self.attributes: self.attributes.throw_on_run = value

# Proposed Fix:
    # FIX: Name "throw_on_run" already defined on line 353  [no-redef]
    @throw_on_run.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 363
**Error:** Name "patience" already defined on line 360  [no-redef]
**Solve:**
```python
# Original Code:
    def patience(self) -> int:
        return self.attributes.patience if self.attributes else 50
    @patience.setter
    def patience(self, value):
        if self.attributes: self.attributes.patience = value

# Proposed Fix:
    # FIX: Name "patience" already defined on line 360  [no-redef]
    @patience.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 370
**Error:** Name "pass_pro_rating" already defined on line 367  [no-redef]
**Solve:**
```python
# Original Code:
    def pass_pro_rating(self) -> int:
        return self.attributes.pass_pro_rating if self.attributes else 50
    @pass_pro_rating.setter
    def pass_pro_rating(self, value):
        if self.attributes: self.attributes.pass_pro_rating = value

# Proposed Fix:
    # FIX: Name "pass_pro_rating" already defined on line 367  [no-redef]
    @pass_pro_rating.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 377
**Error:** Name "juke_efficiency" already defined on line 374  [no-redef]
**Solve:**
```python
# Original Code:
    def juke_efficiency(self) -> int:
        return self.attributes.juke_efficiency if self.attributes else 50
    @juke_efficiency.setter
    def juke_efficiency(self, value):
        if self.attributes: self.attributes.juke_efficiency = value

# Proposed Fix:
    # FIX: Name "juke_efficiency" already defined on line 374  [no-redef]
    @juke_efficiency.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 384
**Error:** Name "release" already defined on line 381  [no-redef]
**Solve:**
```python
# Original Code:
    def release(self) -> int:
        return self.attributes.release if self.attributes else 50
    @release.setter
    def release(self, value):
        if self.attributes: self.attributes.release = value

# Proposed Fix:
    # FIX: Name "release" already defined on line 381  [no-redef]
    @release.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 391
**Error:** Name "blocking_tenacity" already defined on line 388  [no-redef]
**Solve:**
```python
# Original Code:
    def blocking_tenacity(self) -> int:
        return self.attributes.blocking_tenacity if self.attributes else 50
    @blocking_tenacity.setter
    def blocking_tenacity(self, value):
        if self.attributes: self.attributes.blocking_tenacity = value

# Proposed Fix:
    # FIX: Name "blocking_tenacity" already defined on line 388  [no-redef]
    @blocking_tenacity.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 398
**Error:** Name "pull_speed" already defined on line 395  [no-redef]
**Solve:**
```python
# Original Code:
    def pull_speed(self) -> int:
        return self.attributes.pull_speed if self.attributes else 50
    @pull_speed.setter
    def pull_speed(self, value):
        if self.attributes: self.attributes.pull_speed = value

# Proposed Fix:
    # FIX: Name "pull_speed" already defined on line 395  [no-redef]
    @pull_speed.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 405
**Error:** Name "anchor" already defined on line 402  [no-redef]
**Solve:**
```python
# Original Code:
    def anchor(self) -> int:
        return self.attributes.anchor if self.attributes else 50
    @anchor.setter
    def anchor(self, value):
        if self.attributes: self.attributes.anchor = value

# Proposed Fix:
    # FIX: Name "anchor" already defined on line 402  [no-redef]
    @anchor.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 412
**Error:** Name "discipline" already defined on line 409  [no-redef]
**Solve:**
```python
# Original Code:
    def discipline(self) -> int:
        return self.attributes.discipline if self.attributes else 50
    @discipline.setter
    def discipline(self, value):
        if self.attributes: self.attributes.discipline = value

# Proposed Fix:
    # FIX: Name "discipline" already defined on line 409  [no-redef]
    @discipline.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 419
**Error:** Name "first_step" already defined on line 416  [no-redef]
**Solve:**
```python
# Original Code:
    def first_step(self) -> int:
        return self.attributes.first_step if self.attributes else 50
    @first_step.setter
    def first_step(self, value):
        if self.attributes: self.attributes.first_step = value

# Proposed Fix:
    # FIX: Name "first_step" already defined on line 416  [no-redef]
    @first_step.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 426
**Error:** Name "gap_integrity" already defined on line 423  [no-redef]
**Solve:**
```python
# Original Code:
    def gap_integrity(self) -> int:
        return self.attributes.gap_integrity if self.attributes else 50
    @gap_integrity.setter
    def gap_integrity(self, value):
        if self.attributes: self.attributes.gap_integrity = value

# Proposed Fix:
    # FIX: Name "gap_integrity" already defined on line 423  [no-redef]
    @gap_integrity.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 433
**Error:** Name "coverage_disguise" already defined on line 430  [no-redef]
**Solve:**
```python
# Original Code:
    def coverage_disguise(self) -> int:
        return self.attributes.coverage_disguise if self.attributes else 50
    @coverage_disguise.setter
    def coverage_disguise(self, value):
        if self.attributes: self.attributes.coverage_disguise = value

# Proposed Fix:
    # FIX: Name "coverage_disguise" already defined on line 430  [no-redef]
    @coverage_disguise.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 440
**Error:** Name "blitz_timing" already defined on line 437  [no-redef]
**Solve:**
```python
# Original Code:
    def blitz_timing(self) -> int:
        return self.attributes.blitz_timing if self.attributes else 50
    @blitz_timing.setter
    def blitz_timing(self, value):
        if self.attributes: self.attributes.blitz_timing = value

# Proposed Fix:
    # FIX: Name "blitz_timing" already defined on line 437  [no-redef]
    @blitz_timing.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 447
**Error:** Name "run_fit" already defined on line 444  [no-redef]
**Solve:**
```python
# Original Code:
    def run_fit(self) -> int:
        return self.attributes.run_fit if self.attributes else 50
    @run_fit.setter
    def run_fit(self, value):
        if self.attributes: self.attributes.run_fit = value

# Proposed Fix:
    # FIX: Name "run_fit" already defined on line 444  [no-redef]
    @run_fit.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 454
**Error:** Name "press" already defined on line 451  [no-redef]
**Solve:**
```python
# Original Code:
    def press(self) -> int:
        return self.attributes.press if self.attributes else 50
    @press.setter
    def press(self, value):
        if self.attributes: self.attributes.press = value

# Proposed Fix:
    # FIX: Name "press" already defined on line 451  [no-redef]
    @press.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 461
**Error:** Name "ball_tracking" already defined on line 458  [no-redef]
**Solve:**
```python
# Original Code:
    def ball_tracking(self) -> int:
        return self.attributes.ball_tracking if self.attributes else 50
    @ball_tracking.setter
    def ball_tracking(self, value):
        if self.attributes: self.attributes.ball_tracking = value

# Proposed Fix:
    # FIX: Name "ball_tracking" already defined on line 458  [no-redef]
    @ball_tracking.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 468
**Error:** Name "run_support" already defined on line 465  [no-redef]
**Solve:**
```python
# Original Code:
    def run_support(self) -> int:
        return self.attributes.run_support if self.attributes else 50
    @run_support.setter
    def run_support(self, value):
        if self.attributes: self.attributes.run_support = value

# Proposed Fix:
    # FIX: Name "run_support" already defined on line 465  [no-redef]
    @run_support.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 475
**Error:** Name "hang_time" already defined on line 472  [no-redef]
**Solve:**
```python
# Original Code:
    def hang_time(self) -> int:
        return self.attributes.hang_time if self.attributes else 50
    @hang_time.setter
    def hang_time(self, value):
        if self.attributes: self.attributes.hang_time = value

# Proposed Fix:
    # FIX: Name "hang_time" already defined on line 472  [no-redef]
    @hang_time.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 482
**Error:** Name "coffin_corner" already defined on line 479  [no-redef]
**Solve:**
```python
# Original Code:
    def coffin_corner(self) -> int:
        return self.attributes.coffin_corner if self.attributes else 50
    @coffin_corner.setter
    def coffin_corner(self, value):
        if self.attributes: self.attributes.coffin_corner = value

# Proposed Fix:
    # FIX: Name "coffin_corner" already defined on line 479  [no-redef]
    @coffin_corner.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 489
**Error:** Name "return_vision" already defined on line 486  [no-redef]
**Solve:**
```python
# Original Code:
    def return_vision(self) -> int:
        return self.attributes.return_vision if self.attributes else 50
    @return_vision.setter
    def return_vision(self, value):
        if self.attributes: self.attributes.return_vision = value

# Proposed Fix:
    # FIX: Name "return_vision" already defined on line 486  [no-redef]
    @return_vision.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 497
**Error:** Name "arm_slot" already defined on line 494  [no-redef]
**Solve:**
```python
# Original Code:
    def arm_slot(self) -> str:
        return self.physics.arm_slot if self.physics else "OverTop"
    @arm_slot.setter
    def arm_slot(self, value):
        if self.physics: self.physics.arm_slot = value

# Proposed Fix:
    # FIX: Name "arm_slot" already defined on line 494  [no-redef]
    @arm_slot.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 504
**Error:** Name "release_point_height" already defined on line 501  [no-redef]
**Solve:**
```python
# Original Code:
    def release_point_height(self) -> float:
        return self.physics.release_point_height if self.physics else 6.0
    @release_point_height.setter
    def release_point_height(self, value):
        if self.physics: self.physics.release_point_height = value

# Proposed Fix:
    # FIX: Name "release_point_height" already defined on line 501  [no-redef]
    @release_point_height.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 511
**Error:** Name "vision_cone_angle" already defined on line 508  [no-redef]
**Solve:**
```python
# Original Code:
    def vision_cone_angle(self) -> int:
        return self.physics.vision_cone_angle if self.physics else 45
    @vision_cone_angle.setter
    def vision_cone_angle(self, value):
        if self.physics: self.physics.vision_cone_angle = value

# Proposed Fix:
    # FIX: Name "vision_cone_angle" already defined on line 508  [no-redef]
    @vision_cone_angle.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 518
**Error:** Name "break_tackle_threshold" already defined on line 515  [no-redef]
**Solve:**
```python
# Original Code:
    def break_tackle_threshold(self) -> float:
        return self.physics.break_tackle_threshold if self.physics else 100.0
    @break_tackle_threshold.setter
    def break_tackle_threshold(self, value):
        if self.physics: self.physics.break_tackle_threshold = value

# Proposed Fix:
    # FIX: Name "break_tackle_threshold" already defined on line 515  [no-redef]
    @break_tackle_threshold.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 526
**Error:** Name "xp" already defined on line 523  [no-redef]
**Solve:**
```python
# Original Code:
    def xp(self) -> int:
        return self.progression.xp if self.progression else 0
    @xp.setter
    def xp(self, value):
        if self.progression: self.progression.xp = value

# Proposed Fix:
    # FIX: Name "xp" already defined on line 523  [no-redef]
    @xp.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 533
**Error:** Name "level" already defined on line 530  [no-redef]
**Solve:**
```python
# Original Code:
    def level(self) -> int:
        return self.progression.level if self.progression else 1
    @level.setter
    def level(self, value):
        if self.progression: self.progression.level = value

# Proposed Fix:
    # FIX: Name "level" already defined on line 530  [no-redef]
    @level.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 540
**Error:** Name "skill_points" already defined on line 537  [no-redef]
**Solve:**
```python
# Original Code:
    def skill_points(self) -> int:
        return self.progression.skill_points if self.progression else 0
    @skill_points.setter
    def skill_points(self, value):
        if self.progression: self.progression.skill_points = value

# Proposed Fix:
    # FIX: Name "skill_points" already defined on line 537  [no-redef]
    @skill_points.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 547
**Error:** Name "development_trait" already defined on line 544  [no-redef]
**Solve:**
```python
# Original Code:
    def development_trait(self) -> str:
        return self.progression.development_trait if self.progression else "NORMAL"
    @development_trait.setter
    def development_trait(self, value):
        if self.progression: self.progression.development_trait = value

# Proposed Fix:
    # FIX: Name "development_trait" already defined on line 544  [no-redef]
    @development_trait.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 558
**Error:** Name "abilities" already defined on line 555  [no-redef]
**Solve:**
```python
# Original Code:
    def abilities(self) -> Optional[dict]:
        return self.progression.abilities if self.progression else {}
    @abilities.setter
    def abilities(self, value):
        if self.progression: self.progression.abilities = value

# Proposed Fix:
    # FIX: Name "abilities" already defined on line 555  [no-redef]
    @abilities.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 566
**Error:** Name "attribute_xp" already defined on line 563  [no-redef]
**Solve:**
```python
# Original Code:
    def attribute_xp(self) -> Optional[dict]:
        return self.progression.attribute_xp if self.progression else {}
    @attribute_xp.setter
    def attribute_xp(self, value):
        if self.progression: self.progression.attribute_xp = value

# Proposed Fix:
    # FIX: Name "attribute_xp" already defined on line 563  [no-redef]
    @attribute_xp.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 574
**Error:** Name "morale" already defined on line 571  [no-redef]
**Solve:**
```python
# Original Code:
    def morale(self) -> int:
        return self.contract.morale if self.contract else 50
    @morale.setter
    def morale(self, value):
        if self.contract: self.contract.morale = value

# Proposed Fix:
    # FIX: Name "morale" already defined on line 571  [no-redef]
    @morale.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 582
**Error:** Name "injury_status" already defined on line 579  [no-redef]
**Solve:**
```python
# Original Code:
    def injury_status(self) -> str:
        return self.injury.injury_status if self.injury else "ACTIVE"
    @injury_status.setter
    def injury_status(self, value):
        if self.injury: self.injury.injury_status = value

# Proposed Fix:
    # FIX: Name "injury_status" already defined on line 579  [no-redef]
    @injury_status.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 589
**Error:** Name "injury_type" already defined on line 586  [no-redef]
**Solve:**
```python
# Original Code:
    def injury_type(self) -> Optional[str]:
        return self.injury.injury_type if self.injury else None
    @injury_type.setter
    def injury_type(self, value):
        if self.injury: self.injury.injury_type = value

# Proposed Fix:
    # FIX: Name "injury_type" already defined on line 586  [no-redef]
    @injury_type.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 596
**Error:** Name "weeks_to_recovery" already defined on line 593  [no-redef]
**Solve:**
```python
# Original Code:
    def weeks_to_recovery(self) -> int:
        return self.injury.weeks_to_recovery if self.injury else 0
    @weeks_to_recovery.setter
    def weeks_to_recovery(self, value):
        if self.injury: self.injury.weeks_to_recovery = value

# Proposed Fix:
    # FIX: Name "weeks_to_recovery" already defined on line 593  [no-redef]
    @weeks_to_recovery.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 603
**Error:** Name "injury_severity" already defined on line 600  [no-redef]
**Solve:**
```python
# Original Code:
    def injury_severity(self) -> int:
        return self.injury.injury_severity if self.injury else 0
    @injury_severity.setter
    def injury_severity(self, value):
        if self.injury: self.injury.injury_severity = value

# Proposed Fix:
    # FIX: Name "injury_severity" already defined on line 600  [no-redef]
    @injury_severity.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 610
**Error:** Name "injury_recurrence_risk" already defined on line 607  [no-redef]
**Solve:**
```python
# Original Code:
    def injury_recurrence_risk(self) -> float:
        return self.injury.injury_recurrence_risk if self.injury else 0.0
    @injury_recurrence_risk.setter
    def injury_recurrence_risk(self, value):
        if self.injury: self.injury.injury_recurrence_risk = value

# Proposed Fix:
    # FIX: Name "injury_recurrence_risk" already defined on line 607  [no-redef]
    @injury_recurrence_risk.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 622
**Error:** Name "contract_years" already defined on line 619  [no-redef]
**Solve:**
```python
# Original Code:
    def contract_years(self) -> int:
        return self.contract.contract_years if self.contract else 1
    @contract_years.setter
    def contract_years(self, value):
        if self.contract: self.contract.contract_years = value

# Proposed Fix:
    # FIX: Name "contract_years" already defined on line 619  [no-redef]
    @contract_years.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 629
**Error:** Name "contract_salary" already defined on line 626  [no-redef]
**Solve:**
```python
# Original Code:
    def contract_salary(self) -> int:
        return self.contract.contract_salary if self.contract else 1000000
    @contract_salary.setter
    def contract_salary(self, value):
        if self.contract: self.contract.contract_salary = value

# Proposed Fix:
    # FIX: Name "contract_salary" already defined on line 626  [no-redef]
    @contract_salary.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 636
**Error:** Name "is_rookie" already defined on line 633  [no-redef]
**Solve:**
```python
# Original Code:
    def is_rookie(self) -> bool:
        return self.contract.is_rookie if self.contract else False
    @is_rookie.setter
    def is_rookie(self, value):
        if self.contract: self.contract.is_rookie = value

# Proposed Fix:
    # FIX: Name "is_rookie" already defined on line 633  [no-redef]
    @is_rookie.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 643
**Error:** Name "is_retired" already defined on line 640  [no-redef]
**Solve:**
```python
# Original Code:
    def is_retired(self) -> bool:
        return self.contract.is_retired if self.contract else False
    @is_retired.setter
    def is_retired(self, value):
        if self.contract: self.contract.is_retired = value

# Proposed Fix:
    # FIX: Name "is_retired" already defined on line 640  [no-redef]
    @is_retired.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 650
**Error:** Name "retirement_year" already defined on line 647  [no-redef]
**Solve:**
```python
# Original Code:
    def retirement_year(self) -> Optional[int]:
        return self.contract.retirement_year if self.contract else None
    @retirement_year.setter
    def retirement_year(self, value):
        if self.contract: self.contract.retirement_year = value

# Proposed Fix:
    # FIX: Name "retirement_year" already defined on line 647  [no-redef]
    @retirement_year.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 657
**Error:** Name "legacy_score" already defined on line 654  [no-redef]
**Solve:**
```python
# Original Code:
    def legacy_score(self) -> int:
        return self.contract.legacy_score if self.contract else 0
    @legacy_score.setter
    def legacy_score(self, value):
        if self.contract: self.contract.legacy_score = value

# Proposed Fix:
    # FIX: Name "legacy_score" already defined on line 654  [no-redef]
    @legacy_score.setter
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 662
**Error:** Name "PlayerSeasonStats" is not defined  [name-defined]
**Solve:**
```python
# Original Code:

    # History
    season_stats: Mapped[List["PlayerSeasonStats"]] = relationship("PlayerSeasonStats", back_populates="player")

    # New: Game Starts (OL Chemistry)

# Proposed Fix:
    # FIX: Name "PlayerSeasonStats" is not defined  [name-defined]
    season_stats: Mapped[List["PlayerSeasonStats"]] = relationship("PlayerSeasonStats", back_populates="player")
```


---

### File: `backend/app/models/player.py`
**Lines of Code:** 668
**Error:** Name "BodyPart" is not defined  [name-defined]
**Solve:**
```python
# Original Code:

    # Hyper-Immersive Relationships
    body_health: Mapped["BodyPart"] = relationship("BodyPart", back_populates="player", uselist=False)

    # --- Phase 3: Player Decomposition (1:1 Relationships) ---

# Proposed Fix:
    # FIX: Name "BodyPart" is not defined  [name-defined]
    body_health: Mapped["BodyPart"] = relationship("BodyPart", back_populates="player", uselist=False)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 67
**Error:** Need type annotation for "team_stats"  [var-annotated]
**Solve:**
```python
# Original Code:

        # Initialize team stats
        team_stats = {
            team.id: {
                'team_id': team.id,

# Proposed Fix:
        team_stats: Any = {
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 99
**Error:** Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
**Solve:**
```python
# Original Code:
            # Record opponents for SOS
            if home_id in team_stats:
                team_stats[home_id]['opponents'].append(away_id)
            if away_id in team_stats:
                team_stats[away_id]['opponents'].append(home_id)

# Proposed Fix:
    # FIX: Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
                team_stats[home_id]['opponents'].append(away_id)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 99
**Error:** Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
**Solve:**
```python
# Original Code:
            # Record opponents for SOS
            if home_id in team_stats:
                team_stats[home_id]['opponents'].append(away_id)
            if away_id in team_stats:
                team_stats[away_id]['opponents'].append(home_id)

# Proposed Fix:
    # FIX: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
                team_stats[home_id]['opponents'].append(away_id)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 99
**Error:** Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
**Solve:**
```python
# Original Code:
            # Record opponents for SOS
            if home_id in team_stats:
                team_stats[home_id]['opponents'].append(away_id)
            if away_id in team_stats:
                team_stats[away_id]['opponents'].append(home_id)

# Proposed Fix:
    # FIX: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
                team_stats[home_id]['opponents'].append(away_id)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 101
**Error:** Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
**Solve:**
```python
# Original Code:
                team_stats[home_id]['opponents'].append(away_id)
            if away_id in team_stats:
                team_stats[away_id]['opponents'].append(home_id)

            if not game.is_played:

# Proposed Fix:
    # FIX: Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
                team_stats[away_id]['opponents'].append(home_id)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 101
**Error:** Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
**Solve:**
```python
# Original Code:
                team_stats[home_id]['opponents'].append(away_id)
            if away_id in team_stats:
                team_stats[away_id]['opponents'].append(home_id)

            if not game.is_played:

# Proposed Fix:
    # FIX: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
                team_stats[away_id]['opponents'].append(home_id)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 101
**Error:** Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
**Solve:**
```python
# Original Code:
                team_stats[home_id]['opponents'].append(away_id)
            if away_id in team_stats:
                team_stats[away_id]['opponents'].append(home_id)

            if not game.is_played:

# Proposed Fix:
    # FIX: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"  [union-attr]
                team_stats[away_id]['opponents'].append(home_id)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 111
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                away_team = team_stats[away_id]

                home_team['points_for'] += game.home_score
                home_team['points_against'] += game.away_score
                away_team['points_for'] += game.away_score

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                home_team['points_for'] += game.home_score
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 112
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:

                home_team['points_for'] += game.home_score
                home_team['points_against'] += game.away_score
                away_team['points_for'] += game.away_score
                away_team['points_against'] += game.home_score

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                home_team['points_against'] += game.away_score
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 113
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                home_team['points_for'] += game.home_score
                home_team['points_against'] += game.away_score
                away_team['points_for'] += game.away_score
                away_team['points_against'] += game.home_score


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                away_team['points_for'] += game.away_score
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 114
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                home_team['points_against'] += game.away_score
                away_team['points_for'] += game.away_score
                away_team['points_against'] += game.home_score

                # Determine winner

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                away_team['points_against'] += game.home_score
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 119
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                winner_id = None
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                    home_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 119
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                winner_id = None
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                    home_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 119
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                winner_id = None
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                    home_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 119
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                winner_id = None
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                    home_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 120
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id
                elif game.home_score < game.away_score:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                    away_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 120
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id
                elif game.home_score < game.away_score:

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                    away_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 120
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id
                elif game.home_score < game.away_score:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                    away_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 120
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id
                elif game.home_score < game.away_score:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                    away_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 123
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    winner_id = home_id
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                    home_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 123
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    winner_id = home_id
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                    home_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 123
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    winner_id = home_id
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                    home_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 123
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    winner_id = home_id
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                    home_team['losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 124
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id
                else:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                    away_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 124
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id
                else:

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                    away_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 124
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id
                else:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                    away_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 124
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id
                else:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                    away_team['wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 127
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    winner_id = away_id
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                    home_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 127
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    winner_id = away_id
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                    home_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 127
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    winner_id = away_id
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                    home_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 127
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    winner_id = away_id
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                    home_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 128
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1

                # Update Head-to-Head

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                    away_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 128
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1

                # Update Head-to-Head

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                    away_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 128
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1

                # Update Head-to-Head

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                    away_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 128
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1

                # Update Head-to-Head

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                    away_team['ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 132
**Error:** Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [index]
**Solve:**
```python
# Original Code:
                # Update Head-to-Head
                if winner_id == home_id:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

# Proposed Fix:
    # FIX: Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [index]
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 132
**Error:** Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
**Solve:**
```python
# Original Code:
                # Update Head-to-Head
                if winner_id == home_id:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

# Proposed Fix:
    # FIX: Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 132
**Error:** Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
**Solve:**
```python
# Original Code:
                # Update Head-to-Head
                if winner_id == home_id:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

# Proposed Fix:
    # FIX: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 132
**Error:** Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
**Solve:**
```python
# Original Code:
                # Update Head-to-Head
                if winner_id == home_id:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

# Proposed Fix:
    # FIX: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 134
**Error:** Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [index]
**Solve:**
```python
# Original Code:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

                # Update Division Record

# Proposed Fix:
    # FIX: Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [index]
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 134
**Error:** Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
**Solve:**
```python
# Original Code:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

                # Update Division Record

# Proposed Fix:
    # FIX: Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 134
**Error:** Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
**Solve:**
```python
# Original Code:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

                # Update Division Record

# Proposed Fix:
    # FIX: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 134
**Error:** Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
**Solve:**
```python
# Original Code:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

                # Update Division Record

# Proposed Fix:
    # FIX: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"  [union-attr]
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 139
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference'] and home_team['division'] == away_team['division']:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        home_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 139
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference'] and home_team['division'] == away_team['division']:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        home_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 139
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference'] and home_team['division'] == away_team['division']:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        home_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 139
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference'] and home_team['division'] == away_team['division']:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        home_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 140
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        away_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 140
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        away_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 140
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        away_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 140
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        away_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 142
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        home_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 142
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        home_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 142
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        home_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 142
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        home_team['division_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 143
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        away_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 143
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        away_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 143
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        away_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 143
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        away_team['division_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 145
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        home_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 145
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        home_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 145
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        home_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 145
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        home_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 146
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1

                # Update Conference Record

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        away_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 146
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1

                # Update Conference Record

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        away_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 146
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1

                # Update Conference Record

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        away_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 146
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1

                # Update Conference Record

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        away_team['division_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 151
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference']:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        home_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 151
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference']:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        home_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 151
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference']:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        home_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 151
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                if home_team['conference'] == away_team['conference']:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        home_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 152
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        away_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 152
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        away_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 152
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        away_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 152
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        away_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 154
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        home_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 154
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        home_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 154
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        home_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 154
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        home_team['conference_losses'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 155
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        away_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 155
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        away_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 155
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        away_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 155
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        away_team['conference_wins'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 157
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        home_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 157
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        home_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 157
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        home_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 157
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        home_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 158
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1

        # Calculate derived stats (Win %, Diff, SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "int")  [operator]
                        away_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 158
**Error:** No overload variant of "__add__" of "list" matches argument type "int"  [operator]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1

        # Calculate derived stats (Win %, Diff, SOS)

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "int"  [operator]
                        away_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 158
**Error:** Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1

        # Calculate derived stats (Win %, Diff, SOS)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
                        away_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 158
**Error:** Unsupported operand types for + ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1

        # Calculate derived stats (Win %, Diff, SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "int")  [operator]
                        away_team['conference_ties'] += 1
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported left operand type for + ("dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported left operand type for + ("dict[Any, Any]")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** No overload variant of "__add__" of "list" matches argument type "str"  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "str"  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** No overload variant of "__add__" of "list" matches argument type "float"  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "float"  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for + ("str" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "dict[Any, Any]")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for + ("str" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "list[Any]")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for + ("str" and "float")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "float")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for + ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "list[Any]")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for + ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']

# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "str")  [operator]
            total_games = stats['wins'] + stats['losses'] + stats['ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for / ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for / ("float" and "list[Any]")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for / ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for / ("float" and "str")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** No overload variant of "__add__" of "list" matches argument type "float"  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "float"  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for + ("str" and "float")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "float")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for * ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "dict[Any, Any]")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for * ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "list[Any]")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for * ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "str")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for > ("list[Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for > ("list[Any]" and "int")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 163
**Error:** Unsupported operand types for > ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

# Proposed Fix:
    # FIX: Unsupported operand types for > ("str" and "int")  [operator]
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported left operand type for - ("dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported left operand type for - ("dict[Any, Any]")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported operand types for - ("dict[Any, Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported operand types for - ("dict[Any, Any]" and "float")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported left operand type for - ("list[Any]")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported left operand type for - ("list[Any]")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported operand types for - ("list[Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported operand types for - ("list[Any]" and "float")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported left operand type for - ("str")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported left operand type for - ("str")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported operand types for - ("str" and "float")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported operand types for - ("str" and "float")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported operand types for - ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported operand types for - ("float" and "dict[Any, Any]")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported operand types for - ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported operand types for - ("float" and "list[Any]")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Unsupported operand types for - ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Unsupported operand types for - ("float" and "str")  [operator]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 164
**Error:** Incompatible types in assignment (expression has type "Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
            stats['point_differential'] = stats['points_for'] - stats['points_against']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 165
**Error:** Argument 1 to "round" has incompatible type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float"; expected "_SupportsRound2[Any]"  [arg-type]
**Solve:**
```python
# Original Code:
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)

            # Division Win %

# Proposed Fix:
    # FIX: Argument 1 to "round" has incompatible type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float"; expected "_SupportsRound2[Any]"  [arg-type]
            stats['win_percentage'] = round(stats['win_percentage'], 3)
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported left operand type for + ("dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported left operand type for + ("dict[Any, Any]")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** No overload variant of "__add__" of "list" matches argument type "str"  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "str"  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** No overload variant of "__add__" of "list" matches argument type "float"  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "float"  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported operand types for + ("str" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "dict[Any, Any]")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported operand types for + ("str" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "list[Any]")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported operand types for + ("str" and "float")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "float")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported operand types for + ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "list[Any]")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 168
**Error:** Unsupported operand types for + ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:

            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "str")  [operator]
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for / ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for / ("float" and "list[Any]")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for / ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for / ("float" and "str")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** No overload variant of "__add__" of "list" matches argument type "float"  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "float"  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for + ("str" and "float")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "float")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for * ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "dict[Any, Any]")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for * ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "list[Any]")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for * ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "str")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for > ("list[Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for > ("list[Any]" and "int")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for > ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0

            # Conference Win %

# Proposed Fix:
    # FIX: Unsupported operand types for > ("str" and "int")  [operator]
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported left operand type for + ("dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported left operand type for + ("dict[Any, Any]")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** No overload variant of "__add__" of "list" matches argument type "str"  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "str"  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** No overload variant of "__add__" of "list" matches argument type "float"  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "float"  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported operand types for + ("str" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "dict[Any, Any]")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported operand types for + ("str" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "list[Any]")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported operand types for + ("str" and "float")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "float")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported operand types for + ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "list[Any]")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 172
**Error:** Unsupported operand types for + ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:

            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "str")  [operator]
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for / ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for / ("float" and "list[Any]")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for / ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for / ("float" and "str")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")  [assignment]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("dict[Any, Any]" and "float")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** No overload variant of "__add__" of "list" matches argument type "float"  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: No overload variant of "__add__" of "list" matches argument type "float"  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for + ("str" and "float")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("str" and "float")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for * ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "dict[Any, Any]")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for * ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "list[Any]")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for * ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for * ("float" and "str")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for > ("list[Any]" and "int")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for > ("list[Any]" and "int")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 173
**Error:** Unsupported operand types for > ("str" and "int")  [operator]
**Solve:**
```python
# Original Code:
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)

# Proposed Fix:
    # FIX: Unsupported operand types for > ("str" and "int")  [operator]
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 185
**Error:** Item "Column[str]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
**Solve:**
```python
# Original Code:
            valid_opponents = 0

            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']

# Proposed Fix:
    # FIX: Item "Column[str]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
            for opp_id in opponents:
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 185
**Error:** Item "Column[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
**Solve:**
```python
# Original Code:
            valid_opponents = 0

            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']

# Proposed Fix:
    # FIX: Item "Column[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
            for opp_id in opponents:
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 185
**Error:** Item "Column[float]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
**Solve:**
```python
# Original Code:
            valid_opponents = 0

            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']

# Proposed Fix:
    # FIX: Item "Column[float]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
            for opp_id in opponents:
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 185
**Error:** Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
**Solve:**
```python
# Original Code:
            valid_opponents = 0

            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']

# Proposed Fix:
    # FIX: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)  [union-attr]
            for opp_id in opponents:
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 187
**Error:** Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
**Solve:**
```python
# Original Code:
            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
                    valid_opponents += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "dict[Any, Any]")  [operator]
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 187
**Error:** Unsupported operand types for + ("float" and "list[Any]")  [operator]
**Solve:**
```python
# Original Code:
            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
                    valid_opponents += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "list[Any]")  [operator]
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 187
**Error:** Unsupported operand types for + ("float" and "str")  [operator]
**Solve:**
```python
# Original Code:
            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
                    valid_opponents += 1


# Proposed Fix:
    # FIX: Unsupported operand types for + ("float" and "str")  [operator]
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 187
**Error:** Incompatible types in assignment (expression has type "float | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
                    valid_opponents += 1


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "float | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", variable has type "float")  [assignment]
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 187
**Error:** Invalid index type "Any | str" for "dict[Column[Any], dict[str, dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float]]"; expected type "Column[Any]"  [index]
**Solve:**
```python
# Original Code:
            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
                    valid_opponents += 1


# Proposed Fix:
    # FIX: Invalid index type "Any | str" for "dict[Column[Any], dict[str, dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float]]"; expected type "Column[Any]"  [index]
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 226
**Error:** Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:

        # 1. Group by Division and Rank
        divisions = {}
        for data in standings_data:
            div_key = f"{data['conference']}-{data['division']}"

# Proposed Fix:
        divisions: dict[str, float] = {}
```


---

### File: `backend/app/services/standings_calculator.py`
**Lines of Code:** 239
**Error:** Need type annotation for "conferences" (hint: "conferences: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:

        # 2. Group by Conference and Rank
        conferences = {}
        for data in standings_data:
            conf = data['conference']

# Proposed Fix:
        conferences: dict[str, float] = {}
```


---

### File: `backend/app/services/schedule_generator.py`
**Lines of Code:** 26
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:
    """

    def __init__(self, db: Session, seed: int = None):
        self.db = db
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, db: Session, seed: int = None):
```


---

### File: `backend/app/services/schedule_generator.py`
**Lines of Code:** 34
**Error:** Incompatible default for argument "start_date" (default has type "None", argument has type "datetime")  [assignment]
**Solve:**
```python
# Original Code:
        season_id: int,
        teams: List[Team],
        start_date: datetime = None,
        games_per_week: int = 16
    ) -> List[Game]:

# Proposed Fix:
    # FIX: Incompatible default for argument "start_date" (default has type "None", argument has type "datetime")  [assignment]
        start_date: datetime = None,
```


---

### File: `backend/app/services/schedule_generator.py`
**Lines of Code:** 50
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        """
        if start_date is None:
            start_date = self._get_next_sunday()

        # Organize teams by division

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            start_date = self._get_next_sunday()
```


---

### File: `backend/app/services/schedule_generator.py`
**Lines of Code:** 82
**Error:** Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
            Dict[str, List[Team]]: Key is "Conference-Division" (e.g., "AFC-North"), value is list of Teams.
        """
        divisions = {}
        for team in teams:
            div_key = f"{team.conference}-{team.division}"

# Proposed Fix:
        divisions: dict[str, float] = {}
```


---

### File: `backend/app/services/schedule_generator.py`
**Lines of Code:** 166
**Error:** Need type annotation for "matchups" (hint: "matchups: list[<type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
            game_count[away.id] += 1

        matchups = []
        team_list = sorted(teams, key=lambda t: game_count[t.id])


# Proposed Fix:
        matchups: list[Any] = []
```


---

### File: `backend/app/services/playbook/gameplan_service.py`
**Lines of Code:** 50
**Error:** Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
**Solve:**
```python
# Original Code:
            off_bonus += 5.0

        gameplan.prep_bonus_offense = off_bonus
        gameplan.prep_bonus_defense = def_bonus
        self.db.commit()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
        gameplan.prep_bonus_offense = off_bonus
```


---

### File: `backend/app/services/playbook/gameplan_service.py`
**Lines of Code:** 51
**Error:** Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
**Solve:**
```python
# Original Code:

        gameplan.prep_bonus_offense = off_bonus
        gameplan.prep_bonus_defense = def_bonus
        self.db.commit()


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")  [assignment]
        gameplan.prep_bonus_defense = def_bonus
```


---

### File: `backend/app/services/playbook/gameplan_service.py`
**Lines of Code:** 66
**Error:** Incompatible types in assignment (expression has type "list[Any]", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
        if skill_key not in current_skills:
            current_skills.append(skill_key)
            tree.unlocked_skills = current_skills
            self.db.commit()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "list[Any]", variable has type "Column[Any]")  [assignment]
            tree.unlocked_skills = current_skills
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 114
**Error:** Need type annotation for "event_counts" (hint: "event_counts: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:

        # Count events by type
        event_counts = {}
        for event in events:
            event_type = event.event_type

# Proposed Fix:
        event_counts: dict[str, float] = {}
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 135
**Error:** Unsupported operand types for >= ("int" and "object")  [operator]
**Solve:**
```python
# Original Code:
        # Sacks in game
        sack_count = counts.get(EventType.SACK_EVENT, 0)
        if sack_count >= TRAIT_TRIGGERS["sacks_in_game"]["threshold"]:
            result = self._award_trait(db, player_id, "sacks_in_game")
            if result:

# Proposed Fix:
    # FIX: Unsupported operand types for >= ("int" and "object")  [operator]
        if sack_count >= TRAIT_TRIGGERS["sacks_in_game"]["threshold"]:
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 142
**Error:** Unsupported operand types for >= ("int" and "object")  [operator]
**Solve:**
```python
# Original Code:
        # TDs in game
        td_count = counts.get(EventType.TOUCHDOWN_EVENT, 0)
        if td_count >= TRAIT_TRIGGERS["tds_in_game"]["threshold"]:
            result = self._award_trait(db, player_id, "tds_in_game")
            if result:

# Proposed Fix:
    # FIX: Unsupported operand types for >= ("int" and "object")  [operator]
        if td_count >= TRAIT_TRIGGERS["tds_in_game"]["threshold"]:
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 149
**Error:** Unsupported operand types for >= ("int" and "object")  [operator]
**Solve:**
```python
# Original Code:
        # Dropped passes in game
        drop_count = counts.get(EventType.DROPPED_PASS, 0)
        if drop_count >= TRAIT_TRIGGERS["dropped_passes_in_game"]["threshold"]:
            result = self._award_trait(db, player_id, "dropped_passes_in_game")
            if result:

# Proposed Fix:
    # FIX: Unsupported operand types for >= ("int" and "object")  [operator]
        if drop_count >= TRAIT_TRIGGERS["dropped_passes_in_game"]["threshold"]:
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 162
**Error:** Unsupported operand types for >= ("int" and "object")  [operator]
**Solve:**
```python
# Original Code:
        # Injuries in season
        injury_count = counts.get(EventType.PLAYER_INJURED, 0)
        if injury_count >= TRAIT_TRIGGERS["injuries_in_season"]["threshold"]:
            result = self._award_trait(db, player_id, "injuries_in_season")
            if result:

# Proposed Fix:
    # FIX: Unsupported operand types for >= ("int" and "object")  [operator]
        if injury_count >= TRAIT_TRIGGERS["injuries_in_season"]["threshold"]:
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 169
**Error:** Unsupported operand types for >= ("int" and "object")  [operator]
**Solve:**
```python
# Original Code:
        # Fumbles in season
        fumble_count = counts.get(EventType.CRITICAL_FUMBLE, 0) + counts.get(EventType.TURNOVER_EVENT, 0)
        if fumble_count >= TRAIT_TRIGGERS["fumbles_in_season"]["threshold"]:
            result = self._award_trait(db, player_id, "fumbles_in_season")
            if result:

# Proposed Fix:
    # FIX: Unsupported operand types for >= ("int" and "object")  [operator]
        if fumble_count >= TRAIT_TRIGGERS["fumbles_in_season"]["threshold"]:
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 176
**Error:** Unsupported operand types for >= ("int" and "object")  [operator]
**Solve:**
```python
# Original Code:
        # Spectacular catches in season
        catch_count = counts.get(EventType.SPECTACULAR_CATCH, 0)
        if catch_count >= TRAIT_TRIGGERS["spectacular_catches_in_season"]["threshold"]:
            result = self._award_trait(db, player_id, "spectacular_catches_in_season")
            if result:

# Proposed Fix:
    # FIX: Unsupported operand types for >= ("int" and "object")  [operator]
        if catch_count >= TRAIT_TRIGGERS["spectacular_catches_in_season"]["threshold"]:
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 226
**Error:** "object" has no attribute "value"  [attr-defined]
**Solve:**
```python
# Original Code:
            "player_id": player_id,
            "badge_name": trait_name,
            "tier": trigger["tier"].value,
            "is_positive": trigger["is_positive"]
        })

# Proposed Fix:
    # FIX: "object" has no attribute "value"  [attr-defined]
            "tier": trigger["tier"].value,
```


---

### File: `backend/app/services/trait_evolution_service.py`
**Lines of Code:** 235
**Error:** "object" has no attribute "value"  [attr-defined]
**Solve:**
```python
# Original Code:
            "trait_name": trait_name,
            "action": "EARNED",
            "tier": trigger["tier"].value
        }


# Proposed Fix:
    # FIX: "object" has no attribute "value"  [attr-defined]
            "tier": trigger["tier"].value
```


---

### File: `backend/app/services/salary_cap_service.py`
**Lines of Code:** 89
**Error:** "Team" has no attribute "salary_cap_total"  [attr-defined]
**Solve:**
```python
# Original Code:
            "team_id": team.id,
            "team_name": team.name,
            "total_cap": team.salary_cap_total,
            "used_cap": used_cap,
            "available_cap": team.salary_cap_space,

# Proposed Fix:
    # FIX: "Team" has no attribute "salary_cap_total"  [attr-defined]
            "total_cap": team.salary_cap_total,
```


---

### File: `backend/app/services/salary_cap_service.py`
**Lines of Code:** 92
**Error:** "Team" has no attribute "salary_cap_total"  [attr-defined]
**Solve:**
```python
# Original Code:
            "used_cap": used_cap,
            "available_cap": team.salary_cap_space,
            "cap_percentage": round((used_cap / team.salary_cap_total) * 100, 1) if team.salary_cap_total > 0 else 0,
            "top_contracts": top_contracts_data,
            "position_breakdown": pos_breakdown,

# Proposed Fix:
    # FIX: "Team" has no attribute "salary_cap_total"  [attr-defined]
            "cap_percentage": round((used_cap / team.salary_cap_total) * 100, 1) if team.salary_cap_total > 0 else 0,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 297
**Error:** Incompatible types in assignment (expression has type "Any | float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
                # Normalize threshold (lower is better for breaking tackles)
                threshold = getattr(player, attr_name, 100)
                attr_value = max(40, min(99, 100 - (threshold / 2)))
            else:
                attr_value = getattr(player, attr_name, 50)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | float", variable has type "int")  [assignment]
                attr_value = max(40, min(99, 100 - (threshold / 2)))
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 54
**Error:** Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:

        if part == "head":
            health.head_health = max(0, health.head_health - damage)
        elif part == "torso":
            health.torso_health = max(0, health.torso_health - damage)

# Proposed Fix:
    # FIX: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
            health.head_health = max(0, health.head_health - damage)
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 54
**Error:** Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:

        if part == "head":
            health.head_health = max(0, health.head_health - damage)
        elif part == "torso":
            health.torso_health = max(0, health.torso_health - damage)

# Proposed Fix:
    # FIX: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
            health.head_health = max(0, health.head_health - damage)
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 56
**Error:** Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:
            health.head_health = max(0, health.head_health - damage)
        elif part == "torso":
            health.torso_health = max(0, health.torso_health - damage)
        elif part == "right_arm":
            health.right_arm_health = max(0, health.right_arm_health - damage)

# Proposed Fix:
    # FIX: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
            health.torso_health = max(0, health.torso_health - damage)
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 56
**Error:** Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:
            health.head_health = max(0, health.head_health - damage)
        elif part == "torso":
            health.torso_health = max(0, health.torso_health - damage)
        elif part == "right_arm":
            health.right_arm_health = max(0, health.right_arm_health - damage)

# Proposed Fix:
    # FIX: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
            health.torso_health = max(0, health.torso_health - damage)
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 58
**Error:** Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:
            health.torso_health = max(0, health.torso_health - damage)
        elif part == "right_arm":
            health.right_arm_health = max(0, health.right_arm_health - damage)
        elif part == "right_leg":
            health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty

# Proposed Fix:
    # FIX: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
            health.right_arm_health = max(0, health.right_arm_health - damage)
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 58
**Error:** Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:
            health.torso_health = max(0, health.torso_health - damage)
        elif part == "right_arm":
            health.right_arm_health = max(0, health.right_arm_health - damage)
        elif part == "right_leg":
            health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty

# Proposed Fix:
    # FIX: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
            health.right_arm_health = max(0, health.right_arm_health - damage)
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 60
**Error:** Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:
            health.right_arm_health = max(0, health.right_arm_health - damage)
        elif part == "right_leg":
            health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty

    def process_weekly_recovery(self, player_id: int):

# Proposed Fix:
    # FIX: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"  [arg-type]
            health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 60
**Error:** Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
**Solve:**
```python
# Original Code:
            health.right_arm_health = max(0, health.right_arm_health - damage)
        elif part == "right_leg":
            health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty

    def process_weekly_recovery(self, player_id: int):

# Proposed Fix:
    # FIX: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"  [arg-type]
            health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty
```


---

### File: `backend/app/services/depth_chart_service.py`
**Lines of Code:** 16
**Error:** Need type annotation for "chart" (hint: "chart: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        Filters out injured players (OUT, IR).
        """
        chart = {}
        for p in players:
            # Check injury status

# Proposed Fix:
        chart: dict[str, float] = {}
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 12
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:

class InjurySystem:
    def __init__(self, seed: int = None):
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))


# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, seed: int = None):
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 37
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        if severity_roll <= 50:
            severity = self.rng.randint(1, 3)
            player.injury_type = "Minor Sprain" # Placeholder, could be more specific
            player.injury_status = InjuryStatus.QUESTIONABLE
        elif severity_roll <= 80:

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_type = "Minor Sprain" # Placeholder, could be more specific
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 38
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            severity = self.rng.randint(1, 3)
            player.injury_type = "Minor Sprain" # Placeholder, could be more specific
            player.injury_status = InjuryStatus.QUESTIONABLE
        elif severity_roll <= 80:
            severity = self.rng.randint(4, 7)

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_status = InjuryStatus.QUESTIONABLE
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 41
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        elif severity_roll <= 80:
            severity = self.rng.randint(4, 7)
            player.injury_type = "Muscle Tear"
            player.injury_status = InjuryStatus.OUT
        else:

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_type = "Muscle Tear"
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 42
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            severity = self.rng.randint(4, 7)
            player.injury_type = "Muscle Tear"
            player.injury_status = InjuryStatus.OUT
        else:
            severity = self.rng.randint(8, 10)

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_status = InjuryStatus.OUT
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 45
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        else:
            severity = self.rng.randint(8, 10)
            player.injury_type = "Major Fracture" # or Ligament Tear
            player.injury_status = InjuryStatus.IR


# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_type = "Major Fracture" # or Ligament Tear
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 46
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            severity = self.rng.randint(8, 10)
            player.injury_type = "Major Fracture" # or Ligament Tear
            player.injury_status = InjuryStatus.IR

        player.injury_severity = severity

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_status = InjuryStatus.IR
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 48
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            player.injury_status = InjuryStatus.IR

        player.injury_severity = severity

        # Calculate Recovery Weeks

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_severity = severity
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 52
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        # Calculate Recovery Weeks
        weeks = self.calculate_recovery_weeks(player, severity, medical_rating)
        player.weeks_to_recovery = weeks

        # Initial Recurrence Risk (Setback probability)

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.weeks_to_recovery = weeks
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 56
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        # Initial Recurrence Risk (Setback probability)
        # Higher severity = higher risk
        player.injury_recurrence_risk = severity * 0.02 # 2% per severity point initially (e.g. 20% for severity 10)

        logger.info(f"Player {player.id} injured: {player.injury_type} (Severity {severity}), Out for {weeks} weeks")

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_recurrence_risk = severity * 0.02 # 2% per severity point initially (e.g. 20% for severity 10)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 111
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            # Setback!
            added_weeks = self.rng.randint(1, 4)
            player.weeks_to_recovery += added_weeks
            # Increase recurrence risk for future checks
            player.injury_recurrence_risk += 0.05

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.weeks_to_recovery += added_weeks
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 113
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            player.weeks_to_recovery += added_weeks
            # Increase recurrence risk for future checks
            player.injury_recurrence_risk += 0.05
            logger.info(f"Player {player.id} suffered a setback in rehab. Added {added_weeks} weeks.")
            return

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_recurrence_risk += 0.05
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 119
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        # Progress Recovery
        if player.weeks_to_recovery > 0:
            player.weeks_to_recovery -= 1

        if player.weeks_to_recovery <= 0:

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.weeks_to_recovery -= 1
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 132
**Error:** Returning Any from function declared to return "bool"  [no-any-return]
**Solve:**
```python
# Original Code:

        roll = self.rng.random() # 0.0 to 1.0
        return roll < (player.injury_recurrence_risk * risk_modifier)

    def clear_injury(self, player: Player):

# Proposed Fix:
    # FIX: Returning Any from function declared to return "bool"  [no-any-return]
        return roll < (player.injury_recurrence_risk * risk_modifier)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 141
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        self.apply_permanent_damage(player)

        player.injury_status = InjuryStatus.ACTIVE
        player.injury_type = None
        player.injury_severity = 0

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_status = InjuryStatus.ACTIVE
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 142
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:

        player.injury_status = InjuryStatus.ACTIVE
        player.injury_type = None
        player.injury_severity = 0
        player.injury_recurrence_risk = 0.0

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_type = None
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 143
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        player.injury_status = InjuryStatus.ACTIVE
        player.injury_type = None
        player.injury_severity = 0
        player.injury_recurrence_risk = 0.0
        logger.info(f"Player {player.id} recovered from injury.")

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_severity = 0
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 144
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        player.injury_type = None
        player.injury_severity = 0
        player.injury_recurrence_risk = 0.0
        logger.info(f"Player {player.id} recovered from injury.")


# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_recurrence_risk = 0.0
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 177
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:

                # Also drop injury resistance permanently
                player.injury_resistance = max(0, player.injury_resistance - 5)

    # =========================================================================

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                player.injury_resistance = max(0, player.injury_resistance - 5)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 287
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        if self.rng.random() < escalation_chance:
            increase = self.rng.randint(1, InjuryConfig.INJURY_ESCALATION_MAX_INCREASE)
            player.injury_severity = min(10, severity + increase)
            return True


# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_severity = min(10, severity + increase)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 322
**Error:** Incompatible types in assignment (expression has type "None", variable has type "dict[str, int]")  [assignment]
**Solve:**
```python
# Original Code:
    weeks_to_recovery: int = 0
    can_play_through: bool = False        # Based on toughness/Ragknow
    performance_penalties: Dict[str, int] = None

    def __post_init__(self):

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "None", variable has type "dict[str, int]")  [assignment]
    performance_penalties: Dict[str, int] = None
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 326
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
    def __post_init__(self):
        if self.performance_penalties is None:
            self.performance_penalties = {}



# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            self.performance_penalties = {}
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 336
**Error:** Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
**Solve:**
```python
# Original Code:
    player: Player,
    play_context: PlayContext,
    rng: DeterministicRNG = None
) -> float:
    """

# Proposed Fix:
    # FIX: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
    rng: DeterministicRNG = None
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 479
**Error:** Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
**Solve:**
```python
# Original Code:
    player: Player,
    current_severity: int,
    rng: DeterministicRNG = None
) -> Optional[int]:
    """

# Proposed Fix:
    # FIX: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
    rng: DeterministicRNG = None
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 519
**Error:** Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
**Solve:**
```python
# Original Code:
    play_context: PlayContext,
    players_on_field: List[Player],
    rng: DeterministicRNG = None
) -> List[InjuryEvent]:
    """

# Proposed Fix:
    # FIX: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
    rng: DeterministicRNG = None
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 536
**Error:** Argument "seed" to "InjurySystem" has incompatible type "int | None"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
    """
    injuries = []
    injury_system = InjurySystem(seed=rng.randint(0, 1000000) if rng else None)

    for player in players_on_field:

# Proposed Fix:
    injury_system = InjurySystem(seed=int(rng.randint(0), 1000000) if rng else None)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 591
**Error:** Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
**Solve:**
```python
# Original Code:
def _determine_injury_details(
    severity: int,
    rng: DeterministicRNG = None
) -> tuple:
    """

# Proposed Fix:
    # FIX: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")  [assignment]
    rng: DeterministicRNG = None
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 626
**Error:** Incompatible default for argument "injury_system" (default has type "None", argument has type "InjurySystem")  [assignment]
**Solve:**
```python
# Original Code:


def apply_injury_event_to_player(player: Player, event: InjuryEvent, injury_system: InjurySystem = None):
    """
    Apply an InjuryEvent to a player's status.

# Proposed Fix:
    # FIX: Incompatible default for argument "injury_system" (default has type "None", argument has type "InjurySystem")  [assignment]
def apply_injury_event_to_player(player: Player, event: InjuryEvent, injury_system: InjurySystem = None):
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 635
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        injury_system: Optional InjurySystem instance for recovery calculations
    """
    player.injury_severity = event.severity
    player.injury_type = event.injury_type
    player.weeks_to_recovery = event.weeks_to_recovery

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
    player.injury_severity = event.severity
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 636
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
    """
    player.injury_severity = event.severity
    player.injury_type = event.injury_type
    player.weeks_to_recovery = event.weeks_to_recovery


# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
    player.injury_type = event.injury_type
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 637
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
    player.injury_severity = event.severity
    player.injury_type = event.injury_type
    player.weeks_to_recovery = event.weeks_to_recovery

    # Set status based on severity and can_play_through

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
    player.weeks_to_recovery = event.weeks_to_recovery
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 641
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
    # Set status based on severity and can_play_through
    if event.can_play_through:
        player.injury_status = InjuryStatus.QUESTIONABLE
    elif event.severity <= 3:
        player.injury_status = InjuryStatus.QUESTIONABLE

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_status = InjuryStatus.QUESTIONABLE
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 643
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        player.injury_status = InjuryStatus.QUESTIONABLE
    elif event.severity <= 3:
        player.injury_status = InjuryStatus.QUESTIONABLE
    elif event.severity <= 7:
        player.injury_status = InjuryStatus.OUT

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_status = InjuryStatus.QUESTIONABLE
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 645
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        player.injury_status = InjuryStatus.QUESTIONABLE
    elif event.severity <= 7:
        player.injury_status = InjuryStatus.OUT
    else:
        player.injury_status = InjuryStatus.IR

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_status = InjuryStatus.OUT
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 647
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        player.injury_status = InjuryStatus.OUT
    else:
        player.injury_status = InjuryStatus.IR

    # Set recurrence risk

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_status = InjuryStatus.IR
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 650
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:

    # Set recurrence risk
    player.injury_recurrence_risk = event.severity * 0.02

    logger.info(

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
    player.injury_recurrence_risk = event.severity * 0.02
```


---

### File: `backend/app/orchestrator/play_caller.py`
**Lines of Code:** 148
**Error:** Returning Any from function declared to return "bool"  [no-any-return]
**Solve:**
```python
# Original Code:
        pass_prob = max(0.05, min(0.95, pass_prob))

        return self.rng.random() < pass_prob

    def call_audible(

# Proposed Fix:
    # FIX: Returning Any from function declared to return "bool"  [no-any-return]
        return self.rng.random() < pass_prob
```


---

### File: `backend/app/orchestrator/play_caller.py`
**Lines of Code:** 152
**Error:** Name "Player" is not defined  [name-defined]
**Solve:**
```python
# Original Code:
    def call_audible(
        self,
        qb: "Player",
        current_play: str,
        new_play: str,

# Proposed Fix:
    # FIX: Name "Player" is not defined  [name-defined]
        qb: "Player",
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 60
**Error:** "Game" has no attribute "current_quarter"  [attr-defined]
**Solve:**
```python
# Original Code:
                game.home_score = state.get("home_score", 0)
                game.away_score = state.get("away_score", 0)
                game.current_quarter = state.get("quarter", 1)
                game.time_left = state.get("time_left", "15:00")


# Proposed Fix:
    # FIX: "Game" has no attribute "current_quarter"  [attr-defined]
                game.current_quarter = state.get("quarter", 1)
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 61
**Error:** "Game" has no attribute "time_left"  [attr-defined]
**Solve:**
```python
# Original Code:
                game.away_score = state.get("away_score", 0)
                game.current_quarter = state.get("quarter", 1)
                game.time_left = state.get("time_left", "15:00")

                # Update game data with plays and config

# Proposed Fix:
    # FIX: "Game" has no attribute "time_left"  [attr-defined]
                game.time_left = state.get("time_left", "15:00")
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 67
**Error:** Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
                current_data["plays"] = [p.model_dump() for p in history]
                current_data["state"] = state
                game.game_data = current_data

                await self.db.commit()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "Column[Any]")  [assignment]
                game.game_data = current_data
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 91
**Error:** Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
**Solve:**
```python
# Original Code:

            if game:
                game.is_played = True
                await self.db.commit()
                logger.info("Game finalized", extra={"game_id": game_id})

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
                game.is_played = True
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 66
**Error:** Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:

        # 3. Update Season Status
        season.status = SeasonStatus.POST_SEASON
        season.current_week = 19
        self.db.commit()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
        season.status = SeasonStatus.POST_SEASON
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 67
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
        # 3. Update Season Status
        season.status = SeasonStatus.POST_SEASON
        season.current_week = 19
        self.db.commit()


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        season.current_week = 19
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 93
**Error:** Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:

        # Group by Division to find winners
        divisions = {}
        for team_stat in conf_teams:
            div = team_stat.division

# Proposed Fix:
        divisions: dict[str, float] = {}
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 126
**Error:** Incompatible return value type (got "list[Team | None]", expected "list[Team]")  [return-value]
**Solve:**
```python
# Original Code:
            ordered_teams.append(team)

        return ordered_teams

    def _create_wild_card_round(self, season_id: int, conference: str, seeds: List[Team]):

# Proposed Fix:
    # FIX: Incompatible return value type (got "list[Team | None]", expected "list[Team]")  [return-value]
        return ordered_teams
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 282
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            self._create_divisional_round(season_id, "AFC")
            self._create_divisional_round(season_id, "NFC")
            season.current_week = 20

        elif current_week == 20: # Divisional -> Conference

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            season.current_week = 20
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 287
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            self._create_conference_round(season_id, "AFC")
            self._create_conference_round(season_id, "NFC")
            season.current_week = 21

        elif current_week == 21: # Conference -> Super Bowl

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            season.current_week = 21
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 291
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
        elif current_week == 21: # Conference -> Super Bowl
            self._create_super_bowl(season_id)
            season.current_week = 22

        elif current_week == 22: # Super Bowl -> Offseason

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            season.current_week = 22
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 295
**Error:** Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
        elif current_week == 22: # Super Bowl -> Offseason
            # Season over, move to offseason
            season.status = SeasonStatus.OFF_SEASON
            # We don't advance week here, offseason starts at week 22 or resets?
            # Usually offseason is a state, not a week.

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
            season.status = SeasonStatus.OFF_SEASON
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 333
**Error:** Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, Column[int] | Team | None]], Column[int] | Team | None]"; expected "Callable[[dict[str, Column[int] | Team | None]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"  [arg-type]
**Solve:**
```python
# Original Code:

        # Sort by seed (1 is best)
        remaining_teams.sort(key=lambda x: x["seed"])

        # 1 vs Lowest (which is the last in the sorted list)

# Proposed Fix:
        remaining_teams.sort(key=Callable(lambda) x: x["seed"])
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 333
**Error:** Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")  [return-value]
**Solve:**
```python
# Original Code:

        # Sort by seed (1 is best)
        remaining_teams.sort(key=lambda x: x["seed"])

        # 1 vs Lowest (which is the last in the sorted list)

# Proposed Fix:
    # FIX: Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")  [return-value]
        remaining_teams.sort(key=lambda x: x["seed"])
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 373
**Error:** Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, Column[int] | Team | None]], Column[int] | Team | None]"; expected "Callable[[dict[str, Column[int] | Team | None]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"  [arg-type]
**Solve:**
```python
# Original Code:
            winners.append({"team": team, "seed": winner_seed})

        winners.sort(key=lambda x: x["seed"])

        # Higher seed hosts

# Proposed Fix:
        winners.sort(key=Callable(lambda) x: x["seed"])
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 373
**Error:** Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")  [return-value]
**Solve:**
```python
# Original Code:
            winners.append({"team": team, "seed": winner_seed})

        winners.sort(key=lambda x: x["seed"])

        # Higher seed hosts

# Proposed Fix:
    # FIX: Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")  [return-value]
        winners.sort(key=lambda x: x["seed"])
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 404
**Error:** Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"  [union-attr]
**Solve:**
```python
# Original Code:
        nfc_conf = self.db.execute(stmt_nfc).scalar_one_or_none()

        afc_winner = self.db.execute(select(Team).where(Team.id == afc_conf.winner_id)).scalar_one_or_none()
        nfc_winner = self.db.execute(select(Team).where(Team.id == nfc_conf.winner_id)).scalar_one_or_none()


# Proposed Fix:
    # FIX: Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"  [union-attr]
        afc_winner = self.db.execute(select(Team).where(Team.id == afc_conf.winner_id)).scalar_one_or_none()
```


---

### File: `backend/app/services/playoff_service.py`
**Lines of Code:** 405
**Error:** Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"  [union-attr]
**Solve:**
```python
# Original Code:

        afc_winner = self.db.execute(select(Team).where(Team.id == afc_conf.winner_id)).scalar_one_or_none()
        nfc_winner = self.db.execute(select(Team).where(Team.id == nfc_conf.winner_id)).scalar_one_or_none()

        # Super Bowl (Home/Away arbitrary, let's say AFC is Home this year)

# Proposed Fix:
    # FIX: Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"  [union-attr]
        nfc_winner = self.db.execute(select(Team).where(Team.id == nfc_conf.winner_id)).scalar_one_or_none()
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 19
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:

class PlayerDevelopmentService:
    def __init__(self, db: AsyncSession, seed: int = None):
        self.db = db
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, db: AsyncSession, seed: int = None):
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 58
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
        new_rating = min(99, max(1, budget_impact))

        team.medical_rating = new_rating
        team.training_staff_quality = new_rating


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        team.medical_rating = new_rating
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 59
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:

        team.medical_rating = new_rating
        team.training_staff_quality = new_rating

    def _apply_team_training(self, team: Team):

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        team.training_staff_quality = new_rating
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 78
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
            # Dev Trait Multiplier
            if player.development_trait == DevelopmentTrait.STAR:
                xp_gain *= 1.25
            elif player.development_trait == DevelopmentTrait.SUPERSTAR:
                xp_gain *= 1.5

# Proposed Fix:
                xp_gain = int(xp_gain * 1.25)
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 80
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
                xp_gain *= 1.25
            elif player.development_trait == DevelopmentTrait.SUPERSTAR:
                xp_gain *= 1.5
            elif player.development_trait == DevelopmentTrait.XFACTOR:
                xp_gain *= 2.0

# Proposed Fix:
                xp_gain = int(xp_gain * 1.5)
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 82
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
                xp_gain *= 1.5
            elif player.development_trait == DevelopmentTrait.XFACTOR:
                xp_gain *= 2.0

            # Coach Bonus

# Proposed Fix:
                xp_gain = int(xp_gain * 2.0)
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 85
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:

            # Coach Bonus
            xp_gain *= (1.0 + coach_bonus)

            # Age Penalty/Bonus

# Proposed Fix:
            xp_gain = int(xp_gain * (1.0 + coach_bonus))
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 89
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
            # Age Penalty/Bonus
            if player.age > 30:
                xp_gain *= 0.8
            elif player.age < 24:
                xp_gain *= 1.2

# Proposed Fix:
                xp_gain = int(xp_gain * 0.8)
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 91
**Error:** Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
                xp_gain *= 0.8
            elif player.age < 24:
                xp_gain *= 1.2

            player.xp += int(xp_gain)

# Proposed Fix:
                xp_gain = int(xp_gain * 1.2)
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 118
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        if current_val < 99:
            setattr(player, stat_to_boost, current_val + 1)
            player.skill_points -= 1

            # Recalculate Overall (Simplified)

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.skill_points -= 1
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 147
**Error:** Argument "medical_rating" to "process_recovery_step" of "InjurySystem" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        """Update recovery time for injured players."""
        for player in team.players:
            self.injury_system.process_recovery_step(player, medical_rating=team.medical_rating)

    def _update_team_morale(self, team: Team):

# Proposed Fix:
            self.injury_system.process_recovery_step(player, medical_rating=int(team.medical_rating))
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 154
**Error:** Incompatible types in assignment (expression has type "ColumnElement[float | Decimal]", variable has type "float")  [assignment]
**Solve:**
```python
# Original Code:
        win_pct = 0.5
        if (team.wins + team.losses) > 0:
            win_pct = team.wins / (team.wins + team.losses)

        for player in team.players:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[float | Decimal]", variable has type "float")  [assignment]
            win_pct = team.wins / (team.wins + team.losses)
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 188
**Error:** Argument 1 to "calculate_injury_risk_multiplier" of "InjurySystem" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        Get the injury risk multiplier based on the team's training staff quality.
        """
        return self.injury_system.calculate_injury_risk_multiplier(team.training_staff_quality)

# Proposed Fix:
    # FIX: Argument 1 to "calculate_injury_risk_multiplier" of "InjurySystem" has incompatible type "Column[int]"; expected "int"  [arg-type]
        return self.injury_system.calculate_injury_risk_multiplier(team.training_staff_quality)
```


---

### File: `backend/app/core/mcp_cache.py`
**Lines of Code:** 9
**Error:** Incompatible types in assignment (expression has type "None", variable has type Module)  [assignment]
**Solve:**
```python
# Original Code:
    import redis
except ImportError:
    redis = None

logger = logging.getLogger(__name__)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "None", variable has type Module)  [assignment]
    redis = None
```


---

### File: `backend/app/core/mcp_cache.py`
**Lines of Code:** 48
**Error:** Argument 1 to "loads" has incompatible type "Awaitable[Any] | Any"; expected "str | bytes | bytearray"  [arg-type]
**Solve:**
```python
# Original Code:
                if data:
                    logger.debug(f"MCP Redis Cache HIT: {key}")
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")

# Proposed Fix:
    # FIX: Argument 1 to "loads" has incompatible type "Awaitable[Any] | Any"; expected "str | bytes | bytearray"  [arg-type]
                    return json.loads(data)
```


---

### File: `backend/app/core/trade_config.py`
**Lines of Code:** 106
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
        """Gets the value multiplier for a position."""
        tier = self.get_position_tier(position)
        return self.POSITION_VALUE_TIERS[tier]["multiplier"]

    def get_archetype_modifiers(self, archetype: GMArchetype) -> Dict[str, float]:

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
        return self.POSITION_VALUE_TIERS[tier]["multiplier"]
```


---

### File: `backend/app/core/logging_config.py`
**Lines of Code:** 36
**Error:** Cannot find implementation or library stub for module named "structlog"  [import-not-found]
**Solve:**
```python
# Original Code:
from typing import TYPE_CHECKING, Any, Callable

import structlog
from structlog.types import EventDict, WrappedLogger


# Proposed Fix:
    # FIX: Cannot find implementation or library stub for module named "structlog"  [import-not-found]
import structlog
```


---

### File: `backend/app/core/logging_config.py`
**Lines of Code:** 37
**Error:** Cannot find implementation or library stub for module named "structlog.types"  [import-not-found]
**Solve:**
```python
# Original Code:

import structlog
from structlog.types import EventDict, WrappedLogger

if TYPE_CHECKING:

# Proposed Fix:
    # FIX: Cannot find implementation or library stub for module named "structlog.types"  [import-not-found]
from structlog.types import EventDict, WrappedLogger
```


---

### File: `backend/app/core/logging_config.py`
**Lines of Code:** 369
**Error:** Returning Any from function declared to return "Response"  [no-any-return]
**Solve:**
```python
# Original Code:
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:

# Proposed Fix:
    # FIX: Returning Any from function declared to return "Response"  [no-any-return]
            return response
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 16
**Error:** Incompatible return value type (got "Any | None", expected "str")  [return-value]
**Solve:**
```python
# Original Code:

def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", None)

async def database_exception_handler(request: Request, exc: IntegrityError):

# Proposed Fix:
    return str(getattr(request.state, "request_id", None))
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 22
**Error:** Missing named argument "details" for "ErrorResponse"  [call-arg]
**Solve:**
```python
# Original Code:
    logger.error(f"Database integrity error: {exc}", extra={"request_id": get_request_id(request)})

    error_response = ErrorResponse(
        status_code=status.HTTP_409_CONFLICT,
        error=ErrorDetail(

# Proposed Fix:
    # FIX: Missing named argument "details" for "ErrorResponse"  [call-arg]
    error_response = ErrorResponse(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 24
**Error:** Missing named argument "field" for "ErrorDetail"  [call-arg]
**Solve:**
```python
# Original Code:
    error_response = ErrorResponse(
        status_code=status.HTTP_409_CONFLICT,
        error=ErrorDetail(
            code="DB_INTEGRITY_ERROR",
            message="The operation conflicts with existing data constraints.",

# Proposed Fix:
    # FIX: Missing named argument "field" for "ErrorDetail"  [call-arg]
        error=ErrorDetail(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 42
**Error:** Missing named argument "details" for "ErrorResponse"  [call-arg]
**Solve:**
```python
# Original Code:
    logger.error(f"Database operational error: {exc}", extra={"request_id": get_request_id(request)})

    error_response = ErrorResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        error=ErrorDetail(

# Proposed Fix:
    # FIX: Missing named argument "details" for "ErrorResponse"  [call-arg]
    error_response = ErrorResponse(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 44
**Error:** Missing named argument "field" for "ErrorDetail"  [call-arg]
**Solve:**
```python
# Original Code:
    error_response = ErrorResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        error=ErrorDetail(
            code="DB_CONNECTION_ERROR",
            message="Unable to connect to the database. Please try again later.",

# Proposed Fix:
    # FIX: Missing named argument "field" for "ErrorDetail"  [call-arg]
        error=ErrorDetail(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 73
**Error:** Missing named argument "field" for "ErrorDetail"  [call-arg]
**Solve:**
```python
# Original Code:
    error_response = ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="The request data is invalid."

# Proposed Fix:
    # FIX: Missing named argument "field" for "ErrorDetail"  [call-arg]
        error=ErrorDetail(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 73
**Error:** Missing named argument "value" for "ErrorDetail"  [call-arg]
**Solve:**
```python
# Original Code:
    error_response = ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="The request data is invalid."

# Proposed Fix:
    # FIX: Missing named argument "value" for "ErrorDetail"  [call-arg]
        error=ErrorDetail(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 102
**Error:** Missing named argument "field" for "ErrorDetail"  [call-arg]
**Solve:**
```python
# Original Code:
    error_response = ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error=ErrorDetail(
            code="DATA_VALIDATION_ERROR",
            message="The data provided is invalid."

# Proposed Fix:
    # FIX: Missing named argument "field" for "ErrorDetail"  [call-arg]
        error=ErrorDetail(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 102
**Error:** Missing named argument "value" for "ErrorDetail"  [call-arg]
**Solve:**
```python
# Original Code:
    error_response = ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error=ErrorDetail(
            code="DATA_VALIDATION_ERROR",
            message="The data provided is invalid."

# Proposed Fix:
    # FIX: Missing named argument "value" for "ErrorDetail"  [call-arg]
        error=ErrorDetail(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 120
**Error:** Missing named argument "details" for "ErrorResponse"  [call-arg]
**Solve:**
```python
# Original Code:
    logger.exception(f"Unhandled exception: {exc}", extra={"request_id": get_request_id(request)})

    error_response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error=ErrorDetail(

# Proposed Fix:
    # FIX: Missing named argument "details" for "ErrorResponse"  [call-arg]
    error_response = ErrorResponse(
```


---

### File: `backend/app/core/error_handlers.py`
**Lines of Code:** 122
**Error:** Missing named argument "field" for "ErrorDetail"  [call-arg]
**Solve:**
```python
# Original Code:
    error_response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please contact support if the issue persists.",

# Proposed Fix:
    # FIX: Missing named argument "field" for "ErrorDetail"  [call-arg]
        error=ErrorDetail(
```


---

### File: `backend/app/core/db_helpers.py`
**Lines of Code:** 9
**Error:** Incompatible default for argument "detail" (default has type "None", argument has type "str")  [assignment]
**Solve:**
```python
# Original Code:
T = TypeVar("T")

def get_object_or_404(db: Session, model: Type[T], object_id: Any, detail: str = None) -> T:
    """
    Get a record by ID or raise 404.

# Proposed Fix:
    # FIX: Incompatible default for argument "detail" (default has type "None", argument has type "str")  [assignment]
def get_object_or_404(db: Session, model: Type[T], object_id: Any, detail: str = None) -> T:
```


---

### File: `backend/app/core/db_helpers.py`
**Lines of Code:** 13
**Error:** "type[T]" has no attribute "id"  [attr-defined]
**Solve:**
```python
# Original Code:
    Get a record by ID or raise 404.
    """
    stmt = select(model).where(model.id == object_id)
    obj = db.execute(stmt).scalar_one_or_none()
    if obj is None:

# Proposed Fix:
    # FIX: "type[T]" has no attribute "id"  [attr-defined]
    stmt = select(model).where(model.id == object_id)
```


---

### File: `backend/app/core/db_helpers.py`
**Lines of Code:** 23
**Error:** Incompatible default for argument "detail" (default has type "None", argument has type "str")  [assignment]
**Solve:**
```python
# Original Code:


async def get_object_or_404_async(db: AsyncSession, model: Type[T], object_id: Any, detail: str = None) -> T:
    """
    Get a record by ID or raise 404 (Async).

# Proposed Fix:
    # FIX: Incompatible default for argument "detail" (default has type "None", argument has type "str")  [assignment]
async def get_object_or_404_async(db: AsyncSession, model: Type[T], object_id: Any, detail: str = None) -> T:
```


---

### File: `backend/app/core/db_helpers.py`
**Lines of Code:** 27
**Error:** "type[T]" has no attribute "id"  [attr-defined]
**Solve:**
```python
# Original Code:
    Get a record by ID or raise 404 (Async).
    """
    stmt = select(model).where(model.id == object_id)
    result = await db.execute(stmt)
    obj = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: "type[T]" has no attribute "id"  [attr-defined]
    stmt = select(model).where(model.id == object_id)
```


---

### File: `backend/app/core/auth.py`
**Lines of Code:** 10
**Error:** Cannot find implementation or library stub for module named "firebase_admin"  [import-not-found]
**Solve:**
```python
# Original Code:
import os
from typing import Optional
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Header

# Proposed Fix:
    # FIX: Cannot find implementation or library stub for module named "firebase_admin"  [import-not-found]
import firebase_admin
```


---

### File: `backend/app/core/auth.py`
**Lines of Code:** 83
**Error:** Returning Any from function declared to return "dict[Any, Any]"  [no-any-return]
**Solve:**
```python
# Original Code:
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

# Proposed Fix:
    # FIX: Returning Any from function declared to return "dict[Any, Any]"  [no-any-return]
        return decoded_token
```


---

### File: `backend/app/core/redis_cache.py`
**Lines of Code:** 33
**Error:** "Settings" has no attribute "REDIS_URL"  [attr-defined]
**Solve:**
```python
# Original Code:
        try:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True

# Proposed Fix:
    # FIX: "Settings" has no attribute "REDIS_URL"  [attr-defined]
                settings.REDIS_URL,
```


---

### File: `backend/app/core/redis_cache.py`
**Lines of Code:** 37
**Error:** Incompatible types in "await" (actual type "Awaitable[bool] | bool | Any", expected type "Awaitable[Any]")  [misc]
**Solve:**
```python
# Original Code:
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("✅ Connected to Redis for chemistry caching")
        except Exception as e:

# Proposed Fix:
    # FIX: Incompatible types in "await" (actual type "Awaitable[bool] | bool | Any", expected type "Awaitable[Any]")  [misc]
            await self.redis.ping()
```


---

### File: `backend/app/core/redis_cache.py`
**Lines of Code:** 81
**Error:** Returning Any from function declared to return "dict[Any, Any] | None"  [no-any-return]
**Solve:**
```python
# Original Code:
            if cached:
                logger.debug(f"✅ Chemistry cache HIT: {key}")
                return json.loads(cached)
            else:
                logger.debug(f"❌ Chemistry cache MISS: {key}")

# Proposed Fix:
    # FIX: Returning Any from function declared to return "dict[Any, Any] | None"  [no-any-return]
                return json.loads(cached)
```


---

### File: `backend/app/core/database.py`
**Lines of Code:** 22
**Error:** Dict entry 0 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
**Solve:**
```python
# Original Code:
if not is_sqlite:
    engine_args.update({
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,

# Proposed Fix:
    # FIX: Dict entry 0 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
        "pool_size": settings.DB_POOL_SIZE,
```


---

### File: `backend/app/core/database.py`
**Lines of Code:** 23
**Error:** Dict entry 1 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
**Solve:**
```python
# Original Code:
    engine_args.update({
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,

# Proposed Fix:
    # FIX: Dict entry 1 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
        "max_overflow": settings.DB_MAX_OVERFLOW,
```


---

### File: `backend/app/core/database.py`
**Lines of Code:** 24
**Error:** Dict entry 2 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
**Solve:**
```python
# Original Code:
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
    })

# Proposed Fix:
    # FIX: Dict entry 2 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
        "pool_timeout": settings.DB_POOL_TIMEOUT,
```


---

### File: `backend/app/core/database.py`
**Lines of Code:** 25
**Error:** Dict entry 3 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
**Solve:**
```python
# Original Code:
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
    })


# Proposed Fix:
    # FIX: Dict entry 3 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"  [dict-item]
        "pool_recycle": settings.DB_POOL_RECYCLE,
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 189
**Error:** Dict entry 1 has incompatible type "str": "float"; expected "str": "int"  [dict-item]
**Solve:**
```python
# Original Code:
        },
        tier="GOLD",
        min_stat_threshold={"receptions": 100, "drop_rate_max": 0.05},
    ),
    "deep_threat": TraitDefinition(

# Proposed Fix:
    # FIX: Dict entry 1 has incompatible type "str": "float"; expected "str": "int"  [dict-item]
        min_stat_threshold={"receptions": 100, "drop_rate_max": 0.05},
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 596
**Error:** Incompatible default for argument "db" (default has type "None", argument has type "Session")  [assignment]
**Solve:**
```python
# Original Code:
    """

    def __init__(self, db: Session = None):
        """Initialize with optional database session for async operations."""
        self.db = db

# Proposed Fix:
    # FIX: Incompatible default for argument "db" (default has type "None", argument has type "Session")  [assignment]
    def __init__(self, db: Session = None):
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 629
**Error:** Incompatible return value type (got "Sequence[Trait]", expected "list[Trait]")  [return-value]
**Solve:**
```python
# Original Code:
    def get_all_traits(db: Session) -> List[Trait]:
        """List all available traits in the system."""
        return db.scalars(select(Trait)).all()

    @staticmethod

# Proposed Fix:
    # FIX: Incompatible return value type (got "Sequence[Trait]", expected "list[Trait]")  [return-value]
        return db.scalars(select(Trait)).all()
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 711
**Error:** Unsupported operand types for <= ("int" and "None")  [operator]
**Solve:**
```python
# Original Code:
                    .where(Trait.tier == trait_tier)
                )
                if existing_count >= cap:
                    raise ValueError(
                        f"Player already has {existing_count} {trait_tier.value} traits "

# Proposed Fix:
    # FIX: Unsupported operand types for <= ("int" and "None")  [operator]
                if existing_count >= cap:
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 745
**Error:** Name "get_player_traits" already defined on line 631  [no-redef]
**Solve:**
```python
# Original Code:
    # -------------------------------------------------------------------------

    async def get_player_traits(self, player_id: int) -> List[TraitDefinition]:
        """
        Async instance method wrapper for get_player_traits.

# Proposed Fix:
    # FIX: Name "get_player_traits" already defined on line 631  [no-redef]
    async def get_player_traits(self, player_id: int) -> List[TraitDefinition]:
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 757
**Error:** Subclass of "Session" and "AsyncSession" cannot exist: would have incompatible method signatures  [unreachable]
**Solve:**
```python
# Original Code:
        from sqlalchemy.ext.asyncio import AsyncSession

        if isinstance(self.db, AsyncSession):
            result = await self.db.execute(
                sa_select(Trait)

# Proposed Fix:
    # FIX: Subclass of "Session" and "AsyncSession" cannot exist: would have incompatible method signatures  [unreachable]
        if isinstance(self.db, AsyncSession):
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 758
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:

        if isinstance(self.db, AsyncSession):
            result = await self.db.execute(
                sa_select(Trait)
                .join(PlayerTrait, Trait.id == PlayerTrait.trait_id)

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            result = await self.db.execute(
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 900
**Error:** Incompatible default for argument "context" (default has type "None", argument has type "dict[str, Any]")  [assignment]
**Solve:**
```python
# Original Code:
        player: Player,
        trait_def: TraitDefinition,
        context: Dict[str, Any] = None
    ) -> Dict[str, float]:
        """

# Proposed Fix:
    # FIX: Incompatible default for argument "context" (default has type "None", argument has type "dict[str, Any]")  [assignment]
        context: Dict[str, Any] = None
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 911
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
        # Initialize player modifiers if needed
        if not hasattr(player, "active_modifiers"):
            player.active_modifiers = {}
        if not hasattr(player, "active_traits"):
            player.active_traits = []

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
            player.active_modifiers = {}
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 913
**Error:** "Player" has no attribute "active_traits"  [attr-defined]
**Solve:**
```python
# Original Code:
            player.active_modifiers = {}
        if not hasattr(player, "active_traits"):
            player.active_traits = []

        # Track active trait

# Proposed Fix:
    # FIX: "Player" has no attribute "active_traits"  [attr-defined]
            player.active_traits = []
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 916
**Error:** "Player" has no attribute "active_traits"  [attr-defined]
**Solve:**
```python
# Original Code:

        # Track active trait
        if trait_def.name not in player.active_traits:
            player.active_traits.append(trait_def.name)


# Proposed Fix:
    # FIX: "Player" has no attribute "active_traits"  [attr-defined]
        if trait_def.name not in player.active_traits:
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 917
**Error:** "Player" has no attribute "active_traits"  [attr-defined]
**Solve:**
```python
# Original Code:
        # Track active trait
        if trait_def.name not in player.active_traits:
            player.active_traits.append(trait_def.name)

        # Apply each effect

# Proposed Fix:
    # FIX: "Player" has no attribute "active_traits"  [attr-defined]
            player.active_traits.append(trait_def.name)
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 922
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
        for effect_key, effect_value in trait_def.effects.items():
            # Accumulate effects (don't overwrite)
            current = player.active_modifiers.get(effect_key, 0)
            player.active_modifiers[effect_key] = current + effect_value


# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
            current = player.active_modifiers.get(effect_key, 0)
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 923
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
            # Accumulate effects (don't overwrite)
            current = player.active_modifiers.get(effect_key, 0)
            player.active_modifiers[effect_key] = current + effect_value

        return trait_def.effects

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
            player.active_modifiers[effect_key] = current + effect_value
```


---

### File: `backend/app/services/ability_service.py`
**Lines of Code:** 143
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
                return False, f"Insufficient XP: requires {ability_def.xp_cost}, has {player.xp}", player

            player.xp -= ability_def.xp_cost

            # Add ability to player

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.xp -= ability_def.xp_cost
```


---

### File: `backend/app/services/ability_service.py`
**Lines of Code:** 148
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            abilities_dict = player.abilities or {}
            abilities_dict[ability_key] = True
            player.abilities = abilities_dict

            self.db.commit()

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.abilities = abilities_dict
```


---

### File: `backend/app/services/ability_service.py`
**Lines of Code:** 165
**Error:** "type[ErrorCategory]" has no attribute "SERVICE_ERROR"  [attr-defined]
**Solve:**
```python
# Original Code:
        except Exception as e:
            self.db.rollback()
            log_error(logger, ErrorCategory.SERVICE_ERROR, "Failed to unlock ability", exc_info=e)
            return False, str(e), None


# Proposed Fix:
    # FIX: "type[ErrorCategory]" has no attribute "SERVICE_ERROR"  [attr-defined]
            log_error(logger, ErrorCategory.SERVICE_ERROR, "Failed to unlock ability", exc_info=e)
```


---

### File: `backend/app/services/ability_service.py`
**Lines of Code:** 184
**Error:** Returning Any from function declared to return "bool"  [no-any-return]
**Solve:**
```python
# Original Code:

        abilities_dict = player.abilities or {}
        return abilities_dict.get(ability_key, False)

    def get_player_ability_status(

# Proposed Fix:
    # FIX: Returning Any from function declared to return "bool"  [no-any-return]
        return abilities_dict.get(ability_key, False)
```


---

### File: `backend/app/scripts/seed_teams.py`
**Lines of Code:** 42
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
            else:
                print(f"Updating {data.abbreviation}...")
                team.logo_url = logo_url
                team.primary_color = data.colors.primary_hex
                team.secondary_color = data.colors.secondary_hex

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
                team.logo_url = logo_url
```


---

### File: `backend/app/scripts/seed_teams.py`
**Lines of Code:** 43
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
                print(f"Updating {data.abbreviation}...")
                team.logo_url = logo_url
                team.primary_color = data.colors.primary_hex
                team.secondary_color = data.colors.secondary_hex
                # Update other fields if needed

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
                team.primary_color = data.colors.primary_hex
```


---

### File: `backend/app/scripts/seed_teams.py`
**Lines of Code:** 44
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
                team.logo_url = logo_url
                team.primary_color = data.colors.primary_hex
                team.secondary_color = data.colors.secondary_hex
                # Update other fields if needed


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
                team.secondary_color = data.colors.secondary_hex
```


---

### File: `backend/app/scripts/seed_coaches.py`
**Lines of Code:** 66
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
                if existing:
                    # Update existing coach
                    existing.first_name = coach_data.first_name
                    existing.last_name = coach_data.last_name
                    if off_scheme:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
                    existing.first_name = coach_data.first_name
```


---

### File: `backend/app/scripts/seed_coaches.py`
**Lines of Code:** 67
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
                    # Update existing coach
                    existing.first_name = coach_data.first_name
                    existing.last_name = coach_data.last_name
                    if off_scheme:
                        existing.playbook_offense = off_scheme

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
                    existing.last_name = coach_data.last_name
```


---

### File: `backend/app/scripts/seed_coaches.py`
**Lines of Code:** 69
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
                    existing.last_name = coach_data.last_name
                    if off_scheme:
                        existing.playbook_offense = off_scheme
                    if def_scheme:
                        existing.playbook_defense = def_scheme

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
                        existing.playbook_offense = off_scheme
```


---

### File: `backend/app/scripts/seed_coaches.py`
**Lines of Code:** 71
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
                        existing.playbook_offense = off_scheme
                    if def_scheme:
                        existing.playbook_defense = def_scheme
                    if role == "Head Coach":
                        existing.philosophy = philosophy_dict

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
                        existing.playbook_defense = def_scheme
```


---

### File: `backend/app/scripts/seed_coaches.py`
**Lines of Code:** 73
**Error:** Incompatible types in assignment (expression has type "dict[str, int]", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
                        existing.playbook_defense = def_scheme
                    if role == "Head Coach":
                        existing.philosophy = philosophy_dict
                    coaches_updated += 1
                else:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "dict[str, int]", variable has type "Column[Any]")  [assignment]
                        existing.philosophy = philosophy_dict
```


---

### File: `backend/app/api/endpoints/settings.py`
**Lines of Code:** 43
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:

    if update.user_team_id is not None:
        settings.user_team_id = update.user_team_id
    if update.difficulty_level is not None:
        settings.difficulty_level = update.difficulty_level

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        settings.user_team_id = update.user_team_id
```


---

### File: `backend/app/api/endpoints/settings.py`
**Lines of Code:** 45
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
        settings.user_team_id = update.user_team_id
    if update.difficulty_level is not None:
        settings.difficulty_level = update.difficulty_level

    db.commit()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
        settings.difficulty_level = update.difficulty_level
```


---

### File: `backend/app/api/endpoints/scouts.py`
**Lines of Code:** 82
**Error:** Argument "scout_id" to "ScoutInfo" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
    scouts = [
        ScoutInfo(
            scout_id=s.id,
            name=s.name,
            region=s.region or "NATIONAL",

# Proposed Fix:
            scout_id=int(s.id),
```


---

### File: `backend/app/api/endpoints/scouts.py`
**Lines of Code:** 83
**Error:** Argument "name" to "ScoutInfo" has incompatible type "Column[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
        ScoutInfo(
            scout_id=s.id,
            name=s.name,
            region=s.region or "NATIONAL",
            specialty=s.position_specialty or "GENERALIST",

# Proposed Fix:
            name=str(s.name),
```


---

### File: `backend/app/api/endpoints/scouts.py`
**Lines of Code:** 84
**Error:** Argument "region" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
            scout_id=s.id,
            name=s.name,
            region=s.region or "NATIONAL",
            specialty=s.position_specialty or "GENERALIST",
            bias=s.bias or "NEUTRAL",

# Proposed Fix:
            region=str(s.region) or "NATIONAL",
```


---

### File: `backend/app/api/endpoints/scouts.py`
**Lines of Code:** 85
**Error:** Argument "specialty" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
            name=s.name,
            region=s.region or "NATIONAL",
            specialty=s.position_specialty or "GENERALIST",
            bias=s.bias or "NEUTRAL",
            efficiency=s.efficiency,

# Proposed Fix:
            specialty=str(s.position_specialty) or "GENERALIST",
```


---

### File: `backend/app/api/endpoints/scouts.py`
**Lines of Code:** 86
**Error:** Argument "bias" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
            region=s.region or "NATIONAL",
            specialty=s.position_specialty or "GENERALIST",
            bias=s.bias or "NEUTRAL",
            efficiency=s.efficiency,
            accuracy=s.evaluation_ability

# Proposed Fix:
            bias=str(s.bias) or "NEUTRAL",
```


---

### File: `backend/app/api/endpoints/scouts.py`
**Lines of Code:** 87
**Error:** Argument "efficiency" to "ScoutInfo" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
            specialty=s.position_specialty or "GENERALIST",
            bias=s.bias or "NEUTRAL",
            efficiency=s.efficiency,
            accuracy=s.evaluation_ability
        )

# Proposed Fix:
            efficiency=int(s.efficiency),
```


---

### File: `backend/app/api/endpoints/scouts.py`
**Lines of Code:** 88
**Error:** Argument "accuracy" to "ScoutInfo" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
            bias=s.bias or "NEUTRAL",
            efficiency=s.efficiency,
            accuracy=s.evaluation_ability
        )
        for s in db_scouts

# Proposed Fix:
            accuracy=int(s.evaluation_ability)
```


---

### File: `backend/app/api/endpoints/playbook.py`
**Lines of Code:** 223
**Error:** Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, object]], object]"; expected "Callable[[dict[str, object]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"  [arg-type]
**Solve:**
```python
# Original Code:

    # Sort by familiarity
    player_familiarity.sort(key=lambda x: x["average_familiarity"], reverse=True)

    total_avg = sum(p["average_familiarity"] for p in player_familiarity) / len(player_familiarity)

# Proposed Fix:
    player_familiarity.sort(key=Callable(lambda) x: x["average_familiarity"], reverse=True)
```


---

### File: `backend/app/api/endpoints/playbook.py`
**Lines of Code:** 223
**Error:** Incompatible return value type (got "object", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")  [return-value]
**Solve:**
```python
# Original Code:

    # Sort by familiarity
    player_familiarity.sort(key=lambda x: x["average_familiarity"], reverse=True)

    total_avg = sum(p["average_familiarity"] for p in player_familiarity) / len(player_familiarity)

# Proposed Fix:
    # FIX: Incompatible return value type (got "object", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")  [return-value]
    player_familiarity.sort(key=lambda x: x["average_familiarity"], reverse=True)
```


---

### File: `backend/app/api/endpoints/playbook.py`
**Lines of Code:** 225
**Error:** Generator has incompatible item type "object"; expected "bool"  [misc]
**Solve:**
```python
# Original Code:
    player_familiarity.sort(key=lambda x: x["average_familiarity"], reverse=True)

    total_avg = sum(p["average_familiarity"] for p in player_familiarity) / len(player_familiarity)

    return {

# Proposed Fix:
    # FIX: Generator has incompatible item type "object"; expected "bool"  [misc]
    total_avg = sum(p["average_familiarity"] for p in player_familiarity) / len(player_familiarity)
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 44
**Error:** Argument "head_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
    return BodyHealthResponse(
        player_id=player_id,
        head_health=health.head_health,
        torso_health=health.torso_health,
        right_arm_health=health.right_arm_health,

# Proposed Fix:
        head_health=float(health.head_health),
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 45
**Error:** Argument "torso_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
        player_id=player_id,
        head_health=health.head_health,
        torso_health=health.torso_health,
        right_arm_health=health.right_arm_health,
        left_arm_health=health.left_arm_health,

# Proposed Fix:
        torso_health=float(health.torso_health),
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 46
**Error:** Argument "right_arm_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
        head_health=health.head_health,
        torso_health=health.torso_health,
        right_arm_health=health.right_arm_health,
        left_arm_health=health.left_arm_health,
        right_leg_health=health.right_leg_health,

# Proposed Fix:
        right_arm_health=float(health.right_arm_health),
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 47
**Error:** Argument "left_arm_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
        torso_health=health.torso_health,
        right_arm_health=health.right_arm_health,
        left_arm_health=health.left_arm_health,
        right_leg_health=health.right_leg_health,
        left_leg_health=health.left_leg_health,

# Proposed Fix:
        left_arm_health=float(health.left_arm_health),
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 48
**Error:** Argument "right_leg_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
        right_arm_health=health.right_arm_health,
        left_arm_health=health.left_arm_health,
        right_leg_health=health.right_leg_health,
        left_leg_health=health.left_leg_health,
        general_wear=health.general_wear,

# Proposed Fix:
        right_leg_health=float(health.right_leg_health),
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 49
**Error:** Argument "left_leg_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
        left_arm_health=health.left_arm_health,
        right_leg_health=health.right_leg_health,
        left_leg_health=health.left_leg_health,
        general_wear=health.general_wear,
        is_injured=player.injury_status != "HEALTHY"

# Proposed Fix:
        left_leg_health=float(health.left_leg_health),
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 50
**Error:** Argument "general_wear" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
        right_leg_health=health.right_leg_health,
        left_leg_health=health.left_leg_health,
        general_wear=health.general_wear,
        is_injured=player.injury_status != "HEALTHY"
    )

# Proposed Fix:
        general_wear=float(health.general_wear),
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 126
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            added_weeks = random.randint(2, 6)
            recovery_weeks += added_weeks
            player.injury_recurrence_risk += 0.10
        else:
            # Successful surgery - reduce recovery by 30-50%

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.injury_recurrence_risk += 0.10
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 132
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            recovery_weeks = max(1, int(recovery_weeks * (1 - reduction)))

        player.weeks_to_recovery = recovery_weeks

    elif treatment == "PLAY_THROUGH":

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.weeks_to_recovery = recovery_weeks
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 153
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        }

        player.injury_status = InjuryStatus.QUESTIONABLE

    else:  # REST

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_status = InjuryStatus.QUESTIONABLE
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 157
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
    else:  # REST
        # Standard recovery - no changes to weeks
        player.injury_status = InjuryStatus.OUT

    db.commit()

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.injury_status = InjuryStatus.OUT
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 191
**Error:** Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[InjuryStatus.ACTIVE]")  [comparison-overlap]
**Solve:**
```python
# Original Code:
    injured_players = db.query(Player).filter(
        Player.team_id == team_id,
        Player.injury_status != InjuryStatus.ACTIVE
    ).all()


# Proposed Fix:
    # FIX: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[InjuryStatus.ACTIVE]")  [comparison-overlap]
        Player.injury_status != InjuryStatus.ACTIVE
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 191
**Error:** Argument 2 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
**Solve:**
```python
# Original Code:
    injured_players = db.query(Player).filter(
        Player.team_id == team_id,
        Player.injury_status != InjuryStatus.ACTIVE
    ).all()


# Proposed Fix:
    # FIX: Argument 2 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
        Player.injury_status != InjuryStatus.ACTIVE
```


---

### File: `backend/app/api/endpoints/data.py`
**Lines of Code:** 26
**Error:** Need type annotation for "state"  [var-annotated]
**Solve:**
```python
# Original Code:

    # Use game_data for transient state not in columns
    state = game.game_data or {}

    # Determine possession string (home/away) from ID if available

# Proposed Fix:
    state: dict[str, float] = game.game_data or {}
```


---

### File: `backend/app/api/endpoints/data.py`
**Lines of Code:** 37
**Error:** Incompatible types in assignment (expression has type "ColumnElement[Any] | Any", variable has type "str")  [assignment]
**Solve:**
```python
# Original Code:
            possession = "home"
    elif "possession" in state:
        possession = state["possession"]

    return {

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[Any] | Any", variable has type "str")  [assignment]
        possession = state["possession"]
```


---

### File: `backend/app/api/endpoints/data.py`
**Lines of Code:** 125
**Error:** No overload variant of "get" of "dict" matches argument types "str", "list[Never]"  [call-overload]
**Solve:**
```python
# Original Code:
    # Assuming logs are in game_data['plays'] or similar
    # If not, return empty list for now
    logs = (game.game_data or {}).get("plays", [])

    return {

# Proposed Fix:
    # FIX: No overload variant of "get" of "dict" matches argument types "str", "list[Never]"  [call-overload]
    logs = (game.game_data or {}).get("plays", [])
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 58
**Error:** Argument "id" to "CoachResponse" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

    return CoachResponse(
        id=coach.id,
        first_name=coach.first_name,
        last_name=coach.last_name,

# Proposed Fix:
        id=int(coach.id),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 59
**Error:** Argument "first_name" to "CoachResponse" has incompatible type "Column[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
    return CoachResponse(
        id=coach.id,
        first_name=coach.first_name,
        last_name=coach.last_name,
        role=coach.role,

# Proposed Fix:
        first_name=str(coach.first_name),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 60
**Error:** Argument "last_name" to "CoachResponse" has incompatible type "Column[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
        id=coach.id,
        first_name=coach.first_name,
        last_name=coach.last_name,
        role=coach.role,
        tier=coach.tier.value if hasattr(coach.tier, 'value') else str(coach.tier),

# Proposed Fix:
        last_name=str(coach.last_name),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 61
**Error:** Argument "role" to "CoachResponse" has incompatible type "Column[str]"; expected "str"  [arg-type]
**Solve:**
```python
# Original Code:
        first_name=coach.first_name,
        last_name=coach.last_name,
        role=coach.role,
        tier=coach.tier.value if hasattr(coach.tier, 'value') else str(coach.tier),
        team_id=coach.team_id,

# Proposed Fix:
        role=str(coach.role),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 63
**Error:** Argument "team_id" to "CoachResponse" has incompatible type "Column[int]"; expected "int | None"  [arg-type]
**Solve:**
```python
# Original Code:
        role=coach.role,
        tier=coach.tier.value if hasattr(coach.tier, 'value') else str(coach.tier),
        team_id=coach.team_id,
        team_name=team_name,
        offense_rating=coach.offense_rating,

# Proposed Fix:
        team_id=int | None(coach.team_id),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 65
**Error:** Argument "offense_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        team_id=coach.team_id,
        team_name=team_name,
        offense_rating=coach.offense_rating,
        defense_rating=coach.defense_rating,
        development_rating=coach.development_rating,

# Proposed Fix:
        offense_rating=int(coach.offense_rating),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 66
**Error:** Argument "defense_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        team_name=team_name,
        offense_rating=coach.offense_rating,
        defense_rating=coach.defense_rating,
        development_rating=coach.development_rating,
        playbook_offense=coach.playbook_offense,

# Proposed Fix:
        defense_rating=int(coach.defense_rating),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 67
**Error:** Argument "development_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        offense_rating=coach.offense_rating,
        defense_rating=coach.defense_rating,
        development_rating=coach.development_rating,
        playbook_offense=coach.playbook_offense,
        playbook_defense=coach.playbook_defense

# Proposed Fix:
        development_rating=int(coach.development_rating),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 68
**Error:** Argument "playbook_offense" to "CoachResponse" has incompatible type "Column[str]"; expected "str | None"  [arg-type]
**Solve:**
```python
# Original Code:
        defense_rating=coach.defense_rating,
        development_rating=coach.development_rating,
        playbook_offense=coach.playbook_offense,
        playbook_defense=coach.playbook_defense
    )

# Proposed Fix:
        playbook_offense=str | None(coach.playbook_offense),
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 69
**Error:** Argument "playbook_defense" to "CoachResponse" has incompatible type "Column[str]"; expected "str | None"  [arg-type]
**Solve:**
```python
# Original Code:
        development_rating=coach.development_rating,
        playbook_offense=coach.playbook_offense,
        playbook_defense=coach.playbook_defense
    )


# Proposed Fix:
        playbook_defense=str | None(coach.playbook_defense)
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 129
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        raise HTTPException(status_code=400, detail="Coach is already employed")

    team = db.query(Team).filter(Team.id == request.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
    team = db.query(Team).filter(Team.id == request.team_id).first()
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 165
**Error:** Incompatible types in assignment (expression has type "None", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:

    team_id = coach.team_id
    coach.team_id = None
    db.commit()


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "None", variable has type "Column[int]")  [assignment]
    coach.team_id = None
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 208
**Error:** Incompatible types in assignment (expression has type "None", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:

        if current_hc and current_hc.id != coach_id:
            current_hc.team_id = None  # Fire

        coach.role = "Head Coach"

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "None", variable has type "Column[int]")  [assignment]
            current_hc.team_id = None  # Fire
```


---

### File: `backend/app/api/endpoints/coaches.py`
**Lines of Code:** 210
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
            current_hc.team_id = None  # Fire

        coach.role = "Head Coach"
        db.commit()


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
        coach.role = "Head Coach"
```


---

### File: `backend/app/orchestrator/match_context.py`
**Lines of Code:** 25
**Error:** Incompatible default for argument "weather_config" (default has type "None", argument has type "dict[Any, Any]")  [assignment]
**Solve:**
```python
# Original Code:
    """

    def __init__(self, home_team_id: int, away_team_id: int, db: AsyncSession, weather_config: Dict = None):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id

# Proposed Fix:
    # FIX: Incompatible default for argument "weather_config" (default has type "None", argument has type "dict[Any, Any]")  [assignment]
    def __init__(self, home_team_id: int, away_team_id: int, db: AsyncSession, weather_config: Dict = None):
```


---

### File: `backend/app/orchestrator/match_context.py`
**Lines of Code:** 77
**Error:** "Player" has no attribute "active_traits"  [attr-defined]
**Solve:**
```python
# Original Code:
        # Flatten traits to active_traits list for efficient access during game loop
        for p in list(self.home_roster.values()) + list(self.away_roster.values()):
            p.active_traits = [pt.trait.name for pt in p.player_traits if pt.trait]

        # Initialize fatigue for all players

# Proposed Fix:
    # FIX: "Player" has no attribute "active_traits"  [attr-defined]
            p.active_traits = [pt.trait.name for pt in p.player_traits if pt.trait]
```


---

### File: `backend/app/engine/probability_engine.py`
**Lines of Code:** 162
**Error:** Returning Any from function declared to return "bool"  [no-any-return]
**Solve:**
```python
# Original Code:
        Resolve a boolean outcome based on probability.
        """
        return rng.random() < probability

    @staticmethod

# Proposed Fix:
    # FIX: Returning Any from function declared to return "bool"  [no-any-return]
        return rng.random() < probability
```


---

### File: `backend/app/engine/probability_engine.py`
**Lines of Code:** 211
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
        """
        random_factor = rng.uniform(-variance, variance)
        return base_value + random_factor + modifiers

    @staticmethod

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
        return base_value + random_factor + modifiers
```


---

### File: `backend/app/engine/probability_engine.py`
**Lines of Code:** 226
**Error:** Returning Any from function declared to return "float"  [no-any-return]
**Solve:**
```python
# Original Code:
        """
        val = rng.gauss(mean, std_dev)
        return max(min_val, min(max_val, val))

# Proposed Fix:
    # FIX: Returning Any from function declared to return "float"  [no-any-return]
        return max(min_val, min(max_val, val))
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 79
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"  [union-attr]
**Solve:**
```python
# Original Code:

    return {
        "games_played": stats.games_played or 0,
        "passing_yards": stats.passing_yards or 0,
        "passing_tds": stats.passing_tds or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"  [union-attr]
        "games_played": stats.games_played or 0,
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 80
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_yards"  [union-attr]
**Solve:**
```python
# Original Code:
    return {
        "games_played": stats.games_played or 0,
        "passing_yards": stats.passing_yards or 0,
        "passing_tds": stats.passing_tds or 0,
        "rushing_yards": stats.rushing_yards or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_yards"  [union-attr]
        "passing_yards": stats.passing_yards or 0,
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 81
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_tds"  [union-attr]
**Solve:**
```python
# Original Code:
        "games_played": stats.games_played or 0,
        "passing_yards": stats.passing_yards or 0,
        "passing_tds": stats.passing_tds or 0,
        "rushing_yards": stats.rushing_yards or 0,
        "rushing_tds": stats.rushing_tds or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_tds"  [union-attr]
        "passing_tds": stats.passing_tds or 0,
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 82
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_yards"  [union-attr]
**Solve:**
```python
# Original Code:
        "passing_yards": stats.passing_yards or 0,
        "passing_tds": stats.passing_tds or 0,
        "rushing_yards": stats.rushing_yards or 0,
        "rushing_tds": stats.rushing_tds or 0,
        "receiving_yards": stats.receiving_yards or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_yards"  [union-attr]
        "rushing_yards": stats.rushing_yards or 0,
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 83
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_tds"  [union-attr]
**Solve:**
```python
# Original Code:
        "passing_tds": stats.passing_tds or 0,
        "rushing_yards": stats.rushing_yards or 0,
        "rushing_tds": stats.rushing_tds or 0,
        "receiving_yards": stats.receiving_yards or 0,
        "receiving_tds": stats.receiving_tds or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_tds"  [union-attr]
        "rushing_tds": stats.rushing_tds or 0,
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 84
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_yards"  [union-attr]
**Solve:**
```python
# Original Code:
        "rushing_yards": stats.rushing_yards or 0,
        "rushing_tds": stats.rushing_tds or 0,
        "receiving_yards": stats.receiving_yards or 0,
        "receiving_tds": stats.receiving_tds or 0,
    }

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_yards"  [union-attr]
        "receiving_yards": stats.receiving_yards or 0,
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 85
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_tds"  [union-attr]
**Solve:**
```python
# Original Code:
        "rushing_tds": stats.rushing_tds or 0,
        "receiving_yards": stats.receiving_yards or 0,
        "receiving_tds": stats.receiving_tds or 0,
    }


# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_tds"  [union-attr]
        "receiving_tds": stats.receiving_tds or 0,
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 271
**Error:** "type[Player]" has no attribute "traits"  [attr-defined]
**Solve:**
```python
# Original Code:

    # Get player with traits
    stmt = select(Player).options(selectinload(Player.traits)).where(Player.id == player_id)
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: "type[Player]" has no attribute "traits"  [attr-defined]
    stmt = select(Player).options(selectinload(Player.traits)).where(Player.id == player_id)
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 279
**Error:** Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"  [arg-type]
**Solve:**
```python
# Original Code:

    # Get trait definitions
    trait_service = TraitService(db)
    traits_data = await trait_service.get_player_traits(player_id)
    traits_brief = [

# Proposed Fix:
    # FIX: Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"  [arg-type]
    trait_service = TraitService(db)
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 280
**Error:** Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")  [misc]
**Solve:**
```python
# Original Code:
    # Get trait definitions
    trait_service = TraitService(db)
    traits_data = await trait_service.get_player_traits(player_id)
    traits_brief = [
        TraitInfoBrief(

# Proposed Fix:
    # FIX: Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")  [misc]
    traits_data = await trait_service.get_player_traits(player_id)
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 280
**Error:** Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"  [call-arg]
**Solve:**
```python
# Original Code:
    # Get trait definitions
    trait_service = TraitService(db)
    traits_data = await trait_service.get_player_traits(player_id)
    traits_brief = [
        TraitInfoBrief(

# Proposed Fix:
    # FIX: Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"  [call-arg]
    traits_data = await trait_service.get_player_traits(player_id)
```


---

### File: `backend/app/api/endpoints/players.py`
**Lines of Code:** 280
**Error:** Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"  [arg-type]
**Solve:**
```python
# Original Code:
    # Get trait definitions
    trait_service = TraitService(db)
    traits_data = await trait_service.get_player_traits(player_id)
    traits_brief = [
        TraitInfoBrief(

# Proposed Fix:
    # FIX: Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"  [arg-type]
    traits_data = await trait_service.get_player_traits(player_id)
```


---

### File: `backend/app/api/endpoints/abilities.py`
**Lines of Code:** 41
**Error:** Name "AbilityStatus" already defined (possibly by an import)  [no-redef]
**Solve:**
```python
# Original Code:


class AbilityStatus(BaseModel):
    """Status of an ability for a player."""
    key: str

# Proposed Fix:
    # FIX: Name "AbilityStatus" already defined (possibly by an import)  [no-redef]
class AbilityStatus(BaseModel):
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 261
**Error:** Need type annotation for "games_data" (hint: "games_data: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:

        # OPTIMIZATION 2: Group by game_id in memory (no additional queries)
        games_data = {}
        for game_id, week, position, player_id in rows:
            if game_id not in games_data:

# Proposed Fix:
        games_data: dict[str, float] = {}
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 357
**Error:** Incompatible types in assignment (expression has type "ChemistryMetadata | None", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:

        # Store metadata in match context for PlayResolver access
        match_context.home_ol_chemistry = home_chemistry
        match_context.away_ol_chemistry = away_chemistry


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ChemistryMetadata | None", variable has type "int")  [assignment]
        match_context.home_ol_chemistry = home_chemistry
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 358
**Error:** Incompatible types in assignment (expression has type "ChemistryMetadata | None", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
        # Store metadata in match context for PlayResolver access
        match_context.home_ol_chemistry = home_chemistry
        match_context.away_ol_chemistry = away_chemistry

        return home_chemistry, away_chemistry

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ChemistryMetadata | None", variable has type "int")  [assignment]
        match_context.away_ol_chemistry = away_chemistry
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 400
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
                if player:
                    if not hasattr(player, "active_modifiers"):
                        player.active_modifiers = {}

                    # Apply scaled bonuses

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                        player.active_modifiers = {}
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 404
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
                    # Apply scaled bonuses
                    for attr, bonus in chemistry.bonuses.items():
                        player.active_modifiers[attr] = (
                            player.active_modifiers.get(attr, 0) + bonus
                        )

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                        player.active_modifiers[attr] = (
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 405
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
                    for attr, bonus in chemistry.bonuses.items():
                        player.active_modifiers[attr] = (
                            player.active_modifiers.get(attr, 0) + bonus
                        )


# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                            player.active_modifiers.get(attr, 0) + bonus
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 410
**Error:** "Player" has no attribute "chemistry_effects"  [attr-defined]
**Solve:**
```python
# Original Code:
                    # Store advanced effects metadata
                    if not hasattr(player, "chemistry_effects"):
                        player.chemistry_effects = {}

                    player.chemistry_effects = chemistry.advanced_effects

# Proposed Fix:
    # FIX: "Player" has no attribute "chemistry_effects"  [attr-defined]
                        player.chemistry_effects = {}
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 412
**Error:** "Player" has no attribute "chemistry_effects"  [attr-defined]
**Solve:**
```python
# Original Code:
                        player.chemistry_effects = {}

                    player.chemistry_effects = chemistry.advanced_effects

        return chemistry

# Proposed Fix:
    # FIX: "Player" has no attribute "chemistry_effects"  [attr-defined]
                    player.chemistry_effects = chemistry.advanced_effects
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 130
**Error:** Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        else:
            # Add resolvers for other command types here
            context = {}
            if self.current_match_context and self.current_match_context.weather_config:
                context["weather"] = self.current_match_context.weather_config

# Proposed Fix:
            context: dict[str, float] = {}
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 131
**Error:** Right operand of "and" is never evaluated  [unreachable]
**Solve:**
```python
# Original Code:
            # Add resolvers for other command types here
            context = {}
            if self.current_match_context and self.current_match_context.weather_config:
                context["weather"] = self.current_match_context.weather_config
            result = command.execute(context, rng=self.rng)

# Proposed Fix:
    # FIX: Right operand of "and" is never evaluated  [unreachable]
            if self.current_match_context and self.current_match_context.weather_config:
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 132
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
            context = {}
            if self.current_match_context and self.current_match_context.weather_config:
                context["weather"] = self.current_match_context.weather_config
            result = command.execute(context, rng=self.rng)


# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
                context["weather"] = self.current_match_context.weather_config
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 138
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        # Called AFTER play outcome is finalized for determinism
        if result and self.current_match_context:
            play_context = self._build_injury_play_context(command, result)
            players = (command.offense or []) + (command.defense or [])
            if players:

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            play_context = self._build_injury_play_context(command, result)
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 173
**Error:** Right operand of "and" is never evaluated  [unreachable]
**Solve:**
```python
# Original Code:

    def _get_weather_temp(self) -> float:
        if self.current_match_context and self.current_match_context.weather_config:
            return self.current_match_context.weather_config.get("temperature", 75.0)
        return 75.0

# Proposed Fix:
    # FIX: Right operand of "and" is never evaluated  [unreachable]
        if self.current_match_context and self.current_match_context.weather_config:
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 174
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
    def _get_weather_temp(self) -> float:
        if self.current_match_context and self.current_match_context.weather_config:
            return self.current_match_context.weather_config.get("temperature", 75.0)
        return 75.0


# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            return self.current_match_context.weather_config.get("temperature", 75.0)
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 198
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        medical_rating = 50
        if self.current_match_context:
            medical_rating = getattr(self.current_match_context, "medical_staff_rating", 50)

        # Get average fatigue from the players involved

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            medical_rating = getattr(self.current_match_context, "medical_staff_rating", 50)
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 221
**Error:** Right operand of "or" is never evaluated  [unreachable]
**Solve:**
```python
# Original Code:

    def _get_weather_effects(self) -> Optional[WeatherEffects]:
        if not self.current_match_context or not self.current_match_context.weather_config:
            return None


# Proposed Fix:
    # FIX: Right operand of "or" is never evaluated  [unreachable]
        if not self.current_match_context or not self.current_match_context.weather_config:
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 224
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
            return None

        config = self.current_match_context.weather_config
        weather = GameWeather(
            temperature=config.get("temperature", 75.0),

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
        config = self.current_match_context.weather_config
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 309
**Error:** Unexpected keyword argument "ratings" for "WideReceiverPhysics"  [call-arg]
**Solve:**
```python
# Original Code:
            "forty_time": 4.45
        }
        return WideReceiverPhysics(
            ratings=ratings,
            height_inches=getattr(wr, "height", 72),

# Proposed Fix:
    # FIX: Unexpected keyword argument "ratings" for "WideReceiverPhysics"  [call-arg]
        return WideReceiverPhysics(
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 309
**Error:** Unexpected keyword argument "hand_size" for "WideReceiverPhysics"  [call-arg]
**Solve:**
```python
# Original Code:
            "forty_time": 4.45
        }
        return WideReceiverPhysics(
            ratings=ratings,
            height_inches=getattr(wr, "height", 72),

# Proposed Fix:
    # FIX: Unexpected keyword argument "hand_size" for "WideReceiverPhysics"  [call-arg]
        return WideReceiverPhysics(
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 331
**Error:** Unexpected keyword argument "ratings" for "RunningBackPhysics"  [call-arg]
**Solve:**
```python
# Original Code:
            "forty_time": 4.5
        }
        return RunningBackPhysics(
            ratings=ratings,
            weight=float(getattr(rb, "weight", 210)),

# Proposed Fix:
    # FIX: Unexpected keyword argument "ratings" for "RunningBackPhysics"  [call-arg]
        return RunningBackPhysics(
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 333
**Error:** Argument "weight" to "RunningBackPhysics" has incompatible type "float"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        return RunningBackPhysics(
            ratings=ratings,
            weight=float(getattr(rb, "weight", 210)),
        )


# Proposed Fix:
            weight=int(float(getattr(rb), "weight", 210)),
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 352
**Error:** Unexpected keyword argument "ratings" for "DefensiveBackPhysics"  [call-arg]
**Solve:**
```python
# Original Code:
            "strength": getattr(db, "strength", 60)
        }
        return DefensiveBackPhysics(ratings=ratings)

    def _calculate_physics_separation(

# Proposed Fix:
    # FIX: Unexpected keyword argument "ratings" for "DefensiveBackPhysics"  [call-arg]
        return DefensiveBackPhysics(ratings=ratings)
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 441
**Error:** Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
            Dictionary with aggregate modifiers and narratives
        """
        context = {}

        # Build game context for interactions

# Proposed Fix:
        context: dict[str, float] = {}
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 446
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        # Note: command may not have all these attributes, so we use getattr with defaults
        if self.current_match_context:
            context = {
                "HOME": getattr(command, "is_home_team", False),
                "AWAY": not getattr(command, "is_home_team", False),

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            context = {
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 507
**Error:** Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
            Dictionary with aggregate modifiers and narratives
        """
        context = {}

        # Build game context for interactions

# Proposed Fix:
        context: dict[str, float] = {}
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 511
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        # Build game context for interactions
        if self.current_match_context:
            context = {
                "HOME": getattr(command, "is_home_team", False),
                "AWAY": not getattr(command, "is_home_team", False),

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            context = {
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 656
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
            chem_bonus = 0
            if self.current_match_context:
                 if getattr(command, "is_home_team", True):
                     chem_bonus = getattr(self.current_match_context, "home_ol_chemistry", 0)
                 else:

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
                 if getattr(command, "is_home_team", True):
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 724
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        # Safety check: ensure results are valid
        if interaction_results is None or not isinstance(interaction_results, dict):
            interaction_results = {
                "total_offense_boost": 0.0,
                "total_defense_boost": 0.0,

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            interaction_results = {
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 861
**Error:** Need type annotation for "crunch_context" (hint: "crunch_context: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:

            # Build crunch time context from match context
            crunch_context = {}
            if self.current_match_context:
                crunch_context = {

# Proposed Fix:
            crunch_context: dict[str, float] = {}
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 863
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
            crunch_context = {}
            if self.current_match_context:
                crunch_context = {
                    "quarter": getattr(self.current_match_context, "quarter", 1),
                    "time_remaining": getattr(self.current_match_context, "time_remaining", 900),

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
                crunch_context = {
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 919
**Error:** Right operand of "and" is never evaluated  [unreachable]
**Solve:**
```python
# Original Code:
        # B-007: Apply momentum modifier to success chance
        momentum_modifier = 0.0
        if self.momentum_engine and self.current_match_context:
            # Determine offense team ID
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))

# Proposed Fix:
    # FIX: Right operand of "and" is never evaluated  [unreachable]
        if self.momentum_engine and self.current_match_context:
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 921
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        if self.momentum_engine and self.current_match_context:
            # Determine offense team ID
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
            if hasattr(command, 'is_home_team') and not command.is_home_team:
                offense_team_id = str(getattr(self.current_match_context, 'away_team_id', 'away'))

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 1184
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        # Safety check: ensure results are valid
        if interaction_results is None or not isinstance(interaction_results, dict):
            interaction_results = {
                "total_offense_boost": 0.0,
                "total_defense_boost": 0.0,

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            interaction_results = {
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 1310
**Error:** Right operand of "and" is never evaluated  [unreachable]
**Solve:**
```python
# Original Code:
        # B-008: Apply momentum modifier to run play
        momentum_yards_bonus = 0.0
        if self.momentum_engine and self.current_match_context:
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
            raw_modifier = self.momentum_engine.get_performance_modifier(offense_team_id)

# Proposed Fix:
    # FIX: Right operand of "and" is never evaluated  [unreachable]
        if self.momentum_engine and self.current_match_context:
```


---

### File: `backend/app/orchestrator/play_resolver.py`
**Lines of Code:** 1311
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        momentum_yards_bonus = 0.0
        if self.momentum_engine and self.current_match_context:
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
            raw_modifier = self.momentum_engine.get_performance_modifier(offense_team_id)
            # Convert to yards bonus: 1.1 -> +0.5 yards, 0.9 -> -0.5 yards

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 12
**Error:** Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker  [import-untyped]
**Solve:**
```python
# Original Code:

try:
    import nflreadpy as nfl
    import polars as pl
    HAS_NFLREADPY = True

# Proposed Fix:
    # FIX: Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker  [import-untyped]
    import nflreadpy as nfl
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 120
**Error:** Returning Any from function declared to return "DataFrame"  [no-any-return]
**Solve:**
```python
# Original Code:
        self._rosters_cache = df
        logger.info(f"Loaded {len(df)} roster entries.")
        return df

    def import_nextgen_stats(self) -> pl.DataFrame:

# Proposed Fix:
    # FIX: Returning Any from function declared to return "DataFrame"  [no-any-return]
        return df
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 137
**Error:** Returning Any from function declared to return "DataFrame"  [no-any-return]
**Solve:**
```python
# Original Code:
            self._nextgen_cache = df
            logger.info(f"Loaded {len(df)} Next Gen Stats entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load Next Gen Stats: {e}")

# Proposed Fix:
    # FIX: Returning Any from function declared to return "DataFrame"  [no-any-return]
            return df
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 157
**Error:** Returning Any from function declared to return "DataFrame"  [no-any-return]
**Solve:**
```python
# Original Code:
            self._combine_cache = df
            logger.info(f"Loaded {len(df)} Combine entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load Combine data: {e}")

# Proposed Fix:
    # FIX: Returning Any from function declared to return "DataFrame"  [no-any-return]
            return df
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 177
**Error:** Returning Any from function declared to return "DataFrame"  [no-any-return]
**Solve:**
```python
# Original Code:
            self._ftn_cache = df
            logger.info(f"Loaded {len(df)} FTN charting entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load FTN charting: {e}")

# Proposed Fix:
    # FIX: Returning Any from function declared to return "DataFrame"  [no-any-return]
            return df
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 197
**Error:** Returning Any from function declared to return "DataFrame"  [no-any-return]
**Solve:**
```python
# Original Code:
            self._player_stats_cache = df
            logger.info(f"Loaded {len(df)} player stats entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load player stats: {e}")

# Proposed Fix:
    # FIX: Returning Any from function declared to return "DataFrame"  [no-any-return]
            return df
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 217
**Error:** Returning Any from function declared to return "DataFrame"  [no-any-return]
**Solve:**
```python
# Original Code:
            self._contracts_cache = df
            logger.info(f"Loaded {len(df)} contract entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load contracts: {e}")

# Proposed Fix:
    # FIX: Returning Any from function declared to return "DataFrame"  [no-any-return]
            return df
```


---

### File: `backend/app/core/mcp_client.py`
**Lines of Code:** 40
**Error:** Item "None" of "ClientSession | None" has no attribute "initialize"  [union-attr]
**Solve:**
```python
# Original Code:

            # Initialize session
            await self.session.initialize()
            logger.info(f"Connected to MCP server: {self.name}")


# Proposed Fix:
    # FIX: Item "None" of "ClientSession | None" has no attribute "initialize"  [union-attr]
            await self.session.initialize()
```


---

### File: `backend/app/core/mcp_client.py`
**Lines of Code:** 44
**Error:** Item "None" of "ClientSession | None" has no attribute "list_tools"  [union-attr]
**Solve:**
```python
# Original Code:

            # List tools
            result = await self.session.list_tools()
            self._tools = result.tools
            logger.info(f"Discovered {len(self._tools)} tools for server {self.name}")

# Proposed Fix:
    # FIX: Item "None" of "ClientSession | None" has no attribute "list_tools"  [union-attr]
            result = await self.session.list_tools()
```


---

### File: `backend/app/core/mcp_client.py`
**Lines of Code:** 121
**Error:** Subclass of "CallToolResult" and "dict[Any, Any]" cannot exist: would have incompatible method signatures  [unreachable]
**Solve:**
```python
# Original Code:

            # Audit Log: Response
            sanitized_result = self._sanitize(result) if isinstance(result, (dict, list)) else str(result)
            logger.info(f"MCP Tool Call Response - Server: {self.name}, Tool: {tool_name}, Duration: {duration:.4f}s, Result: {sanitized_result}")


# Proposed Fix:
    # FIX: Subclass of "CallToolResult" and "dict[Any, Any]" cannot exist: would have incompatible method signatures  [unreachable]
            sanitized_result = self._sanitize(result) if isinstance(result, (dict, list)) else str(result)
```


---

### File: `backend/app/core/mcp_client.py`
**Lines of Code:** 121
**Error:** Subclass of "CallToolResult" and "list[Any]" cannot exist: would have incompatible method signatures  [unreachable]
**Solve:**
```python
# Original Code:

            # Audit Log: Response
            sanitized_result = self._sanitize(result) if isinstance(result, (dict, list)) else str(result)
            logger.info(f"MCP Tool Call Response - Server: {self.name}, Tool: {tool_name}, Duration: {duration:.4f}s, Result: {sanitized_result}")


# Proposed Fix:
    # FIX: Subclass of "CallToolResult" and "list[Any]" cannot exist: would have incompatible method signatures  [unreachable]
            sanitized_result = self._sanitize(result) if isinstance(result, (dict, list)) else str(result)
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 18
**Error:** Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"  [arg-type]
**Solve:**
```python
# Original Code:
        self.db = db
        self.enhanced_chemistry = EnhancedChemistryService(db)
        self.trait_service = TraitService(db)  # NEW: Trait service

    async def apply_chemistry_boosts(self, match_context: MatchContext):

# Proposed Fix:
    # FIX: Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"  [arg-type]
        self.trait_service = TraitService(db)  # NEW: Trait service
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 58
**Error:** Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")  [misc]
**Solve:**
```python
# Original Code:
        for player_id, player in roster.items():
            # Get player's traits
            trait_defs = await self.trait_service.get_player_traits(player_id)

            if not trait_defs:

# Proposed Fix:
    # FIX: Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")  [misc]
            trait_defs = await self.trait_service.get_player_traits(player_id)
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 58
**Error:** Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"  [call-arg]
**Solve:**
```python
# Original Code:
        for player_id, player in roster.items():
            # Get player's traits
            trait_defs = await self.trait_service.get_player_traits(player_id)

            if not trait_defs:

# Proposed Fix:
    # FIX: Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"  [call-arg]
            trait_defs = await self.trait_service.get_player_traits(player_id)
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 58
**Error:** Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"  [arg-type]
**Solve:**
```python
# Original Code:
        for player_id, player in roster.items():
            # Get player's traits
            trait_defs = await self.trait_service.get_player_traits(player_id)

            if not trait_defs:

# Proposed Fix:
    # FIX: Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"  [arg-type]
            trait_defs = await self.trait_service.get_player_traits(player_id)
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 65
**Error:** "Player" has no attribute "active_traits"  [attr-defined]
**Solve:**
```python
# Original Code:
            # Initialize trait storage on player
            if not hasattr(player, "active_traits"):
                player.active_traits = []
            if not hasattr(player, "trait_effects"):
                player.trait_effects = {}

# Proposed Fix:
    # FIX: "Player" has no attribute "active_traits"  [attr-defined]
                player.active_traits = []
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 67
**Error:** "Player" has no attribute "trait_effects"  [attr-defined]
**Solve:**
```python
# Original Code:
                player.active_traits = []
            if not hasattr(player, "trait_effects"):
                player.trait_effects = {}

            # Apply each trait

# Proposed Fix:
    # FIX: "Player" has no attribute "trait_effects"  [attr-defined]
                player.trait_effects = {}
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 71
**Error:** "Player" has no attribute "active_traits"  [attr-defined]
**Solve:**
```python
# Original Code:
            # Apply each trait
            for trait_def in trait_defs:
                player.active_traits.append(trait_def.name)

                # Check if trait is active (simplified - assume ON_FIELD traits are active)

# Proposed Fix:
    # FIX: "Player" has no attribute "active_traits"  [attr-defined]
                player.active_traits.append(trait_def.name)
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 77
**Error:** "Player" has no attribute "trait_effects"  [attr-defined]
**Solve:**
```python
# Original Code:
                    # Apply individual effects
                    for effect_key, effect_value in trait_def.effects.items():
                        player.trait_effects[effect_key] = effect_value

                    # Track team-wide traits

# Proposed Fix:
    # FIX: "Player" has no attribute "trait_effects"  [attr-defined]
                        player.trait_effects[effect_key] = effect_value
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 101
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
            if player.position in ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT"]:
                if not hasattr(player, "active_modifiers"):
                    player.active_modifiers = {}

                # +5 awareness to all offensive players

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                    player.active_modifiers = {}
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 104
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:

                # +5 awareness to all offensive players
                player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5
                logger.debug(f"Field General boost applied to {player.last_name} ({player.position})")


# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 113
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
            if player.position in ["DE", "DT", "LB", "CB", "S"]:
                if not hasattr(player, "active_modifiers"):
                    player.active_modifiers = {}

                # +5 play recognition to all defenders

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                    player.active_modifiers = {}
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 116
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:

                # +5 play recognition to all defenders
                player.active_modifiers["play_recognition"] = player.active_modifiers.get("play_recognition", 0) + 5
                logger.debug(f"Green Dot boost applied to {player.last_name} ({player.position})")


# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                player.active_modifiers["play_recognition"] = player.active_modifiers.get("play_recognition", 0) + 5
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 156
**Error:** Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStart]]", variable has type "Select[tuple[Game]]")  [assignment]
**Solve:**
```python
# Original Code:
        for game in last_games:
            # Check if the SAME players started at the SAME positions in this game
            stmt = select(PlayerGameStart).filter(
                PlayerGameStart.game_id == game.id,
                PlayerGameStart.team_id == team_id,

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStart]]", variable has type "Select[tuple[Game]]")  [assignment]
            stmt = select(PlayerGameStart).filter(
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 165
**Error:** "Game" has no attribute "position"  [attr-defined]
**Solve:**
```python
# Original Code:

            # Convert to map
            game_starters = {s.position: s.player_id for s in starts}

            # Compare with current

# Proposed Fix:
    # FIX: "Game" has no attribute "position"  [attr-defined]
            game_starters = {s.position: s.player_id for s in starts}
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 165
**Error:** "Game" has no attribute "player_id"  [attr-defined]
**Solve:**
```python
# Original Code:

            # Convert to map
            game_starters = {s.position: s.player_id for s in starts}

            # Compare with current

# Proposed Fix:
    # FIX: "Game" has no attribute "player_id"  [attr-defined]
            game_starters = {s.position: s.player_id for s in starts}
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 188
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
                if player:
                    if not hasattr(player, "active_modifiers"):
                        player.active_modifiers = {}

                    # Boost Attributes

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                        player.active_modifiers = {}
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 192
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
                    # Boost Attributes
                    # Using a simple +5 for now as per example
                    player.active_modifiers["pass_block"] = player.active_modifiers.get("pass_block", 0) + 5
                    player.active_modifiers["run_block"] = player.active_modifiers.get("run_block", 0) + 5
                    player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                    player.active_modifiers["pass_block"] = player.active_modifiers.get("pass_block", 0) + 5
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 193
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
                    # Using a simple +5 for now as per example
                    player.active_modifiers["pass_block"] = player.active_modifiers.get("pass_block", 0) + 5
                    player.active_modifiers["run_block"] = player.active_modifiers.get("run_block", 0) + 5
                    player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5


# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                    player.active_modifiers["run_block"] = player.active_modifiers.get("run_block", 0) + 5
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 194
**Error:** "Player" has no attribute "active_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
                    player.active_modifiers["pass_block"] = player.active_modifiers.get("pass_block", 0) + 5
                    player.active_modifiers["run_block"] = player.active_modifiers.get("run_block", 0) + 5
                    player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5

    async def record_starters(self, game_id: int, home_team_id: int, away_team_id: int):

# Proposed Fix:
    # FIX: "Player" has no attribute "active_modifiers"  [attr-defined]
                    player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5
```


---

### File: `backend/app/services/pre_game_service.py`
**Lines of Code:** 230
**Error:** Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStart]]", variable has type "Select[tuple[Player]]")  [assignment]
**Solve:**
```python
# Original Code:
            if pos in ol_positions:
                # Check if already recorded
                stmt = select(PlayerGameStart).filter(
                    PlayerGameStart.game_id == game.id,
                    PlayerGameStart.team_id == team_id,

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStart]]", variable has type "Select[tuple[Player]]")  [assignment]
                stmt = select(PlayerGameStart).filter(
```


---

### File: `backend/app/api/endpoints/teams.py`
**Lines of Code:** 213
**Error:** Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:

    # Explicit reassignment to ensure SQLAlchemy tracks change
    head_coach.philosophy = current_philosophy

    await db.commit()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "Column[Any]")  [assignment]
    head_coach.philosophy = current_philosophy
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 144
**Error:** Argument 2 to "generate_player" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        for pos, count in POSITIONS.items():
            for _ in range(count):
                player = generate_player(pos, team.id)
                all_players.append(player)


# Proposed Fix:
    # FIX: Argument 2 to "generate_player" has incompatible type "Column[Any]"; expected "int"  [arg-type]
                player = generate_player(pos, team.id)
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 294
**Error:** Argument 1 to "calculate_overall_rating_modifier" has incompatible type "float | int"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        base_rating = sum(ratings.values()) / len(ratings) if ratings else 70
        accolades = PLAYER_ACCOMPLISHMENTS.get((p_data.get("first_name"), p_data.get("last_name")))
        final_overall = calculate_overall_rating_modifier(base_rating, p_data, accolades)

        # Helper function for safe int conversion

# Proposed Fix:
    # FIX: Argument 1 to "calculate_overall_rating_modifier" has incompatible type "float | int"; expected "int"  [arg-type]
        final_overall = calculate_overall_rating_modifier(base_rating, p_data, accolades)
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 383
**Error:** No overload variant of "get" of "dict" matches argument type "str"  [call-overload]
**Solve:**
```python
# Original Code:

    for fa in FREE_AGENT_SIGNINGS_2025:
        team_id = team_lookup.get(fa.new_team)
        if not team_id:
            logger.warning(f"Unknown team {fa.new_team} for {fa.first_name} {fa.last_name}")

# Proposed Fix:
    # FIX: No overload variant of "get" of "dict" matches argument type "str"  [call-overload]
        team_id = team_lookup.get(fa.new_team)
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 397
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            # Update existing player with new team and ratings
            existing.team_id = team_id
            existing.contract_years = fa.contract_years
            existing.contract_salary = fa.apy
            existing.overall_rating = fa.overall_rating

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            existing.contract_years = fa.contract_years
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 398
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            existing.team_id = team_id
            existing.contract_years = fa.contract_years
            existing.contract_salary = fa.apy
            existing.overall_rating = fa.overall_rating
            if fa.speed:

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            existing.contract_salary = fa.apy
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 401
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            existing.overall_rating = fa.overall_rating
            if fa.speed:
                existing.speed = fa.speed
            if fa.strength:
                existing.strength = fa.strength

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                existing.speed = fa.speed
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 403
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
                existing.speed = fa.speed
            if fa.strength:
                existing.strength = fa.strength
            if fa.awareness:
                existing.awareness = fa.awareness

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                existing.strength = fa.strength
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 405
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
                existing.strength = fa.strength
            if fa.awareness:
                existing.awareness = fa.awareness
            players_updated += 1
        else:

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                existing.awareness = fa.awareness
```


---

### File: `backend/app/services/ai/gemini_client.py`
**Lines of Code:** 67
**Error:** Unused "type: ignore" comment  [unused-ignore]
**Solve:**
```python
# Original Code:
        try:
            from google import genai
            from google.genai.types import HttpOptions  # type: ignore[import-not-found]

            # Initialize client with API key

# Proposed Fix:
    # FIX: Unused "type: ignore" comment  [unused-ignore]
            from google.genai.types import HttpOptions  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/ai/gemini_client.py`
**Lines of Code:** 113
**Error:** Unused "type: ignore" comment  [unused-ignore]
**Solve:**
```python
# Original Code:

        try:
            from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]

            response = self._client.models.generate_content(

# Proposed Fix:
    # FIX: Unused "type: ignore" comment  [unused-ignore]
            from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/ai/gemini_client.py`
**Lines of Code:** 115
**Error:** Item "None" of "Any | None" has no attribute "models"  [union-attr]
**Solve:**
```python
# Original Code:
            from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]

            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,

# Proposed Fix:
    # FIX: Item "None" of "Any | None" has no attribute "models"  [union-attr]
            response = self._client.models.generate_content(
```


---

### File: `backend/app/services/ai/gemini_client.py`
**Lines of Code:** 123
**Error:** Returning Any from function declared to return "str | None"  [no-any-return]
**Solve:**
```python
# Original Code:
                )
            )
            return response.text

        except Exception as e:

# Proposed Fix:
    # FIX: Returning Any from function declared to return "str | None"  [no-any-return]
            return response.text
```


---

### File: `backend/app/services/ai/gemini_client.py`
**Lines of Code:** 154
**Error:** Unused "type: ignore" comment  [unused-ignore]
**Solve:**
```python
# Original Code:

        try:
            from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]

            # Build JSON schema from Pydantic model

# Proposed Fix:
    # FIX: Unused "type: ignore" comment  [unused-ignore]
            from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/ai/gemini_client.py`
**Lines of Code:** 159
**Error:** Item "None" of "Any | None" has no attribute "models"  [union-attr]
**Solve:**
```python
# Original Code:
            json_schema = response_schema.model_json_schema()

            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,

# Proposed Fix:
    # FIX: Item "None" of "Any | None" has no attribute "models"  [union-attr]
            response = self._client.models.generate_content(
```


---

### File: `backend/app/services/ai/gemini_client.py`
**Lines of Code:** 205
**Error:** Incompatible types in assignment (expression has type "str | None", variable has type "T | None")  [assignment]
**Solve:**
```python
# Original Code:
                    )
                else:
                    result = await self.generate_text(prompt, temperature)

                if result is not None:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str | None", variable has type "T | None")  [assignment]
                    result = await self.generate_text(prompt, temperature)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 66
**Error:** Need type annotation for "game_config" (hint: "game_config: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        # Configuration
        self.play_delay_seconds = 5.0  # Delay between plays for animation
        self.game_config = {}

        self.last_clock_strategy = "NORMAL"

# Proposed Fix:
        self.game_config: dict[str, float] = {}
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 93
**Error:** Incompatible types in assignment (expression has type "Column[Any]", variable has type "None")  [assignment]
**Solve:**
```python
# Original Code:
            await self.db_session.commit()
            await self.db_session.refresh(new_game)
            self.current_game_id = new_game.id

            # Initialize Deterministic RNG with Game ID

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Column[Any]", variable has type "None")  [assignment]
            self.current_game_id = new_game.id
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 123
**Error:** Argument 1 to "record_starters" of "PreGameService" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

                # 3. Record Starters (for future chemistry)
                await pre_game_service.record_starters(new_game.id, home_team_id, away_team_id)

                logger.info("Pre-game services executed", extra={"game_id": new_game.id})

# Proposed Fix:
    # FIX: Argument 1 to "record_starters" of "PreGameService" has incompatible type "Column[Any]"; expected "int"  [arg-type]
                await pre_game_service.record_starters(new_game.id, home_team_id, away_team_id)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 133
**Error:** Incompatible types in assignment (expression has type "MomentumEngine", variable has type "None")  [assignment]
**Solve:**
```python
# Original Code:
            self.play_resolver.register_players(self.match_context)
            # B-006: Wire momentum engine to play resolver
            self.play_resolver.momentum_engine = self.momentum_engine

            logger.info(

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "MomentumEngine", variable has type "None")  [assignment]
            self.play_resolver.momentum_engine = self.momentum_engine
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 156
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
            return

        try:
            stmt = select(Game).where(Game.id == self.current_game_id)
            result = await self.db_session.execute(stmt)

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
        try:
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 183
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
            return

        try:
            stmt = select(Game).where(Game.id == self.current_game_id)
            result = await self.db_session.execute(stmt)

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
        try:
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 219
**Error:** Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
**Solve:**
```python
# Original Code:
            away_stmt = select(Team).where(Team.id == game.away_team_id)

            home_result = await self.db_session.execute(home_stmt)
            away_result = await self.db_session.execute(away_stmt)


# Proposed Fix:
    # FIX: Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
            home_result = await self.db_session.execute(home_stmt)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 220
**Error:** Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
**Solve:**
```python
# Original Code:

            home_result = await self.db_session.execute(home_stmt)
            away_result = await self.db_session.execute(away_stmt)

            home_team = home_result.scalar_one_or_none()

# Proposed Fix:
    # FIX: Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
            away_result = await self.db_session.execute(away_stmt)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 238
**Error:** Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
                # For ties, update both with tie logic
                new_home_elo, new_away_elo = EloService.update_ratings(
                    home_team.elo_rating or 1500.0,
                    away_team.elo_rating or 1500.0,
                    point_diff=0,

# Proposed Fix:
    # FIX: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
                    home_team.elo_rating or 1500.0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 239
**Error:** Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
                new_home_elo, new_away_elo = EloService.update_ratings(
                    home_team.elo_rating or 1500.0,
                    away_team.elo_rating or 1500.0,
                    point_diff=0,
                    is_tie=True

# Proposed Fix:
    # FIX: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
                    away_team.elo_rating or 1500.0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 245
**Error:** Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
            elif home_score > away_score:
                new_home_elo, new_away_elo = EloService.update_ratings(
                    home_team.elo_rating or 1500.0,
                    away_team.elo_rating or 1500.0,
                    point_diff=point_diff

# Proposed Fix:
    # FIX: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
                    home_team.elo_rating or 1500.0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 246
**Error:** Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
                new_home_elo, new_away_elo = EloService.update_ratings(
                    home_team.elo_rating or 1500.0,
                    away_team.elo_rating or 1500.0,
                    point_diff=point_diff
                )

# Proposed Fix:
    # FIX: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
                    away_team.elo_rating or 1500.0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 252
**Error:** Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
                # Away team won
                new_away_elo, new_home_elo = EloService.update_ratings(
                    away_team.elo_rating or 1500.0,
                    home_team.elo_rating or 1500.0,
                    point_diff=point_diff

# Proposed Fix:
    # FIX: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
                    away_team.elo_rating or 1500.0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 253
**Error:** Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
**Solve:**
```python
# Original Code:
                new_away_elo, new_home_elo = EloService.update_ratings(
                    away_team.elo_rating or 1500.0,
                    home_team.elo_rating or 1500.0,
                    point_diff=point_diff
                )

# Proposed Fix:
    # FIX: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"  [arg-type]
                    home_team.elo_rating or 1500.0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 261
**Error:** Item "None" of "AsyncSession | None" has no attribute "commit"  [union-attr]
**Solve:**
```python
# Original Code:
            away_team.elo_rating = new_away_elo

            await self.db_session.commit()

            logger.info(

# Proposed Fix:
    # FIX: Item "None" of "AsyncSession | None" has no attribute "commit"  [union-attr]
            await self.db_session.commit()
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 276
**Error:** Incompatible default for argument "game" (default has type "None", argument has type "Game")  [assignment]
**Solve:**
```python
# Original Code:
            logger.exception("Error updating Elo ratings", extra={"game_id": game.id})

    async def _save_player_stats(self, game: Game = None) -> None:
        """Aggregate and save player stats from game history."""
        if not self.history:

# Proposed Fix:
    # FIX: Incompatible default for argument "game" (default has type "None", argument has type "Game")  [assignment]
    async def _save_player_stats(self, game: Game = None) -> None:
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 283
**Error:** Statement is unreachable  [unreachable]
**Solve:**
```python
# Original Code:
        # If game object not passed, fetch it
        if not game and self.current_game_id:
             stmt = select(Game).where(Game.id == self.current_game_id)
             result = await self.db_session.execute(stmt)
             game = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: Statement is unreachable  [unreachable]
             stmt = select(Game).where(Game.id == self.current_game_id)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 351
**Error:** Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
**Solve:**
```python
# Original Code:
                # Fallback: query player if not in match context (shouldn't happen often)
                stmt = select(Player).where(Player.id == pid)
                result = await self.db_session.execute(stmt)
                player = result.scalar_one_or_none()
                if player:

# Proposed Fix:
    # FIX: Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
                result = await self.db_session.execute(stmt)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 354
**Error:** Incompatible types in assignment (expression has type "int | Any | None", variable has type "Column[int] | None")  [assignment]
**Solve:**
```python
# Original Code:
                player = result.scalar_one_or_none()
                if player:
                    team_id = player.team_id

            if not team_id:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int | Any | None", variable has type "Column[int] | None")  [assignment]
                    team_id = player.team_id
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 360
**Error:** Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStats]]", variable has type "Select[tuple[Player]]")  [assignment]
**Solve:**
```python
# Original Code:

            # Check if exists first
            stmt = select(PlayerGameStats).where(
                PlayerGameStats.player_id == pid,
                PlayerGameStats.game_id == game.id

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStats]]", variable has type "Select[tuple[Player]]")  [assignment]
            stmt = select(PlayerGameStats).where(
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 364
**Error:** Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
**Solve:**
```python
# Original Code:
                PlayerGameStats.game_id == game.id
            )
            result = await self.db_session.execute(stmt)
            pgs = result.scalar_one_or_none()


# Proposed Fix:
    # FIX: Item "None" of "AsyncSession | None" has no attribute "execute"  [union-attr]
            result = await self.db_session.execute(stmt)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 375
**Error:** Item "None" of "AsyncSession | None" has no attribute "add"  [union-attr]
**Solve:**
```python
# Original Code:
                    **stats
                )
                self.db_session.add(pgs)
            else:
                # Update existing

# Proposed Fix:
    # FIX: Item "None" of "AsyncSession | None" has no attribute "add"  [union-attr]
                self.db_session.add(pgs)
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 383
**Error:** Item "None" of "AsyncSession | None" has no attribute "commit"  [union-attr]
**Solve:**
```python
# Original Code:
            count += 1

        await self.db_session.commit()
        logger.info("Player stats saved", extra={"game_id": game.id, "player_count": count})


# Proposed Fix:
    # FIX: Item "None" of "AsyncSession | None" has no attribute "commit"  [union-attr]
        await self.db_session.commit()
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 395
**Error:** Need type annotation for "offense_players" (hint: "offense_players: list[<type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:

        # For now, we are not using real player objects
        offense_players = []
        defense_players = []


# Proposed Fix:
        offense_players: list[Any] = []
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 396
**Error:** Need type annotation for "defense_players" (hint: "defense_players: list[<type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        # For now, we are not using real player objects
        offense_players = []
        defense_players = []

        # 1. Create a play command

# Proposed Fix:
        defense_players: list[Any] = []
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 425
**Error:** Value of type "Coroutine[Any, Any, None]" must be used  [unused-coroutine]
**Solve:**
```python
# Original Code:
        logger.debug("Play resolved")

        self._save_progress()

        return result

# Proposed Fix:
    # FIX: Value of type "Coroutine[Any, Any, None]" must be used  [unused-coroutine]
        self._save_progress()
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 605
**Error:** Incompatible types in assignment (expression has type "dict[str, int]", variable has type "CoachingPhilosophy")  [assignment]
**Solve:**
```python
# Original Code:
            )

            coach_philosophy = {
                "aggressiveness": int(aggression * 100),
                "pass_tendency": 50 # Default, could be loaded from Coach model

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "dict[str, int]", variable has type "CoachingPhilosophy")  [assignment]
            coach_philosophy = {
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 640
**Error:** "PlayResult" has no attribute "player_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
        # Attach read info to result for frontend
        if qb_read:
            result.player_modifiers = result.player_modifiers or {}
            result.player_modifiers["quarterback_read"] = qb_read


# Proposed Fix:
    # FIX: "PlayResult" has no attribute "player_modifiers"  [attr-defined]
            result.player_modifiers = result.player_modifiers or {}
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 641
**Error:** "PlayResult" has no attribute "player_modifiers"  [attr-defined]
**Solve:**
```python
# Original Code:
        if qb_read:
            result.player_modifiers = result.player_modifiers or {}
            result.player_modifiers["quarterback_read"] = qb_read

        self.history.append(result)

# Proposed Fix:
    # FIX: "PlayResult" has no attribute "player_modifiers"  [attr-defined]
            result.player_modifiers["quarterback_read"] = qb_read
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 928
**Error:** Argument "time_remaining" to "GameSituation" has incompatible type "float"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
                sit_def = ClockGameSituation(
                    quarter=self.current_quarter,
                    time_remaining=post_play_time,
                    down=self.down,
                    distance=self.distance,

# Proposed Fix:
                    time_remaining=int(post_play_time),
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 952
**Error:** Argument "time_remaining" to "GameSituation" has incompatible type "float"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
                     sit_off = ClockGameSituation(
                        quarter=self.current_quarter,
                        time_remaining=post_play_time,
                        down=self.down,
                        distance=self.distance,

# Proposed Fix:
                        time_remaining=int(post_play_time),
```


---

### File: `backend/app/services/ai/scouting_ai.py`
**Lines of Code:** 16
**Error:** Unused "type: ignore" comment  [unused-ignore]
**Solve:**
```python
# Original Code:
from functools import lru_cache

from app.schemas.scouting import ScoutingReportAI, PlayerBackstory  # type: ignore[import-not-found]
from app.services.ai.gemini_client import get_gemini_client  # type: ignore[import-not-found]


# Proposed Fix:
    # FIX: Unused "type: ignore" comment  [unused-ignore]
from app.schemas.scouting import ScoutingReportAI, PlayerBackstory  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/ai/scouting_ai.py`
**Lines of Code:** 17
**Error:** Unused "type: ignore" comment  [unused-ignore]
**Solve:**
```python
# Original Code:

from app.schemas.scouting import ScoutingReportAI, PlayerBackstory  # type: ignore[import-not-found]
from app.services.ai.gemini_client import get_gemini_client  # type: ignore[import-not-found]

logger = logging.getLogger(__name__)

# Proposed Fix:
    # FIX: Unused "type: ignore" comment  [unused-ignore]
from app.services.ai.gemini_client import get_gemini_client  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/ai/scouting_ai.py`
**Lines of Code:** 89
**Error:** Returning Any from function declared to return "ScoutingReportAI"  [no-any-return]
**Solve:**
```python
# Original Code:
                # Cache the result
                _report_cache[cache_key] = result
                return result

        # Fallback to template

# Proposed Fix:
    # FIX: Returning Any from function declared to return "ScoutingReportAI"  [no-any-return]
                return result
```


---

### File: `backend/app/services/ai/scouting_ai.py`
**Lines of Code:** 288
**Error:** Returning Any from function declared to return "PlayerBackstory"  [no-any-return]
**Solve:**
```python
# Original Code:
            if result:
                _backstory_cache[cache_key] = result
                return result

        # Fallback

# Proposed Fix:
    # FIX: Returning Any from function declared to return "PlayerBackstory"  [no-any-return]
                return result
```


---

### File: `backend/app/services/ai/__init__.py`
**Lines of Code:** 7
**Error:** Unused "type: ignore" comment  [unused-ignore]
**Solve:**
```python
# Original Code:
"""

from app.services.ai.gemini_client import GeminiClient, get_gemini_client  # type: ignore[import-not-found]

__all__ = ["GeminiClient", "get_gemini_client"]

# Proposed Fix:
    # FIX: Unused "type: ignore" comment  [unused-ignore]
from app.services.ai.gemini_client import GeminiClient, get_gemini_client  # type: ignore[import-not-found]
```


---

### File: `backend/app/services/rookie_generator.py`
**Lines of Code:** 18
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:

class RookieGenerator:
    def __init__(self, db: Session, seed: int = None):
        self.db = db
        # Use provided seed or a random one if not provided, but encapsulated in DeterministicRNG

# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, db: Session, seed: int = None):
```


---

### File: `backend/app/services/rookie_generator.py`
**Lines of Code:** 57
**Error:** Argument 2 to "_create_rookie" of "RookieGenerator" has incompatible type "Any | None"; expected "dict[Any, Any]"  [arg-type]
**Solve:**
```python
# Original Code:
                upto += weight

            player = self._create_rookie(selected_pos, league_avgs.get(selected_pos.value if hasattr(selected_pos, 'value') else selected_pos))
            players.append(player)


# Proposed Fix:
    # FIX: Argument 2 to "_create_rookie" of "RookieGenerator" has incompatible type "Any | None"; expected "dict[Any, Any]"  [arg-type]
            player = self._create_rookie(selected_pos, league_avgs.get(selected_pos.value if hasattr(selected_pos, 'value') else selected_pos))
```


---

### File: `backend/app/services/rookie_generator.py`
**Lines of Code:** 64
**Error:** Incompatible default for argument "stats_context" (default has type "None", argument has type "dict[Any, Any]")  [assignment]
**Solve:**
```python
# Original Code:
        return players

    def _create_rookie(self, position: Position, stats_context: dict = None) -> Player:
        first = self.rng.choice(FIRST_NAMES)
        last = self.rng.choice(LAST_NAMES)

# Proposed Fix:
    # FIX: Incompatible default for argument "stats_context" (default has type "None", argument has type "dict[Any, Any]")  [assignment]
    def _create_rookie(self, position: Position, stats_context: dict = None) -> Player:
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 14
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:

class GMAgent:
    def __init__(self, db: Session, team_id: int, seed: int = None):
        self.db = db
        self.team_id = team_id

# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, db: Session, team_id: int, seed: int = None):
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 87
**Error:** Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
**Solve:**
```python
# Original Code:

            # 3. Value Calculation
            offered_value = self._calculate_package_value(offered_players, offered_picks, is_acquiring=True)
            requested_value = self._calculate_package_value(requested_players, requested_picks, is_acquiring=False)


# Proposed Fix:
    # FIX: Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
            offered_value = self._calculate_package_value(offered_players, offered_picks, is_acquiring=True)
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 88
**Error:** Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
**Solve:**
```python
# Original Code:
            # 3. Value Calculation
            offered_value = self._calculate_package_value(offered_players, offered_picks, is_acquiring=True)
            requested_value = self._calculate_package_value(requested_players, requested_picks, is_acquiring=False)

            # Base score is the difference in value

# Proposed Fix:
    # FIX: Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
            requested_value = self._calculate_package_value(requested_players, requested_picks, is_acquiring=False)
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 94
**Error:** Argument 2 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
**Solve:**
```python
# Original Code:

            # 4. Apply GM Personality Modifiers
            modified_score = self._apply_gm_traits(raw_score, offered_players, requested_players, offered_picks, requested_picks)

            # 5. MCP/LLM Context (Mocked for now, but structured for integration)

# Proposed Fix:
    # FIX: Argument 2 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
            modified_score = self._apply_gm_traits(raw_score, offered_players, requested_players, offered_picks, requested_picks)
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 94
**Error:** Argument 3 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
**Solve:**
```python
# Original Code:

            # 4. Apply GM Personality Modifiers
            modified_score = self._apply_gm_traits(raw_score, offered_players, requested_players, offered_picks, requested_picks)

            # 5. MCP/LLM Context (Mocked for now, but structured for integration)

# Proposed Fix:
    # FIX: Argument 3 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
            modified_score = self._apply_gm_traits(raw_score, offered_players, requested_players, offered_picks, requested_picks)
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 98
**Error:** Argument 1 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
**Solve:**
```python
# Original Code:
            # 5. MCP/LLM Context (Mocked for now, but structured for integration)
            try:
                llm_adjustment = await self._get_llm_trade_opinion(offered_players, requested_players)
                modified_score += llm_adjustment.get("score_modifier", 0)
                if llm_adjustment.get("reasoning"):

# Proposed Fix:
    # FIX: Argument 1 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
                llm_adjustment = await self._get_llm_trade_opinion(offered_players, requested_players)
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 98
**Error:** Argument 2 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
**Solve:**
```python
# Original Code:
            # 5. MCP/LLM Context (Mocked for now, but structured for integration)
            try:
                llm_adjustment = await self._get_llm_trade_opinion(offered_players, requested_players)
                modified_score += llm_adjustment.get("score_modifier", 0)
                if llm_adjustment.get("reasoning"):

# Proposed Fix:
    # FIX: Argument 2 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"  [arg-type]
                llm_adjustment = await self._get_llm_trade_opinion(offered_players, requested_players)
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 107
**Error:** Unsupported operand types for - ("object" and "int")  [operator]
**Solve:**
```python
# Original Code:
            # 6. Final Decision
            # Aggression lowers the threshold to accept
            acceptance_threshold = 0 - (self.gm_traits["aggression"] - 50) * 0.5

            decision = "ACCEPT" if modified_score >= acceptance_threshold else "REJECT"

# Proposed Fix:
    # FIX: Unsupported operand types for - ("object" and "int")  [operator]
            acceptance_threshold = 0 - (self.gm_traits["aggression"] - 50) * 0.5
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 133
**Error:** Incompatible default for argument "target_position" (default has type "None", argument has type "str")  [assignment]
**Solve:**
```python
# Original Code:
            }

    def generate_trade_proposal(self, target_position: str = None) -> Dict[str, Any]:
        """
        Propose a trade to address a team need.

# Proposed Fix:
    # FIX: Incompatible default for argument "target_position" (default has type "None", argument has type "str")  [assignment]
    def generate_trade_proposal(self, target_position: str = None) -> Dict[str, Any]:
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 182
**Error:** Unsupported operand types for / ("object" and "int")  [operator]
**Solve:**
```python
# Original Code:

        # Skill factor: 0.8 to 1.2 (High skill reduces price)
        skill_factor = 1.2 - (negotiation_skill / 250)

        counter_offer = demand * skill_factor

# Proposed Fix:
    # FIX: Unsupported operand types for / ("object" and "int")  [operator]
        skill_factor = 1.2 - (negotiation_skill / 250)
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 355
**Error:** Item "None" of "Team | None" has no attribute "players"  [union-attr]
**Solve:**
```python
# Original Code:
        Returns a multiplier > 1.0 for high need, < 1.0 for surplus.
        """
        players_at_pos = [p for p in self.team.players if p.position == position]
        count = len(players_at_pos)


# Proposed Fix:
    # FIX: Item "None" of "Team | None" has no attribute "players"  [union-attr]
        players_at_pos = [p for p in self.team.players if p.position == position]
```


---

### File: `backend/app/services/draft_assistant.py`
**Lines of Code:** 70
**Error:** No overload variant of "select" matches argument types "InstrumentedAttribute[int]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[int]", overloaded function, overloaded function, overloaded function  [call-overload]
**Solve:**
```python
# Original Code:

        # 2. Get available players - select only needed columns to avoid lazy loading
        players_stmt = select(
            Player.id,
            Player.first_name,

# Proposed Fix:
    # FIX: No overload variant of "select" matches argument types "InstrumentedAttribute[int]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[int]", overloaded function, overloaded function, overloaded function  [call-overload]
        players_stmt = select(
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 101
**Error:** Dict entry 0 has incompatible type "str": "str"; expected "int": "dict[Any, Any]"  [dict-item]
**Solve:**
```python
# Original Code:

        if not games:
            return {"error": "No unplayed games found for this week"}

        results = {}

# Proposed Fix:
    # FIX: Dict entry 0 has incompatible type "str": "str"; expected "int": "dict[Any, Any]"  [dict-item]
            return {"error": "No unplayed games found for this week"}
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 133
**Error:** Argument "home_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
            # Start game session (this will create/update db entry)
            await orchestrator.start_new_game_session(
                home_team_id=game.home_team_id,
                away_team_id=game.away_team_id,
                config={"fast_sim": use_fast_sim, "weather": weather_config},

# Proposed Fix:
                home_team_id=int(game.home_team_id),
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 134
**Error:** Argument "away_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
            await orchestrator.start_new_game_session(
                home_team_id=game.home_team_id,
                away_team_id=game.away_team_id,
                config={"fast_sim": use_fast_sim, "weather": weather_config},
                db_session=self.db

# Proposed Fix:
                away_team_id=int(game.away_team_id),
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 143
**Error:** Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
**Solve:**
```python
# Original Code:

            # Update the original game record with the results
            game.is_played = True
            game.home_score = orchestrator.home_score
            game.away_score = orchestrator.away_score

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
            game.is_played = True
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 144
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            # Update the original game record with the results
            game.is_played = True
            game.home_score = orchestrator.home_score
            game.away_score = orchestrator.away_score
            game.game_data = {

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            game.home_score = orchestrator.home_score
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 145
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            game.is_played = True
            game.home_score = orchestrator.home_score
            game.away_score = orchestrator.away_score
            game.game_data = {
                "final_score": f"{orchestrator.home_score}-{orchestrator.away_score}",

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            game.away_score = orchestrator.away_score
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 146
**Error:** Incompatible types in assignment (expression has type "dict[str, object]", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
            game.home_score = orchestrator.home_score
            game.away_score = orchestrator.away_score
            game.game_data = {
                "final_score": f"{orchestrator.home_score}-{orchestrator.away_score}",
                "plays": len(orchestrator.history),

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "dict[str, object]", variable has type "Column[Any]")  [assignment]
            game.game_data = {
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 176
**Error:** Dict entry 0 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"  [dict-item]
**Solve:**
```python
# Original Code:

        return {
            "week": week,
            "games_simulated": len(results),
            "results": results

# Proposed Fix:
    # FIX: Dict entry 0 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"  [dict-item]
            "week": week,
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 177
**Error:** Dict entry 1 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"  [dict-item]
**Solve:**
```python
# Original Code:
        return {
            "week": week,
            "games_simulated": len(results),
            "results": results
        }

# Proposed Fix:
    # FIX: Dict entry 1 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"  [dict-item]
            "games_simulated": len(results),
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 178
**Error:** Dict entry 2 has incompatible type "str": "dict[Column[Any], dict[str, object]]"; expected "int": "dict[Any, Any]"  [dict-item]
**Solve:**
```python
# Original Code:
            "week": week,
            "games_simulated": len(results),
            "results": results
        }


# Proposed Fix:
    # FIX: Dict entry 2 has incompatible type "str": "dict[Column[Any], dict[str, object]]"; expected "int": "dict[Any, Any]"  [dict-item]
            "results": results
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 218
**Error:** Argument "home_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

        await orchestrator.start_new_game_session(
            home_team_id=game.home_team_id,
            away_team_id=game.away_team_id,
            config={"fast_sim": use_fast_sim, "weather": weather_config},

# Proposed Fix:
            home_team_id=int(game.home_team_id),
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 219
**Error:** Argument "away_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        await orchestrator.start_new_game_session(
            home_team_id=game.home_team_id,
            away_team_id=game.away_team_id,
            config={"fast_sim": use_fast_sim, "weather": weather_config},
            db_session=self.db

# Proposed Fix:
            away_team_id=int(game.away_team_id),
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 226
**Error:** Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
**Solve:**
```python
# Original Code:
        await self._run_simulation(orchestrator, play_count)

        game.is_played = True
        game.home_score = orchestrator.home_score
        game.away_score = orchestrator.away_score

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
        game.is_played = True
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 227
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:

        game.is_played = True
        game.home_score = orchestrator.home_score
        game.away_score = orchestrator.away_score
        game.game_data = {

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        game.home_score = orchestrator.home_score
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 228
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
        game.is_played = True
        game.home_score = orchestrator.home_score
        game.away_score = orchestrator.away_score
        game.game_data = {
            "final_score": f"{orchestrator.home_score}-{orchestrator.away_score}",

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        game.away_score = orchestrator.away_score
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 229
**Error:** Incompatible types in assignment (expression has type "dict[str, object]", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
        game.home_score = orchestrator.home_score
        game.away_score = orchestrator.away_score
        game.game_data = {
            "final_score": f"{orchestrator.home_score}-{orchestrator.away_score}",
            "plays": len(orchestrator.history),

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "dict[str, object]", variable has type "Column[Any]")  [assignment]
        game.game_data = {
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 272
**Error:** Value of type "Coroutine[Any, Any, None]" must be used  [unused-coroutine]
**Solve:**
```python
# Original Code:

        orchestrator.is_running = False
        orchestrator.save_game_result()

    async def simulate_full_season(

# Proposed Fix:
    # FIX: Value of type "Coroutine[Any, Any, None]" must be used  [unused-coroutine]
        orchestrator.save_game_result()
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 299
**Error:** Incompatible types in assignment (expression has type "Column[int]", variable has type "int | None")  [assignment]
**Solve:**
```python
# Original Code:

        if end_week is None:
            end_week = season.total_weeks

        all_results = {}

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Column[int]", variable has type "int | None")  [assignment]
            end_week = season.total_weeks
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 303
**Error:** Unsupported operand types for + ("None" and "int")  [operator]
**Solve:**
```python
# Original Code:
        all_results = {}

        for week_num in range(start_week, end_week + 1):
            logger.info("Simulating week", extra={"season_id": season_id, "week": week_num})
            week_results = await self.simulate_week(season_id, week_num)

# Proposed Fix:
    # FIX: Unsupported operand types for + ("None" and "int")  [operator]
        for week_num in range(start_week, end_week + 1):
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 309
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:

            # Update season's current week
            season.current_week = week_num
            await self.db.commit()


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            season.current_week = week_num
```


---

### File: `backend/app/services/week_simulator.py`
**Lines of Code:** 314
**Error:** Unsupported operand types for + ("None" and "int")  [operator]
**Solve:**
```python
# Original Code:
        return {
            "season_id": season_id,
            "weeks_simulated": list(range(start_week, end_week + 1)),
            "results": all_results
        }

# Proposed Fix:
    # FIX: Unsupported operand types for + ("None" and "int")  [operator]
            "weeks_simulated": list(range(start_week, end_week + 1)),
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 19
**Error:** Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
**Solve:**
```python
# Original Code:

class OffseasonService:
    def __init__(self, db: Session, seed: int = None):
        self.db = db
        self.standings_calculator = StandingsCalculator(db)

# Proposed Fix:
    # FIX: Incompatible default for argument "seed" (default has type "None", argument has type "int")  [assignment]
    def __init__(self, db: Session, seed: int = None):
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 31
**Error:** Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
            raise ValueError("Season not found")

        season.status = SeasonStatus.OFF_SEASON
        # We might want a more granular status enum for phases, but for now we use OFF_SEASON
        # and maybe track phase in a separate field or just assume flow.

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
        season.status = SeasonStatus.OFF_SEASON
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 172
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        players = list(self.db.execute(stmt).scalars().all())
        for player in players:
            player.contract_years -= 1
            if player.contract_years <= 0:
                player.team_id = None # Released to Free Agency

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
            player.contract_years -= 1
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 175
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            if player.contract_years <= 0:
                player.team_id = None # Released to Free Agency
                player.contract_years = 0

    def generate_draft_order(self, season_id: int) -> None:

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                player.contract_years = 0
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 205
**Error:** "TeamStanding" has no attribute "win_pct"  [attr-defined]
**Solve:**
```python
# Original Code:
        # Note: Standings are already sorted best to worst by calculate_standings
        # We want worst to best for draft order
        standings.sort(key=lambda x: (x.win_pct, x.wins, x.point_differential))

        # Find SB Winner and Loser to move to end

# Proposed Fix:
    # FIX: "TeamStanding" has no attribute "win_pct"  [attr-defined]
        standings.sort(key=lambda x: (x.win_pct, x.wins, x.point_differential))
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 208
**Error:** Incompatible types in assignment (expression has type "Select[tuple[PlayoffMatchup]]", variable has type "Select[tuple[Team]]")  [assignment]
**Solve:**
```python
# Original Code:

        # Find SB Winner and Loser to move to end
        stmt = select(PlayoffMatchup).where(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.SUPER_BOWL

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[PlayoffMatchup]]", variable has type "Select[tuple[Team]]")  [assignment]
        stmt = select(PlayoffMatchup).where(
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 216
**Error:** "Team" has no attribute "winner_id"  [attr-defined]
**Solve:**
```python
# Original Code:
        ordered_team_ids = [s.team_id for s in standings]

        if sb_matchup and sb_matchup.winner_id:
            winner_id = sb_matchup.winner_id
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id

# Proposed Fix:
    # FIX: "Team" has no attribute "winner_id"  [attr-defined]
        if sb_matchup and sb_matchup.winner_id:
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 217
**Error:** "Team" has no attribute "winner_id"  [attr-defined]
**Solve:**
```python
# Original Code:

        if sb_matchup and sb_matchup.winner_id:
            winner_id = sb_matchup.winner_id
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id


# Proposed Fix:
    # FIX: "Team" has no attribute "winner_id"  [attr-defined]
            winner_id = sb_matchup.winner_id
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 218
**Error:** "Team" has no attribute "home_team_id"  [attr-defined]
**Solve:**
```python
# Original Code:
        if sb_matchup and sb_matchup.winner_id:
            winner_id = sb_matchup.winner_id
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id

            if winner_id in ordered_team_ids:

# Proposed Fix:
    # FIX: "Team" has no attribute "home_team_id"  [attr-defined]
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 218
**Error:** "Team" has no attribute "winner_id"  [attr-defined]
**Solve:**
```python
# Original Code:
        if sb_matchup and sb_matchup.winner_id:
            winner_id = sb_matchup.winner_id
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id

            if winner_id in ordered_team_ids:

# Proposed Fix:
    # FIX: "Team" has no attribute "winner_id"  [attr-defined]
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 218
**Error:** "Team" has no attribute "away_team_id"  [attr-defined]
**Solve:**
```python
# Original Code:
        if sb_matchup and sb_matchup.winner_id:
            winner_id = sb_matchup.winner_id
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id

            if winner_id in ordered_team_ids:

# Proposed Fix:
    # FIX: "Team" has no attribute "away_team_id"  [attr-defined]
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 247
**Error:** Need type annotation for "position_counts" (hint: "position_counts: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        stmt = select(Player).where(Player.team_id == team_id)
        players = list(self.db.execute(stmt).scalars().all())
        position_counts = {}
        for p in players:
            position_counts[p.position] = position_counts.get(p.position, 0) + 1

# Proposed Fix:
        position_counts: dict[str, float] = {}
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 279
**Error:** Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
**Solve:**
```python
# Original Code:
        """Get top available rookie prospects."""
        stmt = select(Player).where(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(limit)

# Proposed Fix:
    # FIX: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
            Player.is_rookie == True,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 279
**Error:** Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
**Solve:**
```python
# Original Code:
        """Get top available rookie prospects."""
        stmt = select(Player).where(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(limit)

# Proposed Fix:
    # FIX: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
            Player.is_rookie == True,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 314
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:

        # Assign player to team
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        pick.player_id = player.id
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 316
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False


# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.contract_years = 4
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 317
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False

        self.db.commit()

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.is_rookie = False
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 328
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            raise ValueError("No active pick to trade.")

        pick.team_id = target_team_id
        self.db.commit()
        return pick

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        pick.team_id = target_team_id
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 341
**Error:** Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
**Solve:**
```python
# Original Code:
        # Optimization: Just get top 20 to choose from
        stmt = select(Player).where(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(20)

# Proposed Fix:
    # FIX: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
            Player.is_rookie == True,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 341
**Error:** Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
**Solve:**
```python
# Original Code:
        # Optimization: Just get top 20 to choose from
        stmt = select(Player).where(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(20)

# Proposed Fix:
    # FIX: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
            Player.is_rookie == True,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 350
**Error:** Argument 1 to "_get_team_needs" of "OffseasonService" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

        rookie_pool = list(rookies)
        team_needs = self._get_team_needs(pick.team_id)

        TARGET_COUNTS = {

# Proposed Fix:
    # FIX: Argument 1 to "_get_team_needs" of "OffseasonService" has incompatible type "Column[int]"; expected "int"  [arg-type]
        team_needs = self._get_team_needs(pick.team_id)
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 380
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
    def _execute_pick(self, pick: DraftPick, player: Player) -> DraftPickSummary:
        """Internal helper to execute a pick."""
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
        pick.player_id = player.id
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 382
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False


# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.contract_years = 4
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 383
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False

        self.db.commit()

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
        player.is_rookie = False
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 388
**Error:** Argument "round" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

        return DraftPickSummary(
            round=pick.round,
            pick_number=pick.pick_number,
            team_id=pick.team_id,

# Proposed Fix:
            round=int(pick.round),
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 389
**Error:** Argument "pick_number" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        return DraftPickSummary(
            round=pick.round,
            pick_number=pick.pick_number,
            team_id=pick.team_id,
            player_name=f"{player.first_name} {player.last_name}",

# Proposed Fix:
            pick_number=int(pick.pick_number),
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 390
**Error:** Argument "team_id" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
            round=pick.round,
            pick_number=pick.pick_number,
            team_id=pick.team_id,
            player_name=f"{player.first_name} {player.last_name}",
            player_position=player.position,

# Proposed Fix:
            team_id=int(pick.team_id),
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 431
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
                    player = fa_pool.pop(0)
                    player.team_id = team.id
                    player.contract_years = 1

        self.db.commit()

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                    player.contract_years = 1
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 443
**Error:** Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[False]")  [comparison-overlap]
**Solve:**
```python
# Original Code:

        stmt = select(Player).where(
            Player.is_retired == False,
            Player.team_id != None
        )

# Proposed Fix:
    # FIX: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[False]")  [comparison-overlap]
            Player.is_retired == False,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 443
**Error:** Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
**Solve:**
```python
# Original Code:

        stmt = select(Player).where(
            Player.is_retired == False,
            Player.team_id != None
        )

# Proposed Fix:
    # FIX: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
            Player.is_retired == False,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 467
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:

            if should_retire:
                player.is_retired = True
                player.retirement_year = season.year
                player.team_id = None

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                player.is_retired = True
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 468
**Error:** Cannot assign to a method  [method-assign]
**Solve:**
```python
# Original Code:
            if should_retire:
                player.is_retired = True
                player.retirement_year = season.year
                player.team_id = None
                retired_names.append(f"{player.first_name} {player.last_name}")

# Proposed Fix:
    # FIX: Cannot assign to a method  [method-assign]
                player.retirement_year = season.year
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 473
**Error:** Argument 2 to "_check_hall_of_fame" of "OffseasonService" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

                # Check Hall of Fame
                self._check_hall_of_fame(player, season.year)

        self.db.commit()

# Proposed Fix:
    # FIX: Argument 2 to "_check_hall_of_fame" of "OffseasonService" has incompatible type "Column[int]"; expected "int"  [arg-type]
                self._check_hall_of_fame(player, season.year)
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 511
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"  [union-attr]
**Solve:**
```python
# Original Code:

        return {
            "games_played": stats.games_played or 0,
            "pass_yards": stats.pass_yards or 0,
            "pass_tds": stats.pass_tds or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"  [union-attr]
            "games_played": stats.games_played or 0,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 512
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_yards"  [union-attr]
**Solve:**
```python
# Original Code:
        return {
            "games_played": stats.games_played or 0,
            "pass_yards": stats.pass_yards or 0,
            "pass_tds": stats.pass_tds or 0,
            "rush_yards": stats.rush_yards or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_yards"  [union-attr]
            "pass_yards": stats.pass_yards or 0,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 513
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_tds"  [union-attr]
**Solve:**
```python
# Original Code:
            "games_played": stats.games_played or 0,
            "pass_yards": stats.pass_yards or 0,
            "pass_tds": stats.pass_tds or 0,
            "rush_yards": stats.rush_yards or 0,
            "rush_tds": stats.rush_tds or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_tds"  [union-attr]
            "pass_tds": stats.pass_tds or 0,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 514
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_yards"  [union-attr]
**Solve:**
```python
# Original Code:
            "pass_yards": stats.pass_yards or 0,
            "pass_tds": stats.pass_tds or 0,
            "rush_yards": stats.rush_yards or 0,
            "rush_tds": stats.rush_tds or 0,
            "rec_yards": stats.rec_yards or 0,

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_yards"  [union-attr]
            "rush_yards": stats.rush_yards or 0,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 515
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_tds"  [union-attr]
**Solve:**
```python
# Original Code:
            "pass_tds": stats.pass_tds or 0,
            "rush_yards": stats.rush_yards or 0,
            "rush_tds": stats.rush_tds or 0,
            "rec_yards": stats.rec_yards or 0,
            "rec_tds": stats.rec_tds or 0

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_tds"  [union-attr]
            "rush_tds": stats.rush_tds or 0,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 516
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_yards"  [union-attr]
**Solve:**
```python
# Original Code:
            "rush_yards": stats.rush_yards or 0,
            "rush_tds": stats.rush_tds or 0,
            "rec_yards": stats.rec_yards or 0,
            "rec_tds": stats.rec_tds or 0
        }

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_yards"  [union-attr]
            "rec_yards": stats.rec_yards or 0,
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 517
**Error:** Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_tds"  [union-attr]
**Solve:**
```python
# Original Code:
            "rush_tds": stats.rush_tds or 0,
            "rec_yards": stats.rec_yards or 0,
            "rec_tds": stats.rec_tds or 0
        }

# Proposed Fix:
    # FIX: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_tds"  [union-attr]
            "rec_tds": stats.rec_tds or 0
```


---

### File: `backend/app/services/trait_acquisition_service.py`
**Lines of Code:** 5
**Error:** Module "app.models.stats" has no attribute "PlayerSeasonStats"  [attr-defined]
**Solve:**
```python
# Original Code:
from sqlalchemy import func
from app.models.player import Player
from app.models.stats import PlayerSeasonStats
from app.services.trait_service import TraitService
from app.services.gm_agent import GMAgent

# Proposed Fix:
    # FIX: Module "app.models.stats" has no attribute "PlayerSeasonStats"  [attr-defined]
from app.models.stats import PlayerSeasonStats
```


---

### File: `backend/app/services/trait_acquisition_service.py`
**Lines of Code:** 8
**Error:** Cannot find implementation or library stub for module named "structlog"  [import-not-found]
**Solve:**
```python
# Original Code:
from app.services.trait_service import TraitService
from app.services.gm_agent import GMAgent
import structlog

logger = structlog.get_logger()

# Proposed Fix:
    # FIX: Cannot find implementation or library stub for module named "structlog"  [import-not-found]
import structlog
```


---

### File: `backend/app/services/trait_acquisition_service.py`
**Lines of Code:** 46
**Error:** Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
                        db,
                        player.id,
                        trait_name,
                        source="MILESTONE" # or DEVELOPMENT
                    )

# Proposed Fix:
    # FIX: Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"  [arg-type]
                        trait_name,
```


---

### File: `backend/app/services/trait_acquisition_service.py`
**Lines of Code:** 47
**Error:** Argument "source" to "assign_trait" of "TraitService" has incompatible type "str"; expected "TraitSource"  [arg-type]
**Solve:**
```python
# Original Code:
                        player.id,
                        trait_name,
                        source="MILESTONE" # or DEVELOPMENT
                    )
                    if result:

# Proposed Fix:
                        source=TraitSource("MILESTONE") # or DEVELOPMENT
```


---

### File: `backend/app/services/trait_acquisition_service.py`
**Lines of Code:** 127
**Error:** Incompatible return value type (got "PlayerTrait | None", expected "bool")  [return-value]
**Solve:**
```python
# Original Code:
        # For MVP, we'll just assign it if eligible.

        return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")

# Proposed Fix:
        return bool(TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT"))
```


---

### File: `backend/app/services/trait_acquisition_service.py`
**Lines of Code:** 127
**Error:** Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        # For MVP, we'll just assign it if eligible.

        return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")

# Proposed Fix:
    # FIX: Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"  [arg-type]
        return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")
```


---

### File: `backend/app/services/trait_acquisition_service.py`
**Lines of Code:** 127
**Error:** Argument "source" to "assign_trait" of "TraitService" has incompatible type "str"; expected "TraitSource"  [arg-type]
**Solve:**
```python
# Original Code:
        # For MVP, we'll just assign it if eligible.

        return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")

# Proposed Fix:
        return TraitService.assign_trait(db, player_id, trait_name, source=TraitSource("DEVELOPMENT"))
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 47
**Error:** Argument "team_id" to "TradeAssetRead" has incompatible type "int | None"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
                name=f"{player.first_name} {player.last_name}",
                value=player.overall_rating,
                team_id=player.team_id,
                position=player.position.value if hasattr(player.position, 'value') else str(player.position)
            ))

# Proposed Fix:
                team_id=int(player.team_id),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 55
**Error:** Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"  [arg-type]
**Solve:**
```python
# Original Code:
async def _offer_to_read(db: AsyncSession, offer: TradeOffer) -> TradeOfferRead:
    """Convert a TradeOffer model to TradeOfferRead schema."""
    offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
    requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)


# Proposed Fix:
    # FIX: Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"  [arg-type]
    offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 55
**Error:** Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
async def _offer_to_read(db: AsyncSession, offer: TradeOffer) -> TradeOfferRead:
    """Convert a TradeOffer model to TradeOfferRead schema."""
    offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
    requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)


# Proposed Fix:
    # FIX: Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"  [arg-type]
    offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 56
**Error:** Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"  [arg-type]
**Solve:**
```python
# Original Code:
    """Convert a TradeOffer model to TradeOfferRead schema."""
    offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
    requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)

    return TradeOfferRead(

# Proposed Fix:
    # FIX: Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"  [arg-type]
    requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 56
**Error:** Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
    """Convert a TradeOffer model to TradeOfferRead schema."""
    offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
    requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)

    return TradeOfferRead(

# Proposed Fix:
    # FIX: Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"  [arg-type]
    requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 59
**Error:** Argument "id" to "TradeOfferRead" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

    return TradeOfferRead(
        id=offer.id,
        offering_team_id=offer.offering_team_id,
        receiving_team_id=offer.receiving_team_id,

# Proposed Fix:
        id=int(offer.id),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 60
**Error:** Argument "offering_team_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
    return TradeOfferRead(
        id=offer.id,
        offering_team_id=offer.offering_team_id,
        receiving_team_id=offer.receiving_team_id,
        offered_assets=offered_assets,

# Proposed Fix:
        offering_team_id=int(offer.offering_team_id),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 61
**Error:** Argument "receiving_team_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        id=offer.id,
        offering_team_id=offer.offering_team_id,
        receiving_team_id=offer.receiving_team_id,
        offered_assets=offered_assets,
        requested_assets=requested_assets,

# Proposed Fix:
        receiving_team_id=int(offer.receiving_team_id),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 65
**Error:** Argument "message" to "TradeOfferRead" has incompatible type "Column[str]"; expected "str | None"  [arg-type]
**Solve:**
```python
# Original Code:
        requested_assets=requested_assets,
        status=TradeOfferStatus(offer.status.value),
        message=offer.message,
        gm_response=offer.gm_response,
        created_at=offer.created_at.isoformat() if offer.created_at else "",

# Proposed Fix:
        message=str | None(offer.message),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 66
**Error:** Argument "gm_response" to "TradeOfferRead" has incompatible type "Column[str]"; expected "str | None"  [arg-type]
**Solve:**
```python
# Original Code:
        status=TradeOfferStatus(offer.status.value),
        message=offer.message,
        gm_response=offer.gm_response,
        created_at=offer.created_at.isoformat() if offer.created_at else "",
        expires_at=offer.expires_at.isoformat() if offer.expires_at else None,

# Proposed Fix:
        gm_response=str | None(offer.gm_response),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 69
**Error:** Argument "parent_offer_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int | None"  [arg-type]
**Solve:**
```python
# Original Code:
        created_at=offer.created_at.isoformat() if offer.created_at else "",
        expires_at=offer.expires_at.isoformat() if offer.expires_at else None,
        parent_offer_id=offer.parent_offer_id
    )


# Proposed Fix:
        parent_offer_id=int | None(offer.parent_offer_id)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 109
**Error:** Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")  [assignment]
**Solve:**
```python
# Original Code:
    if request.offered_player_ids:
        for player_id in request.offered_player_ids:
            stmt = select(Player).where(Player.id == player_id)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")  [assignment]
            stmt = select(Player).where(Player.id == player_id)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 121
**Error:** Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")  [assignment]
**Solve:**
```python
# Original Code:
    if request.requested_player_ids:
        for player_id in request.requested_player_ids:
            stmt = select(Player).where(Player.id == player_id)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")  [assignment]
            stmt = select(Player).where(Player.id == player_id)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 129
**Error:** "Team" has no attribute "team_id"  [attr-defined]
**Solve:**
```python
# Original Code:
                    detail=f"Requested player {player_id} not found"
                )
            if player.team_id != request.target_team_id:
                raise HTTPException(
                    status_code=400,

# Proposed Fix:
    # FIX: "Team" has no attribute "team_id"  [attr-defined]
            if player.team_id != request.target_team_id:
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 223
**Error:** Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")  [assignment]
**Solve:**
```python
# Original Code:
    offering_team_id = None
    if request.offered_player_ids:
        stmt = select(Player).where(Player.id == request.offered_player_ids[0])
        result = await db.execute(stmt)
        player = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")  [assignment]
        stmt = select(Player).where(Player.id == request.offered_player_ids[0])
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 227
**Error:** "Team" has no attribute "team_id"  [attr-defined]
**Solve:**
```python
# Original Code:
        player = result.scalar_one_or_none()
        if player:
            offering_team_id = player.team_id

    if not offering_team_id:

# Proposed Fix:
    # FIX: "Team" has no attribute "team_id"  [attr-defined]
            offering_team_id = player.team_id
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 255
**Error:** Argument "offer_id" to "TradeOfferResponse" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

    return TradeOfferResponse(
        offer_id=trade_offer.id,
        status="PENDING",
        message="Trade offer submitted. The GM will review your proposal."

# Proposed Fix:
        offer_id=int(trade_offer.id),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 330
**Error:** Argument "team_id" to "GMAgent" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        async def evaluate_auto():
            with SessionLocal() as sync_db:
                gm_agent = GMAgent(db=sync_db, team_id=offer.receiving_team_id)
                # Pass stored pick data from the offer
                offered_picks = offer.offered_picks if offer.offered_picks else []

# Proposed Fix:
                gm_agent = GMAgent(db=sync_db, team_id=int(offer.receiving_team_id))
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 335
**Error:** Argument "offered_players_ids" to "evaluate_trade" of "GMAgent" has incompatible type "Column[Any] | list[Never]"; expected "list[int]"  [arg-type]
**Solve:**
```python
# Original Code:
                requested_picks = offer.requested_picks if offer.requested_picks else []
                return await gm_agent.evaluate_trade(
                    offered_players_ids=offer.offered_player_ids or [],
                    requested_players_ids=offer.requested_player_ids or [],
                    offered_picks=offered_picks,

# Proposed Fix:
                    offered_players_ids=list(offer.offered_player_ids) or [],
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 336
**Error:** Argument "requested_players_ids" to "evaluate_trade" of "GMAgent" has incompatible type "Column[Any] | list[Never]"; expected "list[int]"  [arg-type]
**Solve:**
```python
# Original Code:
                return await gm_agent.evaluate_trade(
                    offered_players_ids=offer.offered_player_ids or [],
                    requested_players_ids=offer.requested_player_ids or [],
                    offered_picks=offered_picks,
                    requested_picks=requested_picks

# Proposed Fix:
                    requested_players_ids=list(offer.requested_player_ids) or [],
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 337
**Error:** Argument "offered_picks" to "evaluate_trade" of "GMAgent" has incompatible type "Reversible[Any]"; expected "list[dict[Any, Any]]"  [arg-type]
**Solve:**
```python
# Original Code:
                    offered_players_ids=offer.offered_player_ids or [],
                    requested_players_ids=offer.requested_player_ids or [],
                    offered_picks=offered_picks,
                    requested_picks=requested_picks
                )

# Proposed Fix:
                    offered_picks=list(offered_picks),
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 338
**Error:** Argument "requested_picks" to "evaluate_trade" of "GMAgent" has incompatible type "Reversible[Any]"; expected "list[dict[Any, Any]]"  [arg-type]
**Solve:**
```python
# Original Code:
                    requested_players_ids=offer.requested_player_ids or [],
                    offered_picks=offered_picks,
                    requested_picks=requested_picks
                )


# Proposed Fix:
                    requested_picks=list(requested_picks)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 349
**Error:** Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)  [union-attr]
**Solve:**
```python
# Original Code:
        # Execute the trade: swap player team IDs
        # Move offered players to receiving team
        for pid in offer.offered_player_ids or []:
            stmt = select(Player).where(Player.id == pid)
            result = await db.execute(stmt)

# Proposed Fix:
    # FIX: Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)  [union-attr]
        for pid in offer.offered_player_ids or []:
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 350
**Error:** Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[TradeOffer]]")  [assignment]
**Solve:**
```python
# Original Code:
        # Move offered players to receiving team
        for pid in offer.offered_player_ids or []:
            stmt = select(Player).where(Player.id == pid)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[TradeOffer]]")  [assignment]
            stmt = select(Player).where(Player.id == pid)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 354
**Error:** "TradeOffer" has no attribute "team_id"  [attr-defined]
**Solve:**
```python
# Original Code:
            player = result.scalar_one_or_none()
            if player:
                player.team_id = offer.receiving_team_id

        # Move requested players to offering team

# Proposed Fix:
    # FIX: "TradeOffer" has no attribute "team_id"  [attr-defined]
                player.team_id = offer.receiving_team_id
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 357
**Error:** Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)  [union-attr]
**Solve:**
```python
# Original Code:

        # Move requested players to offering team
        for pid in offer.requested_player_ids or []:
            stmt = select(Player).where(Player.id == pid)
            result = await db.execute(stmt)

# Proposed Fix:
    # FIX: Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)  [union-attr]
        for pid in offer.requested_player_ids or []:
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 358
**Error:** Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[TradeOffer]]")  [assignment]
**Solve:**
```python
# Original Code:
        # Move requested players to offering team
        for pid in offer.requested_player_ids or []:
            stmt = select(Player).where(Player.id == pid)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[TradeOffer]]")  [assignment]
            stmt = select(Player).where(Player.id == pid)
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 362
**Error:** "TradeOffer" has no attribute "team_id"  [attr-defined]
**Solve:**
```python
# Original Code:
            player = result.scalar_one_or_none()
            if player:
                player.team_id = offer.offering_team_id

        offer.status = DBTradeOfferStatus.ACCEPTED

# Proposed Fix:
    # FIX: "TradeOffer" has no attribute "team_id"  [attr-defined]
                player.team_id = offer.offering_team_id
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 364
**Error:** Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
                player.team_id = offer.offering_team_id

        offer.status = DBTradeOfferStatus.ACCEPTED
        offer.gm_response = gm_reasoning or request.message or "Trade accepted!"
        logger.info(f"Trade offer {offer_id} ACCEPTED")

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")  [assignment]
        offer.status = DBTradeOfferStatus.ACCEPTED
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 365
**Error:** Incompatible types in assignment (expression has type "Any | str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:

        offer.status = DBTradeOfferStatus.ACCEPTED
        offer.gm_response = gm_reasoning or request.message or "Trade accepted!"
        logger.info(f"Trade offer {offer_id} ACCEPTED")


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | str", variable has type "Column[str]")  [assignment]
        offer.gm_response = gm_reasoning or request.message or "Trade accepted!"
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 369
**Error:** Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:

    elif action == "reject":
        offer.status = DBTradeOfferStatus.REJECTED
        offer.gm_response = gm_reasoning or request.message or "Trade rejected."
        logger.info(f"Trade offer {offer_id} REJECTED")

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")  [assignment]
        offer.status = DBTradeOfferStatus.REJECTED
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 370
**Error:** Incompatible types in assignment (expression has type "Any | str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
    elif action == "reject":
        offer.status = DBTradeOfferStatus.REJECTED
        offer.gm_response = gm_reasoning or request.message or "Trade rejected."
        logger.info(f"Trade offer {offer_id} REJECTED")


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | str", variable has type "Column[str]")  [assignment]
        offer.gm_response = gm_reasoning or request.message or "Trade rejected."
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 405
**Error:** Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:

    # Mark original as countered
    original_offer.status = DBTradeOfferStatus.COUNTERED
    original_offer.gm_response = "Counter-offer submitted."


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")  [assignment]
    original_offer.status = DBTradeOfferStatus.COUNTERED
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 406
**Error:** Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
**Solve:**
```python
# Original Code:
    # Mark original as countered
    original_offer.status = DBTradeOfferStatus.COUNTERED
    original_offer.gm_response = "Counter-offer submitted."

    # Determine the counter-offering team (the original receiving team)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")  [assignment]
    original_offer.gm_response = "Counter-offer submitted."
```


---

### File: `backend/app/api/endpoints/trades.py`
**Lines of Code:** 433
**Error:** Argument "offer_id" to "TradeOfferResponse" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

    return TradeOfferResponse(
        offer_id=counter_offer.id,
        status="PENDING",
        message="Counter-offer submitted. Awaiting response."

# Proposed Fix:
        offer_id=int(counter_offer.id),
```


---

### File: `backend/app/api/endpoints/draft.py`
**Lines of Code:** 30
**Error:** Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
**Solve:**
```python
# Original Code:
    result = await db.execute(
        select(Player)
        .where(Player.is_rookie == True)
        .where(Player.team_id == None)
        .order_by(Player.overall_rating.desc())

# Proposed Fix:
    # FIX: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
        .where(Player.is_rookie == True)
```


---

### File: `backend/app/api/endpoints/draft.py`
**Lines of Code:** 30
**Error:** Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
**Solve:**
```python
# Original Code:
    result = await db.execute(
        select(Player)
        .where(Player.is_rookie == True)
        .where(Player.team_id == None)
        .order_by(Player.overall_rating.desc())

# Proposed Fix:
    # FIX: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
        .where(Player.is_rookie == True)
```


---

### File: `backend/app/api/endpoints/simulation.py`
**Lines of Code:** 71
**Error:** Value of type "Coroutine[Any, Any, None]" must be used  [unused-coroutine]
**Solve:**
```python
# Original Code:
    # Initialize game session synchronously to get ID
    # Mocking Team IDs 1 and 2 for now
    orchestrator.start_new_game_session(home_team_id=1, away_team_id=2, config=request.config)
    game_id = orchestrator.current_game_id


# Proposed Fix:
    # FIX: Value of type "Coroutine[Any, Any, None]" must be used  [unused-coroutine]
    orchestrator.start_new_game_session(home_team_id=1, away_team_id=2, config=request.config)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 132
**Error:** Incompatible types in assignment (expression has type "Select[tuple[int]]", variable has type "Select[tuple[Season]]")  [assignment]
**Solve:**
```python
# Original Code:

    # Calculate basic stats
    stmt = select(func.count(Game.id)).where(Game.season_id == season.id)
    result = await db.execute(stmt)
    total_games = result.scalar() or 0

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[int]]", variable has type "Select[tuple[Season]]")  [assignment]
    stmt = select(func.count(Game.id)).where(Game.season_id == season.id)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 136
**Error:** Incompatible types in assignment (expression has type "Select[tuple[int]]", variable has type "Select[tuple[Season]]")  [assignment]
**Solve:**
```python
# Original Code:
    total_games = result.scalar() or 0

    stmt = select(func.count(Game.id)).where(
        Game.season_id == season.id,
        Game.is_played == True

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[int]]", variable has type "Select[tuple[Season]]")  [assignment]
    stmt = select(func.count(Game.id)).where(
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 144
**Error:** Unsupported operand types for < ("int" and "Season")  [operator]
**Solve:**
```python
# Original Code:

    completion = 0.0
    if total_games > 0:
        completion = (games_played / total_games) * 100


# Proposed Fix:
    # FIX: Unsupported operand types for < ("int" and "Season")  [operator]
    if total_games > 0:
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 145
**Error:** Unsupported left operand type for / ("Season")  [operator]
**Solve:**
```python
# Original Code:
    completion = 0.0
    if total_games > 0:
        completion = (games_played / total_games) * 100

    # Initialize optional fields

# Proposed Fix:
    # FIX: Unsupported left operand type for / ("Season")  [operator]
        completion = (games_played / total_games) * 100
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 145
**Error:** Unsupported operand types for / ("Season" and "int")  [operator]
**Solve:**
```python
# Original Code:
    completion = 0.0
    if total_games > 0:
        completion = (games_played / total_games) * 100

    # Initialize optional fields

# Proposed Fix:
    # FIX: Unsupported operand types for / ("Season" and "int")  [operator]
        completion = (games_played / total_games) * 100
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 145
**Error:** Unsupported operand types for / ("int" and "Season")  [operator]
**Solve:**
```python
# Original Code:
    completion = 0.0
    if total_games > 0:
        completion = (games_played / total_games) * 100

    # Initialize optional fields

# Proposed Fix:
    # FIX: Unsupported operand types for / ("int" and "Season")  [operator]
        completion = (games_played / total_games) * 100
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 160
**Error:** Argument 1 to "get_bracket" of "PlayoffService" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
                with SessionLocal() as sync_db:
                    playoff_service = PlayoffService(sync_db)
                    return playoff_service.get_bracket(season.id)

            playoff_bracket = await run_in_threadpool(get_bracket_sync)

# Proposed Fix:
    # FIX: Argument 1 to "get_bracket" of "PlayoffService" has incompatible type "Column[Any]"; expected "int"  [arg-type]
                    return playoff_service.get_bracket(season.id)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 237
**Error:** Argument 1 to "calculate_standings" of "StandingsCalculator" has incompatible type "Column[Any]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
            with SessionLocal() as sync_db:
                calculator = StandingsCalculator(sync_db)
                return calculator.calculate_standings(season.id)

        flat_standings = await run_in_threadpool(get_standings_sync)

# Proposed Fix:
    # FIX: Argument 1 to "calculate_standings" of "StandingsCalculator" has incompatible type "Column[Any]"; expected "int"  [arg-type]
                return calculator.calculate_standings(season.id)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 243
**Error:** Need type annotation for "conferences" (hint: "conferences: dict[<type>, <type>] = ...")  [var-annotated]
**Solve:**
```python
# Original Code:
        # Group by Conference -> Division
        grouped_standings = []
        conferences = {}

        for team in flat_standings:

# Proposed Fix:
        conferences: dict[str, float] = {}
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 302
**Error:** Incompatible types in assignment (expression has type "Update", variable has type "Select[tuple[Season]]")  [assignment]
**Solve:**
```python
# Original Code:
        # Deactivate all other seasons
        from sqlalchemy import update
        stmt = update(Season).values(is_active=False)
        await db.execute(stmt)


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Update", variable has type "Select[tuple[Season]]")  [assignment]
        stmt = update(Season).values(is_active=False)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 306
**Error:** Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
**Solve:**
```python
# Original Code:

        # Activate this season
        existing.is_active = True
        await db.commit()
        await db.refresh(existing)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
        existing.is_active = True
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 317
**Error:** Incompatible types in assignment (expression has type "Update", variable has type "Select[tuple[Season]]")  [assignment]
**Solve:**
```python
# Original Code:
    # Simple update statement:
    from sqlalchemy import update
    stmt = update(Season).values(is_active=False)
    await db.execute(stmt)
    await db.flush()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Update", variable has type "Select[tuple[Season]]")  [assignment]
    stmt = update(Season).values(is_active=False)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 366
**Error:** Name "timedelta" is not defined  [name-defined]
**Solve:**
```python
# Original Code:
            # 2. Calculate Regular Season Start Date
            # Add weeks * 7 days
            regular_start_date = start_date_val + timedelta(weeks=preseason_weeks_count)

            # 3. Generate Regular Season Schedule

# Proposed Fix:
    # FIX: Name "timedelta" is not defined  [name-defined]
            regular_start_date = start_date_val + timedelta(weeks=preseason_weeks_count)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 377
**Error:** Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
**Solve:**
```python
# Original Code:
            # Ensure regular games are not marked as preseason
            for game in regular_games:
                game.is_preseason = False

            all_games.extend(regular_games)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")  [assignment]
                game.is_preseason = False
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 392
**Error:** Name "timedelta" is not defined  [name-defined]
**Solve:**
```python
# Original Code:
        if days_until_sunday == 0:
            days_until_sunday = 7
        start_date = (today + timedelta(days=days_until_sunday)).replace(hour=13, minute=0, second=0, microsecond=0)

    # We need to commit new_season so it's visible to sync session?

# Proposed Fix:
    # FIX: Name "timedelta" is not defined  [name-defined]
        start_date = (today + timedelta(days=days_until_sunday)).replace(hour=13, minute=0, second=0, microsecond=0)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 476
**Error:** Incompatible types in assignment (expression has type "Select[tuple[Game]]", variable has type "Select[tuple[Season]]")  [assignment]
**Solve:**
```python
# Original Code:

    # Build query with eager loading to prevent N+1 queries
    stmt = select(Game).options(
        joinedload(Game.home_team),
        joinedload(Game.away_team),

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Select[tuple[Game]]", variable has type "Select[tuple[Season]]")  [assignment]
    stmt = select(Game).options(
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 547
**Error:** Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
        if season.current_week >= preseason_weeks:
            # Transition from preseason to regular season
            season.status = SeasonStatus.REGULAR_SEASON
            season.current_week = 1
            logger.info(f"Season {season_id} transitioning from preseason to regular season")

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
            season.status = SeasonStatus.REGULAR_SEASON
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 548
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            # Transition from preseason to regular season
            season.status = SeasonStatus.REGULAR_SEASON
            season.current_week = 1
            logger.info(f"Season {season_id} transitioning from preseason to regular season")
        else:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            season.current_week = 1
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 551
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            logger.info(f"Season {season_id} transitioning from preseason to regular season")
        else:
            season.current_week += 1
    elif season.current_week >= season.total_weeks:
        # Move to playoffs or offseason

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
            season.current_week += 1
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 555
**Error:** Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
        # Move to playoffs or offseason
        if season.status == SeasonStatus.REGULAR_SEASON:
            season.status = SeasonStatus.POST_SEASON
            season.current_week = 1
        else:

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
            season.status = SeasonStatus.POST_SEASON
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 556
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
        if season.status == SeasonStatus.REGULAR_SEASON:
            season.status = SeasonStatus.POST_SEASON
            season.current_week = 1
        else:
            season.status = SeasonStatus.OFF_SEASON

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
            season.current_week = 1
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 558
**Error:** Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
            season.current_week = 1
        else:
            season.status = SeasonStatus.OFF_SEASON
    else:
        season.current_week += 1

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
            season.status = SeasonStatus.OFF_SEASON
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 560
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
            season.status = SeasonStatus.OFF_SEASON
    else:
        season.current_week += 1

    logger.info(f"Season {season_id} advanced to week {season.current_week}, status: {season.status}")

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
        season.current_week += 1
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 604
**Error:** Incompatible types in assignment (expression has type "Column[int]", variable has type "int | None")  [assignment]
**Solve:**
```python
# Original Code:
    # Use current week if not specified
    if week is None:
        week = season.current_week

    # Create simulator and run

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Column[int]", variable has type "int | None")  [assignment]
        week = season.current_week
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 611
**Error:** Argument "week" to "simulate_week" of "WeekSimulator" has incompatible type "int | None"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
    results = await simulator.simulate_week(
        season_id=season_id,
        week=week,
        play_count=play_count,
        use_fast_sim=True

# Proposed Fix:
        week=int(week),
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 620
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
    # Auto-advance to next week after simulating
    if week == season.current_week and season.current_week < season.total_weeks:
        season.current_week += 1
        await db.commit()


# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
        season.current_week += 1
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 670
**Error:** Argument "week" to "simulate_week" of "WeekSimulator" has incompatible type "Column[int]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:
        await simulator.simulate_week(
            season_id=season_id,
            week=season.current_week,
            play_count=50, # Faster sim
            use_fast_sim=True

# Proposed Fix:
            week=int(season.current_week),
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 677
**Error:** Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
**Solve:**
```python
# Original Code:
        # Advance week logic (duplicated from advance_week to avoid API overhead)
        if season.current_week >= season.total_weeks:
             season.status = SeasonStatus.POST_SEASON
             season.current_week = 1
             # Generate playoffs - use sync session

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")  [assignment]
             season.status = SeasonStatus.POST_SEASON
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 678
**Error:** Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
        if season.current_week >= season.total_weeks:
             season.status = SeasonStatus.POST_SEASON
             season.current_week = 1
             # Generate playoffs - use sync session
             def generate_playoffs_sync(s_id):

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")  [assignment]
             season.current_week = 1
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 686
**Error:** Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
**Solve:**
```python
# Original Code:
             await run_in_threadpool(generate_playoffs_sync, season_id)
        else:
             season.current_week += 1

        await db.commit()

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")  [assignment]
             season.current_week += 1
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 905
**Error:** Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
**Solve:**
```python
# Original Code:
        # We can use sync_db to query
        available_players = sync_db.query(Player).filter(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(20).all()

# Proposed Fix:
    # FIX: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
            Player.is_rookie == True,
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 905
**Error:** Argument 1 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
**Solve:**
```python
# Original Code:
        # We can use sync_db to query
        available_players = sync_db.query(Player).filter(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(20).all()

# Proposed Fix:
    # FIX: Argument 1 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
            Player.is_rookie == True,
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 909
**Error:** Too many arguments for "DraftAssistant"  [call-arg]
**Solve:**
```python
# Original Code:
        ).order_by(Player.overall_rating.desc()).limit(20).all()

        assistant = DraftAssistant(sync_db)
        suggestion = await assistant.suggest_pick(team_id, available_players)
        return suggestion

# Proposed Fix:
    # FIX: Too many arguments for "DraftAssistant"  [call-arg]
        assistant = DraftAssistant(sync_db)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 910
**Error:** Missing positional arguments "available_players", "db" in call to "suggest_pick" of "DraftAssistant"  [call-arg]
**Solve:**
```python
# Original Code:

        assistant = DraftAssistant(sync_db)
        suggestion = await assistant.suggest_pick(team_id, available_players)
        return suggestion
    finally:

# Proposed Fix:
    # FIX: Missing positional arguments "available_players", "db" in call to "suggest_pick" of "DraftAssistant"  [call-arg]
        suggestion = await assistant.suggest_pick(team_id, available_players)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 910
**Error:** Argument 2 to "suggest_pick" of "DraftAssistant" has incompatible type "list[Player]"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

        assistant = DraftAssistant(sync_db)
        suggestion = await assistant.suggest_pick(team_id, available_players)
        return suggestion
    finally:

# Proposed Fix:
    # FIX: Argument 2 to "suggest_pick" of "DraftAssistant" has incompatible type "list[Player]"; expected "int"  [arg-type]
        suggestion = await assistant.suggest_pick(team_id, available_players)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 1030
**Error:** Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
**Solve:**
```python
# Original Code:

        if is_rookie_only:
            stmt = stmt.where(Player.is_rookie == True)

        if position_group == "QB":

# Proposed Fix:
    # FIX: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")  [comparison-overlap]
            stmt = stmt.where(Player.is_rookie == True)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 1030
**Error:** Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
**Solve:**
```python
# Original Code:

        if is_rookie_only:
            stmt = stmt.where(Player.is_rookie == True)

        if position_group == "QB":

# Proposed Fix:
    # FIX: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"  [arg-type]
            stmt = stmt.where(Player.is_rookie == True)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 1048
**Error:** Incompatible types in assignment (expression has type "Any | float", variable has type "int")  [assignment]
**Solve:**
```python
# Original Code:
            if position_group == "QB":
                # Simple MVP score: Yards/10 + TDs*6 - Ints*3
                score = (p.pass_yards or 0)/10 + (p.pass_tds or 0)*6 - (p.pass_ints or 0)*3 + (p.rush_yards or 0)/10 + (p.rush_tds or 0)*6
                stats_dict = {"Pass Yds": p.pass_yards, "Pass TDs": p.pass_tds, "Ints": p.pass_ints}
            elif position_group == "OFFENSE":

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Any | float", variable has type "int")  [assignment]
                score = (p.pass_yards or 0)/10 + (p.pass_tds or 0)*6 - (p.pass_ints or 0)*3 + (p.rush_yards or 0)/10 + (p.rush_tds or 0)*6
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 1093
**Error:** Incompatible types in assignment (expression has type "Column[Any] | int", variable has type "int | None")  [assignment]
**Solve:**
```python
# Original Code:
    if not season_id:
        season = db.execute(select(Season).where(Season.is_active == True)).scalar_one_or_none()
        season_id = season.id if season else 0

    service = SalaryCapService(db)

# Proposed Fix:
    # FIX: Incompatible types in assignment (expression has type "Column[Any] | int", variable has type "int | None")  [assignment]
        season_id = season.id if season else 0
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 1096
**Error:** Argument 2 to "get_team_cap_breakdown" of "SalaryCapService" has incompatible type "int | None"; expected "int"  [arg-type]
**Solve:**
```python
# Original Code:

    service = SalaryCapService(db)
    return service.get_team_cap_breakdown(team_id, season_id)



# Proposed Fix:
    # FIX: Argument 2 to "get_team_cap_breakdown" of "SalaryCapService" has incompatible type "int | None"; expected "int"  [arg-type]
    return service.get_team_cap_breakdown(team_id, season_id)
```


---

### File: `backend/app/api/endpoints/season.py`
**Lines of Code:** 1172
**Error:** Name "suggest_draft_pick" already defined on line 893  [no-redef]
**Solve:**
```python
# Original Code:
# ===== Draft Assistant Endpoint =====

@router.post("/draft/suggest-pick", response_model=draft_schemas.DraftSuggestionResponse)
@handle_errors
async def suggest_draft_pick(

# Proposed Fix:
    # FIX: Name "suggest_draft_pick" already defined on line 893  [no-redef]
@router.post("/draft/suggest-pick", response_model=draft_schemas.DraftSuggestionResponse)
```


---

### File: `backend/app/core/setup.py`
**Lines of Code:** 33
**Error:** Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RateLimitExceeded], Response]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
**Solve:**
```python
# Original Code:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



# Proposed Fix:
    # FIX: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RateLimitExceeded], Response]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```


---

### File: `backend/app/core/setup.py`
**Lines of Code:** 58
**Error:** Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], IntegrityError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
**Solve:**
```python
# Original Code:
def configure_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers."""
    app.add_exception_handler(IntegrityError, database_exception_handler)
    app.add_exception_handler(OperationalError, database_operational_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Proposed Fix:
    # FIX: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], IntegrityError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
    app.add_exception_handler(IntegrityError, database_exception_handler)
```


---

### File: `backend/app/core/setup.py`
**Lines of Code:** 59
**Error:** Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], OperationalError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
**Solve:**
```python
# Original Code:
    """Register all exception handlers."""
    app.add_exception_handler(IntegrityError, database_exception_handler)
    app.add_exception_handler(OperationalError, database_operational_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_handler)

# Proposed Fix:
    # FIX: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], OperationalError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
    app.add_exception_handler(OperationalError, database_operational_error_handler)
```


---

### File: `backend/app/core/setup.py`
**Lines of Code:** 60
**Error:** Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RequestValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
**Solve:**
```python
# Original Code:
    app.add_exception_handler(IntegrityError, database_exception_handler)
    app.add_exception_handler(OperationalError, database_operational_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

# Proposed Fix:
    # FIX: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RequestValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
```


---

### File: `backend/app/core/setup.py`
**Lines of Code:** 61
**Error:** Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], ValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
**Solve:**
```python
# Original Code:
    app.add_exception_handler(OperationalError, database_operational_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_handler)
    app.add_exception_handler(Exception, generic_exception_handler)


# Proposed Fix:
    # FIX: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], ValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"  [arg-type]
    app.add_exception_handler(ValidationError, pydantic_validation_handler)
```


---

## Backend Security (Bandit) Issues

### File: `backend/app/api/endpoints/abilities.py`
**Lines of Code:** 216
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    # Generate the actual coverage (simulated)
    actual_coverages = ["Cover 1", "Cover 2", "Cover 2 Man", "Cover 3", "Cover 4", "Cover 0 Blitz"]
    actual_coverage = random.choice(actual_coverages)

    # Determine if read is correct

# Proposed Fix:
    actual_coverage = secrets.choice(actual_coverages)
```


---

### File: `backend/app/api/endpoints/abilities.py`
**Lines of Code:** 219
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

    # Determine if read is correct
    rng = random.random()
    is_correct = rng < base_accuracy


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
    rng = random.random()
```


---

### File: `backend/app/api/endpoints/abilities.py`
**Lines of Code:** 242
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    if is_correct:
        predicted = actual_coverage
        key_read = random.choice(key_reads)
    else:
        # Wrong read - give a different coverage

# Proposed Fix:
        key_read = secrets.choice(key_reads)
```


---

### File: `backend/app/api/endpoints/abilities.py`
**Lines of Code:** 246
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # Wrong read - give a different coverage
        wrong_options = [c for c in actual_coverages if c != actual_coverage]
        predicted = random.choice(wrong_options)
        key_read = random.choice(key_reads) + " (Disguised)"


# Proposed Fix:
        predicted = secrets.choice(wrong_options)
```


---

### File: `backend/app/api/endpoints/abilities.py`
**Lines of Code:** 247
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        wrong_options = [c for c in actual_coverages if c != actual_coverage]
        predicted = random.choice(wrong_options)
        key_read = random.choice(key_reads) + " (Disguised)"

    return PreSnapInsightResponse(

# Proposed Fix:
        key_read = secrets.choice(key_reads) + " (Disguised)"
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 122
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

        # Check for complication
        if random.random() < surgery_risk:
            # Complication - adds 2-6 weeks
            added_weeks = random.randint(2, 6)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        if random.random() < surgery_risk:
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 124
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        if random.random() < surgery_risk:
            # Complication - adds 2-6 weeks
            added_weeks = random.randint(2, 6)
            recovery_weeks += added_weeks
            player.injury_recurrence_risk += 0.10

# Proposed Fix:
            added_weeks = secrets.randbelow(2, 6)
```


---

### File: `backend/app/api/endpoints/medical.py`
**Lines of Code:** 129
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        else:
            # Successful surgery - reduce recovery by 30-50%
            reduction = random.uniform(0.30, 0.50)
            recovery_weeks = max(1, int(recovery_weeks * (1 - reduction)))


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
            reduction = random.uniform(0.30, 0.50)
```


---

### File: `backend/app/api/endpoints/physics_api.py`
**Lines of Code:** 92
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    """
    # Create RNG
    seed = request.seed or random.randint(0, 999999)
    rng = random.Random(seed)


# Proposed Fix:
    seed = request.seed or secrets.randbelow(0, 999999)
```


---

### File: `backend/app/api/endpoints/physics_api.py`
**Lines of Code:** 93
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    # Create RNG
    seed = request.seed or random.randint(0, 999999)
    rng = random.Random(seed)

    # Create mock players (in production, fetch from DB)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
    rng = random.Random(seed)
```


---

### File: `backend/app/api/endpoints/physics_api.py`
**Lines of Code:** 192
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                play_type = data.get("play_type", "PASS")
                los = data.get("los", 50)
                seed = data.get("seed", random.randint(0, 999999))

                # Run simulation

# Proposed Fix:
                seed = data.get("seed", secrets.randbelow(0, 999999))
```


---

### File: `backend/app/api/endpoints/physics_api.py`
**Lines of Code:** 195
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

                # Run simulation
                rng = random.Random(seed)
                offense = _create_mock_offense()
                defense = _create_mock_defense()

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
                rng = random.Random(seed)
```


---

### File: `backend/app/core/injury_config.py`
**Lines of Code:** 30
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '1.0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
PLAY_TYPE_MULTIPLIERS: Dict[str, float] = {
    "STANDARD": 1.0,
    "PASS_PLAY": 1.0,
    "RUN_PLAY": 1.1,
    "QB_KNOCKDOWN": 1.2,           # QB hit while releasing ball (pressure throw)

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '1.0' (Severity: Low   Confidence: Medium)
    "PASS_PLAY": 1.0,
```


---

### File: `backend/app/core/random_utils.py`
**Lines of Code:** 29
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        """
        self._seed_val = seed
        self._rng = random.Random(self._generate_int_seed(seed))

    def _generate_int_seed(self, seed: Any) -> int:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        self._rng = random.Random(self._generate_int_seed(seed))
```


---

### File: `backend/app/core/redis_cache.py`
**Lines of Code:** 56
**Error:** [B324:hashlib] Use of weak MD5 hash for security. Consider usedforsecurity=False (Severity: High   Confidence: High)
**Solve:**
```python
# Original Code:
        """Create deterministic hash of OL lineup"""
        lineup_str = ",".join(f"{k}:{v}" for k, v in sorted(lineup.items()))
        return hashlib.md5(lineup_str.encode()).hexdigest()[:12]

    async def get(

# Proposed Fix:
        return hashlib.sha256(lineup_str.encode()).hexdigest()[:12]
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 93
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
def generate_player(position: str, team_id: int) -> Player:
    return Player(
        first_name=random.choice(FIRST_NAMES),
        last_name=random.choice(LAST_NAMES),
        position=position,

# Proposed Fix:
        first_name=secrets.choice(FIRST_NAMES),
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 94
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    return Player(
        first_name=random.choice(FIRST_NAMES),
        last_name=random.choice(LAST_NAMES),
        position=position,
        jersey_number=random.randint(1, 99),

# Proposed Fix:
        last_name=secrets.choice(LAST_NAMES),
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 96
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        last_name=random.choice(LAST_NAMES),
        position=position,
        jersey_number=random.randint(1, 99),
        overall_rating=random.randint(60, 99),
        team_id=team_id,

# Proposed Fix:
        jersey_number=secrets.randbelow(1, 99),
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 97
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        position=position,
        jersey_number=random.randint(1, 99),
        overall_rating=random.randint(60, 99),
        team_id=team_id,
        age=random.randint(21, 35),

# Proposed Fix:
        overall_rating=secrets.randbelow(60, 99),
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 99
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        overall_rating=random.randint(60, 99),
        team_id=team_id,
        age=random.randint(21, 35),
        experience=random.randint(0, 15)
    )

# Proposed Fix:
        age=secrets.randbelow(21, 35),
```


---

### File: `backend/app/core/seed.py`
**Lines of Code:** 100
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        team_id=team_id,
        age=random.randint(21, 35),
        experience=random.randint(0, 15)
    )


# Proposed Fix:
        experience=secrets.randbelow(0, 15)
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 35
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_PROT' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    PRE_SNAP = "PRE_SNAP"           # Mind games before the play
    LINE_OF_SCRIMMAGE = "LOS"       # Initial contact/release battles
    PASS_PROTECTION = "PASS_PROT"   # OL vs DL blocking battles
    ROUTE_VS_COVERAGE = "ROUTE_COV" # WR routes vs DB coverage
    RUN_GAME = "RUN_GAME"           # RB vision vs LB gap integrity

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_PROT' (Severity: Low   Confidence: Medium)
    PASS_PROTECTION = "PASS_PROT"   # OL vs DL blocking battles
```


---

### File: `backend/app/engine/attribute_interaction.py`
**Lines of Code:** 271
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.1' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            situational_modifiers={
                "3RD_AND_LONG": 0.15,       # Rushers more creative
                "DROP_BACK_PASS": 0.10,     # More time for counters
                "QUICK_PASS": -0.20,        # No time for counter moves
            },

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.1' (Severity: Low   Confidence: Medium)
                "DROP_BACK_PASS": 0.10,     # More time for counters
```


---

### File: `backend/app/engine/blocking.py`
**Lines of Code:** 5
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'Pass Set' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:

class BlockType(str, enum.Enum):
    PASS_SET = "Pass Set"
    RUN_DRIVE = "Run Drive"
    ZONE_STEP = "Zone Step"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'Pass Set' (Severity: Low   Confidence: Medium)
    PASS_SET = "Pass Set"
```


---

### File: `backend/app/engine/core/enhanced_event_bus.py`
**Lines of Code:** 39
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_THROWN' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    SNAP = "SNAP"
    HANDOFF = "HANDOFF"
    PASS_THROWN = "PASS_THROWN"
    PASS_CAUGHT = "PASS_CAUGHT"
    PASS_INCOMPLETE = "PASS_INCOMPLETE"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_THROWN' (Severity: Low   Confidence: Medium)
    PASS_THROWN = "PASS_THROWN"
```


---

### File: `backend/app/engine/core/enhanced_event_bus.py`
**Lines of Code:** 40
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_CAUGHT' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    HANDOFF = "HANDOFF"
    PASS_THROWN = "PASS_THROWN"
    PASS_CAUGHT = "PASS_CAUGHT"
    PASS_INCOMPLETE = "PASS_INCOMPLETE"
    INTERCEPTION = "INTERCEPTION"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_CAUGHT' (Severity: Low   Confidence: Medium)
    PASS_CAUGHT = "PASS_CAUGHT"
```


---

### File: `backend/app/engine/core/enhanced_event_bus.py`
**Lines of Code:** 41
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_INCOMPLETE' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    PASS_THROWN = "PASS_THROWN"
    PASS_CAUGHT = "PASS_CAUGHT"
    PASS_INCOMPLETE = "PASS_INCOMPLETE"
    INTERCEPTION = "INTERCEPTION"
    FUMBLE = "FUMBLE"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_INCOMPLETE' (Severity: Low   Confidence: Medium)
    PASS_INCOMPLETE = "PASS_INCOMPLETE"
```


---

### File: `backend/app/engine/event_bus.py`
**Lines of Code:** 58
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'DROPPED_PASS' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    TOUCHDOWN_EVENT = "TOUCHDOWN_EVENT"
    TURNOVER_EVENT = "TURNOVER_EVENT"
    DROPPED_PASS = "DROPPED_PASS"
    PANCAKE_BLOCK = "PANCAKE_BLOCK"
    SPECTACULAR_CATCH = "SPECTACULAR_CATCH"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'DROPPED_PASS' (Severity: Low   Confidence: Medium)
    DROPPED_PASS = "DROPPED_PASS"
```


---

### File: `backend/app/engine/genesis/injury.py`
**Lines of Code:** 412
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        else:
            import random
            roll = random.random()

        if roll >= probability:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
            roll = random.random()
```


---

### File: `backend/app/engine/genesis/injury.py`
**Lines of Code:** 480
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        else:
            import random
            recovery = random.randint(min_weeks, max_weeks)

        return Injury(

# Proposed Fix:
            recovery = secrets.randbelow(min_weeks, max_weeks)
```


---

### File: `backend/app/engine/position_physics.py`
**Lines of Code:** 299
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        import random
        stiff_arm_chance = self.stiff_arm / (self.stiff_arm + defender_tackle)
        return random.random() < stiff_arm_chance

    def _check_fumble(self, force_ratio: float) -> bool:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        return random.random() < stiff_arm_chance
```


---

### File: `backend/app/engine/position_physics.py`
**Lines of Code:** 306
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # Base 2% fumble chance, increases with force ratio
        fumble_chance = 0.02 * force_ratio
        return random.random() < fumble_chance

    def calculate_cut_injury_risk(

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        return random.random() < fumble_chance
```


---

### File: `backend/app/engine/position_physics.py`
**Lines of Code:** 491
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        catch_prob = base_catch * contested_modifier * (1 - traffic_penalty)

        if random.random() < catch_prob:
            return (True, "caught")
        else:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        if random.random() < catch_prob:
```


---

### File: `backend/app/engine/position_physics.py`
**Lines of Code:** 625
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
            int_probability = self.ball_skills / 100 * 0.9

        if random.random() < int_probability:
            return (True, "interception")
        else:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        if random.random() < int_probability:
```


---

### File: `backend/app/engine/position_physics/offensive_line.py`
**Lines of Code:** 28
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_SET' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
class BlockType(str, Enum):
    """Types of blocks."""
    PASS_SET = "PASS_SET"
    DRIVE_BLOCK = "DRIVE_BLOCK"
    REACH_BLOCK = "REACH_BLOCK"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_SET' (Severity: Low   Confidence: Medium)
    PASS_SET = "PASS_SET"
```


---

### File: `backend/app/engine/position_physics/quarterback.py`
**Lines of Code:** 241
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        else:
            import random
            angle = random.random() * 360.0
            deviation = random.random() * accuracy_radius


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
            angle = random.random() * 360.0
```


---

### File: `backend/app/engine/position_physics/quarterback.py`
**Lines of Code:** 242
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
            import random
            angle = random.random() * 360.0
            deviation = random.random() * accuracy_radius

        # Calculate actual landing position

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
            deviation = random.random() * accuracy_radius
```


---

### File: `backend/app/engine/sack_calculator.py`
**Lines of Code:** 98
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        Determine if a play results in a Sack, Throw Away, or Scramble based on probability.
        """
        roll = random.random()

        if roll < sack_prob:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        roll = random.random()
```


---

### File: `backend/app/kernels/cortex/inference.py`
**Lines of Code:** 6
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.5' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    def __init__(self):
        self.tendencies = {
            "pass_heavy": 0.5,
            "blitz_heavy": 0.5,
            "run_outside": 0.5

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.5' (Severity: Low   Confidence: Medium)
            "pass_heavy": 0.5,
```


---

### File: `backend/app/kernels/rpg/training.py`
**Lines of Code:** 94
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

        # Roll for injury
        injury_occurred = random.random() < final_injury_risk

        # If injured, reduce XP gain

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        injury_occurred = random.random() < final_injury_risk
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 179
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
                    "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 179
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
                    "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 179
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
                    "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 180
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
                    "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_tds": 0, "pass_ints": 0,
```


---

### File: `backend/app/orchestrator/game_repository.py`
**Lines of Code:** 180
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0,
                    "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_tds": 0, "pass_ints": 0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 306
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 306
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 306
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 306
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 306
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0' (Severity: Low   Confidence: Medium)
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
```


---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Lines of Code:** 607
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '50' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            coach_philosophy = {
                "aggressiveness": int(aggression * 100),
                "pass_tendency": 50 # Default, could be loaded from Coach model
            }


# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '50' (Severity: Low   Confidence: Medium)
                "pass_tendency": 50 # Default, could be loaded from Coach model
```


---

### File: `backend/app/rpg/coach.py`
**Lines of Code:** 4
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    SKILL_TREES = {
        "Offense": {
            "WestCoastGuru": {"level": 1, "effect": {"short_pass_accuracy": 5}},
            "VerticalThreat": {"level": 1, "effect": {"deep_pass_accuracy": 5}},
            "ZoneRunMaster": {"level": 1, "effect": {"run_block_zone": 5}}

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
            "WestCoastGuru": {"level": 1, "effect": {"short_pass_accuracy": 5}},
```


---

### File: `backend/app/rpg/coach.py`
**Lines of Code:** 5
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "Offense": {
            "WestCoastGuru": {"level": 1, "effect": {"short_pass_accuracy": 5}},
            "VerticalThreat": {"level": 1, "effect": {"deep_pass_accuracy": 5}},
            "ZoneRunMaster": {"level": 1, "effect": {"run_block_zone": 5}}
        },

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
            "VerticalThreat": {"level": 1, "effect": {"deep_pass_accuracy": 5}},
```


---

### File: `backend/app/rpg/coach.py`
**Lines of Code:** 9
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        },
        "Defense": {
            "BlitzHappy": {"level": 1, "effect": {"pass_rush_power": 5}},
            "ZoneCoverageSpecialist": {"level": 1, "effect": {"zone_coverage": 5}},
            "ManPressExpert": {"level": 1, "effect": {"man_coverage": 5}}

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
            "BlitzHappy": {"level": 1, "effect": {"pass_rush_power": 5}},
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 13
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
class InjurySystem:
    def __init__(self, seed: int = None):
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

    def calculate_injury_risk_multiplier(self, training_staff_quality: int) -> float:

# Proposed Fix:
        self.rng = DeterministicRNG(seed if seed is not None else secrets.randbelow(0, 1000000))
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 396
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    - 8-10 (Severe): 5%
    """
    roll = rng.random() if rng else random.random()

    if roll < 0.60:  # Minor

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
    roll = rng.random() if rng else random.random()
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 399
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

    if roll < 0.60:  # Minor
        return rng.randint(1, 3) if rng else random.randint(1, 3)
    elif roll < 0.95:  # Moderate
        return rng.randint(4, 7) if rng else random.randint(4, 7)

# Proposed Fix:
        return rng.randint(1, 3) if rng else secrets.randbelow(1, 3)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 401
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        return rng.randint(1, 3) if rng else random.randint(1, 3)
    elif roll < 0.95:  # Moderate
        return rng.randint(4, 7) if rng else random.randint(4, 7)
    else:  # Severe
        return rng.randint(8, 10) if rng else random.randint(8, 10)

# Proposed Fix:
        return rng.randint(4, 7) if rng else secrets.randbelow(4, 7)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 403
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        return rng.randint(4, 7) if rng else random.randint(4, 7)
    else:  # Severe
        return rng.randint(8, 10) if rng else random.randint(8, 10)



# Proposed Fix:
        return rng.randint(8, 10) if rng else secrets.randbelow(8, 10)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 504
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

    # Roll for escalation
    roll = rng.random() if rng else random.random()

    if roll < escalation_chance:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
    roll = rng.random() if rng else random.random()
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 508
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    if roll < escalation_chance:
        # Injury worsened
        increase = rng.randint(1, InjuryConfig.INJURY_ESCALATION_MAX_INCREASE) if rng else random.randint(1, 2)
        new_severity = min(10, current_severity + increase)
        logger.info(f"Player {player.id} injury escalated from {current_severity} to {new_severity}")

# Proposed Fix:
        increase = rng.randint(1, InjuryConfig.INJURY_ESCALATION_MAX_INCREASE) if rng else secrets.randbelow(1, 2)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 543
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

        # Roll for injury
        roll = rng.random() if rng else random.random()

        if roll < probability:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        roll = rng.random() if rng else random.random()
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 620
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        weeks = rng.randint(min_weeks, max_weeks)
    else:
        injury_type = random.choice(injury_types)
        weeks = random.randint(min_weeks, max_weeks)


# Proposed Fix:
        injury_type = secrets.choice(injury_types)
```


---

### File: `backend/app/rpg/injury_system.py`
**Lines of Code:** 621
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    else:
        injury_type = random.choice(injury_types)
        weeks = random.randint(min_weeks, max_weeks)

    return injury_type, weeks

# Proposed Fix:
        weeks = secrets.randbelow(min_weeks, max_weeks)
```


---

### File: `backend/app/rpg/narrative.py`
**Lines of Code:** 34
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
            return NarrativeEngine.EVENTS[0] # Drama likely

        if random.random() < 0.1:
            return random.choice(NarrativeEngine.EVENTS)


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        if random.random() < 0.1:
```


---

### File: `backend/app/rpg/narrative.py`
**Lines of Code:** 35
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

        if random.random() < 0.1:
            return random.choice(NarrativeEngine.EVENTS)

        return None

# Proposed Fix:
            return secrets.choice(NarrativeEngine.EVENTS)
```


---

### File: `backend/app/rpg/player_archetypes.py`
**Lines of Code:** 199
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        stat_bonuses={
            "technique": 10,
            "pass_block": 5,
            "run_block": 5,
            "awareness": 5,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
            "pass_block": 5,
```


---

### File: `backend/app/rpg/traits.py`
**Lines of Code:** 32
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '10' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "BrickWall": {
            "description": "Increases pass block rating against Bull Rush.",
            "effect": {"pass_block": 10, "condition": "vs_bull_rush"}
        },
        "BallHawk": {

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '10' (Severity: Low   Confidence: Medium)
            "effect": {"pass_block": 10, "condition": "vs_bull_rush"}
```


---

### File: `backend/app/scripts/download_logos.py`
**Lines of Code:** 35
**Error:** [B323:blacklist] By default, Python will create a secure, verified ssl context for use in such classes as HTTPSConnection. However, it still allows using an insecure context via the _create_unverified_context that  reverts to the previous behavior that does not validate certificates or perform hostname checks. (Severity: Medium   Confidence: High)
**Solve:**
```python
# Original Code:

    # Create unverified SSL context
    ssl_context = ssl._create_unverified_context()

    # Create an opener with the unverified context

# Proposed Fix:
    # FIX: [B323:blacklist] By default, Python will create a secure, verified ssl context for use in such classes as HTTPSConnection. However, it still allows using an insecure context via the _create_unverified_context that  reverts to the previous behavior that does not validate certificates or perform hostname checks. (Severity: Medium   Confidence: High)
    ssl_context = ssl._create_unverified_context()
```


---

### File: `backend/app/scripts/download_logos.py`
**Lines of Code:** 50
**Error:** [B310:blacklist] Audit url open for permitted schemes. Allowing use of file:/ or custom schemes is often unexpected. (Severity: Medium   Confidence: High)
**Solve:**
```python
# Original Code:
        try:
            print(f"Downloading {abbr} from {url}...")
            urllib.request.urlretrieve(url, target_file)
            success_count += 1
        except Exception as e:

# Proposed Fix:
    # FIX: [B310:blacklist] Audit url open for permitted schemes. Allowing use of file:/ or custom schemes is often unexpected. (Severity: Medium   Confidence: High)
            urllib.request.urlretrieve(url, target_file)
```


---

### File: `backend/app/scripts/download_logos.py`
**Lines of Code:** 59
**Error:** [B310:blacklist] Audit url open for permitted schemes. Allowing use of file:/ or custom schemes is often unexpected. (Severity: Medium   Confidence: High)
**Solve:**
```python
# Original Code:
                    print(f"Retrying WAS as 'was'...")
                    url = f"{base_url}/was.png"
                    urllib.request.urlretrieve(url, target_file)
                    success_count += 1
                except Exception as e2:

# Proposed Fix:
    # FIX: [B310:blacklist] Audit url open for permitted schemes. Allowing use of file:/ or custom schemes is often unexpected. (Severity: Medium   Confidence: High)
                    urllib.request.urlretrieve(url, target_file)
```


---

### File: `backend/app/services/broadcasting_service.py`
**Lines of Code:** 196
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    def __init__(self, style: BroadcastStyle = BroadcastStyle.ESPN, seed: int = None):
        self.style = style
        self.rng = random.Random(seed)

    def generate_play_commentary(

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        self.rng = random.Random(seed)
```


---

### File: `backend/app/services/database/optimizer.py`
**Lines of Code:** 56
**Error:** [B324:hashlib] Use of weak MD5 hash for security. Consider usedforsecurity=False (Severity: High   Confidence: High)
**Solve:**
```python
# Original Code:
        """Generate cache key from query and params."""
        key_str = query + str(params or {})
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, query: str, params: Optional[Dict] = None) -> Optional[Any]:

# Proposed Fix:
        return hashlib.sha256(key_str.encode()).hexdigest()
```


---

### File: `backend/app/services/draft_assistant.py`
**Lines of Code:** 395
**Error:** [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                    if stats:
                        historical_context = f"League average for {position} in 2024 suggests high value for this archetype."
            except Exception:
                pass


# Proposed Fix:
    # FIX: [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
            except Exception:
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 49
**Error:** [B324:hashlib] Use of weak MD5 hash for security. Consider usedforsecurity=False (Severity: High   Confidence: High)
**Solve:**
```python
# Original Code:
            f"{pos}:{pid}" for pos, pid in sorted(self.position_map.items())
        )
        return hashlib.md5(lineup_string.encode()).hexdigest()[:12]

    def to_dict(self) -> Dict:

# Proposed Fix:
        return hashlib.sha256(lineup_string.encode()).hexdigest()[:12]
```


---

### File: `backend/app/services/enhanced_chemistry_service.py`
**Lines of Code:** 320
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            player_ids=[],
            position_map={},
            bonuses={"pass_block": 0.0, "run_block": 0.0, "awareness": 0.0},
            advanced_effects={
                "stunt_pickup_bonus": 0.0,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.0' (Severity: Low   Confidence: Medium)
            bonuses={"pass_block": 0.0, "run_block": 0.0, "awareness": 0.0},
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 17
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        self.db = db
        self.team_id = team_id
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))
        self.team = db.get(Team, team_id)
        self.gm = self.team.gm if self.team else None

# Proposed Fix:
        self.rng = DeterministicRNG(seed if seed is not None else secrets.randbelow(0, 1000000))
```


---

### File: `backend/app/services/gm_agent.py`
**Lines of Code:** 102
**Error:** [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                if llm_adjustment.get("reasoning"):
                    reasoning.append(llm_adjustment["reasoning"])
            except Exception:
                pass  # Ignore LLM errors


# Proposed Fix:
    # FIX: [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
            except Exception:
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 43
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        hits = snaps_played // 10
        for _ in range(hits):
            if random.random() < 0.3: # 30% chance of meaningful contact
                self._apply_hit_damage(health, position)


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
            if random.random() < 0.3: # 30% chance of meaningful contact
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 50
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    def _apply_hit_damage(self, health: BodyPart, position: str):
        """Logic to distribute damage to body parts"""
        part = random.choice(["head", "torso", "right_arm", "left_arm", "right_leg", "left_leg"])
        damage = random.uniform(0.5, 3.0) # Small micro-tears


# Proposed Fix:
        part = secrets.choice(["head", "torso", "right_arm", "left_arm", "right_leg", "left_leg"])
```


---

### File: `backend/app/services/medical_service.py`
**Lines of Code:** 51
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        """Logic to distribute damage to body parts"""
        part = random.choice(["head", "torso", "right_arm", "left_arm", "right_leg", "left_leg"])
        damage = random.uniform(0.5, 3.0) # Small micro-tears

        if part == "head":

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        damage = random.uniform(0.5, 3.0) # Small micro-tears
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 294
**Error:** [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                   if r.get('gsis_id')
               }
            except Exception:
                pass


# Proposed Fix:
    # FIX: [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
            except Exception:
```


---

### File: `backend/app/services/nflverse_service.py`
**Lines of Code:** 329
**Error:** [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                    if r.get('player_id')
                }
            except Exception:
                pass


# Proposed Fix:
    # FIX: [B110:try_except_pass] Try, Except, Pass detected. (Severity: Low   Confidence: High)
            except Exception:
```


---

### File: `backend/app/services/offseason_service.py`
**Lines of Code:** 22
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        self.db = db
        self.standings_calculator = StandingsCalculator(db)
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))
        self.rookie_generator = RookieGenerator(db, seed=self.rng.randint(0, 1000000))


# Proposed Fix:
        self.rng = DeterministicRNG(seed if seed is not None else secrets.randbelow(0, 1000000))
```


---

### File: `backend/app/services/playbook/clock_management.py`
**Lines of Code:** 222
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'mid' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            context.favor_sideline_routes = True
            context.avoid_middle_field = True
            context.max_pass_depth = "mid"  # No time for deep developing routes
            context.spike_recommended = (
                situation.down == 1 and

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'mid' (Severity: Low   Confidence: Medium)
            context.max_pass_depth = "mid"  # No time for deep developing routes
```


---

### File: `backend/app/services/playbook/clock_management.py`
**Lines of Code:** 231
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'deep' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            context.favor_sideline_routes = True
            context.avoid_middle_field = False
            context.max_pass_depth = "deep"
        elif urgency == UrgencyLevel.MEDIUM:
            context.favor_sideline_routes = False

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'deep' (Severity: Low   Confidence: Medium)
            context.max_pass_depth = "deep"
```


---

### File: `backend/app/services/playbook/clock_management.py`
**Lines of Code:** 235
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'deep' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            context.favor_sideline_routes = False
            context.avoid_middle_field = False
            context.max_pass_depth = "deep"

        # Timeout recommendation

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'deep' (Severity: Low   Confidence: Medium)
            context.max_pass_depth = "deep"
```


---

### File: `backend/app/services/playbook/clock_management.py`
**Lines of Code:** 260
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
                UrgencyLevel.HIGH, UrgencyLevel.CRITICAL
            ],
            "pass_probability_boost": 0.0,
            "sideline_route_boost": 0.0,
            "deep_pass_penalty": 0.0,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.0' (Severity: Low   Confidence: Medium)
            "pass_probability_boost": 0.0,
```


---

### File: `backend/app/services/playbook/clock_management.py`
**Lines of Code:** 262
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.0' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
            "pass_probability_boost": 0.0,
            "sideline_route_boost": 0.0,
            "deep_pass_penalty": 0.0,
            "run_penalty": 0.0,
            "max_play_clock_usage": 40,  # Default full play clock

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.0' (Severity: Low   Confidence: Medium)
            "deep_pass_penalty": 0.0,
```


---

### File: `backend/app/services/playbook/coaching_ai.py`
**Lines of Code:** 97
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

        # Random roll
        roll = random.uniform(0, 100)
        return roll < probability


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        roll = random.uniform(0, 100)
```


---

### File: `backend/app/services/playbook/coaching_ai.py`
**Lines of Code:** 134
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # Random aggression override
        if self.philosophy.aggressiveness > 80:
             if random.random() < 0.1: # 10% chance to go for it just because
                 return True


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
             if random.random() < 0.1: # 10% chance to go for it just because
```


---

### File: `backend/app/services/playbook/defensive_ai.py`
**Lines of Code:** 104
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        """Decide whether to send pressure."""
        # Base rate
        roll = random.random()

        # Increase blitz on obvious passing downs

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        roll = random.random()
```


---

### File: `backend/app/services/playbook/defensive_ai.py`
**Lines of Code:** 146
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
            return BlitzPackage.ALL_OUT

        return random.choice(packages)

# Proposed Fix:
        return secrets.choice(packages)
```


---

### File: `backend/app/services/playbook/play_caller.py`
**Lines of Code:** 81
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # 4. Select with some randomness (not always top choice)
        # Top 3 plays: 60%, 30%, 10% chance
        roll = random.random()
        if roll < 0.6 and len(scored_plays) > 0:
            selected = scored_plays[0][1]

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        roll = random.random()
```


---

### File: `backend/app/services/playbook/playbook.py`
**Lines of Code:** 25
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    """Category of play."""
    RUN = "RUN"
    PASS = "PASS"
    PLAY_ACTION = "PLAY_ACTION"
    SCREEN = "SCREEN"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS' (Severity: Low   Confidence: Medium)
    PASS = "PASS"
```


---

### File: `backend/app/services/player_development_service.py`
**Lines of Code:** 21
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    def __init__(self, db: AsyncSession, seed: int = None):
        self.db = db
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))
        self.injury_system = InjurySystem(seed=seed)


# Proposed Fix:
        self.rng = DeterministicRNG(seed if seed is not None else secrets.randbelow(0, 1000000))
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 57
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.05' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "juke_efficiency": 0.06,
        "break_tackle_threshold": 0.05,
        "pass_pro_rating": 0.05,
        "vision_cone_angle": 0.04,
        "stamina": 0.04,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.05' (Severity: Low   Confidence: Medium)
        "pass_pro_rating": 0.05,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 88
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.08' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "route_running": 0.10,
        "run_block": 0.10,
        "pass_block": 0.08,
        "speed": 0.10,
        "strength": 0.10,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.08' (Severity: Low   Confidence: Medium)
        "pass_block": 0.08,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 104
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.2' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    # -------------------------------------------------------------------------
    "OT": {
        "pass_block": 0.20,
        "run_block": 0.15,
        "strength": 0.12,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.2' (Severity: Low   Confidence: Medium)
        "pass_block": 0.20,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 119
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.16' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    "OG": {
        "run_block": 0.18,
        "pass_block": 0.16,
        "strength": 0.14,
        "awareness": 0.10,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.16' (Severity: Low   Confidence: Medium)
        "pass_block": 0.16,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 132
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.16' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    },
    "C": {
        "pass_block": 0.16,
        "run_block": 0.16,
        "awareness": 0.14,  # Higher for making calls

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.16' (Severity: Low   Confidence: Medium)
        "pass_block": 0.16,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 152
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.12' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "speed": 0.12,
        "acceleration": 0.10,
        "pass_rush_power": 0.12,
        "pass_rush_finesse": 0.12,
        "block_shed": 0.10,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.12' (Severity: Low   Confidence: Medium)
        "pass_rush_power": 0.12,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 153
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.12' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "acceleration": 0.10,
        "pass_rush_power": 0.12,
        "pass_rush_finesse": 0.12,
        "block_shed": 0.10,
        "strength": 0.08,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.12' (Severity: Low   Confidence: Medium)
        "pass_rush_finesse": 0.12,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 167
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.12' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "strength": 0.14,
        "block_shed": 0.14,
        "pass_rush_power": 0.12,
        "awareness": 0.10,
        "tackle": 0.08,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.12' (Severity: Low   Confidence: Medium)
        "pass_rush_power": 0.12,
```


---

### File: `backend/app/services/rating_calculator.py`
**Lines of Code:** 171
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.06' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "tackle": 0.08,
        "gap_integrity": 0.08,
        "pass_rush_finesse": 0.06,
        "acceleration": 0.06,
        "first_step": 0.06,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.06' (Severity: Low   Confidence: Medium)
        "pass_rush_finesse": 0.06,
```


---

### File: `backend/app/services/ratings_generator.py`
**Lines of Code:** 196
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

    # Tier 3
    ratings["pass_block"] = 50 + random.randint(-5, 10)

    return ratings

# Proposed Fix:
    ratings["pass_block"] = 50 + secrets.randbelow(-5, 10)
```


---

### File: `backend/app/services/ratings_generator.py`
**Lines of Code:** 232
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        ratings["agility"] = inverse_scale(shuttle, 4.4, 4.9)

    ratings["stamina"] = 70 + random.randint(0, 15)

    return ratings

# Proposed Fix:
    ratings["stamina"] = 70 + secrets.randbelow(0, 15)
```


---

### File: `backend/app/services/ratings_generator.py`
**Lines of Code:** 374
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        ratings["awareness"] = scale_percentile(ints, 0, 6)
        ratings["tackle"] = scale_percentile(tackles, 30, 90)
        ratings["hit_power"] = 60 + random.randint(-5, 15)

    return ratings

# Proposed Fix:
        ratings["hit_power"] = 60 + secrets.randbelow(-5, 15)
```


---

### File: `backend/app/services/ratings_generator.py`
**Lines of Code:** 423
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # Default ratings for K, P, LS, etc.
        return {
            "kick_power": 70 + random.randint(-10, 20),
            "kick_accuracy": 70 + random.randint(-10, 20),
        }

# Proposed Fix:
            "kick_power": 70 + secrets.randbelow(-10, 20),
```


---

### File: `backend/app/services/ratings_generator.py`
**Lines of Code:** 424
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        return {
            "kick_power": 70 + random.randint(-10, 20),
            "kick_accuracy": 70 + random.randint(-10, 20),
        }


# Proposed Fix:
            "kick_accuracy": 70 + secrets.randbelow(-10, 20),
```


---

### File: `backend/app/services/rookie_generator.py`
**Lines of Code:** 21
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        self.db = db
        # Use provided seed or a random one if not provided, but encapsulated in DeterministicRNG
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

    async def generate_draft_class(self, season_id: int, count: int = 256):

# Proposed Fix:
        self.rng = DeterministicRNG(seed if seed is not None else secrets.randbelow(0, 1000000))
```


---

### File: `backend/app/services/schedule_generator.py`
**Lines of Code:** 28
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
    def __init__(self, db: Session, seed: int = None):
        self.db = db
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

    def generate_schedule(

# Proposed Fix:
        self.rng = DeterministicRNG(seed if seed is not None else secrets.randbelow(0, 1000000))
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 109
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        speed_rating = true_attributes.get("speed", 50)
        base_40 = 5.4 - (speed_rating * 0.012)
        variance_40 = random.uniform(-0.05, 0.05)
        forty = round(base_40 + variance_40, 2)


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        variance_40 = random.uniform(-0.05, 0.05)
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 117
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # 99 Str ~ 365 lbs, 50 Str ~ 250 lbs
        base_power_clean = 200 + (strength * 1.65)
        power_clean = int(base_power_clean + random.uniform(-10, 15))

        # 3. Vertical (Jumping)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        power_clean = int(base_power_clean + random.uniform(-10, 15))
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 122
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        jump = true_attributes.get("jumping", 50)
        base_vert = 20 + (jump * 0.25)
        vert = round(base_vert + random.uniform(-1.5, 1.5), 1)

        # 4. 3-Cone (Agility)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        vert = round(base_vert + random.uniform(-1.5, 1.5), 1)
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 127
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        agility = true_attributes.get("agility", 50)
        base_cone = 8.1 - (agility * 0.016)
        cone = round(base_cone + random.uniform(-0.1, 0.1), 2)

        # 5. Broad Jump (Explosion - mix of Jump/Str)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        cone = round(base_cone + random.uniform(-0.1, 0.1), 2)
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 131
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # 5. Broad Jump (Explosion - mix of Jump/Str)
        base_broad = 100 + (jump * 0.3) + (strength * 0.1)
        broad = int(base_broad + random.uniform(-4, 4))

        # 6. Shuttle (Change of Direction - Agility/Accel)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        broad = int(base_broad + random.uniform(-4, 4))
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 136
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        accel = true_attributes.get("acceleration", 50)
        base_shuttle = 4.9 - (agility * 0.005) - (accel * 0.005)
        shuttle = round(base_shuttle + random.uniform(-0.05, 0.05), 2)

        # 7. GPS Tracked Speed (B-039)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        shuttle = round(base_shuttle + random.uniform(-0.05, 0.05), 2)
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 142
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # 99 Speed ~ 23 mph, 50 Speed ~ 18 mph
        base_gps = 15 + (speed_rating * 0.08)
        gps_speed = round(base_gps + random.uniform(-0.3, 0.5), 1)

        # 8. Position Agility Score (B-040)

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        gps_speed = round(base_gps + random.uniform(-0.3, 0.5), 1)
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 147
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # Composite of agility, acceleration, and position-specific tests
        base_agility_score = (agility * 0.4) + (accel * 0.3) + (speed_rating * 0.3)
        position_agility = round(base_agility_score + random.uniform(-3, 5), 1)

        return CombineResults(

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        position_agility = round(base_agility_score + random.uniform(-3, 5), 1)
```


---

### File: `backend/app/services/scouting/combine.py`
**Lines of Code:** 193
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                class SimpleRNG:
                    def next_float(self) -> float:
                        return random.random()
                rng = SimpleRNG()


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
                        return random.random()
```


---

### File: `backend/app/services/scouting/scout.py`
**Lines of Code:** 125
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
            # Final Value Calculation
            # Noise is random error + systematic bias
            noise = random.randint(-max_error, max_error)
            perceived_val = max(0, min(99, true_val + noise + bias_shift))


# Proposed Fix:
            noise = secrets.randbelow(-max_error, max_error)
```


---

### File: `backend/app/services/stadium/crowd.py`
**Lines of Code:** 105
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        # Chant on big plays
        if event in ["TOUCHDOWN", "SACK", "TURNOVER"]:
            return random.random() < (self.base_passion / 100.0)
        return False


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
            return random.random() < (self.base_passion / 100.0)
```


---

### File: `backend/app/services/stadium/crowd.py`
**Lines of Code:** 111
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        """Wave happens when crowd is happy and there's a lull."""
        if mood in [CrowdMood.ELECTRIC, CrowdMood.EXCITED]:
            return random.random() < 0.1  # 10% chance
        return False


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
            return random.random() < 0.1  # 10% chance
```


---

### File: `backend/app/services/training/camp.py`
**Lines of Code:** 177
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                base_gain = 10.0 * config.xp_multiplier * intensity_mod
                # Randomized minor fluctuation
                gain = base_gain * random.uniform(0.9, 1.1)
                player_total_xp += gain


# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
                gain = base_gain * random.uniform(0.9, 1.1)
```


---

### File: `backend/app/services/training/camp.py`
**Lines of Code:** 186
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                risk = config.injury_risk_base * intensity_mod
                # Simplistic roll - would normally check player health stats
                if random.random() < (risk / 100.0): # Convert percent to probability
                    injuries.append(f"{pid} injured during {config.name}")
                    player_total_xp *= 0.5 # Reduced gain if injured

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
                if random.random() < (risk / 100.0): # Convert percent to probability
```


---

### File: `backend/app/services/training/coach_expertise.py`
**Lines of Code:** 78
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_RUSH_SPECIALIST' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    RECEIVING_COACH = "RECEIVING_COACH"
    DB_WHISPERER = "DB_WHISPERER"
    PASS_RUSH_SPECIALIST = "PASS_RUSH_SPECIALIST"
    LB_GURU = "LB_GURU"
    SPECIAL_TEAMS_ACE = "SPECIAL_TEAMS_ACE"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_RUSH_SPECIALIST' (Severity: Low   Confidence: Medium)
    PASS_RUSH_SPECIALIST = "PASS_RUSH_SPECIALIST"
```


---

### File: `backend/app/services/training/drills.py`
**Lines of Code:** 734
**Error:** [B101:assert_used] Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:

# Count validation
assert len(ALL_DRILLS) >= 50, f"Expected 50+ drills, got {len(ALL_DRILLS)}"

# Proposed Fix:
    # FIX: [B101:assert_used] Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. (Severity: Low   Confidence: High)
assert len(ALL_DRILLS) >= 50, f"Expected 50+ drills, got {len(ALL_DRILLS)}"
```


---

### File: `backend/app/services/training/progression.py`
**Lines of Code:** 225
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
            if attr in ["speed", "acceleration", "agility", "jumping"]:
                # Physical traits hit hardest
                if random.random() < loss_chance:
                    loss = random.randint(1, 1 + years_past_prime)
                    regressed_attrs[attr] = -loss

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
                if random.random() < loss_chance:
```


---

### File: `backend/app/services/training/progression.py`
**Lines of Code:** 226
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                # Physical traits hit hardest
                if random.random() < loss_chance:
                    loss = random.randint(1, 1 + years_past_prime)
                    regressed_attrs[attr] = -loss
            elif attr in ["strength", "throw_power"]:

# Proposed Fix:
                    loss = secrets.randbelow(1, 1 + years_past_prime)
```


---

### File: `backend/app/services/training/progression.py`
**Lines of Code:** 230
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
            elif attr in ["strength", "throw_power"]:
                # Power traits hit slower
                if random.random() < (loss_chance * 0.6):
                    loss = random.randint(1, 2)
                    regressed_attrs[attr] = -loss

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
                if random.random() < (loss_chance * 0.6):
```


---

### File: `backend/app/services/training/progression.py`
**Lines of Code:** 231
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
                # Power traits hit slower
                if random.random() < (loss_chance * 0.6):
                    loss = random.randint(1, 2)
                    regressed_attrs[attr] = -loss
            elif attr in ["awareness", "play_recognition"]:

# Proposed Fix:
                    loss = secrets.randbelow(1, 2)
```


---

### File: `backend/app/services/training/training_programs.py`
**Lines of Code:** 99
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.75' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        "catching": 0.7,
        "route_running": 0.6,
        "pass_block": 0.75,
        "trucking": 0.5,
        "elusiveness": 0.65,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.75' (Severity: Low   Confidence: Medium)
        "pass_block": 0.75,
```


---

### File: `backend/app/services/training/training_programs.py`
**Lines of Code:** 135
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '0.9' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    },
    "OL": {
        "pass_block": 0.9,
        "run_block": 0.85,
        "strength": 0.5,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '0.9' (Severity: Low   Confidence: Medium)
        "pass_block": 0.9,
```


---

### File: `backend/app/services/training/training_programs.py`
**Lines of Code:** 172
**Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
**Solve:**
```python
# Original Code:
        self.season_phase = season_phase
        self.phase_config = PHASE_CONFIGS[season_phase]
        self.rng = random.Random(seed)

    def calculate_xp_threshold(self, current_rating: int) -> int:

# Proposed Fix:
    # FIX: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes. (Severity: Low   Confidence: High)
        self.rng = random.Random(seed)
```


---

### File: `backend/app/services/trait_service.py`
**Lines of Code:** 140
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '10' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
        effects={
            "chip_block_success_rate": 0.40,
            "pass_protection_boost": 10,
            "route_timing_after_chip": 0.15,
            "blitz_awareness_boost": 5,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '10' (Severity: Low   Confidence: Medium)
            "pass_protection_boost": 10,
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 30
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_COMPLETION_SHORT' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    """Types of in-game actions that award attribute XP."""
    # Passing Actions
    PASS_COMPLETION_SHORT = "PASS_COMPLETION_SHORT"
    PASS_COMPLETION_MID = "PASS_COMPLETION_MID"
    PASS_COMPLETION_DEEP = "PASS_COMPLETION_DEEP"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_COMPLETION_SHORT' (Severity: Low   Confidence: Medium)
    PASS_COMPLETION_SHORT = "PASS_COMPLETION_SHORT"
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 31
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_COMPLETION_MID' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    # Passing Actions
    PASS_COMPLETION_SHORT = "PASS_COMPLETION_SHORT"
    PASS_COMPLETION_MID = "PASS_COMPLETION_MID"
    PASS_COMPLETION_DEEP = "PASS_COMPLETION_DEEP"
    PASS_UNDER_PRESSURE = "PASS_UNDER_PRESSURE"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_COMPLETION_MID' (Severity: Low   Confidence: Medium)
    PASS_COMPLETION_MID = "PASS_COMPLETION_MID"
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 32
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_COMPLETION_DEEP' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    PASS_COMPLETION_SHORT = "PASS_COMPLETION_SHORT"
    PASS_COMPLETION_MID = "PASS_COMPLETION_MID"
    PASS_COMPLETION_DEEP = "PASS_COMPLETION_DEEP"
    PASS_UNDER_PRESSURE = "PASS_UNDER_PRESSURE"
    TOUCHDOWN_PASS = "TOUCHDOWN_PASS"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_COMPLETION_DEEP' (Severity: Low   Confidence: Medium)
    PASS_COMPLETION_DEEP = "PASS_COMPLETION_DEEP"
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 33
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_UNDER_PRESSURE' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    PASS_COMPLETION_MID = "PASS_COMPLETION_MID"
    PASS_COMPLETION_DEEP = "PASS_COMPLETION_DEEP"
    PASS_UNDER_PRESSURE = "PASS_UNDER_PRESSURE"
    TOUCHDOWN_PASS = "TOUCHDOWN_PASS"


# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_UNDER_PRESSURE' (Severity: Low   Confidence: Medium)
    PASS_UNDER_PRESSURE = "PASS_UNDER_PRESSURE"
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 34
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'TOUCHDOWN_PASS' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    PASS_COMPLETION_DEEP = "PASS_COMPLETION_DEEP"
    PASS_UNDER_PRESSURE = "PASS_UNDER_PRESSURE"
    TOUCHDOWN_PASS = "TOUCHDOWN_PASS"

    # Rushing Actions

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'TOUCHDOWN_PASS' (Severity: Low   Confidence: Medium)
    TOUCHDOWN_PASS = "TOUCHDOWN_PASS"
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 51
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_PRO_WIN' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    PANCAKE_BLOCK = "PANCAKE_BLOCK"
    SUSTAINED_BLOCK = "SUSTAINED_BLOCK"
    PASS_PRO_WIN = "PASS_PRO_WIN"

    # Defensive Actions

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_PRO_WIN' (Severity: Low   Confidence: Medium)
    PASS_PRO_WIN = "PASS_PRO_WIN"
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 58
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_DEFENDED' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    SACK = "SACK"
    QB_HIT = "QB_HIT"
    PASS_DEFENDED = "PASS_DEFENDED"
    INTERCEPTION = "INTERCEPTION"
    FORCED_FUMBLE = "FORCED_FUMBLE"

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: 'PASS_DEFENDED' (Severity: Low   Confidence: Medium)
    PASS_DEFENDED = "PASS_DEFENDED"
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 141
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '2' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    ActionType.SUSTAINED_BLOCK: {
        "run_block": 2,
        "pass_block": 2,
    },
    ActionType.PASS_PRO_WIN: {

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '2' (Severity: Low   Confidence: Medium)
        "pass_block": 2,
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 144
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '4' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    },
    ActionType.PASS_PRO_WIN: {
        "pass_block": 4,
        "awareness": 1,
    },

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '4' (Severity: Low   Confidence: Medium)
        "pass_block": 4,
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 160
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    ActionType.SACK: {
        "tackle": 3,
        "pass_rush": 5,
        "power_moves": 2,
        "finesse_moves": 2,

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '5' (Severity: Low   Confidence: Medium)
        "pass_rush": 5,
```


---

### File: `backend/app/services/use_based_progression.py`
**Lines of Code:** 165
**Error:** [B105:hardcoded_password_string] Possible hardcoded password: '3' (Severity: Low   Confidence: Medium)
**Solve:**
```python
# Original Code:
    },
    ActionType.QB_HIT: {
        "pass_rush": 3,
        "pursuit": 2,
    },

# Proposed Fix:
    # FIX: [B105:hardcoded_password_string] Possible hardcoded password: '3' (Severity: Low   Confidence: Medium)
        "pass_rush": 3,
```


---
