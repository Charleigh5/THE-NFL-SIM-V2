# Trait System - Technical Specification

**Document ID**: NFL-SIM-TRAIT-001
**Status**: IMPLEMENTED (Phase 1)
**Date**: 2025-12-04
**Priority**: P1 (High)

---

## Executive Summary

The Trait System adds RPG-style character abilities to players, creating deeper strategic gameplay through unique player specializations. This is **Phase 1** of the trait system, implementing the foundational infrastructure and the **top 5 priority traits**.

**Current State**: Database models exist, basic trait tracking implemented
**Target State**: Full trait service with gameplay integration, UI display, and acquisition mechanics

**Estimated Lines**: ~750 lines (backend + frontend)
**Files Created**: 4 new, 2 modified

---

## System Architecture

### Component Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                          │
│  • TraitBadge component (player cards)                      │
│  • TraitTooltip (detailed info)                             │
│  • TraitAcquisitionNotification                             │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│  GET /api/traits/catalog                                    │
│  GET /api/traits/player/{id}                                │
│  POST /api/traits/grant                                     │
│  DELETE /api/traits/remove                                  │
│  GET /api/traits/eligibility/{player_id}/{trait_name}       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 TraitService (Business Logic)                │
│  • initialize_trait_catalog()                               │
│  • grant_trait_to_player()                                  │
│  • remove_trait_from_player()                               │
│  • get_player_traits()                                      │
│  • check_trait_activation()                                 │
│  • apply_trait_effects()                                    │
│  • check_trait_eligibility()                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Database Models (SQLAlchemy)                    │
│  • Trait (id, name, description)                            │
│  • PlayerTrait (player_id, trait_id) [Association Table]    │
│  • Player.traits (relationship)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Trait Catalog

### QB Traits

#### 1. Field General (Elite)

**Acquisition**: Auto-unlock at 90+ awareness, 3+ years experience
**Activation**: Whenever QB is on field with offense active
**Effects**:

- +5 awareness to ALL offensive players
- -15% penalty rate for entire offense
- +20% audible effectiveness
- +1.0 pre-snap adjustment bonus
  **Gameplay Impact**: Elite QBs elevate their entire unit, reducing mistakes and improving play-calling

#### 2. Gunslinger (Gold)

**Acquisition**: Stat Threshold
**Activation**: Pass Play
**Effects**:

- +5 throw power
- -10% release time
- +5% interception chance
  **Gameplay Impact**: Faster release and increased throw power, but slightly higher interception risk.

#### 3. Escape Artist (Gold)

**Acquisition**: Stat Threshold
**Activation**: Scramble
**Effects**:

- +10 scramble speed
- +10 agility
- +15% chance to break sack
  **Gameplay Impact**: Elite agility and speed when scrambling behind the line of scrimmage.

### RB Traits

#### 4. Chip Block Specialist (Silver)

**Acquisition**: Taught by coaching staff or progression
**Activation**: Pass plays when blitz detected
**Effects**:

- 40% chance to significantly slow rusher
- +10 pass protection rating
- +15% better route timing after chip
- +5 awareness vs blitz
  **Gameplay Impact**: Dual-threat backs become better pass protectors

#### 5. Bruiser (Gold)

**Acquisition**: Stat Threshold
**Activation**: Run Play, Contact
**Effects**:

- +10 trucking
- +10 stiff arm
- +25% chance to fall forward
  **Gameplay Impact**: Power runner who excels at trucking and stiff arms.

#### 6. Satellite (Silver)

**Acquisition**: Stat Threshold
**Activation**: Pass Play, Route Running
**Effects**:

- +10 route running
- +5 catching
- +15% mismatch bonus vs LB
  **Gameplay Impact**: Elite receiving back with receiver-like route running skills.

### WR/TE Traits

#### 7. Possession Receiver (Gold)

**Acquisition**: 100+ receptions in a season with <5% drop rate
**Activation**: Contested catch situations, traffic
**Effects**:

- +15 catching in traffic
- -30% drop rate
- -25% fumble chance after catch
- +10 awareness in catch situations
  **Gameplay Impact**: Reliable third-down target, clutch performer

