
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class CareerAccolades:
    pro_bowls: int = 0
    all_pros_1st: int = 0
    all_pros_2nd: int = 0
    mvps: int = 0
    super_bowl_mvps: int = 0
    offensive_player_of_year: int = 0
    defensive_player_of_year: int = 0
    rookie_of_year: int = 0

# Mapping of (First Name, Last Name) -> Accolades
# Focused on active stars who deserve a "Legacy Boost" in ratings
PLAYER_ACCOMPLISHMENTS: Dict[tuple, CareerAccolades] = {
    ("Patrick", "Mahomes"): CareerAccolades(pro_bowls=6, all_pros_1st=2, all_pros_2nd=1, mvps=2, super_bowl_mvps=3, offensive_player_of_year=1),
    ("Lamar", "Jackson"): CareerAccolades(pro_bowls=3, all_pros_1st=2, mvps=2),
    ("Josh", "Allen"): CareerAccolades(pro_bowls=2, all_pros_2nd=1),
    ("Joe", "Burrow"): CareerAccolades(pro_bowls=1),
    ("Aaron", "Rodgers"): CareerAccolades(pro_bowls=10, all_pros_1st=4, all_pros_2nd=1, mvps=4, super_bowl_mvps=1),
    ("Kirk", "Cousins"): CareerAccolades(pro_bowls=4),
    ("Matthew", "Stafford"): CareerAccolades(pro_bowls=2, super_bowl_mvps=0), # Getting respect for the ring
    ("Dak", "Prescott"): CareerAccolades(pro_bowls=3, offensive_player_of_year=0, rookie_of_year=1),
    ("Jalen", "Hurts"): CareerAccolades(pro_bowls=2, all_pros_2nd=1),
    ("Tua", "Tagovailoa"): CareerAccolades(pro_bowls=1),
    ("Justin", "Herbert"): CareerAccolades(pro_bowls=1, rookie_of_year=1),
    ("Trevor", "Lawrence"): CareerAccolades(pro_bowls=1),
    ("Jared", "Goff"): CareerAccolades(pro_bowls=3),

    # RBs
    ("Christian", "McCaffrey"): CareerAccolades(pro_bowls=3, all_pros_1st=2, all_pros_2nd=1, offensive_player_of_year=1),
    ("Derrick", "Henry"): CareerAccolades(pro_bowls=4, all_pros_1st=1, all_pros_2nd=1, offensive_player_of_year=1),
    ("Nick", "Chubb"): CareerAccolades(pro_bowls=4, all_pros_2nd=1),
    ("Saquon", "Barkley"): CareerAccolades(pro_bowls=2, rookie_of_year=1),
    ("Josh", "Jacobs"): CareerAccolades(pro_bowls=2, all_pros_1st=1),
    ("Jonathan", "Taylor"): CareerAccolades(pro_bowls=1, all_pros_1st=1),
    ("Alvin", "Kamara"): CareerAccolades(pro_bowls=5, all_pros_2nd=2, rookie_of_year=1),

    # WRs
    ("Tyreek", "Hill"): CareerAccolades(pro_bowls=8, all_pros_1st=5, all_pros_2nd=1), # Cheat code
    ("Davante", "Adams"): CareerAccolades(pro_bowls=6, all_pros_1st=3),
    ("Justin", "Jefferson"): CareerAccolades(pro_bowls=3, all_pros_1st=1, all_pros_2nd=2, offensive_player_of_year=1),
    ("Ja'Marr", "Chase"): CareerAccolades(pro_bowls=3, all_pros_2nd=1, rookie_of_year=1),
    ("Cooper", "Kupp"): CareerAccolades(pro_bowls=1, all_pros_1st=1, offensive_player_of_year=1, super_bowl_mvps=1),
    ("Stefon", "Diggs"): CareerAccolades(pro_bowls=4, all_pros_1st=1, all_pros_2nd=1),
    ("A.J.", "Brown"): CareerAccolades(pro_bowls=3, all_pros_2nd=2),
    ("CeeDee", "Lamb"): CareerAccolades(pro_bowls=3, all_pros_1st=1, all_pros_2nd=1),
    ("Mike", "Evans"): CareerAccolades(pro_bowls=5, all_pros_2nd=1),
    ("Keenan", "Allen"): CareerAccolades(pro_bowls=6),
    ("Amari", "Cooper"): CareerAccolades(pro_bowls=5),
    ("DeAndre", "Hopkins"): CareerAccolades(pro_bowls=5, all_pros_1st=3, all_pros_2nd=2),

    # TEs
    ("Travis", "Kelce"): CareerAccolades(pro_bowls=9, all_pros_1st=4, all_pros_2nd=3),
    ("George", "Kittle"): CareerAccolades(pro_bowls=5, all_pros_1st=2, all_pros_2nd=2),
    ("Mark", "Andrews"): CareerAccolades(pro_bowls=3, all_pros_1st=1),
    ("T.J.", "Hockenson"): CareerAccolades(pro_bowls=2),

    # OL
    ("Trent", "Williams"): CareerAccolades(pro_bowls=11, all_pros_1st=3, all_pros_2nd=1),
    ("Zack", "Martin"): CareerAccolades(pro_bowls=9, all_pros_1st=7, all_pros_2nd=2),
    ("Lane", "Johnson"): CareerAccolades(pro_bowls=5, all_pros_1st=2, all_pros_2nd=2),
    ("Penei", "Sewell"): CareerAccolades(pro_bowls=2, all_pros_1st=1),
    ("Quenton", "Nelson"): CareerAccolades(pro_bowls=6, all_pros_1st=3, all_pros_2nd=1),
    ("Joel", "Bitonio"): CareerAccolades(pro_bowls=6, all_pros_1st=2, all_pros_2nd=3),
    ("Chris", "Lindstrom"): CareerAccolades(pro_bowls=2, all_pros_2nd=2),
    ("Frank", "Ragnow"): CareerAccolades(pro_bowls=3, all_pros_2nd=2),

    # DE/EDGE
    ("Myles", "Garrett"): CareerAccolades(pro_bowls=5, all_pros_1st=3, all_pros_2nd=1, defensive_player_of_year=1),
    ("T.J.", "Watt"): CareerAccolades(pro_bowls=6, all_pros_1st=4, all_pros_2nd=1, defensive_player_of_year=1),
    ("Nick", "Bosa"): CareerAccolades(pro_bowls=4, all_pros_1st=1, defensive_player_of_year=1, rookie_of_year=1),
    ("Micah", "Parsons"): CareerAccolades(pro_bowls=3, all_pros_1st=2, all_pros_2nd=1, rookie_of_year=1),
    ("Maxx", "Crosby"): CareerAccolades(pro_bowls=3, all_pros_2nd=2),
    ("Khalil", "Mack"): CareerAccolades(pro_bowls=8, all_pros_1st=3, all_pros_2nd=2, defensive_player_of_year=1),
    ("Joey", "Bosa"): CareerAccolades(pro_bowls=4, rookie_of_year=1),
    ("Cameron", "Jordan"): CareerAccolades(pro_bowls=8, all_pros_1st=1, all_pros_2nd=2),
    ("Danielle", "Hunter"): CareerAccolades(pro_bowls=4, all_pros_2nd=1),

    # DT
    ("Chris", "Jones"): CareerAccolades(pro_bowls=5, all_pros_1st=2, all_pros_2nd=3),
    ("Aaron", "Donald"): CareerAccolades(pro_bowls=10, all_pros_1st=8, defensive_player_of_year=3, rookie_of_year=1), # Respect the legend
    ("Cameron", "Heyward"): CareerAccolades(pro_bowls=6, all_pros_1st=3, all_pros_2nd=1),
    ("Dexter", "Lawrence"): CareerAccolades(pro_bowls=2, all_pros_2nd=2),
    ("Quinnen", "Williams"): CareerAccolades(pro_bowls=2, all_pros_1st=1),
    ("Jeffery", "Simmons"): CareerAccolades(pro_bowls=2, all_pros_2nd=2),

    # LB
    ("Fred", "Warner"): CareerAccolades(pro_bowls=3, all_pros_1st=3),
    ("Roquan", "Smith"): CareerAccolades(pro_bowls=2, all_pros_1st=2),
    ("Demario", "Davis"): CareerAccolades(pro_bowls=2, all_pros_1st=1, all_pros_2nd=4),
    ("Bobby", "Wagner"): CareerAccolades(pro_bowls=9, all_pros_1st=6, all_pros_2nd=3),
    ("C.J.", "Mosley"): CareerAccolades(pro_bowls=5, all_pros_2nd=5),
    ("Lavonte", "David"): CareerAccolades(pro_bowls=1, all_pros_1st=1, all_pros_2nd=2),

    # CB
    ("Sauce", "Gardner"): CareerAccolades(pro_bowls=2, all_pros_1st=2, rookie_of_year=1),
    ("Patrick", "Surtain II"): CareerAccolades(pro_bowls=2, all_pros_1st=2),
    ("Jalen", "Ramsey"): CareerAccolades(pro_bowls=7, all_pros_1st=3, all_pros_2nd=1),
    ("Jaire", "Alexander"): CareerAccolades(pro_bowls=2, all_pros_2nd=2),
    ("Darius", "Slay"): CareerAccolades(pro_bowls=6, all_pros_1st=1),
    ("Marshon", "Lattimore"): CareerAccolades(pro_bowls=4, rookie_of_year=1),
    ("Marlon", "Humphrey"): CareerAccolades(pro_bowls=3, all_pros_1st=1),
    ("Tre", "White"): CareerAccolades(pro_bowls=2, all_pros_1st=1, all_pros_2nd=1),
    ("Denzel", "Ward"): CareerAccolades(pro_bowls=3),

    # S
    ("Minkah", "Fitzpatrick"): CareerAccolades(pro_bowls=4, all_pros_1st=3),
    ("Derwin", "James"): CareerAccolades(pro_bowls=3, all_pros_1st=1, all_pros_2nd=1),
    ("Justin", "Simmons"): CareerAccolades(pro_bowls=2, all_pros_2nd=4),
    ("Budda", "Baker"): CareerAccolades(pro_bowls=6, all_pros_1st=2, all_pros_2nd=1),
    ("Kevin", "Byard"): CareerAccolades(pro_bowls=2, all_pros_1st=2),
    ("Jessie", "Bates III"): CareerAccolades(pro_bowls=1, all_pros_2nd=2),
    ("Tyrann", "Mathieu"): CareerAccolades(pro_bowls=3, all_pros_1st=3, all_pros_2nd=1),
    ("Harrison", "Smith"): CareerAccolades(pro_bowls=6, all_pros_1st=1, all_pros_2nd=1),

    # K/P
    ("Justin", "Tucker"): CareerAccolades(pro_bowls=7, all_pros_1st=5, all_pros_2nd=3),
}

for (first, last), data in PLAYER_ACCOMPLISHMENTS.items():
   # Ensure clean lookup keys
   pass
