# Attribute Interaction Engine - Technical Specification

**Document ID**: NFL-SIM-ATTR-INT-001
**Status**: IMPLEMENTED (Set 3)
**Date**: 2025-12-04
**Priority**: P1 (High)

---

## Executive Summary

The **Attribute Interaction Engine** models complex cross-attribute effects between players in head-to-head matchups. Unlike simple skill comparisons (A vs B), this system creates emergent gameplay outcomes that reward strategic roster construction and simulate the chess-match nature of real football.

**Key Examples**:

- **QB Hard Count** vs **DL Discipline** (pre-snap mind games)
- **WR Release** vs **CB Press** (line-of-scrimmage battle)
- **OL Anchor** vs **DL First Step** (pass protection)
- **RB Patience** vs **LB Run Fit** (running game chess)

**Files Created**: 1 new, 1 test file
**Total Lines**: ~800 lines

---

## System Architecture

### Component Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                 AttributeInteractionEngine                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              INTERACTION_CATALOG                      │   │
│  │  • hard_count_vs_discipline                          │   │
│  │  • wr_release_vs_cb_press                            │   │
│  │  • ol_anchor_vs_dl_first_step                        │   │
│  │  • route_running_vs_man_coverage                     │   │
│  │  • rb_patience_vs_lb_run_fit                         │   │
│  │  • ... 12+ defined interactions                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌───────────────┐  ┌──────────────┐  ┌────────────────┐   │
│  │ PRIMARY ATTR  │  │ SECONDARY    │  │ SITUATIONAL    │   │
│  │ COMPARISON    │──│ MODIFIERS    │──│ CONTEXT        │   │
│  │               │  │ (25% weight) │  │ (home, weather)│   │
│  └───────┬───────┘  └──────────────┘  └────────────────┘   │
│          │                                                  │
│          ▼                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              InteractionResult                        │   │
│  │  • outcome (DOMINANT_WIN → DOMINANT_LOSS)            │   │
│  │  • winner_boost / loser_penalty                      │   │
│  │  • narrative text                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Interaction Types

| Type                | Description                     | When Applied          |
| ------------------- | ------------------------------- | --------------------- |
| `PRE_SNAP`          | Mind games before the play      | Before snap animation |
| `LINE_OF_SCRIMMAGE` | Initial contact battles         | At snap               |
| `PASS_PROTECTION`   | OL vs DL blocking battles       | During pass plays     |
| `ROUTE_VS_COVERAGE` | WR routes vs DB coverage        | Post-snap             |
| `RUN_GAME`          | RB vision vs LB gap play        | During run plays      |
| `BALL_CARRIER`      | YAC battles after catch/handoff | After initial play    |
| `LEADERSHIP`        | Team-wide influence effects     | Always active         |

---

## Interaction Outcomes

| Outcome         | Differential | Effect                              |
| --------------- | ------------ | ----------------------------------- |
| `DOMINANT_WIN`  | ≥15 pts      | Max boost, partial penalty to loser |
| `WIN`           | 8-14 pts     | Strong boost, minor penalty         |
| `SLIGHT_WIN`    | 2-7 pts      | Small boost, minimal penalty        |
| `NEUTRAL`       | -1 to +1     | No effect                           |
| `SLIGHT_LOSS`   | -2 to -7     | Small penalty                       |
| `LOSS`          | -8 to -14    | Strong penalty                      |
| `DOMINANT_LOSS` | ≤-15 pts     | Max penalty                         |

---

## Implemented Interactions (12+)

### 1. Hard Count vs Discipline (PRE_SNAP)

```python
attacker_attr = "awareness"      # QB
defender_attr = "discipline"     # DL
importance = 1.5                 # High impact - free play potential
```

**Situational Modifiers**:

- `HOME`: +10% (crowd noise advantage)
- `LOUD_STADIUM`: +15%
- `PLAYOFF`: -10% (defenders more focused)

---

### 2. WR Release vs CB Press (LINE_OF_SCRIMMAGE)

```python
attacker_attr = "release"
defender_attr = "press"
importance = 1.4
```

**Situational Modifiers**:

- `RAIN`: -15% (slippery footing)
- `MAN_COVERAGE`: +20%
- `ZONE`: -10%

---

### 3. OL Anchor vs DL First Step (PASS_PROTECTION)

```python
attacker_attr = "first_step"
defender_attr = "anchor"
importance = 1.8                 # Critical for pass protection
```

**Situational Modifiers**:

- `4TH_QUARTER`: +10% (fatigue helps DL)
- `LONG_DRIVE`: +15%
- `RAIN`: -10%

---

### 4. Route Running vs Man Coverage (ROUTE_VS_COVERAGE)

