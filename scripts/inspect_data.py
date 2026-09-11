import sqlite3

conn = sqlite3.connect("backend/nfl_sim.db")
cur = conn.cursor()

# 1. Teams
cur.execute("SELECT id, city, name FROM team LIMIT 3")
print("Teams:", cur.fetchall())

# 2. Free Agents
cur.execute("SELECT count(*) FROM player WHERE team_id IS NULL")
print("Free agents (team_id IS NULL):", cur.fetchone()[0])

# 3. Team 1 Players
cur.execute("SELECT count(*) FROM player WHERE team_id = 1")
print("Team 1 players:", cur.fetchone()[0])

# 4. Season & Games
cur.execute("SELECT id, year, current_week, status FROM season")
print("Seasons:", cur.fetchall())

cur.execute("SELECT count(*) FROM game WHERE is_played = 0")
print("Unplayed games:", cur.fetchone()[0])

cur.execute("SELECT id, season_id, week, home_team_id, away_team_id, is_played FROM game LIMIT 5")
print("Sample games:", cur.fetchall())

# 5. Injured players
cur.execute("SELECT id, first_name, last_name, injury_status FROM player WHERE injury_status != 'ACTIVE' AND injury_status IS NOT NULL")
print("Injured players:", cur.fetchall())

# 6. Body Health records
cur.execute("SELECT count(*) FROM body_health")
print("Body health records:", cur.fetchone()[0])

conn.close()
