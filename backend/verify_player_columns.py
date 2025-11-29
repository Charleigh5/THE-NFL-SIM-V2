"""Quick verification script to check player table columns."""
import sqlite3

def verify_player_columns():
    """Verify that the player table has the new contract columns."""
    conn = sqlite3.connect('nfl_sim.db')
    cursor = conn.cursor()
    
    # Get column info for player table
    cursor.execute("PRAGMA table_info(player);")
    columns = cursor.fetchall()
    
    print("Player table columns:")
    print("-" * 80)
    for col in columns:
        col_id, name, col_type, not_null, default_val, pk = col
        print(f"  {name:30s} {col_type:15s} {'NOT NULL' if not_null else 'NULL':10s} PK={pk}")
    
    print("\n" + "=" * 80)
    
    # Check for specific columns we're looking for
    column_names = [col[1] for col in columns]
    required_columns = ['contract_years', 'contract_salary', 'is_rookie']
    
    print("\nVerification Results:")
    print("-" * 80)
    for req_col in required_columns:
        status = "✅ FOUND" if req_col in column_names else "❌ MISSING"
        print(f"  {req_col:30s} {status}")
    
    conn.close()
    
    all_present = all(col in column_names for col in required_columns)
    print("\n" + "=" * 80)
    if all_present:
        print("✅ SUCCESS: All contract fields are present in the player table!")
    else:
        print("❌ FAILED: Some contract fields are missing!")
    print("=" * 80)
    
    return all_present

if __name__ == "__main__":
    verify_player_columns()
