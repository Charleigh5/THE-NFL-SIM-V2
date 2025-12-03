"""
Locust load testing configuration for NFL SIM API.

This file defines load tests for critical API endpoints to ensure
the application can handle concurrent users and high traffic.

Run with:
  locust -f backend/locustfile.py --headless -u 100 -r 10 --run-time 60s --host http://localhost:8000

Or with web UI:
  locust -f backend/locustfile.py --host http://localhost:8000
"""
from locust import HttpUser, task, between, events
import random
import json
import logging

logger = logging.getLogger(__name__)


class NFLSimUser(HttpUser):
    """
    Simulates a user interacting with the NFL SIM API.

    This user will perform various operations like viewing teams,
    players, simulating games, and checking season standings.
    """

    # Wait between 1-5 seconds between tasks
    wait_time = between(1, 5)

    def on_start(self):
        """Initialize user session."""
        # Health check to ensure API is ready
        response = self.client.get("/api/system/health")
        if response.status_code != 200:
            logger.error("API health check failed")

    @task(10)
    def view_teams(self):
        """View all teams - high frequency task."""
        with self.client.get(
            "/api/teams",
            catch_response=True,
            name="/api/teams [LIST]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(8)
    def view_team_detail(self):
        """View a specific team's details."""
        team_id = random.randint(1, 32)  # Assuming 32 teams
        with self.client.get(
            f"/api/teams/{team_id}",
            catch_response=True,
            name="/api/teams/[id] [GET]"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # 404 is acceptable if team doesn't exist
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(8)
    def view_team_roster(self):
        """View a team's roster."""
        team_id = random.randint(1, 32)
        with self.client.get(
            f"/api/teams/{team_id}/roster",
            catch_response=True,
            name="/api/teams/[id]/roster [GET]"
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(5)
    def view_players(self):
        """View players with pagination."""
        page = random.randint(1, 10)
        with self.client.get(
            f"/api/players?page={page}&limit=20",
            catch_response=True,
            name="/api/players [LIST]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(5)
    def view_player_detail(self):
        """View a specific player's details."""
        player_id = random.randint(1, 1000)  # Assuming up to 1000 players
        with self.client.get(
            f"/api/players/{player_id}",
            catch_response=True,
            name="/api/players/[id] [GET]"
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(3)
    def view_season_standings(self):
        """View current season standings."""
        with self.client.get(
            "/api/season/standings",
            catch_response=True,
            name="/api/season/standings [GET]"
        ) as response:
            if response.status_code in [200, 404]:  # 404 if no active season
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def view_season_schedule(self):
        """View season schedule."""
        with self.client.get(
            "/api/season/schedule",
            catch_response=True,
            name="/api/season/schedule [GET]"
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(1)
    def simulate_week(self):
        """Simulate a week - lowest frequency, most expensive operation."""
        with self.client.post(
            "/api/simulation/simulate-week",
            json={},
            catch_response=True,
            name="/api/simulation/simulate-week [POST]"
        ) as response:
            # This might fail if no active season, which is acceptable
            if response.status_code in [200, 400, 404]:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def check_system_health(self):
        """Check system health endpoint."""
        with self.client.get(
            "/api/system/health",
            catch_response=True,
            name="/api/system/health [GET]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")


class DraftUser(HttpUser):
    """
    User focused on draft operations.

    This simulates GMs during draft season making heavy use
    of draft-related endpoints.
    """

    wait_time = between(2, 8)

    @task(5)
    def view_draft_prospects(self):
        """View available draft prospects."""
        with self.client.get(
            "/api/draft/prospects",
            catch_response=True,
            name="/api/draft/prospects [GET]"
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(3)
    def get_draft_suggestion(self):
        """Get AI draft pick suggestion."""
        team_id = random.randint(1, 32)
        round_num = random.randint(1, 7)
        pick_num = random.randint(1, 32)

        with self.client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": team_id,
                "round": round_num,
                "pick": pick_num,
                "needs": ["QB", "WR", "OL"]
            },
            catch_response=True,
            name="/api/draft/suggest-pick [POST]"
        ) as response:
            if response.status_code in [200, 400, 404]:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")


# Event handlers for custom metrics
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Log when load test starts."""
    logger.info("NFL SIM Load Test Starting")
    logger.info(f"Target host: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Log when load test stops."""
    logger.info("NFL SIM Load Test Completed")

    # Log summary stats
    stats = environment.stats
    logger.info(f"Total requests: {stats.total.num_requests}")
    logger.info(f"Total failures: {stats.total.num_failures}")
    logger.info(f"Average response time: {stats.total.avg_response_time}ms")
    logger.info(f"Median response time: {stats.total.median_response_time}ms")
    logger.info(f"95th percentile: {stats.total.get_response_time_percentile(0.95)}ms")
    logger.info(f"99th percentile: {stats.total.get_response_time_percentile(0.99)}ms")


# Quick test scenarios
class QuickTestUser(HttpUser):
    """Quick smoke test user for rapid validation."""

    wait_time = between(0.5, 2)

    tasks = [NFLSimUser.view_teams, NFLSimUser.check_system_health]
