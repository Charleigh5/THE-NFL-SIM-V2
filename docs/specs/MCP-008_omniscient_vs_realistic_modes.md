# MCP-008: Omniscient vs Realistic Modes

**Feature ID:** MCP-008
**Status:** SPEC_COMPLETE
**Implementation Status:** IMPLEMENTED (Realistic Default)

## 1. Overview

This feature governs the visibility of "True Attributes" (the data used by the Simulation Engine) versus "Display Attributes" (the data shown to the user). It supports two modes:

1. **Realistic (Fog of War):** Users see estimates, ranges, or "???" based on scouting.
2. **Omniscient (God Mode):** Users see exact ratings (0-100) for all data.

## 2. Current Implementation (`services/scouting/scouting_service.py`)

The system defaults to **Realistic**.

### 2.1 Fog of War Logic

The `ScoutingService.apply_fog_of_war` method:

- Input: `true_attributes`, `ScoutingReport`.
- Logic:
  - If completion == 0%: Returns "???".
  - If Tier == `UNKNOWN`: Returns a wide range (e.g., 60-80).
  - If Tier == `PARTIAL`: Returns a narrow range or grade (e.g., "B+").
  - If Tier == `EXACT`: Returns the value.

### 2.2 Knowledge Tiers

Defined in `scout.py`:

- `UNKNOWN`: No data.
- `ESTIMATE`: Broad range.
- `PARTIAL`: Narrow range / Letter Grade.
- `EXACT`: Numerical precision.

## 3. Omniscient Mode Specification

To enable Omniscient Mode:

### 3.1 Settings Configuration

A global configuration or User Setting `settings.enable_omniscient_mode` (Boolean) controls this.

### 3.2 Service Bypass

In `ScoutingService`:

```python
def get_formatted_report(self, ...):
    if settings.enable_omniscient_mode:
        # Return exact values immediately, bypassing Scout Logic
        return {k: str(v) for k,v in true_attributes.items()}

    # ... else proceed with standard Fog of War
```

## 4. User Experience

- **Draft Room:** In Realistic, prospects have grades (A, B, C). In Omniscient, they have exact numbers (88, 72, 65).
- **Roster:** Opposing player ratings are hidden/estimated in Realistic, visible in Omniscient.