#### 8. Deep Threat (Gold)

**Acquisition**: Stat Threshold
**Activation**: Deep Route
**Effects**:

- +5 speed on deep routes
- +10 deep ball tracking
- +10% separation bonus on deep routes
  **Gameplay Impact**: Specializes in deep routes and beating coverage over the top.

#### 9. Route Technician (Gold)

**Acquisition**: Stat Threshold
**Activation**: Cut Move
**Effects**:

- +10 route running
- +15% separation bonus on cuts
- +5 release
  **Gameplay Impact**: Elite footwork creates separation on sharp cuts.

#### 10. YAC Monster (Silver)

**Acquisition**: Stat Threshold
**Activation**: After Catch
**Effects**:

- +10 break tackle
- +10 elusiveness
- +5 juke move
  **Gameplay Impact**: Dangerous with the ball in hands, hard to tackle.

#### 11. Red Zone Threat (Gold)

**Acquisition**: Stat Threshold
**Activation**: Red Zone
**Effects**:

- +10 catching in Red Zone
- +10 contested catch in Red Zone
- +10 endzone awareness
  **Gameplay Impact**: Dominant inside the 20 yard line.

### OL Traits

#### 12. Anchor (Gold)

**Acquisition**: Stat Threshold
**Activation**: Pass Block, Vs Bull Rush
**Effects**:

- +10 strength blocking
- +10 balance
- +50% pancake resistance
  **Gameplay Impact**: Stout pass protector who rarely gives ground to bull rushes.

#### 13. Pull Specialist (Silver)

**Acquisition**: Coaching Unlock
**Activation**: Pull Block, Run Play
**Effects**:

- +10 speed when pulling
- +10 blocking in space
- +5 awareness when pulling
  **Gameplay Impact**: Agile lineman who excels at pulling and blocking in space.

### DL Traits

#### 14. Edge Threat (Gold)

**Acquisition**: Stat Threshold
**Activation**: Pass Rush, Edge Rush
**Effects**:

- +10 acceleration on rush
- +5 finesse move
- +15% chance to pressure QB
  **Gameplay Impact**: Explosive first step off the edge.

#### 15. Run Stuffer (Gold)

**Acquisition**: Stat Threshold
**Activation**: Run Defense
**Effects**:

- +10 block shedding vs run
- +5 strength vs run
- +5 tackle bonus vs run
  **Gameplay Impact**: Impossible to move in the run game, sheds blocks easily.

### LB Traits

#### 16. Green Dot - Defensive Captain (Elite)

**Acquisition**: Team designation (requires leadership)
**Activation**: Whenever LB is on field with defense active
**Effects**:

- +5 play recognition to ALL defenders
- +20% reduced blown assignments
- +15% blitz effectiveness
- +5 zone/man coverage for entire defense
  **Gameplay Impact**: Defensive quarterbacks coordinate entire unit

#### 17. Coverage Linebacker (Gold)

**Acquisition**: Stat Threshold
**Activation**: Coverage
**Effects**:

- +10 zone coverage
- +5 man coverage
- -10% reaction time
  **Gameplay Impact**: Linebacker with safety-like coverage skills.

#### 18. Enforcer (Silver)

**Acquisition**: Stat Threshold
**Activation**: Tackle, Hit Stick
**Effects**:

- +10 hit power
- +15% forced fumble chance
- +20% fatigue damage to ball carrier
  **Gameplay Impact**: Heavy hitter who causes more fumbles and fatigue.

### DB Traits

#### 19. Pick Artist (Gold)

**Acquisition**: 5+ INTs in a season
**Activation**: Ball in air, in coverage
**Effects**:

- +50% interception rate (1.5x multiplier)
- +30% catch radius for INTs
- +15 ball tracking
- +20% faster reaction to thrown ball
  **Gameplay Impact**: Game-changing ball hawks create turnovers

#### 20. Shutdown Corner (Elite)

**Acquisition**: Stat Threshold
**Activation**: Man Coverage
**Effects**:

