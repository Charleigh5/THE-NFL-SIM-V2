import random
from sqlalchemy.orm import Session
from app.models.player import Player, Position
from app.core.random_utils import DeterministicRNG

FIRST_NAMES = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander", "Patrick", "Jack", "Dennis", "Jerry"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts"]

POSITION_WEIGHTS = {
    Position.QB: 15, Position.RB: 20, Position.WR: 35, Position.TE: 15,
    Position.OT: 25, Position.OG: 20, Position.C: 10,
    Position.DE: 20, Position.DT: 20, Position.LB: 30,
    Position.CB: 30, Position.S: 20,
    Position.K: 5, Position.P: 5
}

class RookieGenerator:
    def __init__(self, db: Session, seed: int = None):
        self.db = db
        # Use provided seed or a random one if not provided, but encapsulated in DeterministicRNG
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

    async def generate_draft_class(self, season_id: int, count: int = 256):
        """Generates a class of rookie players."""

        # Determine count per position based on weights
        total_weight = sum(POSITION_WEIGHTS.values())

        # Fetch league averages via MCP if available
        league_avgs = {}
        try:
            from app.core.mcp_registry import registry
            client = registry.get_client("nfl_stats")
            if client:
                # Mock call to get averages for QB to influence generation
                # In a real scenario, we'd fetch for all positions or cache this
                result = await client.call_tool("get_league_averages", arguments={"position": "QB", "season": 2024})
                if result and not isinstance(result, str): # Ensure we got data
                     league_avgs["QB"] = result
        except Exception as e:
            print(f"MCP Warning: Could not fetch league averages: {e}")

        generated_count = 0
        players = []

        for _ in range(count):
            # Pick a position
            r = self.rng.uniform(0, total_weight)
            upto = 0
            selected_pos = Position.QB
            for pos, weight in POSITION_WEIGHTS.items():
                if upto + weight >= r:
                    selected_pos = pos
                    break
                upto += weight

            player = self._create_rookie(selected_pos, league_avgs.get(selected_pos.value if hasattr(selected_pos, 'value') else selected_pos))
            players.append(player)

        self.db.add_all(players)
        self.db.commit()
        return players

    def _create_rookie(self, position: Position, stats_context: dict = None) -> Player:
        first = self.rng.choice(FIRST_NAMES)
        last = self.rng.choice(LAST_NAMES)

        # Base attributes
        age = self.rng.randint(21, 23)
        height = self.rng.randint(68, 80) # 5'8" to 6'8"
        weight = self.rng.randint(180, 350)

        # Adjust height/weight by position (simplified)
        if position in [Position.OT, Position.OG, Position.C, Position.DT]:
            weight = self.rng.randint(280, 350)
        elif position in [Position.WR, Position.CB, Position.S]:
            weight = self.rng.randint(180, 220)

        # Generate Ratings (Bell curve centered around 65-70 for rookies)
        mean_rating = 68
        if stats_context:
             # If we have context (e.g. high passing yards avg), maybe this is a strong QB class?
             # Or we just use it to slightly bump the mean
             if "passing_yards" in stats_context and stats_context["passing_yards"] > 3000:
                 mean_rating += 2

        overall = int(self.rng.gauss(mean_rating, 8))
        overall = max(50, min(99, overall))

        # Create Player
        player = Player(
            first_name=first,
            last_name=last,
            position=position.value,
            height=height,
            weight=weight,
            age=age,
            experience=0,
            jersey_number=self.rng.randint(1, 99),
            overall_rating=overall,
            is_rookie=True,
            team_id=None, # Free agent / Draft pool

            # Simplified stats generation (just setting base stats to overall for now)
            speed=overall,
            acceleration=overall,
            strength=overall,
            agility=overall,
            awareness=overall - 10, # Rookies have lower awareness

            contract_years=4, # Standard rookie deal
            contract_salary=500000 + (overall * 10000) # Salary based on rating
        )

        return player
