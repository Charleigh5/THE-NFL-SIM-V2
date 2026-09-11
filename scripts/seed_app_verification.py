import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "backend", "nfl_sim.db")

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print(f"Connecting to database at {DB_PATH}")

    # Ensure Player columns exist
    cur.execute("PRAGMA table_info(player)")
    cols = [r[1] for r in cur.fetchall()]
    missing_cols = [
        ("psychological_dna", "TEXT", "'{}'"),
        ("backstory", "TEXT", "'{}'"),
        ("tension_score", "REAL", "0.0"),
        ("trust_in_coach", "INTEGER", "80"),
        ("trust_in_qb", "INTEGER", "80")
    ]
    for col_name, col_type, default_val in missing_cols:
        if col_name not in cols:
            cur.execute(f"ALTER TABLE player ADD COLUMN {col_name} {col_type} DEFAULT {default_val}")
    conn.commit()

    # Seed for both Team 1 (ARI) and Team 12 (GB)
    for team_id in [1, 12]:
        cur.execute("SELECT id, first_name, last_name, position FROM player WHERE team_id = ? ORDER BY id LIMIT 10", (team_id,))
        players = cur.fetchall()
        if not players or len(players) < 5:
            print(f"Skipping team {team_id}: not enough players")
            continue

        p1, p2, p3, p4, p5 = players[:5]
        print(f"Team {team_id} players: P1={p1[1:]}, P2={p2[1:]}, P3={p3[1:]}, P4={p4[1:]}, P5={p5[1:]}")

        # Seed Injured Players
        cur.execute("""
            UPDATE player_injury
            SET injury_status = 'QUESTIONABLE', injury_type = 'Meniscus Tear', injury_severity = 3, weeks_to_recovery = 4, injury_recurrence_risk = 0.25
            WHERE player_id = ?
        """, (p1[0],))
        cur.execute("""
            UPDATE player_injury
            SET injury_status = 'QUESTIONABLE', injury_type = 'High Ankle Sprain', injury_severity = 2, weeks_to_recovery = 2, injury_recurrence_risk = 0.15
            WHERE player_id = ?
        """, (p2[0],))
        cur.execute("""
            UPDATE player_injury
            SET injury_status = 'OUT', injury_type = 'Rotator Cuff Strain', injury_severity = 4, weeks_to_recovery = 6, injury_recurrence_risk = 0.35
            WHERE player_id = ?
        """, (p3[0],))

        for pid, arm_r, leg_r, leg_l in [(p1[0], 95.0, 45.0, 95.0), (p2[0], 95.0, 90.0, 55.0), (p3[0], 40.0, 95.0, 95.0)]:
            cur.execute("SELECT id FROM body_health WHERE player_id = ?", (pid,))
            if cur.fetchone():
                cur.execute("""
                    UPDATE body_health
                    SET head_health = 100.0, neck_health = 100.0, torso_health = 95.0,
                        right_arm_health = ?, left_arm_health = 95.0,
                        right_leg_health = ?, left_leg_health = ?, general_wear = 15.0
                    WHERE player_id = ?
                """, (arm_r, leg_r, leg_l, pid))
            else:
                cur.execute("""
                    INSERT INTO body_health (player_id, head_health, neck_health, torso_health,
                                             right_arm_health, left_arm_health, right_leg_health,
                                             left_leg_health, general_wear)
                    VALUES (?, 100.0, 100.0, 95.0, ?, 95.0, ?, ?, 15.0)
                """, (pid, arm_r, leg_r, leg_l))

        # Seed Disgruntled Star & Respected Captain for Locker Room
        disgruntled_dna = json.dumps({"ego": 92, "greed": 88, "loyalty": 30, "resilience": 40, "paranoia": 85, "professionalism": 30})
        cur.execute("""
            UPDATE player
            SET tension_score = 85.0, trust_in_coach = 40, trust_in_qb = 45, psychological_dna = ?
            WHERE id = ?
        """, (disgruntled_dna, p4[0]))

        captain_dna = json.dumps({"ego": 20, "greed": 30, "loyalty": 95, "resilience": 90, "paranoia": 15, "professionalism": 95})
        cur.execute("""
            UPDATE player
            SET tension_score = 10.0, trust_in_coach = 95, trust_in_qb = 90, overall_rating = 92, experience = 9, psychological_dna = ?
            WHERE id = ?
        """, (captain_dna, p5[0]))

    # Ensure unplayed game for Team 12 as well
    cur.execute("SELECT id FROM season LIMIT 1")
    season = cur.fetchone()
    season_id = season[0] if season else 1

    cur.execute("SELECT id FROM game WHERE home_team_id = 12 AND is_played = 0 LIMIT 1")
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO game (season_id, season, week, date, is_playoff, is_preseason, game_type,
                              home_team_id, away_team_id, home_score, away_score, is_played)
            VALUES (?, 2025, 1, '2025-09-08 13:00:00', 0, 0, 'REGULAR_SEASON', 12, 16, 0, 0, 0)
        """, (season_id,))

    conn.commit()
    conn.close()
    print("Multi-team verification data seeded successfully!")

if __name__ == "__main__":
    seed()
