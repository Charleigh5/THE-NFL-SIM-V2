"""
Scout Data for All 32 NFL Teams
================================
Each team gets 3 scouts:
- National Scout (GENERALIST, NEUTRAL)
- Regional Scout (Based on team location, varied bias)
- Specialist Scout (Position specialty, stronger bias)
"""
from dataclasses import dataclass

from app.models.scout import Region, ScoutBias


@dataclass
class ScoutData:
    team_abbr: str
    name: str
    region: str
    bias: str
    specialty: str
    evaluation_ability: int
    efficiency: int
    reputation: int


# Scout Templates by Region
TEAM_SCOUTS: list[ScoutData] = [
    # AFC EAST
    ScoutData("BUF", "Marcus Williamson", Region.EAST, ScoutBias.ANALYTICS, None, 75, 70, 65),
    ScoutData("BUF", "Tom Polley", Region.MIDWEST, ScoutBias.OLD_SCHOOL, "OL", 80, 60, 70),
    ScoutData("BUF", "Derek Sharpley", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 60),

    ScoutData("MIA", "Carlos Diaz", Region.SOUTH, ScoutBias.RAS_LOVER, "WR", 85, 65, 75),
    ScoutData("MIA", "Frank Johnson", Region.NATIONAL, ScoutBias.NEUTRAL, None, 72, 78, 68),
    ScoutData("MIA", "David Chen", Region.WEST, ScoutBias.ANALYTICS, "DB", 78, 70, 65),

    ScoutData("NE", "Bill Langford", Region.EAST, ScoutBias.CHARACTER, None, 88, 55, 85),
    ScoutData("NE", "James McCarthy", Region.NATIONAL, ScoutBias.TECHNICIAN, "LB", 82, 68, 78),
    ScoutData("NE", "Robert Hall", Region.SOUTH, ScoutBias.OLD_SCHOOL, "OL", 75, 72, 70),

    ScoutData("NYJ", "Mike Tannenbaum Jr", Region.EAST, ScoutBias.ANALYTICS, "QB", 80, 70, 72),
    ScoutData("NYJ", "Sam Decker", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 65),
    ScoutData("NYJ", "Chris Patterson", Region.MIDWEST, ScoutBias.RAS_LOVER, "DL", 76, 68, 68),

    # AFC NORTH
    ScoutData("BAL", "Ozzie Newsome III", Region.EAST, ScoutBias.OLD_SCHOOL, "DL", 90, 60, 88),
    ScoutData("BAL", "Eric DeCosta Jr", Region.SOUTH, ScoutBias.ANALYTICS, None, 85, 72, 82),
    ScoutData("BAL", "Keith Williams", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 75),

    ScoutData("CIN", "Duke Tobin II", Region.MIDWEST, ScoutBias.TECHNICIAN, "WR", 82, 68, 75),
    ScoutData("CIN", "Paul Brown IV", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
    ScoutData("CIN", "Marcus King", Region.SOUTH, ScoutBias.RAS_LOVER, "RB", 78, 70, 68),

    ScoutData("CLE", "Andrew Berry II", Region.MIDWEST, ScoutBias.ANALYTICS, "DB", 88, 75, 80),
    ScoutData("CLE", "Kevin Stefanski Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 72),
    ScoutData("CLE", "Tony Fields", Region.SOUTH, ScoutBias.OLD_SCHOOL, "OL", 80, 65, 75),

    ScoutData("PIT", "Kevin Colbert III", Region.EAST, ScoutBias.CHARACTER, "LB", 85, 60, 85),
    ScoutData("PIT", "Omar Khan Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 78),
    ScoutData("PIT", "Mike Mularkey", Region.MIDWEST, ScoutBias.OLD_SCHOOL, "OL", 76, 68, 72),

    # AFC SOUTH
    ScoutData("HOU", "Nick Caserio Jr", Region.SOUTH, ScoutBias.ANALYTICS, "WR", 82, 75, 78),
    ScoutData("HOU", "Devon Still", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 70),
    ScoutData("HOU", "Marcus Peters", Region.WEST, ScoutBias.RAS_LOVER, "DB", 80, 68, 72),

    ScoutData("IND", "Chris Ballard II", Region.MIDWEST, ScoutBias.CHARACTER, "OL", 85, 65, 80),
    ScoutData("IND", "Ed Dodds Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 75),
    ScoutData("IND", "Sam Houston", Region.SOUTH, ScoutBias.TECHNICIAN, "QB", 78, 70, 72),

    ScoutData("JAX", "Trent Baalke III", Region.SOUTH, ScoutBias.RAS_LOVER, "DL", 78, 70, 70),
    ScoutData("JAX", "Tony Khan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 75, 75, 72),
    ScoutData("JAX", "Marcus Allen", Region.WEST, ScoutBias.OLD_SCHOOL, "RB", 76, 68, 68),

    ScoutData("TEN", "Ran Carthon Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "OL", 80, 65, 75),
    ScoutData("TEN", "Mike Vrabel Jr", Region.NATIONAL, ScoutBias.CHARACTER, "LB", 82, 68, 78),
    ScoutData("TEN", "David Caldwell", Region.EAST, ScoutBias.NEUTRAL, None, 75, 75, 70),

    # AFC WEST
    ScoutData("DEN", "George Paton Jr", Region.WEST, ScoutBias.ANALYTICS, "QB", 82, 72, 78),
    ScoutData("DEN", "John Elway III", Region.NATIONAL, ScoutBias.CHARACTER, None, 78, 68, 82),
    ScoutData("DEN", "Marcus Thompson", Region.MIDWEST, ScoutBias.RAS_LOVER, "WR", 76, 70, 70),

    ScoutData("KC", "Brett Veach Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "WR", 90, 75, 88),
    ScoutData("KC", "Clark Hunt III", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 80),
    ScoutData("KC", "Deron Cherry Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "DB", 82, 68, 78),

    ScoutData("LV", "Dave Ziegler Jr", Region.WEST, ScoutBias.TECHNICIAN, "DL", 78, 70, 72),
    ScoutData("LV", "Tom Brady Jr", Region.NATIONAL, ScoutBias.CHARACTER, "QB", 80, 68, 75),
    ScoutData("LV", "Marcus Davis", Region.SOUTH, ScoutBias.RAS_LOVER, "WR", 76, 72, 68),

    ScoutData("LAC", "Tom Telesco Jr", Region.WEST, ScoutBias.ANALYTICS, "OL", 82, 72, 78),
    ScoutData("LAC", "John Spanos", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 72),
    ScoutData("LAC", "Eric Weddle Jr", Region.SOUTH, ScoutBias.TECHNICIAN, "DB", 80, 68, 75),

    # NFC EAST
    ScoutData("DAL", "Will McClay Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "DL", 88, 65, 85),
    ScoutData("DAL", "Jerry Jones IV", Region.NATIONAL, ScoutBias.RAS_LOVER, None, 70, 75, 78),
    ScoutData("DAL", "Tony Romo Jr", Region.MIDWEST, ScoutBias.TECHNICIAN, "QB", 82, 70, 80),

    ScoutData("NYG", "Joe Schoen Jr", Region.EAST, ScoutBias.ANALYTICS, "OL", 82, 72, 78),
    ScoutData("NYG", "Brian Daboll Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 75, 75),
    ScoutData("NYG", "Chris Mara", Region.SOUTH, ScoutBias.CHARACTER, "LB", 76, 68, 72),

    ScoutData("PHI", "Howie Roseman Jr", Region.EAST, ScoutBias.ANALYTICS, "DL", 90, 78, 88),
    ScoutData("PHI", "Nick Sirianni Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
    ScoutData("PHI", "Brian Dawkins Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "DB", 82, 68, 78),

    ScoutData("WAS", "Martin Mayhew Jr", Region.EAST, ScoutBias.CHARACTER, "WR", 78, 70, 72),
    ScoutData("WAS", "Adam Peters Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 80, 75, 75),
    ScoutData("WAS", "Dan Quinn Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "LB", 76, 68, 70),

    # NFC NORTH
    ScoutData("CHI", "Ryan Poles Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "OL", 82, 75, 78),
    ScoutData("CHI", "Matt Eberflus Jr", Region.NATIONAL, ScoutBias.CHARACTER, "LB", 78, 70, 75),
    ScoutData("CHI", "Mike Ditka III", Region.EAST, ScoutBias.OLD_SCHOOL, "TE", 75, 65, 80),

    ScoutData("DET", "Brad Holmes Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "DL", 88, 78, 85),
    ScoutData("DET", "Dan Campbell Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 72, 82),
    ScoutData("DET", "Barry Sanders Jr", Region.SOUTH, ScoutBias.RAS_LOVER, "RB", 85, 70, 80),

    ScoutData("GB", "Brian Gutekunst Jr", Region.MIDWEST, ScoutBias.TECHNICIAN, "WR", 85, 72, 82),
    ScoutData("GB", "Matt LaFleur Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
    ScoutData("GB", "Aaron Rodgers Jr", Region.WEST, ScoutBias.ANALYTICS, "QB", 78, 68, 85),

    ScoutData("MIN", "Kwesi Adofo-Mensah Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "DB", 85, 78, 80),
    ScoutData("MIN", "Kevin O'Connell Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
    ScoutData("MIN", "Randy Moss Jr", Region.SOUTH, ScoutBias.RAS_LOVER, "WR", 82, 70, 82),

    # NFC SOUTH
    ScoutData("ATL", "Terry Fontenot Jr", Region.SOUTH, ScoutBias.ANALYTICS, "WR", 82, 75, 78),
    ScoutData("ATL", "Raheem Morris Jr", Region.NATIONAL, ScoutBias.CHARACTER, "DB", 78, 72, 75),
    ScoutData("ATL", "Deion Sanders Jr", Region.WEST, ScoutBias.RAS_LOVER, "DB", 80, 68, 82),

    ScoutData("CAR", "Dan Morgan Jr", Region.SOUTH, ScoutBias.OLD_SCHOOL, "LB", 80, 68, 75),
    ScoutData("CAR", "Dave Canales Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
    ScoutData("CAR", "Luke Kuechly Jr", Region.EAST, ScoutBias.TECHNICIAN, "LB", 85, 70, 80),

    ScoutData("NO", "Mickey Loomis Jr", Region.SOUTH, ScoutBias.CHARACTER, "OL", 82, 68, 78),
    ScoutData("NO", "Dennis Allen Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 75),
    ScoutData("NO", "Drew Brees Jr", Region.MIDWEST, ScoutBias.TECHNICIAN, "QB", 85, 70, 85),

    ScoutData("TB", "Jason Licht Jr", Region.SOUTH, ScoutBias.ANALYTICS, "DL", 85, 75, 80),
    ScoutData("TB", "Todd Bowles Jr", Region.NATIONAL, ScoutBias.OLD_SCHOOL, "DB", 80, 70, 78),
    ScoutData("TB", "Derrick Brooks Jr", Region.EAST, ScoutBias.CHARACTER, "LB", 82, 68, 82),

    # NFC WEST
    ScoutData("ARI", "Monti Ossenfort Jr", Region.WEST, ScoutBias.ANALYTICS, "QB", 80, 75, 75),
    ScoutData("ARI", "Jonathan Gannon Jr", Region.NATIONAL, ScoutBias.NEUTRAL, "DB", 78, 72, 72),
    ScoutData("ARI", "Larry Fitzgerald Jr", Region.SOUTH, ScoutBias.TECHNICIAN, "WR", 82, 68, 85),

    ScoutData("LAR", "Les Snead Jr", Region.WEST, ScoutBias.ANALYTICS, "OL", 85, 78, 82),
    ScoutData("LAR", "Sean McVay Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
    ScoutData("LAR", "Aaron Donald Jr", Region.MIDWEST, ScoutBias.OLD_SCHOOL, "DL", 82, 68, 88),

    ScoutData("SF", "John Lynch Jr", Region.WEST, ScoutBias.CHARACTER, "DB", 88, 72, 88),
    ScoutData("SF", "Kyle Shanahan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 85, 78, 85),
    ScoutData("SF", "Jerry Rice Jr", Region.SOUTH, ScoutBias.TECHNICIAN, "WR", 82, 68, 88),

    ScoutData("SEA", "John Schneider Jr", Region.WEST, ScoutBias.RAS_LOVER, "DL", 85, 75, 82),
    ScoutData("SEA", "Pete Carroll Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 70, 85),
    ScoutData("SEA", "Russell Wilson Jr", Region.MIDWEST, ScoutBias.ANALYTICS, "QB", 78, 72, 78),
]


def get_scouts_for_team(abbr: str) -> list[ScoutData]:
    """Get all scouts for a specific team."""
    return [s for s in TEAM_SCOUTS if s.team_abbr == abbr]
