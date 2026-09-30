"""
Migration script to ensure all defensive, kicking, and OL columns exist in player_season_stats table.
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "nfl_sim.db")
db_path = os.path.abspath(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(player_season_stats)")
existing_cols = {col[1] for col in cursor.fetchall()}

new_columns = [
    ("season_id", "INTEGER"),
    ("tackles_solo", "INTEGER DEFAULT 0"),
    ("tackles_assist", "INTEGER DEFAULT 0"),
    ("pass_deflections", "INTEGER DEFAULT 0"),
    ("forced_fumbles", "INTEGER DEFAULT 0"),
    ("tackles_for_loss", "INTEGER DEFAULT 0"),
    ("qb_pressures", "INTEGER DEFAULT 0"),
    ("fg_made", "INTEGER DEFAULT 0"),
    ("fg_att", "INTEGER DEFAULT 0"),
    ("punt_yards", "INTEGER DEFAULT 0"),
    ("punt_att", "INTEGER DEFAULT 0"),
    ("pancakes", "INTEGER DEFAULT 0"),
    ("sacks_allowed", "INTEGER DEFAULT 0"),
    ("pressures_allowed", "INTEGER DEFAULT 0"),
    ("yards_after_contact", "INTEGER DEFAULT 0"),
    ("broken_tackles", "INTEGER DEFAULT 0"),
    ("drops", "INTEGER DEFAULT 0"),
    ("yards_after_catch", "INTEGER DEFAULT 0"),
]

added = []
for col_name, col_def in new_columns:
    if col_name not in existing_cols:
        cursor.execute(f"ALTER TABLE player_season_stats ADD COLUMN {col_name} {col_def}")
        added.append(col_name)

conn.commit()
conn.close()
print(f"Migration completed. Added columns: {added}")
