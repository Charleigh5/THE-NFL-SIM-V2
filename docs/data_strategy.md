# Data Strategy: Logos & Migration

## 1. Logo Acquisition Strategy

### Objective

Acquire high-quality, consistent logos for all 32 NFL teams and integrate them into the application.

### Source

**ESPN CDN**: Reliable, high-quality PNGs with transparent backgrounds.

- **URL Pattern**: `https://a.espncdn.com/i/teamlogos/nfl/500/{abbreviation}.png`
- **Example**: `https://a.espncdn.com/i/teamlogos/nfl/500/buf.png`

### Implementation Plan

1. **Storage Location**:

   - Store images in `frontend/public/logos/`.
   - This allows direct access via `/logos/{abbr}.png` in the frontend without complex bundling imports.

2. **Acquisition Script**:

   - Create `backend/app/scripts/download_logos.py`.
   - Iterate through the `TEAM_DB` keys (abbreviations).
   - Download each image using `requests`.
   - Save to `frontend/public/logos/{abbr}.png`.
   - Handle special cases (e.g., WSH/WAS).

3. **Database Integration**:
   - Update the `Team` model's `logo_url` field.
   - Set value to `/logos/{abbr}.png`.

## 2. Database Migration Strategy

### Goal

Transition from placeholder/generated data to real-world NFL data (Teams & Players).

### Phase 1: Team Data

1. **Source**: `backend/app/data/teams.py` (Already contains rich metadata: colors, city, name).
2. **Enhancement**:
   - Ensure `abbreviation` matches the logo filenames.
   - Add `established_year` or other missing metadata if available.
3. **Seeding**:
   - Create `backend/app/scripts/seed_teams.py`.
   - Upsert logic: Check if team exists by abbreviation; update if yes, create if no.

### Phase 2: Player Data

1. **Source**:
   - **Primary**: `nflverse` data (CSV/JSON) or similar open-source roster data.
   - **Fallback**: Custom JSON file in `backend/app/data/rosters.json` if we want curated ratings.
2. **Data Mapping**:
   - Map source fields (Name, Position, Height, Weight, College, Age) to `Player` model.
   - **Ratings Generation**:
     - Real data often lacks "Overall Rating" in the Madden sense.
     - **Strategy**: Create a `RatingsEngine` service.
     - Input: Player stats/depth chart position.
     - Output: `overall_rating` and specific attributes (Speed, Strength, etc.).
     - _MVP_: Assign ratings based on Depth Chart order (Starter = 80+, Backup = 70+, etc.).
3. **Seeding**:
   - Create `backend/app/scripts/seed_players.py`.
   - Clear existing players (optional, or flag as `legacy`).
   - Iterate through teams and populate rosters.

### Phase 3: Execution Workflow

1. **Backup**: Dump current DB (if needed).
2. **Run**:

   ```bash
   python -m app.scripts.download_logos
   python -m app.scripts.seed_teams
   python -m app.scripts.seed_players
   ```

3. **Verify**: Check `GET /api/teams` and `GET /api/teams/{id}/roster`.
