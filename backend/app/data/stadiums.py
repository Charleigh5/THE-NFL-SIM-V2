from pydantic import BaseModel
from typing import List, Optional

class StadiumModel(BaseModel):
    rank: int
    name: str
    team_ids: List[str]
    capacity: int
    year_built: int
    roof_type: str # Retractable, Fixed, Open, Translucent
    surface: str # Turf, Grass, Hybrid
    cost_billions: float
    features: List[str]

# Complete 30 Stadium Database (Ranked by Capacity)
STADIUM_DB = {
    "METLIFE": StadiumModel(rank=1, name="MetLife Stadium", team_ids=["NYG", "NYJ"], capacity=82500, year_built=2010, roof_type="Open-Air", surface="Turf", cost_billions=1.6, features=["Dual Home Teams", "Neutral Grey Seats"]),
    "LAMBEAU": StadiumModel(rank=2, name="Lambeau Field", team_ids=["GB"], capacity=81441, year_built=1957, roof_type="Open-Air", surface="Grass (Heated)", cost_billions=0.3, features=["Frozen Tundra", "Lambeau Leap", "Atrium"]),
    "ATT": StadiumModel(rank=3, name="AT&T Stadium", team_ids=["DAL"], capacity=80000, year_built=2009, roof_type="Retractable", surface="Turf", cost_billions=1.3, features=["Center Hung Board", "Endzone Suites", "Expandable to 100k"]),
    "ARROWHEAD": StadiumModel(rank=4, name="Arrowhead Stadium", team_ids=["KC"], capacity=76416, year_built=1972, roof_type="Open-Air", surface="Grass", cost_billions=0.043, features=["Loudest Stadium Record", "Sea of Red"]),
    "EMPOWER": StadiumModel(rank=5, name="Empower Field at Mile High", team_ids=["DEN"], capacity=76125, year_built=2001, roof_type="Open-Air", surface="Grass", cost_billions=0.4, features=["Altitude Advantage", "Thundering Floors"]),
    "BOA": StadiumModel(rank=6, name="Bank of America Stadium", team_ids=["CAR"], capacity=75523, year_built=1996, roof_type="Open-Air", surface="Turf", cost_billions=0.248, features=["Uptown Charlotte View", "Black & Blue"]),
    "SUPERDOME": StadiumModel(rank=7, name="Caesars Superdome", team_ids=["NO"], capacity=73208, year_built=1975, roof_type="Fixed Dome", surface="Turf", cost_billions=0.134, features=["Largest Fixed Dome", "Super Bowl Host"]),
    "NRG": StadiumModel(rank=8, name="NRG Stadium", team_ids=["HOU"], capacity=72220, year_built=2002, roof_type="Retractable", surface="Turf", cost_billions=0.352, features=["First Retractable Roof in NFL", "Rodeo Host"]),
    "HIGHMARK": StadiumModel(rank=9, name="Highmark Stadium", team_ids=["BUF"], capacity=71608, year_built=1973, roof_type="Open-Air", surface="Turf", cost_billions=0.022, features=["Windy Conditions", "Bills Mafia"]),
    "MTBANK": StadiumModel(rank=10, name="M&T Bank Stadium", team_ids=["BAL"], capacity=71008, year_built=1998, roof_type="Open-Air", surface="Grass", cost_billions=0.22, features=["Purple Lights", "Ravens Walk"]),
    "MERCEDES": StadiumModel(rank=11, name="Mercedes-Benz Stadium", team_ids=["ATL"], capacity=71000, year_built=2017, roof_type="Retractable (Oculus)", surface="Turf", cost_billions=1.6, features=["Halo Board", "Window to City", "Oculus Roof"]),
    "SOFI": StadiumModel(rank=12, name="SoFi Stadium", team_ids=["LAR", "LAC"], capacity=70000, year_built=2020, roof_type="Translucent Fixed", surface="Matrix Turf", cost_billions=6.75, features=["Infinity Screen", "Open Air Sides", "Canyon Entrance"]),
    "LINCOLN": StadiumModel(rank=13, name="Lincoln Financial Field", team_ids=["PHI"], capacity=69596, year_built=2003, roof_type="Open-Air", surface="Grass", cost_billions=0.512, features=["Wind Turbines", "Solar Panels"]),
    "NISSAN": StadiumModel(rank=14, name="Nissan Stadium", team_ids=["TEN"], capacity=69143, year_built=1999, roof_type="Open-Air", surface="Grass", cost_billions=0.29, features=["Cumberland River View"]),
    "TIAA": StadiumModel(rank=15, name="TIAA Bank Field", team_ids=["JAX"], capacity=69132, year_built=1995, roof_type="Open-Air", surface="Grass", cost_billions=0.121, features=["Swimming Pools", "Largest Video Boards"]),
    "LUMEN": StadiumModel(rank=16, name="Lumen Field", team_ids=["SEA"], capacity=69000, year_built=2002, roof_type="Partial Coverage", surface="Turf", cost_billions=0.43, features=["12th Man Acoustics", "Hawk's Nest"]),
    "LEVIS": StadiumModel(rank=17, name="Levi's Stadium", team_ids=["SF"], capacity=68500, year_built=2014, roof_type="Open-Air", surface="Grass", cost_billions=1.3, features=["Silicon Valley Tech", "Rooftop Farm"]),
    "ACRISURE": StadiumModel(rank=18, name="Acrisure Stadium", team_ids=["PIT"], capacity=68400, year_built=2001, roof_type="Open-Air", surface="Grass", cost_billions=0.281, features=["Great Hall", "Yellow Seats"]),
    "FIRSTENERGY": StadiumModel(rank=19, name="FirstEnergy Stadium", team_ids=["CLE"], capacity=67895, year_built=1999, roof_type="Open-Air", surface="Grass", cost_billions=0.283, features=["Dawg Pound"]),
    "FEDEX": StadiumModel(rank=20, name="FedExField", team_ids=["WAS"], capacity=67717, year_built=1997, roof_type="Open-Air", surface="Grass", cost_billions=0.25, features=["Controversial History"]),
    "LUCAS": StadiumModel(rank=21, name="Lucas Oil Stadium", team_ids=["IND"], capacity=67000, year_built=2008, roof_type="Retractable", surface="Turf", cost_billions=0.72, features=["Barn Design", "Window Wall"]),
    "GILLETTE": StadiumModel(rank=22, name="Gillette Stadium", team_ids=["NE"], capacity=66829, year_built=2002, roof_type="Open-Air", surface="Turf", cost_billions=0.325, features=["Lighthouse", "Bridge"]),
    "USBANK": StadiumModel(rank=23, name="U.S. Bank Stadium", team_ids=["MIN"], capacity=66655, year_built=2016, roof_type="Fixed Translucent", surface="Turf", cost_billions=1.1, features=["ETFE Roof", "Glass Doors", "Viking Ship"]),
    "RAYMOND": StadiumModel(rank=24, name="Raymond James Stadium", team_ids=["TB"], capacity=65890, year_built=1998, roof_type="Open-Air", surface="Grass", cost_billions=0.168, features=["Pirate Ship"]),
    "PAYCOR": StadiumModel(rank=25, name="Paycor Stadium", team_ids=["CIN"], capacity=65515, year_built=2000, roof_type="Open-Air", surface="Turf", cost_billions=0.455, features=["Jungle Theme"]),
    "HARDROCK": StadiumModel(rank=26, name="Hard Rock Stadium", team_ids=["MIA"], capacity=65326, year_built=1987, roof_type="Open-Air (Canopy)", surface="Grass", cost_billions=0.115, features=["Canopy Roof", "Gondola"]),
    "ALLEGIANT": StadiumModel(rank=27, name="Allegiant Stadium", team_ids=["LV"], capacity=65000, year_built=2020, roof_type="Fixed Translucent", surface="Grass (Tray)", cost_billions=2.33, features=["Al Davis Torch", "Lanai Doors", "Field Tray"]),
    "FORD": StadiumModel(rank=28, name="Ford Field", team_ids=["DET"], capacity=65000, year_built=2002, roof_type="Fixed Dome", surface="Turf", cost_billions=0.43, features=["Integrated Warehouse", "Downtown Location"]),
    "STATEFARM": StadiumModel(rank=29, name="State Farm Stadium", team_ids=["ARI"], capacity=63400, year_built=2006, roof_type="Retractable", surface="Grass (Tray)", cost_billions=0.455, features=["Field Tray", "Super Bowl Host"]),
    "SOLDIER": StadiumModel(rank=30, name="Soldier Field", team_ids=["CHI"], capacity=61500, year_built=1924, roof_type="Open-Air", surface="Grass", cost_billions=0.632, features=["Historic Colonnades", "Smallest Capacity"])
}
