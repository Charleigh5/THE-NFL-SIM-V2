"""Application-wide constants."""

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Season Configuration
DEFAULT_REGULAR_SEASON_WEEKS = 18
DEFAULT_PLAYOFF_WEEKS = 4

# Simulation
DEFAULT_PLAYS_PER_GAME = 100
DEFAULT_PLAY_DELAY_SECONDS = 5.0

# League Leaders
DEFAULT_LEADERS_LIMIT = 5
MAX_LEADERS_LIMIT = 20

# Draft
DEFAULT_DRAFT_ROUNDS = 7
PICKS_PER_ROUND = 32

# Salary Cap (2025 NFL Value)
DEFAULT_SALARY_CAP = 279_200_000  # $279.2M (2025 NFL Salary Cap)

# Player Ratings
MIN_PLAYER_RATING = 0
MAX_PLAYER_RATING = 100
DEFAULT_PLAYER_RATING = 50

# =============================================================================
# AGE-BASED GROWTH CURVES (RPG-003)
# =============================================================================

# Position-specific peak age ranges (start_prime, end_prime)
# Players before start_prime are in "Ascension", after end_prime in "Decline"
POSITION_PEAK_AGES = {
    "RB": (23, 26),   # Running backs peak early, decline fastest
    "WR": (25, 28),
    "CB": (25, 28),
    "S": (25, 28),
    "LB": (26, 29),
    "TE": (26, 29),
    "DE": (26, 29),
    "QB": (27, 31),   # Quarterbacks peak late, mental game compensates
    "OT": (27, 31),
    "OG": (27, 31),
    "C": (27, 31),
    "DT": (27, 31),
    "K": (28, 32),    # Kickers/Punters have longest prime windows
    "P": (28, 32),
}

# XP multipliers for each career phase
AGE_PHASE_MULTIPLIERS = {
    "ASCENSION": 1.25,  # Young players learn faster
    "PRIME": 1.0,       # Peak performance, steady growth
    "DECLINE": 0.75,    # Older players learn slower
}

# Regression weights by attribute (higher = regresses faster)
# Speed/athleticism drops first, mental/experience last
REGRESSION_WEIGHTS = {
    # Physical (regress fastest)
    "speed": 1.0,
    "acceleration": 0.95,
    "agility": 0.9,
    "stamina": 0.85,
    "strength": 0.7,
    "injury_resistance": 0.6,
    # Technical (moderate)
    "juke_move": 0.5,
    "spin_move": 0.5,
    "stiff_arm": 0.45,
    "break_tackle": 0.4,
    "trucking": 0.35,
    "catching": 0.3,
    "route_running": 0.25,
    "throw_power": 0.4,
    "throw_accuracy_short": 0.15,
    "throw_accuracy_mid": 0.15,
    "throw_accuracy_deep": 0.2,
    "kick_power": 0.3,
    "kick_accuracy": 0.15,
    # Mental (regress slowest / almost never)
    "awareness": 0.05,
    "play_recognition": 0.05,
    "zone_coverage": 0.1,
    "man_coverage": 0.15,
    "pocket_presence": 0.05,
}

# Database
DEFAULT_DB_POOL_SIZE = 5
DEFAULT_DB_MAX_OVERFLOW = 10
DEFAULT_DB_POOL_TIMEOUT = 30
DEFAULT_DB_POOL_RECYCLE = 3600