```python
attacker_attr = "route_running"
defender_attr = "man_coverage"
importance = 1.6
```

---

### 5. RB Patience vs LB Run Fit (RUN_GAME)

```python
attacker_attr = "patience"
defender_attr = "run_fit"
importance = 1.5
```

---

### Additional Interactions

6. **Coverage Disguise vs Pre-Snap Read**
7. **TE Block-Release vs LB Coverage**
8. **OL Discipline vs DL Inside Counter**
9. **RB Chip vs LB Blitz Timing**
10. **Ball Tracking vs Throw Placement**
11. **OL Pull Speed vs DL Gap Integrity**
12. **Juke Efficiency vs Open Field Tackle**
13. **Field General Leadership Influence**

---

## API Usage

### Basic Calculation

```python
from app.engine.attribute_interaction import AttributeInteractionEngine

engine = AttributeInteractionEngine(rng=deterministic_rng)

result = engine.calculate_interaction(
    "hard_count_vs_discipline",
    qb_player,
    dl_player,
    context={"HOME": True, "PLAYOFF": True}
)

print(result.outcome)        # InteractionOutcome.WIN
print(result.winner_boost)   # 4.5
print(result.narrative)      # "Mahomes masterfully draws Edge offsides..."
```

### Batch Processing

```python
matchups = [
    ("hard_count_vs_discipline", qb, dl),
    ("wr_release_vs_cb_press", wr, cb),
    ("ol_anchor_vs_dl_first_step", lt, re),
]

results = engine.batch_calculate_interactions(matchups, context)
```

### Integration Helper

```python
from app.engine.attribute_interaction import apply_interaction_to_play

aggregate = apply_interaction_to_play(engine, play_context, matchups)

print(aggregate["total_offense_boost"])   # 7.5
print(aggregate["total_defense_boost"])   # 2.1
print(aggregate["dominant_events"])       # List of game-changing moments
```

---

## Calculation Formula

```
Final Differential = (
    AttackerPrimary
    + SecondaryBonuses (25% each, max 2 attrs)
    + SituationalModifiers (scaled by 10x)
    + ExperienceModifier (capped at ±5)
    + RandomVariance (-3 to +3)
) - (
    DefenderPrimary
    + SecondaryBonuses
)

Effect = min(ScaledDifferential × 0.2, 15.0)
```

---

## Testing Strategy

### Unit Tests ✅

- [x] Catalog completeness validation
- [x] Outcome threshold accuracy
- [x] Situational modifier stacking
- [x] Experience bonus calculations
- [x] Narrative generation
- [x] Batch processing
- [x] Effect capping

**Status**: 33/33 tests passing

---

## Integration Points

### 1. PlayResolver Integration

```python
# In _resolve_pass_play():
interactions = engine.get_interactions_for_situation("PASS", "SNAP")
matchups = self._build_matchups(offense, defense, interactions)
effects = apply_interaction_to_play(engine, context, matchups)

# Apply to play outcome
accuracy_modifier += effects["total_offense_boost"]
pressure_modifier += effects["total_defense_boost"]
```

### 2. Pre-Game Setup

```python
# Check for pre-snap interactions (hard counts, disguises)
pregame_effects = engine.calculate_interaction(
    "coverage_disguise_vs_pre_snap_read",
    mike_lb,
    qb,
    context={"3RD_DOWN": True}
)
```

### 3. Narrative Engine

```python
# Feed dominant events to commentary
for event in aggregate["dominant_events"]:
    commentary_engine.add_highlight(event["narrative"])
```

---

## Future Enhancements

### Phase 2: Advanced Interactions

- [ ] Formation-specific interactions
- [ ] Personnel package modifiers
- [ ] Fatigue-decay on effectiveness
- [ ] Trait synergies with interactions

### Phase 3: AI Learning

- [ ] Track player tendencies in interactions
- [ ] AI coaches adjust based on matchup history
- [ ] Dynamic counter-play calling

---

## Files Created

1. `backend/app/engine/attribute_interaction.py` (~650 lines)
2. `backend/tests/unit/test_attribute_interaction.py` (~400 lines)
3. `docs/specs/attribute_interaction_spec.md` (this file)

---

## Performance Considerations

- **Lookup**: O(1) hash map for interaction catalog
- **Calculation**: O(1) per interaction
- **Batch**: O(n) where n = number of matchups
- **Memory**: Minimal - no persistent state between plays

**No performance concerns** - all operations are lightweight

---

## Status Summary

✅ **Set 3 - COMPLETE**

- AttributeInteractionEngine: 100%
- Interaction Catalog (12+ interactions): 100%
- Unit Tests: 100% (33/33 passing)
- Documentation: Complete

🔄 **Next: Set 4 - Gameplay Integration**

---

END OF DOCUMENT
