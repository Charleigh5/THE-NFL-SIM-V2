# Manual Testing: Offseason Flow

This document outlines the manual testing procedure for the entire offseason workflow, from the end of one season to the beginning of the next.

## Prerequisites

1.  **Backend and Frontend Running:** Ensure both the FastAPI backend and the React frontend servers are running.
2.  **Completed Season:** You must have a simulation state where a full regular season and playoffs have concluded. The application should be at the "start of offseason" phase. The easiest way to achieve this is to run a full season simulation via the API.
3.  **Test Database:** It is highly recommended to use a clean, seeded test database (`test_offseason.db`) for this to ensure predictable results.

## Testing Steps

### Step 1: Trigger and Verify Offseason Start

1.  **Action:** From the main dashboard or league page, click the button to advance to the offseason. This might be labeled "Start Offseason" or similar.
2.  **Observe:** The UI should transition to a dedicated Offseason view.
3.  **Verification:**
    *   The main league calendar should now display "Offseason" as the current phase.
    *   A new set of navigation options for offseason stages should appear (e.g., "Player Progression," "Free Agency," "Draft").
    *   Check the browser's developer console (Network tab) for a successful API call that initiates the offseason.

### Step 2: Player Progression Stage

1.  **Action:** Navigate to the "Player Progression" section of the offseason UI.
2.  **Action:** Trigger the player progression event. This may happen automatically or require a button click like "Run Progression."
3.  **Verification:**
    *   **Check Player Ratings:** Identify a few players of different ages (a young player, a player in their prime, an old player).
        *   The young player's ratings should generally increase.
        *   The prime player's ratings may see minor changes.
        *   The old player's ratings should generally decrease.
    *   **Check Player Ages:** All players' ages should have incremented by one year.
    *   **Check API Calls:** Look for network requests related to player progression. The response data should reflect the changes you see on the screen.

### Step 3: Rookie Generation Verification

1.  **Action:** After the "Player Progression" stage, there should be a step to generate rookies. This might be automatic or require a button click.
2.  **Verification:**
    *   Navigate to the "Draft" or "Prospects" screen.
    *   You should see a new class of rookie players.
    *   Verify that the number of rookies is reasonable (e.g., around 250).
    *   Spot-check a few rookies to ensure they have reasonable attributes (e.g., age between 21-23, 0 years of experience, a rookie contract).
    *   Check the API calls related to rookie generation.

### Step 4: Free Agency Simulation

1.  **Action:** Navigate to the "Free Agency" section.
2.  **Verification (Initial State):**
    *   You should see a list of players whose contracts have expired.
    *   Your team's salary cap and available funds should be clearly displayed.
3.  **Action (Signing a Player):**
    *   Attempt to make an offer to a free agent.
    *   If the offer is accepted, the player should be added to your team's roster.
4.  **Verification (Post-Signing):**
    *   The player now appears on your "Front Office" roster screen.
    *   Your team's salary cap space should decrease by the amount of the new contract.
    *   The player should no longer be listed in the free agency pool.
    *   Check for successful API calls related to making an offer and signing a player.

### Step 5: Draft Simulation

1.  **Action:** Navigate to the "NFL Draft" section.
2.  **Verification (Initial State):**
    *   A list of rookie players (the "draft class") should be visible.
    *   The draft order should be displayed, with the worst-performing teams from the previous season picking first.
3.  **Action (Making a Pick):**
    *   When it is your team's turn to pick, select a player from the draft class.
4.  **Verification (Post-Pick):**
    *   The drafted player should be added to your team's roster.
    *   The player should be removed from the available draft pool.
    *   The draft order should advance to the next team.
    *   Verify the API calls that fetch the draft class and submit a draft pick.

### Step 6: Advance to Next Season

1.  **Action:** After the draft is complete, find and click the button to "Start Next Season" or "Advance to Preseason."
2.  **Verification:**
    *   The UI should transition back to the regular season or preseason layout.
    *   The league calendar should now show "Preseason, Week 1" or "Regular Season, Week 1."
    *   Your roster should include the players you signed in free agency and selected in the draft.
    *   The new season's schedule should be generated and visible.

## Success Criteria

- [ ] The application correctly transitions from the end of a season into the offseason phase.
- [ ] Player progression updates ages and attributes logically.
- [ ] Free agency allows for signing players, which correctly updates the roster and salary cap.
- [ ] The draft presents a class of rookies, and drafting a player correctly adds them to the team.
- [ ] The application successfully advances to the next season with all offseason changes persisted.
- [ ] All UI elements update correctly without requiring a manual refresh.
- [ ] No errors are present in the browser console during any of the steps.

## Troubleshooting

*   **Failure to Advance to Offseason:** Check the backend logic that determines the end of the season. Ensure the playoff logic correctly sets the stage for the offseason transition.
*   **Player Progression Not Working:** Check the `offseason_service.py` or similar service on the backend. Verify the logic for age-based attribute changes. Check the corresponding API endpoint.
*   **Free Agency/Draft Picks Don't Save:** This is likely an API issue. Use the Network tab to inspect the `POST` or `PUT` requests being sent when you try to sign or draft a player. Check for error responses from the server. Ensure the database session is being committed correctly on the backend.
*   **Data Is Incorrect (e.g., wrong draft order, wrong players in free agency):** Check the backend services that generate this data. The logic for calculating the draft order or determining which players are free agents may be flawed.
