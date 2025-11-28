from pydantic import BaseModel
from typing import Dict

class TeamColors(BaseModel):
    primary_hex: str
    secondary_hex: str
    accent_hex: str = "#FFFFFF" # Default white if not specified

class TeamIdentity(BaseModel):
    id: str
    city: str
    mascot: str
    abbreviation: str
    conference: str
    division: str
    colors: TeamColors

# Complete 32 Team Database
TEAM_DB = {
    # AFC EAST
    "BUF": TeamIdentity(id="BUF", city="Buffalo", mascot="Bills", abbreviation="BUF", conference="AFC", division="East", colors=TeamColors(primary_hex="#00338D", secondary_hex="#C60C30")),
    "MIA": TeamIdentity(id="MIA", city="Miami", mascot="Dolphins", abbreviation="MIA", conference="AFC", division="East", colors=TeamColors(primary_hex="#008E97", secondary_hex="#FC4C02", accent_hex="#005778")),
    "NE": TeamIdentity(id="NE", city="New England", mascot="Patriots", abbreviation="NE", conference="AFC", division="East", colors=TeamColors(primary_hex="#002244", secondary_hex="#C60C30", accent_hex="#B0B7BC")),
    "NYJ": TeamIdentity(id="NYJ", city="New York", mascot="Jets", abbreviation="NYJ", conference="AFC", division="East", colors=TeamColors(primary_hex="#125740", secondary_hex="#000000", accent_hex="#FFFFFF")),
    
    # AFC NORTH
    "BAL": TeamIdentity(id="BAL", city="Baltimore", mascot="Ravens", abbreviation="BAL", conference="AFC", division="North", colors=TeamColors(primary_hex="#241773", secondary_hex="#000000", accent_hex="#9E7C0C")),
    "CIN": TeamIdentity(id="CIN", city="Cincinnati", mascot="Bengals", abbreviation="CIN", conference="AFC", division="North", colors=TeamColors(primary_hex="#FB4F14", secondary_hex="#000000")),
    "CLE": TeamIdentity(id="CLE", city="Cleveland", mascot="Browns", abbreviation="CLE", conference="AFC", division="North", colors=TeamColors(primary_hex="#311D00", secondary_hex="#FF3C00")),
    "PIT": TeamIdentity(id="PIT", city="Pittsburgh", mascot="Steelers", abbreviation="PIT", conference="AFC", division="North", colors=TeamColors(primary_hex="#FFB612", secondary_hex="#101820", accent_hex="#003087")),

    # AFC SOUTH
    "HOU": TeamIdentity(id="HOU", city="Houston", mascot="Texans", abbreviation="HOU", conference="AFC", division="South", colors=TeamColors(primary_hex="#03202F", secondary_hex="#A71930")),
    "IND": TeamIdentity(id="IND", city="Indianapolis", mascot="Colts", abbreviation="IND", conference="AFC", division="South", colors=TeamColors(primary_hex="#002C5F", secondary_hex="#A2AAAD")),
    "JAX": TeamIdentity(id="JAX", city="Jacksonville", mascot="Jaguars", abbreviation="JAX", conference="AFC", division="South", colors=TeamColors(primary_hex="#101820", secondary_hex="#D7A22A", accent_hex="#006778")),
    "TEN": TeamIdentity(id="TEN", city="Tennessee", mascot="Titans", abbreviation="TEN", conference="AFC", division="South", colors=TeamColors(primary_hex="#0C2340", secondary_hex="#4B92DB", accent_hex="#C8102E")),

    # AFC WEST
    "DEN": TeamIdentity(id="DEN", city="Denver", mascot="Broncos", abbreviation="DEN", conference="AFC", division="West", colors=TeamColors(primary_hex="#FB4F14", secondary_hex="#002244")),
    "KC": TeamIdentity(id="KC", city="Kansas City", mascot="Chiefs", abbreviation="KC", conference="AFC", division="West", colors=TeamColors(primary_hex="#E31837", secondary_hex="#FFB81C")),
    "LV": TeamIdentity(id="LV", city="Las Vegas", mascot="Raiders", abbreviation="LV", conference="AFC", division="West", colors=TeamColors(primary_hex="#000000", secondary_hex="#A5ACAF")),
    "LAC": TeamIdentity(id="LAC", city="Los Angeles", mascot="Chargers", abbreviation="LAC", conference="AFC", division="West", colors=TeamColors(primary_hex="#0080C6", secondary_hex="#FFC20E")),

    # NFC EAST
    "DAL": TeamIdentity(id="DAL", city="Dallas", mascot="Cowboys", abbreviation="DAL", conference="NFC", division="East", colors=TeamColors(primary_hex="#003594", secondary_hex="#869397", accent_hex="#002244")),
    "NYG": TeamIdentity(id="NYG", city="New York", mascot="Giants", abbreviation="NYG", conference="NFC", division="East", colors=TeamColors(primary_hex="#012352", secondary_hex="#A3162D", accent_hex="#9BA1A2")),
    "PHI": TeamIdentity(id="PHI", city="Philadelphia", mascot="Eagles", abbreviation="PHI", conference="NFC", division="East", colors=TeamColors(primary_hex="#004C54", secondary_hex="#A5ACAF", accent_hex="#000000")),
    "WAS": TeamIdentity(id="WAS", city="Washington", mascot="Commanders", abbreviation="WAS", conference="NFC", division="East", colors=TeamColors(primary_hex="#5A1414", secondary_hex="#FFB612")),

    # NFC NORTH
    "CHI": TeamIdentity(id="CHI", city="Chicago", mascot="Bears", abbreviation="CHI", conference="NFC", division="North", colors=TeamColors(primary_hex="#0B162A", secondary_hex="#C83803")),
    "DET": TeamIdentity(id="DET", city="Detroit", mascot="Lions", abbreviation="DET", conference="NFC", division="North", colors=TeamColors(primary_hex="#0076B6", secondary_hex="#B0B7BC", accent_hex="#000000")),
    "GB": TeamIdentity(id="GB", city="Green Bay", mascot="Packers", abbreviation="GB", conference="NFC", division="North", colors=TeamColors(primary_hex="#183028", secondary_hex="#FFB81C")),
    "MIN": TeamIdentity(id="MIN", city="Minnesota", mascot="Vikings", abbreviation="MIN", conference="NFC", division="North", colors=TeamColors(primary_hex="#4F2683", secondary_hex="#FFC62F")),

    # NFC SOUTH
    "ATL": TeamIdentity(id="ATL", city="Atlanta", mascot="Falcons", abbreviation="ATL", conference="NFC", division="South", colors=TeamColors(primary_hex="#A71930", secondary_hex="#000000", accent_hex="#A5ACAF")),
    "CAR": TeamIdentity(id="CAR", city="Carolina", mascot="Panthers", abbreviation="CAR", conference="NFC", division="South", colors=TeamColors(primary_hex="#0085CA", secondary_hex="#101820", accent_hex="#BFC0BF")),
    "NO": TeamIdentity(id="NO", city="New Orleans", mascot="Saints", abbreviation="NO", conference="NFC", division="South", colors=TeamColors(primary_hex="#D3BC8D", secondary_hex="#10181F")),
    "TB": TeamIdentity(id="TB", city="Tampa Bay", mascot="Buccaneers", abbreviation="TB", conference="NFC", division="South", colors=TeamColors(primary_hex="#D50A0A", secondary_hex="#34302B", accent_hex="#FF7900")),

    # NFC WEST
    "ARI": TeamIdentity(id="ARI", city="Arizona", mascot="Cardinals", abbreviation="ARI", conference="NFC", division="West", colors=TeamColors(primary_hex="#97233F", secondary_hex="#000000", accent_hex="#FFB612")),
    "LAR": TeamIdentity(id="LAR", city="Los Angeles", mascot="Rams", abbreviation="LAR", conference="NFC", division="West", colors=TeamColors(primary_hex="#003594", secondary_hex="#FFA300", accent_hex="#FFD100")),
    "SF": TeamIdentity(id="SF", city="San Francisco", mascot="49ers", abbreviation="SF", conference="NFC", division="West", colors=TeamColors(primary_hex="#AA0000", secondary_hex="#AD995D")),
    "SEA": TeamIdentity(id="SEA", city="Seattle", mascot="Seahawks", abbreviation="SEA", conference="NFC", division="West", colors=TeamColors(primary_hex="#002244", secondary_hex="#69BE28", accent_hex="#A5ACAF"))
}
