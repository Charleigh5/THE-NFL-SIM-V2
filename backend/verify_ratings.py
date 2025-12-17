
import sqlite3
import pandas as pd

conn = sqlite3.connect('nfl_sim.db')
cursor = conn.cursor()

def verify_player(first, last):
    cursor.execute("SELECT overall_rating, speed, awareness, age, experience FROM player WHERE first_name=? AND last_name=?", (first, last))
    res = cursor.fetchone()
    if res:
        print(f"{first} {last}: OVR={res[0]}, Spd={res[1]}, Awr={res[2]}, Age={res[3]}, Exp={res[4]}")
    else:
        print(f"{first} {last}: NOT FOUND")

print("--- STAR PLAYER VERIFICATION ---")
verify_player("Patrick", "Mahomes")
verify_player("Tyreek", "Hill")
verify_player("Myles", "Garrett")
verify_player("Justin", "Jefferson")
verify_player("Trent", "Williams")
verify_player("Sauce", "Gardner")

print("\n--- DETROIT LIONS ---")
cursor.execute("SELECT first_name, last_name, overall_rating FROM player WHERE team_id = (SELECT id FROM team WHERE abbreviation='DET') ORDER BY overall_rating DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"{row[0]} {row[1]}: {row[2]}")

conn.close()
