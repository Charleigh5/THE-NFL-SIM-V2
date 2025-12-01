# GM Philosophies and Team Strategies

## GM Philosophies

The `GM` model includes a `philosophy` attribute that dictates their decision-making logic during the offseason and season.

### Philosophy Types

1. **WIN_NOW**

   - **Goal**: Maximize current roster strength to win a Super Bowl immediately.
   - **Behavior**:
     - Trades draft picks for high-rated veterans.
     - Aggressive in Free Agency for top-tier talent.
     - Less likely to trade away older, productive players.
     - Willing to sacrifice future cap space.

2. **REBUILD**

   - **Goal**: Accumulate assets for future success.
   - **Behavior**:
     - Trades veterans for draft picks.
     - Prioritizes playing rookies and young players.
     - Conservative in Free Agency (short-term deals or value signings).
     - Hoards cap space.

3. **BALANCED**

   - **Goal**: Maintain competitiveness while keeping an eye on the future.
   - **Behavior**:
     - Standard valuation of picks vs. players.
     - Fills needs through both Draft and Free Agency.
     - Avoids extreme risks.

4. **CAP_SAVER**

   - **Goal**: Maintain a healthy salary cap situation.
   - **Behavior**:
     - Avoids overpaying in Free Agency.
     - Cuts expensive veterans who are underperforming.
     - Prioritizes rookie contracts and cheap veterans.

5. **AGGRESSIVE**
   - **Goal**: Make splashy moves to improve the team.
   - **Behavior**:
     - High trade frequency.
     - Trades up in the draft.
     - Makes big offers in Free Agency.
     - High risk, high reward.

### Traits

GMs can also have specific traits that modify their behavior:

- `ScoutingGuru`: Bonus to draft pick success rate.
- `CapWizard`: Bonus to contract negotiation (players accept less).
- `Trader`: More likely to find trade partners.

## Team Strategies (Coaching)

Team strategy is primarily driven by the Head Coach's playbooks and philosophy.

### Offensive Playbooks

- **West Coast**: Short, quick passes. High completion %, lower YPA.
- **Spread**: 3-4 WR sets. High passing volume.
- **Vertical**: Deep passing. High YPA, lower completion %.
- **Power Run**: Focus on running the ball, controlling the clock.
- **Balanced**: Mix of run and pass.

### Defensive Playbooks

- **4-3**: 4 Linemen, 3 Linebackers. Standard balanced defense.
- **3-4**: 3 Linemen, 4 Linebackers. versatile, good for blitzing.
- **Nickel**: 5 Defensive Backs. Good against pass-heavy teams.
- **Dime**: 6 Defensive Backs. Pure pass coverage.

## Historical Data Structure

To support a rich history of the league, we store aggregated data for past seasons.

### Models

1. **SeasonHistory**

   - Stores summary of a completed season.
   - **Fields**: Year, Champion, Runner-Up, MVP, OPOY, DPOY, OROY, DROY.
   - **Purpose**: "Hall of Champions" view, league history.

2. **PlayerSeasonStats**

   - Aggregated stats for a player for a specific season.
   - **Fields**: Games Played, Passing/Rushing/Receiving/Defensive stats, Awards (Pro Bowl, All-Pro).
   - **Purpose**: Player career stats view, historical comparisons.

3. **TeamSeasonStats**
   - Aggregated stats for a team for a specific season.
   - **Fields**: Wins, Losses, Points For, Points Against, Playoff Result.
   - **Purpose**: Team history view, franchise records.
