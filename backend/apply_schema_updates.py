import sqlite3

def update_schema():
    conn = sqlite3.connect('backend/nfl_sim.db')
    cursor = conn.cursor()
    
    # Check if columns exist
    cursor.execute("PRAGMA table_info(player)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'contract_years' not in columns:
        print("Adding contract_years...")
        cursor.execute("ALTER TABLE player ADD COLUMN contract_years INTEGER DEFAULT 1")
        
    if 'contract_salary' not in columns:
        print("Adding contract_salary...")
        cursor.execute("ALTER TABLE player ADD COLUMN contract_salary INTEGER DEFAULT 1000000")
        
    if 'is_rookie' not in columns:
        print("Adding is_rookie...")
        cursor.execute("ALTER TABLE player ADD COLUMN is_rookie BOOLEAN DEFAULT 0")
        
    conn.commit()
    conn.close()
    print("Schema updated.")

if __name__ == "__main__":
    update_schema()
