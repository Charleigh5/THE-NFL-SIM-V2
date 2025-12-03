# Probability Engine Design Document

## Overview

The `ProbabilityEngine` is the core mathematical kernel for resolving in-game events based on player attributes, environmental factors, and random chance. It replaces legacy coin-flip logic with a deterministic yet variable system that rewards better players and strategies.

## Core Concepts

### 1. Attribute Comparison

All contested actions (e.g., WR vs CB, OL vs DL) are resolved by comparing relevant attributes.

- **Delta**: `Attacker Attribute - Defender Attribute`
- **Scaling**: The delta is scaled to a probability modifier (e.g., +10 delta = +10% success chance).
- **Caps**: Modifiers are capped to prevent automatic wins/losses (e.g., max +/- 30%).

### 2. Base Probabilities

Every action has a base probability of success (e.g., a short pass has a base 75% completion rate).

- **Formula**: `Final Probability = Base Probability + Attribute Modifiers + Context Modifiers`

### 3. Tiered Outcomes

Outcomes are not binary. We support four tiers of result:

- **Critical Failure**: Turnover, Sack, or huge loss. (Roll < 0.05)
- **Failure**: Incomplete pass, stuffed run.
- **Success**: Completion, positive gain.
- **Critical Success**: Big play, broken tackle, touchdown. (Roll > 0.95)

### 4. Variance Models

- **Uniform**: For simple checks.
- **Normal Distribution (Bell Curve)**: For yards gained, to cluster results around the mean while allowing for outliers.

## API Design

### `compare_attributes(attacker_val: int, defender_val: int, scale: float = 0.01) -> float`

Compares two attributes and returns a probability modifier.

### `resolve_tiered_outcome(probability: float, critical_threshold: float = 0.05) -> OutcomeType`

Returns an `OutcomeType` enum based on the roll.

### `calculate_normal_outcome(mean: float, std_dev: float, min_val: float, max_val: float) -> float`

Returns a value from a normal distribution, useful for yards gained.

### `calculate_catch_probability(receiver: Player, defender: Player, throw_quality: float) -> float`

Specific helper for catch mechanics, factoring in:

- Receiver `Catching`, `Traffic`
- Defender `ManCoverage`, `ZoneCoverage`
- Throw Quality (from QB accuracy)

## Integration Plan

1. **Refactor `ProbabilityEngine` class**: Add new methods.
2. **Update `PlayResolver`**: Replace direct math with Engine calls.
3. **Unit Tests**: Verify distribution and edge cases.
