# Testing Attributes Convention

This document outlines the convention for using `data-testid` attributes in the application to facilitate End-to-End (E2E) testing with Playwright.

## General Rules

1.  **Attribute Name**: Always use `data-testid`.
2.  **Casing**: Use `kebab-case` for all values.
3.  **Structure**: The value should generally follow the structure: `[page/context]-[component]-[element]-[state/variant]`.

## Naming Patterns

### Pages
Top-level page containers should have a `data-testid` identifying the page.
-   `front-office-page`
-   `season-dashboard-page`
-   `offseason-dashboard-page`

### Components
Major components within a page should be identifiable.
-   `standings-table`
-   `league-leaders`
-   `playoff-bracket`

### Interactive Elements
Buttons, inputs, and links should be clearly labeled.
-   `[action]-button` (e.g., `simulate-week-button`, `save-roster-button`)
-   `[field]-input` (e.g., `player-search-input`)
-   `[destination]-link` (e.g., `view-roster-link`)

### Lists and Items
When rendering lists of items, the container and individual items should be accessible.
-   List Container: `[item-type]-list` (e.g., `player-list`, `team-list`)
-   List Item: `[item-type]-item-[id]` (e.g., `player-item-123`) or just `[item-type]-item` if filtering by text content.

### Specific Examples

#### Front Office
-   `front-office-header`
-   `roster-table`
-   `player-row-[player-id]`
-   `position-filter`

#### Season Dashboard
-   `season-summary-card`
-   `standings-table`
-   `schedule-view`
-   `simulate-week-button`

#### Playoff Bracket
-   `playoff-bracket-container`
-   `matchup-card-[matchup-id]`
-   `round-header-[round-name]`

#### Offseason Dashboard
-   `offseason-stage-indicator`
-   `draft-board`
-   `trade-modal`
-   `free-agency-list`

## Best Practices
-   Avoid using dynamic IDs that change on every render unless they are stable entity IDs.
-   Do not rely on CSS classes or text content for selectors if a `data-testid` can be added.
-   Keep names descriptive but concise.
