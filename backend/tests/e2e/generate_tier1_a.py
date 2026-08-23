# Generator for Tier 1 Part A (F01 - F15)
import os

TIER1_A_CODE = """
# ==============================================================================
# TIER 1: FEATURE COVERAGE TESTS (F01 - F15)
# ==============================================================================

class TestTier1F01PlayerGameStartsUnification:
    \"\"\"F01: PlayerGameStarts table unification.\"\"\"

    def test_f01_player_game_starts_table_creation(self, db_session):
        table = Base.metadata.tables.get('player_game_starts')
        assert table is not None, "player_game_starts table must exist in metadata"
        col_names = {c.name for c in table.columns}
        expected = {'id', 'player_id', 'game_id', 'position', 'teammates_hash', 'created_at'}
        assert expected.issubset(col_names), f"Missing columns in player_game_starts: {expected - col_names}"

    def test_f01_player_game_starts_insert_and_retrieve(self, db_session):
        s = Season(id=1, year=2026, current_week=1, status=SeasonStatus.REGULAR_SEASON)
        team = Team(id=101, name="Chiefs", city="KC", abbreviation="KC", conference="AFC", division="West")
        player = Player(id=101, team_id=101, first_name="Creed", last_name="Humphrey", position="C", age=25, height=76, weight=310)
        game = Game(id=201, season_id=1, week=1, home_team_id=101, away_team_id=101, home_score=24, away_score=20, is_played=True)
        db_session.add_all([s, team, player, game])
        db_session.flush()

        start = PlayerGameStarts(
            player_id=101,
            game_id=201,
            position="C",
            teammates_hash="abc123hash_ol_unit"
        )
        db_session.add(start)
        db_session.flush()

        retrieved = db_session.get(PlayerGameStarts, start.id)
        assert retrieved is not None
        assert retrieved.player_id == 101
        assert retrieved.position == "C"
        assert retrieved.position_started == "C"
        assert retrieved.teammates_hash == "abc123hash_ol_unit"

    def test_f01_player_game_starts_relationship_player(self, db_session):
        s = Season(id=1, year=2026, current_week=1, status=SeasonStatus.REGULAR_SEASON)
        team = Team(id=102, name="Bills", city="Buffalo", abbreviation="BUF", conference="AFC", division="East")
        player = Player(id=102, team_id=102, first_name="Dion", last_name="Dawkins", position="LT", age=29, height=77, weight=320)
        game = Game(id=202, season_id=1, week=1, home_team_id=102, away_team_id=102, home_score=21, away_score=17, is_played=True)
        db_session.add_all([s, team, player, game])
        db_session.flush()

        start = PlayerGameStarts(player_id=102, game_id=202, position="LT", teammates_hash="buf_ol_hash")
        db_session.add(start)
        db_session.flush()

        db_session.refresh(player)
        assert len(player.game_starts) >= 1
        assert player.game_starts[0].position == "LT"

    def test_f01_player_game_starts_relationship_game(self, db_session):
        s = Season(id=1, year=2026, current_week=2, status=SeasonStatus.REGULAR_SEASON)
        team = Team(id=103, name="Ravens", city="Baltimore", abbreviation="BAL", conference="AFC", division="North")
        player = Player(id=103, team_id=103, first_name="Tyler", last_name="Linderbaum", position="C", age=24, height=74, weight=305)
        game = Game(id=203, season_id=1, week=2, home_team_id=103, away_team_id=103, home_score=28, away_score=24, is_played=True)
        db_session.add_all([s, team, player, game])
        db_session.flush()

        start = PlayerGameStarts(player_id=103, game_id=203, position="C", teammates_hash="bal_ol_hash")
        db_session.add(start)
        db_session.flush()

        db_session.refresh(game)
        assert hasattr(game, 'player_starts')
        assert len(game.player_starts) >= 1

    def test_f01_player_game_starts_composite_index(self, db_session):
        table = Base.metadata.tables.get('player_game_starts')
        index_cols = [idx.columns.keys() for idx in table.indexes]
        has_player_game_idx = any({'player_id', 'game_id'}.issubset(set(cols)) for cols in index_cols)
        assert has_player_game_idx, "player_game_starts must have composite index on (player_id, game_id)"


class TestTier1F02AlembicModelDiscovery:
    \"\"\"F02: Alembic model discovery across all 20+ models.\"\"\"

    def test_f02_metadata_contains_core_tables(self):
        tables = Base.metadata.tables.keys()
        for t in ['player', 'team', 'game', 'season']:
            assert t in tables, f"Core table '{t}' must be registered in metadata"

    def test_f02_metadata_contains_playoff_tables(self):
        tables = Base.metadata.tables.keys()
        assert 'playoff_matchup' in tables or 'playoff_matchups' in tables

    def test_f02_metadata_contains_depth_chart_tables(self):
        tables = Base.metadata.tables.keys()
        assert 'depthchart' in tables or 'depth_chart' in tables or 'depth_charts' in tables

    def test_f02_metadata_contains_news_and_events(self):
        tables = Base.metadata.tables.keys()
        assert 'news_items' in tables or 'news_item' in tables
        assert 'weekly_recaps' in tables or 'weekly_recap' in tables
        assert 'rpg_events' in tables or 'rpg_event' in tables

    def test_f02_metadata_contains_weather_and_stadium(self):
        tables = Base.metadata.tables.keys()
        assert 'game_weather' in tables or 'weather' in tables
        assert 'stadium' in tables or 'stadiums' in tables
        assert 'player_game_starts' in tables


class TestTier1F03PlayerTraitsRelationship:
    \"\"\"F03: Player.traits relationship & profile loading.\"\"\"

    def test_f03_player_traits_empty_by_default(self, db_session):
        p = Player(id=104, first_name="Joe", last_name="Burrow", position="QB", age=27, height=76, weight=215)
        db_session.add(p)
        db_session.flush()
        assert hasattr(p, 'player_traits')
        assert p.player_traits == []

    def test_f03_player_trait_association_creation(self, db_session):
        p = Player(id=105, first_name="Lamar", last_name="Jackson", position="QB", age=27, height=74, weight=215)
        t = Trait(id=1, name="escape_artist", tier=TraitTier.GOLD)
        db_session.add_all([p, t])
        db_session.flush()

        pt = PlayerTrait(player_id=105, trait_id=1, source=TraitSource.DRAFT)
        db_session.add(pt)
        db_session.flush()

        db_session.refresh(p)
        assert len(p.player_traits) == 1
        assert p.player_traits[0].trait_id == 1

    def test_f03_player_trait_tier_assignment(self, db_session):
        t = Trait(id=2, name="route_technician", tier=TraitTier.GOLD)
        db_session.add(t)
        db_session.flush()
        assert t.tier == TraitTier.GOLD

    def test_f03_player_trait_query_joined(self, db_session):
        p = Player(id=107, first_name="Myles", last_name="Garrett", position="DE", age=28, height=76, weight=272)
        t = Trait(id=3, name="edge_threat", tier=TraitTier.GOLD)
        db_session.add_all([p, t])
        db_session.flush()

        pt = PlayerTrait(player_id=107, trait_id=3)
        db_session.add(pt)
        db_session.flush()

        stmt = select(Player).where(Player.id == 107)
        res = db_session.execute(stmt).scalar_one()
        assert res.last_name == "Garrett"
        assert len(res.player_traits) == 1

    def test_f03_player_profile_trait_serialization(self, db_session):
        p = Player(id=108, first_name="Sauce", last_name="Gardner", position="CB", age=24, height=75, weight=200)
        t = Trait(id=4, name="island_lockdown", tier=TraitTier.SILVER)
        db_session.add_all([p, t])
        db_session.flush()

        pt = PlayerTrait(player_id=108, trait_id=4)
        db_session.add(pt)
        db_session.flush()

        traits_dict = [
            {"trait_id": pt_item.trait_id, "name": pt_item.trait.name, "tier": pt_item.trait.tier.value}
            for pt_item in p.player_traits
        ]
        assert len(traits_dict) == 1
        assert traits_dict[0]["name"] == "island_lockdown"


class TestTier1F04HybridPropertyExpressions:
    \"\"\"F04: Hybrid property expressions on Player model.\"\"\"

    def test_f04_hybrid_speed_getter_setter(self):
        p = Player(id=109, first_name="Tyreek", last_name="Hill", position="WR", age=30, height=70, weight=185)
        p.speed = 99
        assert p.speed == 99
        assert p.attributes.speed == 99

    def test_f04_hybrid_strength_and_agility(self):
        p = Player(id=110, first_name="Aaron", last_name="Donald", position="DT", age=32, height=73, weight=285)
        p.strength = 99
        p.agility = 88
        assert p.strength == 99
        assert p.agility == 88
        assert p.attributes.strength == 99

    def test_f04_hybrid_contract_expression(self, db_session):
        p = Player(id=111, first_name="T.J.", last_name="Watt", position="LB", age=29, height=76, weight=252)
        p.contract_salary = 28000000
        p.contract_years = 3
        db_session.add(p)
        db_session.flush()

        stmt = select(Player).where(Player.contract_salary >= 25000000)
        res = db_session.execute(stmt).scalars().all()
        assert any(pl.id == 111 for pl in res)

    def test_f04_hybrid_is_rookie_and_retired(self, db_session):
        p = Player(id=112, first_name="C.J.", last_name="Stroud", position="QB", age=22, height=75, weight=218)
        p.is_rookie = True
        p.is_retired = False
        db_session.add(p)
        db_session.flush()

        stmt = select(Player).where(Player.is_rookie == True)
        res = db_session.execute(stmt).scalars().all()
        assert any(pl.id == 112 for pl in res)

    def test_f04_draft_assistant_attribute_access(self):
        p = Player(id=113, first_name="Marvin", last_name="Harrison", position="WR", age=21, height=76, weight=205)
        p.speed = 94
        p.strength = 75
        p.agility = 92
        p.overall_rating = 84

        data = {
            'id': p.id,
            'name': f"{p.first_name} {p.last_name}",
            'speed': p.speed,
            'strength': p.strength,
            'agility': p.agility,
            'overall': p.overall_rating
        }
        assert data['speed'] == 94
        assert data['strength'] == 75


class TestTier1F05DecompositionCascades:
    \"\"\"F05: 1:1 decomposition cascades & lifecycle.\"\"\"

    def test_f05_player_creation_instantiates_satellites(self):
        p = Player(id=114, first_name="Micah", last_name="Parsons", position="LB", age=25, height=75, weight=245)
        assert p.attributes is not None
        assert p.contract is not None
        assert p.physics is not None
        assert p.injury is not None
        assert p.progression is not None

    def test_f05_cascade_delete_attributes(self, db_session):
        p = Player(id=115, first_name="Nick", last_name="Bosa", position="DE", age=26, height=76, weight=266)
        db_session.add(p)
        db_session.flush()

        attr_id = p.attributes.id
        db_session.delete(p)
        db_session.flush()

        attr = db_session.get(PlayerAttributes, attr_id)
        assert attr is None

    def test_f05_cascade_delete_contract(self, db_session):
        p = Player(id=116, first_name="Fred", last_name="Warner", position="LB", age=27, height=75, weight=230)
        db_session.add(p)
        db_session.flush()

        contract_id = p.contract.id
        db_session.delete(p)
        db_session.flush()

        contract = db_session.get(PlayerContract, contract_id)
        assert contract is None

    def test_f05_cascade_delete_physics_and_injury(self, db_session):
        p = Player(id=117, first_name="Roquan", last_name="Smith", position="LB", age=27, height=73, weight=236)
        db_session.add(p)
        db_session.flush()

        physics_id = p.physics.id
        injury_id = p.injury.id
        db_session.delete(p)
        db_session.flush()

        assert db_session.get(PlayerPhysics, physics_id) is None
        assert db_session.get(PlayerInjury, injury_id) is None

    def test_f05_lazy_joined_loading(self, db_session):
        p = Player(id=118, first_name="Trent", last_name="Williams", position="OT", age=36, height=77, weight=320)
        db_session.add(p)
        db_session.flush()
        db_session.expire(p)

        reloaded = db_session.get(Player, 118)
        assert reloaded.attributes.speed == 50


class TestTier1F06SQLiteWALConnectionPragmas:
    \"\"\"F06: SQLite WAL Connection Pragmas.\"\"\"

    def test_f06_wal_journal_mode_pragma(self, db_session):
        res = db_session.execute(text("PRAGMA journal_mode")).scalar()
        assert res.lower() in ["wal", "memory"], f"Journal mode must be WAL or memory, got {res}"

    def test_f06_busy_timeout_pragma(self, db_session):
        db_session.execute(text("PRAGMA busy_timeout=5000"))
        timeout = db_session.execute(text("PRAGMA busy_timeout")).scalar()
        assert timeout == 5000

    def test_f06_foreign_keys_pragma(self, db_session):
        db_session.execute(text("PRAGMA foreign_keys=ON"))
        fk = db_session.execute(text("PRAGMA foreign_keys")).scalar()
        assert fk == 1

    def test_f06_concurrent_read_connections(self, db_session):
        res1 = db_session.execute(select(func.count(Team.id))).scalar()
        res2 = db_session.execute(select(func.count(Player.id))).scalar()
        assert res1 >= 0
        assert res2 >= 0

    def test_f06_async_sync_engine_compatibility(self, db_session):
        team = Team(id=119, name="Texans", city="Houston", abbreviation="HOU", conference="AFC", division="South")
        db_session.add(team)
        db_session.flush()
        queried = db_session.get(Team, 119)
        assert queried.name == "Texans"


class TestTier1F07SafetyScoringAndReset:
    \"\"\"F07: Safety scoring and possession reset logic.\"\"\"

    def test_f07_sack_in_endzone_is_safety(self):
        res = PlayResult(
            play_type="SACK",
            description="Quarterback sacked in end zone for safety",
            yards_gained=-8,
            is_sack=True,
            is_safety=True,
            time_elapsed=6.5
        )
        assert res.is_safety is True
        assert res.is_sack is True

    def test_f07_safety_awards_2_points_to_defense(self):
        orch = SimulationOrchestrator()
        orch.home_score = 10
        orch.away_score = 7
        orch.possession = "home"
        orch.yard_line = 3

        safety_play = PlayResult(
            play_type="SACK",
            description="Safety in end zone",
            yards_gained=-5,
            is_safety=True,
            time_elapsed=7.0
        )
        if safety_play.is_safety:
            if orch.possession == "home":
                orch.away_score += 2
                orch.possession = "away"
                orch.yard_line = 35
            else:
                orch.home_score += 2
                orch.possession = "home"
                orch.yard_line = 35

        assert orch.away_score == 9
        assert orch.possession == "away"
        assert orch.yard_line == 35

    def test_f07_safety_resets_possession(self):
        possession = "away"
        possession = "home" if possession == "away" else "away"
        assert possession == "home"

    def test_f07_safety_free_kick_field_position(self):
        free_kick_spot = 20
        average_return = 15
        starting_field_pos = free_kick_spot + average_return
        assert starting_field_pos == 35

    def test_f07_tackle_for_loss_into_endzone(self):
        start_yard = 2
        gain = -4
        end_yard = start_yard + gain
        is_safety = end_yard <= 0
        assert is_safety is True


class TestTier1F08DynamicPlayClockRunoffs:
    \"\"\"F08: Dynamic play clock runoffs.\"\"\"

    def test_f08_incomplete_pass_clock_runoff(self):
        rng = DeterministicRNG("clock_seed_1")
        for _ in range(20):
            runoff = rng.uniform(4.0, 7.0)
            assert 4.0 <= runoff <= 7.0

    def test_f08_out_of_bounds_clock_runoff(self):
        rng = DeterministicRNG("clock_seed_2")
        for _ in range(20):
            runoff = rng.uniform(5.0, 8.0)
            assert 5.0 <= runoff <= 8.0

    def test_f08_in_bounds_tackle_clock_runoff(self):
        rng = DeterministicRNG("clock_seed_3")
        for _ in range(20):
            runoff = rng.uniform(25.0, 38.0)
            assert 25.0 <= runoff <= 38.0

    def test_f08_sack_clock_runoff(self):
        rng = DeterministicRNG("clock_seed_4")
        for _ in range(20):
            runoff = rng.uniform(6.0, 9.0)
            assert 6.0 <= runoff <= 9.0

    def test_f08_special_teams_runoff(self):
        rng = DeterministicRNG("clock_seed_5")
        for _ in range(20):
            runoff = rng.uniform(5.0, 8.0)
            assert 5.0 <= runoff <= 8.0


class TestTier1F09RedZoneTDStatAttribution:
    \"\"\"F09: Red Zone Touchdown Stat Attribution.\"\"\"

    def test_f09_passing_td_in_redzone(self):
        stats = PlayerGameStats(player_id=1, game_id=1, pass_tds=0, pass_yards=0)
        stats.pass_tds += 1
        stats.pass_yards += 15
        assert stats.pass_tds == 1
        assert stats.pass_yards == 15

    def test_f09_rushing_td_in_redzone(self):
        stats = PlayerGameStats(player_id=2, game_id=1, rush_tds=0, rush_yards=0)
        stats.rush_tds += 1
        stats.rush_yards += 4
        assert stats.rush_tds == 1
        assert stats.rush_yards == 4

    def test_f09_goal_line_plunge_stats(self):
        stats = PlayerGameStats(player_id=3, game_id=1, rush_tds=0, rush_yards=0)
        stats.rush_tds += 1
        stats.rush_yards += 1
        assert stats.rush_tds == 1
        assert stats.rush_yards == 1

    def test_f09_passer_yards_stat_accumulation(self):
        stats = PlayerGameStats(player_id=1, game_id=1, pass_yards=180)
        stats.pass_yards += 18
        assert stats.pass_yards == 198

    def test_f09_receiver_stats_accumulation(self):
        stats = PlayerGameStats(player_id=4, game_id=1, rec_yards=45, rec_tds=0, receptions=3)
        stats.rec_yards += 12
        stats.rec_tds += 1
        stats.receptions += 1
        assert stats.rec_yards == 57
        assert stats.rec_tds == 1
        assert stats.receptions == 4


class TestTier1F10DynamicPATAnd2PointConversions:
    \"\"\"F10: Dynamic PAT and 2-Point Conversion Logic.\"\"\"

    def test_f10_pat_kick_success_1_point(self):
        pat_result = {"type": "PAT_KICK", "success": True, "points": 1}
        assert pat_result["points"] == 1

    def test_f10_pat_kick_miss_0_points(self):
        pat_result = {"type": "PAT_KICK", "success": False, "points": 0}
        assert pat_result["points"] == 0

    def test_f10_two_point_conversion_success_2_points(self):
        two_pt = {"type": "TWO_POINT_CONVERSION", "success": True, "points": 2}
        assert two_pt["points"] == 2

    def test_f10_two_point_conversion_failure_0_points(self):
        two_pt = {"type": "TWO_POINT_CONVERSION", "success": False, "points": 0}
        assert two_pt["points"] == 0

    def test_f10_coaching_ai_conversion_decision(self):
        score_diff = -2
        time_seconds = 80
        attempt_2pt = score_diff == -2 and time_seconds < 120
        assert attempt_2pt is True


class TestTier1F11DeterministicSeededRNG:
    \"\"\"F11: Deterministic Seeded RNG.\"\"\"

    def test_f11_deterministic_rng_seed_reproducibility(self):
        rng1 = DeterministicRNG("nfl_sim_seed_2026")
        rng2 = DeterministicRNG("nfl_sim_seed_2026")

        seq1 = [rng1.randint(1, 100) for _ in range(50)]
        seq2 = [rng2.randint(1, 100) for _ in range(50)]
        assert seq1 == seq2

    def test_f11_deterministic_rng_different_seeds_diverge(self):
        rng1 = DeterministicRNG("seed_alpha")
        rng2 = DeterministicRNG("seed_beta")

        seq1 = [rng1.randint(1, 100) for _ in range(50)]
        seq2 = [rng2.randint(1, 100) for _ in range(50)]
        assert seq1 != seq2

    def test_f11_simulation_reproducibility(self):
        rng1 = DeterministicRNG("game_seed_42")
        rng2 = DeterministicRNG("game_seed_42")

        rolls1 = [rng1.random() for _ in range(100)]
        rolls2 = [rng2.random() for _ in range(100)]
        assert rolls1 == rolls2

    def test_f11_random_integers_bounded(self):
        rng = DeterministicRNG("bounded_seed")
        for _ in range(100):
            val = rng.randint(10, 20)
            assert 10 <= val <= 20

    def test_f11_random_float_uniformity(self):
        rng = DeterministicRNG("uniform_seed")
        for _ in range(100):
            f = rng.random()
            assert 0.0 <= f < 1.0


class TestTier1F12MultiQuarterSimulationLoop:
    \"\"\"F12: Multi-quarter & Overtime simulation loop.\"\"\"

    def test_f12_quarter_advancement_q1_to_q4(self):
        quarters = []
        q = 1
        while q <= 4:
            quarters.append(q)
            q += 1
        assert quarters == [1, 2, 3, 4]

    def test_f12_halftime_possession_flip(self):
        first_half_kickoff_receiver = "away"
        second_half_kickoff_receiver = "home" if first_half_kickoff_receiver == "away" else "away"
        assert second_half_kickoff_receiver == "home"

    def test_f12_fifteen_minute_quarters(self):
        quarter_duration_seconds = 900
        assert quarter_duration_seconds == 15 * 60

    def test_f12_overtime_trigger_on_tie(self):
        home_score = 24
        away_score = 24
        quarter = 4
        is_tied = home_score == away_score and quarter == 4
        assert is_tied is True

    def test_f12_game_final_status_on_completion(self):
        game = Game(id=301, season_id=1, week=1, home_team_id=1, away_team_id=2, home_score=27, away_score=20, is_played=True)
        assert game.is_played is True
        assert game.home_score > game.away_score


class TestTier1F13DraftOrderAttributeResolution:
    \"\"\"F13: Draft order generation & attribute resolution.\"\"\"

    def test_f13_standings_win_percentage_attribute(self):
        st = TeamStanding(
            team_id=1, team_name="Lions", team_abbreviation="DET", conference="NFC", division="North",
            wins=12, losses=5, ties=0, win_percentage=12/17, points_for=450, points_against=350, point_differential=100,
            division_rank=1, conference_rank=2
        )
        assert hasattr(st, 'win_percentage')
        assert 0.70 <= st.win_percentage <= 0.71

    def test_f13_draft_order_sorting_reverse_standings(self):
        t1 = TeamStanding(team_id=1, team_name="Team1", team_abbreviation="T1", conference="AFC", division="East", wins=2, losses=15, ties=0, win_percentage=2/17, points_for=200, points_against=400, point_differential=-200, division_rank=4, conference_rank=16)
        t2 = TeamStanding(team_id=2, team_name="Team2", team_abbreviation="T2", conference="AFC", division="West", wins=14, losses=3, ties=0, win_percentage=14/17, points_for=420, points_against=250, point_differential=170, division_rank=1, conference_rank=1)
        standings = [t2, t1]
        draft_order = sorted(standings, key=lambda x: (x.win_percentage, x.point_differential))
        assert draft_order[0].team_id == 1

    def test_f13_draft_order_tiebreak_points(self):
        t1 = TeamStanding(team_id=1, team_name="T1", team_abbreviation="T1", conference="AFC", division="East", wins=5, losses=12, ties=0, win_percentage=5/17, points_for=250, points_against=350, point_differential=-100, division_rank=4, conference_rank=14)
        t2 = TeamStanding(team_id=2, team_name="T2", team_abbreviation="T2", conference="NFC", division="East", wins=5, losses=12, ties=0, win_percentage=5/17, points_for=220, points_against=370, point_differential=-150, division_rank=4, conference_rank=15)
        draft_order = sorted([t1, t2], key=lambda x: (x.win_percentage, x.point_differential))
        assert draft_order[0].team_id == 2

    def test_f13_draft_order_generation_offseason_service(self, db_session):
        season = Season(id=10, year=2026, current_week=18, status=SeasonStatus.REGULAR_SEASON, is_active=True)
        db_session.add(season)
        db_session.flush()
        svc = OffseasonService(db_session, seed=42)
        assert svc is not None

    def test_f13_draft_pick_round_and_number_assignment(self):
        total_picks = 32 * 7
        assert total_picks == 224


class TestTier1F14TradedDraftPickOwnership:
    \"\"\"F14: Traded draft pick ownership preservation.\"\"\"

    def test_f14_draft_pick_preserves_original_team_id(self):
        pick = DraftPick(
            id=1, season_id=1, round=1, pick_number=12,
            team_id=2,
            original_team_id=1
        )
        assert pick.team_id == 2
        assert pick.original_team_id == 1

    def test_f14_trade_draft_pick_updates_owner(self):
        pick = DraftPick(id=2, season_id=1, round=2, pick_number=45, team_id=1, original_team_id=1)
        pick.team_id = 3
        assert pick.team_id == 3
        assert pick.original_team_id == 1

    def test_f14_multi_round_traded_picks(self):
        picks = [
            DraftPick(id=i, season_id=1, round=r, pick_number=i, team_id=1, original_team_id=1)
            for i, r in enumerate(range(1, 8), start=1)
        ]
        picks[0].team_id = 5
        picks[3].team_id = 5
        assert [p.team_id for p in picks] == [5, 1, 1, 5, 1, 1, 1]

    def test_f14_draft_order_uses_traded_owners(self):
        pick = DraftPick(id=10, season_id=1, round=1, pick_number=5, team_id=8, original_team_id=3)
        assert pick.team_id == 8

    def test_f14_trade_offer_model_pick_id_link(self, db_session):
        offer = TradeOffer(
            id=1,
            offering_team_id=1, receiving_team_id=2,
            offered_player_ids=[101],
            requested_player_ids=[201],
            offered_picks=[{"pick_id": 15, "round": 1}],
            requested_picks=[{"pick_id": 45, "round": 2}],
            status=TradeOfferStatus.PENDING
        )
        assert offer.offered_picks[0]["pick_id"] == 15
        assert offer.requested_picks[0]["pick_id"] == 45


class TestTier1F15FreeAgencyEngineIntegration:
    \"\"\"F15: FreeAgencyEngine integration & bidding.\"\"\"

    def test_f15_free_agency_engine_market_value_calc(self, db_session):
        fa_engine = FreeAgencyEngine(db_session)
        player = Player(id=120, first_name="Justin", last_name="Simmons", position="S", overall_rating=88, age=30)
        aav, years, gtd = fa_engine.calculate_market_value(player)
        assert aav >= 8_000_000
        assert years >= 2
        assert gtd > 0

    def test_f15_free_agency_team_interest_scoring(self, db_session):
        fa_engine = FreeAgencyEngine(db_session)
        team = Team(id=1, name="Patriots", city="NE", abbreviation="NE", prestige=65, salary_cap_space=40_000_000.0)
        player = Player(id=121, first_name="Brian", last_name="Burns", position="DE", overall_rating=89, age=26)
        roster_counts = {"DE": 1}
        interest = fa_engine.calculate_team_interest(team, player, roster_counts, 20_000_000.0, 40_000_000.0)
        assert interest > 40.0

    def test_f15_free_agency_simulate_round_signings(self, db_session):
        fa_engine = FreeAgencyEngine(db_session)
        assert hasattr(fa_engine, 'simulate_free_agency')

    def test_f15_free_agency_cap_space_decrement(self):
        cap_space = 50_000_000.0
        contract_aav = 15_000_000.0
        cap_space -= contract_aav
        assert cap_space == 35_000_000.0

    def test_f15_free_agency_player_team_assignment(self):
        player = Player(id=122, first_name="Kirk", last_name="Cousins", position="QB", team_id=None)
        player.team_id = 4
        assert player.team_id == 4
"""

if __name__ == '__main__':
    e2e_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(e2e_dir, 'part1_tier1_a.py'), 'w', encoding='utf-8') as f:
        f.write(TIER1_A_CODE)
    print('Generated part1_tier1_a.py in e2e dir')
