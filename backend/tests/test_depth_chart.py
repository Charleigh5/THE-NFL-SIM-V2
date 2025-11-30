import pytest
from app.models.player import Player
from app.services.depth_chart_service import DepthChartService

def test_organize_roster():
    players = [
        Player(id=1, first_name="A", last_name="QB", position="QB", overall_rating=90),
        Player(id=2, first_name="B", last_name="QB", position="QB", overall_rating=80),
        Player(id=3, first_name="C", last_name="WR", position="WR", overall_rating=85),
    ]
    
    chart = DepthChartService.organize_roster(players)
    
    assert "QB" in chart
    assert len(chart["QB"]) == 2
    assert chart["QB"][0].id == 1 # Highest rated first
    assert "WR" in chart
    assert len(chart["WR"]) == 1

def test_get_starters_offense():
    players = []
    # QB
    players.append(Player(id=1, position="QB", overall_rating=90))
    # RB
    players.append(Player(id=2, position="RB", overall_rating=88))
    # WRs
    players.append(Player(id=3, position="WR", overall_rating=95))
    players.append(Player(id=4, position="WR", overall_rating=90))
    players.append(Player(id=5, position="WR", overall_rating=85))
    # TE
    players.append(Player(id=6, position="TE", overall_rating=80))
    # OL
    players.append(Player(id=7, position="OT", overall_rating=90)) # LT
    players.append(Player(id=8, position="OT", overall_rating=89)) # RT
    players.append(Player(id=9, position="OG", overall_rating=88)) # LG
    players.append(Player(id=10, position="OG", overall_rating=87)) # RG
    players.append(Player(id=11, position="C", overall_rating=86))  # C
    
    starters = DepthChartService.get_starters(players, "standard")
    
    assert starters["QB"].id == 1
    assert starters["RB"].id == 2
    assert starters["WR1"].id == 3
    assert starters["WR2"].id == 4
    assert starters["WR3"].id == 5
    assert starters["TE"].id == 6
    assert starters["LT"].id == 7
    assert starters["RT"].id == 8

def test_get_starters_defense():
    players = []
    # DL
    players.append(Player(id=20, position="DE", overall_rating=90))
    players.append(Player(id=21, position="DE", overall_rating=89))
    players.append(Player(id=22, position="DT", overall_rating=92))
    players.append(Player(id=23, position="DT", overall_rating=91))
    # LB
    players.append(Player(id=24, position="LB", overall_rating=88))
    players.append(Player(id=25, position="LB", overall_rating=87))
    players.append(Player(id=26, position="LB", overall_rating=86))
    # DB
    players.append(Player(id=27, position="CB", overall_rating=95))
    players.append(Player(id=28, position="CB", overall_rating=94))
    players.append(Player(id=29, position="S", overall_rating=90))
    players.append(Player(id=30, position="S", overall_rating=89))
    
    starters = DepthChartService.get_starters(players, "standard")
    
    assert starters["LE"].id == 20
    assert starters["RE"].id == 21
    assert starters["DT1"].id == 22
    assert starters["DT2"].id == 23
    assert starters["LOLB"].id == 24
    assert starters["MLB"].id == 25
    assert starters["ROLB"].id == 26
    assert starters["CB1"].id == 27
    assert starters["CB2"].id == 28
    assert starters["FS"].id == 29
    assert starters["SS"].id == 30
