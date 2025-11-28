import requests
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000/api"
RESULTS = []

def test_endpoint(name, method, url, expected_status=200, **kwargs):
    """Test an API endpoint and record results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, **kwargs)
        else:
            response = requests.post(url, **kwargs)
        
        status = response.status_code
        success = status == expected_status
        
        result = {
            "test": name,
            "url": url,
            "status_code": status,
            "expected": expected_status,
            "success": success,
            "response_time_ms": response.elapsed.total_seconds() * 1000
        }
        
        if success:
            print(f"✅ PASS - Status: {status}, Time: {result['response_time_ms']:.0f}ms")
            if response.headers.get('content-type') == 'application/json':
                data = response.json()
                if isinstance(data, list):
                    print(f"   Returned {len(data)} items")
                    result["data_count"] = len(data)
                else:
                    print(f"   Response keys: {list(data.keys())}")
                result["sample_data"] = str(data)[:200]
        else:
            print(f"❌ FAIL - Expected {expected_status}, got {status}")
            result["error"] = response.text[:200]
        
        RESULTS.append(result)
        return response
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        RESULTS.append({
            "test": name,
            "url": url,
            "success": False,
            "error": str(e)
        })
        return None

def main():
    print(f"API Verification Test Suite")
    print(f"Started: {datetime.now()}")
    print(f"Base URL: {BASE_URL}")
    
    # Task 1.2: Test GET /api/teams
    test_endpoint(
        "1.2 Get All Teams",
        "GET",
        f"{BASE_URL}/teams"
    )
    
    # Task 1.3: Test GET /api/teams/{id} with valid ID
    test_endpoint(
        "1.3a Get Team by ID (Valid)",
        "GET",
        f"{BASE_URL}/teams/1"
    )
    
    # Task 1.3: Test GET /api/teams/{id} with invalid ID
    test_endpoint(
        "1.3b Get Team by ID (Invalid)",
        "GET",
        f"{BASE_URL}/teams/999",
        expected_status=404
    )
    
    # Task 1.4: Test GET /api/teams/{id}/roster
    test_endpoint(
        "1.4 Get Team Roster",
        "GET",
        f"{BASE_URL}/teams/1/roster"
    )
    
    # Task 1.5: Test GET /api/players/{id}
    test_endpoint(
        "1.5a Get Player by ID (Valid)",
        "GET",
        f"{BASE_URL}/players/1"
    )
    
    test_endpoint(
        "1.5b Get Player by ID (Invalid)",
        "GET",
        f"{BASE_URL}/players/9999",
        expected_status=404
    )
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for r in RESULTS if r.get('success'))
    failed = len(RESULTS) - passed
    
    print(f"Total Tests: {len(RESULTS)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED!")
    
    # Calculate average response time for successful tests
    response_times = [r['response_time_ms'] for r in RESULTS if 'response_time_ms' in r]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print(f"\nAverage Response Time: {avg_time:.0f}ms")
    
    # Save results to JSON
    with open('api_test_results.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(RESULTS),
                "passed": passed,
                "failed": failed,
                "avg_response_time_ms": avg_time if response_times else None
            },
            "results": RESULTS
        }, f, indent=2)
    
    print(f"\nResults saved to: api_test_results.json")
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