- +10 man coverage
- +10 press coverage
- -20% receiver separation
  **Gameplay Impact**: Elite man coverage specialist who erases receivers.

#### 21. Zone Hawk (Gold)

**Acquisition**: Stat Threshold
**Activation**: Zone Coverage
**Effects**:

- +10 zone coverage
- -15% reaction time in zone
- +10% interception chance in zone
  **Gameplay Impact**: Elite zone coverage instincts and break-on-ball speed.

### Special Teams Traits

#### 22. Clutch Kicker (Silver)

**Acquisition**: Stat Threshold
**Activation**: Clutch Moment, Field Goal
**Effects**:

- +15 accuracy in clutch
- Immune to "Ice the Kicker"
- +5 kick power in clutch
  **Gameplay Impact**: Immune to pressure in critical game-winning situations.

#### 23. Coffin Corner (Silver)

**Acquisition**: Stat Threshold
**Activation**: Punt Inside 50
**Effects**:

- +15 accuracy
- +30% backspin chance
- -20% touchback chance
  **Gameplay Impact**: Elite precision punting inside the 20.

### General Traits

#### 24. Iron Man (Silver)

**Acquisition**: Progression
**Activation**: Always
**Effects**:

- +20% fatigue recovery
- +15% injury resistance
- -10% stamina drain
  **Gameplay Impact**: Superior conditioning and durability.

#### 25. Mentor (Silver)

**Acquisition**: Progression
**Activation**: Weekly Training
**Effects**:

- +10% XP boost to position group
- Delays regression
  **Gameplay Impact**: Veteran presence that accelerates development of younger players.

## Database Schema

### Existing Models (Already in place)

```python
class Trait(Base):
    __tablename__ = 'traits'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

class PlayerTrait(Base):
    __tablename__ = 'player_traits'
    player_id = Column(Integer, ForeignKey('player.id'), primary_key=True)
    trait_id = Column(Integer, ForeignKey('traits.id'), primary_key=True)

class Player(Base):
    # ... existing fields ...
    traits = relationship("Trait", secondary="player_traits")
```

**No migration needed** - schema already exists!

---

## API Design

### 1. GET /api/traits/catalog

**Response**:

```json
[
  {
    "name": "Field General",
    "description": "Elite QB leadership...",
    "position_requirements": ["QB"],
    "acquisition_method": "AUTO_UNLOCK",
    "effects": {
      "team_awareness_boost": 5,
      "team_penalty_reduction": 0.15
    },
    "tier": "ELITE"
  }
]
```

### 2. GET /api/traits/player/{player_id}

**Response**:

```json
{
  "player_id": 123,
  "player_name": "John Smith",
  "position": "QB",
  "traits": [
    {
      "name": "Field General",
      "effects": {...}
    }
  ]
}
```

### 3. POST /api/traits/grant

**Request**:

```json
{
  "player_id": 123,
  "trait_name": "Field General"
}
```

**Response**:

```json
{
  "message": "Successfully granted 'Field General' to player 123"
}
```

---

## Trait Acquisition Methods

| Method             | Description                               | Example                                  |
| ------------------ | ----------------------------------------- | ---------------------------------------- |
| `AUTO_UNLOCK`      | Automatically granted when conditions met | Field General (90 AWR + 3 YOE)           |
| `STAT_THRESHOLD`   | Earned via season performance             | Possession Receiver (100 REC, <5% drops) |
| `COACHING_UNLOCK`  | Taught by coaching staff                  | Chip Block Specialist                    |
| `TEAM_DESIGNATION` | Assigned by team (captain, etc)           | Green Dot                                |
| `PROGRESSION`      | Unlocked via XP/level                     | Future traits                            |

---

## Gameplay Integration Points

### 1. Pre-Game (MatchContext Setup)

```python
# Apply traits when loading roster
for player in team_roster:
    traits = await trait_service.get_player_traits(player.id)
    for trait in traits:
        if trait_service.check_trait_activation(trait, {"triggers": ["ON_FIELD"]}):
            trait_service.apply_trait_effects(player, trait, context)
```

