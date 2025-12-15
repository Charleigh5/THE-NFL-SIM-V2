# MCP-011: Trade Value Formula

**Feature ID:** MCP-011
**Status:** SPEC_COMPLETE
**Implementation Status:** IMPLEMENTED

## 1. Overview

The Trade Value Formula determines the "currency" value of players and draft picks to facilitate fair trades between the User and AI, or AI vs AI. It ensures that star players demand significant returns and that draft picks follow standard valuation charts (Jimmy Johnson / Fitzgerald-Spielberger).

## 2. Integration (`services/gm_agent.py`)

The core logic resides in `GMAgent._calculate_package_value`.

### 2.1 Player Valuation Algorithm

A player's trade value is a product of several multipliers:
$$ Value = Base \times Age \times Position \times Contract \times Risk $$

1. **Base Value (Exponential):**

   - Based on Overall Rating (OVR).
   - Formula: `((OVR - 50) ^ 1.6) / 2.0`.
   - _Impact:_ A 90 OVR player is exponentially more valuable than a 75 OVR player.

2. **Age Modifier:**

   - `< 24`: 1.3x (Young Premium).
   - `> 30`: 0.95x - 0.5x (Veteran Decline).

3. **Positional Value:**

   - QB: Highest multiplier (e.g. 1.2x - 1.5x).
   - RB/Special Teams: Lower multiplier.
   - Source: `trade_config.py`.

4. **Contract Efficiency:**

   - Cheap Production (Rookie Deal / Star Performance): 1.1x - 1.25x.
   - Overpaid (Albatross): 0.6x - 0.85x.

5. **Flight Risk:**
   - Expiring contract on a bad team: 0.85x (Rental Discount).

### 2.2 Draft Pick Valuation

- **Current Year:** Uses standard Draft Value Chart (e.g., Pick 1 = 3000 pts).
- **Future Years:** Discounted by one round per year out.
- **Normalization:** Draft points are normalized to the Player Value scale (approx `/ 30.0`) so that a 1st Round Pick (~1000 pts) equates to a solid Starter (~33 player value).

## 3. Trade Acceptance Logic

A trade is accepted if:
`Offered Value >= Requested Value - AggressionModifier`

- **Aggression:** An Aggressive GM might overpay (lower threshold) to get their guy.
- **Team Needs:** Players at positions of need receive a further value boost (e.g. 1.2x) during evaluation by the acquiring team.
