import sys
import os
from fastapi.testclient import TestClient

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def verify_api_errors():
    print("Starting Manual API Error Verification...")
    
    # 1. 404 Not Found - Team
    print("\nTest 1: GET /api/v1/teams/999999 (Non-existent Team)")
    try:
        response = client.get("/api/v1/teams/999999")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        if response.status_code == 404:
            print("  PASS")
        else:
            print("  FAIL")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 2. 404 Not Found - Player
    print("\nTest 2: GET /api/v1/players/999999 (Non-existent Player)")
    try:
        response = client.get("/api/v1/players/999999")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        if response.status_code == 404:
            print("  PASS")
        else:
            print("  FAIL")
    except Exception as e:
        print(f"  ERROR: {e}")
        
    # 3. 404 Not Found (Route Mismatch) - Invalid ID type
    print("\nTest 3: GET /api/v1/teams/invalid_id (Invalid ID Type)")
    try:
        response = client.get("/api/v1/teams/invalid_id")
        print(f"  Status Code: {response.status_code}")
        # FastAPI int path converter prevents matching, so 404 is expected
        if response.status_code == 404:
            print("  PASS (404 Expected for type mismatch in path)")
        elif response.status_code == 422:
            print("  PASS (422 Returned)")
        else:
            print(f"  FAIL: Expected 404 or 422, got {response.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    verify_api_errors()