### 2. During Play Resolution

```python
# Check for situational traits
if situation == "CONTESTED_CATCH":
    if player.has_trait("Possession Receiver"):
        catching_bonus = get_trait_effect("contested_catch_bonus")  # +15
        player.catching += catching_bonus
```

### 3. Post-Season (Trait Acquisition)

```python
# Check eligibility after season
for player in all_players:
    if player.position == "CB" and player.season_stats.interceptions >= 5:
        await trait_service.grant_trait_to_player(player.id, "Pick Artist")
```

---

## Testing Strategy

### Unit Tests ✅

- [x] Trait catalog validation
- [x] Eligibility checking
- [x] Effect structures
- [x] Tier classification
- [x] Position requirements

**Status**: 9/9 tests passing

### Integration Tests (TODO)

- [ ] Trait grant/remove flow
- [ ] Database persistence
- [ ] API endpoint testing
- [ ] Gameplay integration

---

## Implementation Checklist

### Phase 1: Foundation ✅ (COMPLETE)

- [x] `TraitService` with catalog
- [x] Top 5 trait definitions
- [x] API endpoints
- [x] Router registration
- [x] Unit tests (9/9 passing)

### Phase 2: Gameplay Integration (Next)

- [ ] Integrate trait effects into PlayResolver
- [ ] Add trait checks in pre-game setup
- [ ] Implement Field General team boosts
- [ ] Implement Possession Receiver catch bonus
- [ ] Implement Green Dot defensive coordination

### Phase 3: UI Integration

- [ ] Create `TraitBadge` component
- [ ] Create `TraitTooltip` component
- [ ] Add traits to player cards
- [ ] Add trait notifications

### Phase 4: Acquisition Mechanics

- [ ] Post-season trait grant logic
- [ ] Eligibility checking in offseason
- [ ] Coaching unlock interface

---

## Files Created

1. `backend/app/services/trait_service.py` (350 lines)
2. `backend/app/api/endpoints/traits.py` (200 lines)
3. `backend/tests/unit/test_trait_service.py` (150 lines)
4. `docs/specs/trait_system_spec.md` (this file)

## Files Modified

1. `backend/app/main.py` (+2 lines - router registration)

---

## Performance Considerations

- **Trait lookup**: O(1) hash map lookup from TRAIT_CATALOG
- **Player traits query**: Single JOIN query with proper indexing
- **Effect application**: In-memory modifications to player objects

**No performance concerns expected** - trait checks are lightweight

---

## Future Enhancements (Phase 2+)

1. **Expanded Catalog**: 25 traits implemented (Complete)
2. **Attribute Interactions**: Cross-attribute effects system ✅ (See `attribute_interaction_spec.md`)
3. **Trait Trees**: Prerequisites and synergies
4. **Dynamic Traits**: Temporary boosts (e.g., "Hot Hand")
5. **Trait Evolution**: Traits that upgrade over time
6. **Negative Traits**: Debuffs and weaknesses

---

## Related Systems

- **Attribute Interaction Engine**: See [`attribute_interaction_spec.md`](./attribute_interaction_spec.md) for cross-attribute effects (Set 3)
- **Gameplay Integration**: Traits interact with the AttributeInteractionEngine to create compound effects

---

## Status Summary

✅ **Phase 1 - COMPLETE** (Foundation)

- Service layer: 100%
- API layer: 100%
- Tests: 100% (9/9 passing)
- Documentation: Complete

✅ **Set 2 - COMPLETE** (Expanded Catalog)

- 25 traits implemented across all position groups
- Tests: 100% passing
- Documentation: Complete

✅ **Set 3 - COMPLETE** (Attribute Interactions)

- AttributeInteractionEngine: 100%
- 12+ cross-attribute interactions defined
- Tests: 100% (33/33 passing)
- Documentation: Complete

🔄 **Next: Set 4 - Gameplay Integration**

- Integrate traits with AttributeInteractionEngine
- Wire interactions into PlayResolver
- UI display of trait/interaction effects

---

END OF DOCUMENT
