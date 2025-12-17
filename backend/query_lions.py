import sqlite3

conn = sqlite3.connect('nfl_sim.db')
cursor = conn.cursor()

# Get Detroit Lions team_id
cursor.execute("SELECT id FROM team WHERE abbreviation = 'DET'")
lions_id = cursor.fetchone()[0]

# Get players
cursor.execute("""
    SELECT position, first_name, last_name, overall_rating, speed, strength, awareness
    FROM player
    WHERE team_id = ?
    ORDER BY overall_rating DESC
""", (lions_id,))

players = cursor.fetchall()

offense_pos = ['QB', 'RB', 'WR', 'TE', 'OT', 'OG', 'C']
defense_pos = ['DE', 'DT', 'LB', 'CB', 'S']

print("=" * 65)
print("DETROIT LIONS - OFFENSE STARTERS")
print("=" * 65)
print(f"{'POS':<5} {'PLAYER':<25} {'OVR':>4} {'SPD':>4} {'STR':>4} {'AWR':>4}")
print("-" * 65)

for pos in offense_pos:
    pos_players = [p for p in players if p[0] == pos][:2]
    for p in pos_players:
        print(f"{p[0]:<5} {p[1] + ' ' + p[2]:<25} {p[3]:>4} {p[4]:>4} {p[5]:>4} {p[6]:>4}")

print()
print("=" * 65)
print("DETROIT LIONS - DEFENSE STARTERS")
print("=" * 65)
print(f"{'POS':<5} {'PLAYER':<25} {'OVR':>4} {'SPD':>4} {'STR':>4} {'AWR':>4}")
print("-" * 65)

for pos in defense_pos:
    pos_players = [p for p in players if p[0] == pos][:2]
    for p in pos_players:
        print(f"{p[0]:<5} {p[1] + ' ' + p[2]:<25} {p[3]:>4} {p[4]:>4} {p[5]:>4} {p[6]:>4}")

conn.close()
