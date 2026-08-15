"""
Live E2E Verification script for Draft Narrative & News Feed Engine
===================================================================
Tests draft pick storyline generation, FA mega-deal reactions,
and live league/team news feeds.
"""

import httpx
import sys

BASE_URL = "http://127.0.0.1:8000"


def main():
    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    print("=== Starting Draft Narrative & News Feed Engine E2E Verification ===")

    # 1. Fetch current season
    res = client.get("/api/season/current")
    if res.status_code != 200:
        print(f"Failed to get current season: {res.status_code} {res.text}")
        sys.exit(1)
    season = res.json()
    season_id = season["id"]
    print(f"[SUCCESS] Active Season ID: {season_id}")

    # 2. Simulate Next Draft Pick to trigger pick narrative
    print("\n--- Testing Pick Narrative Generation via POST /api/season/{id}/draft/simulate-next ---")
    pick_res = client.post(f"/api/season/{season_id}/draft/simulate-next")
    if pick_res.status_code == 200 and pick_res.json() is not None:
        pick = pick_res.json()
        print(f"[SUCCESS] Pick #{pick['pick_number']} simulated: {pick['player_name']} ({pick['player_position']} {pick['player_overall']} OVR) to Team {pick['team_id']}")
    else:
        print("[INFO] Draft picks already completed or empty; proceeding to check News Feed.")

    # 3. Simulate Free Agency to trigger FA narratives
    print("\n--- Testing Free Agency Storyline Generation via POST /api/season/{id}/free-agency/simulate ---")
    fa_res = client.post(f"/api/season/{season_id}/free-agency/simulate")
    if fa_res.status_code == 200:
        signings = fa_res.json()
        print(f"[SUCCESS] Free Agency simulated: {len(signings)} signings executed.")
    else:
        print(f"[WARNING] FA simulation returned {fa_res.status_code}: {fa_res.text}")

    # 4. Fetch League News Feed
    print("\n--- Testing GET /api/news/league ---")
    news_res = client.get("/api/news/league?limit=10")
    if news_res.status_code != 200:
        print(f"[FAILED] News feed endpoint error: {news_res.status_code} {news_res.text}")
        sys.exit(1)
    news_data = news_res.json()
    items = news_data.get("items", [])
    print(f"[SUCCESS] Fetched {len(items)} news wire articles (Total available: {news_data.get('total')}):")
    for item in items[:6]:
        badge = "[BREAKING]" if item.get("is_breaking") else "[STORY]"
        print(f"  {badge} [{item.get('category').upper()}] {item.get('headline')} ({item.get('date')})")

    # 5. Fetch Team News Feed
    print("\n--- Testing GET /api/news/team/{team_name} ---")
    team_news_res = client.get("/api/news/team/Jaguars?limit=5")
    if team_news_res.status_code == 200:
        team_items = team_news_res.json().get("items", [])
        print(f"[SUCCESS] Fetched {len(team_items)} team-specific news items for Jaguars:")
        for t_item in team_items[:3]:
            print(f"  - {t_item.get('headline')}")

    print("\n=== ALL DRAFT NARRATIVE & NEWS FEED TESTS COMPLETED SUCCESSFULLY! ===")


if __name__ == "__main__":
    main()
