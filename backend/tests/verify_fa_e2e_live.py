"""
Live E2E Verification script for Free Agency Simulation
======================================================
Tests the live FastAPI endpoints for Market Overview and FA Simulation.
"""

import httpx
import sys

BASE_URL = "http://127.0.0.1:8000"


def main():
    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    print("=== Starting Free Agency E2E Verification ===")

    # 1. Check current season
    res = client.get("/api/season/current")
    if res.status_code != 200:
        print(f"Failed to get current season: {res.status_code} {res.text}")
        sys.exit(1)
    season = res.json()
    season_id = season["id"]
    print(f"[SUCCESS] Active Season ID: {season_id}, Year: {season.get('year')}")

    # 2. Process Contracts
    print("\n--- Testing POST /api/season/{id}/offseason/contracts ---")
    contract_res = client.post(f"/api/season/{season_id}/offseason/contracts")
    if contract_res.status_code != 200:
        print(f"[FAILED] Contract processing error: {contract_res.status_code} {contract_res.text}")
        sys.exit(1)
    c_data = contract_res.json()
    print(f"[SUCCESS] Contracts processed: {c_data.get('released_count', 0)} players entered Free Agency!")

    # 2. Test Market Overview
    print("\n--- Testing GET /api/season/{id}/free-agency/market ---")
    market_res = client.get(f"/api/season/{season_id}/free-agency/market?limit=10")
    if market_res.status_code != 200:
        print(f"[FAILED] Market endpoint error: {market_res.status_code} {market_res.text}")
        sys.exit(1)
    market_players = market_res.json()
    print(f"[SUCCESS] Fetched {len(market_players)} top free agents from market:")
    for p in market_players[:5]:
        print(f"  - {p['name']} ({p['position']}, {p['overall_rating']} OVR, {p['tier']}): Projected ${p['projected_market_value']:,} ({p['projected_years']} yrs) | Suitors: {', '.join(p['top_interested_teams'])}")

    # 3. Test Free Agency Simulation
    print("\n--- Testing POST /api/season/{id}/free-agency/simulate ---")
    sim_res = client.post(f"/api/season/{season_id}/free-agency/simulate")
    if sim_res.status_code != 200:
        print(f"[FAILED] FA simulate endpoint error: {sim_res.status_code} {sim_res.text}")
        sys.exit(1)
    signings = sim_res.json()
    print(f"[SUCCESS] Free Agency Simulation generated {len(signings)} signings!")

    if signings:
        print("Sample executed contracts:")
        for s in signings[:5]:
            print(f"  - {s['player_name']} ({s['position']} {s['overall_rating']} OVR) -> {s['team_name']}")
            print(f"    Deal: {s['contract_years']} yr / ${s['total_value']:,} (${s['annual_avg']:,}/yr, ${s['guaranteed']:,} GTD) | Grade: {s['signing_grade']} (Wave {s['signing_round']}, {s['bidding_teams_count']} bids)")

    print("\n=== ALL FREE AGENCY E2E TESTS PASSED SUCCESSFULLY! ===")


if __name__ == "__main__":
    main()
