"""
Unit Tests: Capology Double-Entry Ledger Engine
================================================
Empirical verification of mathematical double-entry invariants,
zero-sum transaction proofs, post-June 1st splits, and sub-millisecond latency.
"""

import time
import pytest
from app.services.cap_ledger_service import CapLedgerService, BASE_LEAGUE_YEAR, BASE_SALARY_CAP
from app.models.cap_ledger import CapAccountType, CapTransactionType
from app.schemas.cap_ledger import LedgerSimulateRequest


@pytest.fixture
def ledger_service():
    """Returns a clean in-memory CapLedgerService instance."""
    return CapLedgerService(db=None)


def test_double_entry_invariant_proof_of_balance(ledger_service):
    """
    Directive 1: Proof of balance invariant.
    Any transaction where sum(debits) + sum(credits) != 0 MUST be rejected.
    """
    # 1. Balanced transaction (sum == 0) succeeds
    balanced_entries = [
        (CapAccountType.ACTIVE_SALARY_LIABILITY, 5_000_000),
        (CapAccountType.CAP_ROOM, -5_000_000),
    ]
    tx = ledger_service.book_transaction(
        team_id=1,
        transaction_type=CapTransactionType.INITIAL_ALLOCATION,
        league_year=BASE_LEAGUE_YEAR,
        description="Test balanced entry",
        entries=balanced_entries,
    )
    assert tx.id is not None
    assert tx.net_cap_delta == -5_000_000

    # 2. Unbalanced transaction (sum != 0) must raise ValueError
    unbalanced_entries = [
        (CapAccountType.ACTIVE_SALARY_LIABILITY, 5_000_000),
        (CapAccountType.CAP_ROOM, -4_000_000),  # $1,000,000 leak!
    ]
    with pytest.raises(ValueError, match="Double-Entry Invariant Violation"):
        ledger_service.book_transaction(
            team_id=1,
            transaction_type=CapTransactionType.INITIAL_ALLOCATION,
            league_year=BASE_LEAGUE_YEAR,
            description="Out of balance leak",
            entries=unbalanced_entries,
        )


def test_contract_signing_transaction(ledger_service):
    """
    Directive 2: Contract Signing.
    $10M base salary + $25M signing bonus (5-year proration = $5M/yr).
    First year cap hit = $15M.
    """
    tx = ledger_service.record_contract_signing(
        team_id=1,
        player_id=101,
        annual_base_salary=10_000_000,
        signing_bonus_total=25_000_000,
        real_years=5,
        void_years=0,
        player_name="Patrick Mahomes",
    )

    assert tx.transaction_type == CapTransactionType.CONTRACT_SIGNING
    assert tx.net_cap_delta == -15_000_000

    stmt = ledger_service.get_team_statement(team_id=1, league_year=BASE_LEAGUE_YEAR)
    assert stmt.is_balanced is True
    assert stmt.proof_of_balance_delta == 0
    assert stmt.active_salary_liability == 10_000_000
    assert stmt.unamortized_bonus_pool == 5_000_000
    assert stmt.available_cap_room == BASE_SALARY_CAP - 15_000_000


def test_contract_restructure_kick_the_can(ledger_service):
    """
    Directive 3: Contract Restructure.
    Convert $10M base salary into signing bonus prorated over 5 years ($2M/year).
    Current year cap savings = $8M.
    """
    # Initial signing
    ledger_service.record_contract_signing(
        team_id=2,
        player_id=201,
        annual_base_salary=15_000_000,
        signing_bonus_total=0,
        real_years=5,
    )
    stmt_before = ledger_service.get_team_statement(team_id=2, league_year=BASE_LEAGUE_YEAR)
    room_before = stmt_before.available_cap_room

    # Restructure $10M of base salary
    tx_restructure = ledger_service.record_contract_restructure(
        team_id=2,
        player_id=201,
        amount_to_convert=10_000_000,
        remaining_years=5,
        player_name="Star Edge Rusher",
    )
    assert tx_restructure.net_cap_delta == 8_000_000  # Saved $8M!

    stmt_after = ledger_service.get_team_statement(team_id=2, league_year=BASE_LEAGUE_YEAR)
    assert stmt_after.is_balanced is True
    assert stmt_after.available_cap_room == room_before + 8_000_000
    assert stmt_after.active_salary_liability == 5_000_000  # $15M - $10M
    assert stmt_after.unamortized_bonus_pool == 2_000_000   # $10M / 5


def test_pre_june_1_release_immediate_acceleration(ledger_service):
    """
    Directive 4: Pre-June 1st Release.
    Accelerates all remaining unamortized signing bonus into current year dead money.
    """
    txs = ledger_service.record_player_release(
        team_id=3,
        player_id=301,
        base_salary_saved=6_000_000,
        unamortized_bonus_total=8_000_000,
        post_june_1=False,
    )
    assert len(txs) == 1
    tx = txs[0]
    assert tx.transaction_type == CapTransactionType.RELEASE_PRE_JUNE_1
    # Net cap impact: $8M dead - $6M saved base = -$2M cap room delta
    assert tx.net_cap_delta == -2_000_000

    stmt = ledger_service.get_team_statement(team_id=3, league_year=BASE_LEAGUE_YEAR)
    assert stmt.is_balanced is True
    assert stmt.dead_money_liability == 8_000_000


def test_post_june_1_release_two_year_split(ledger_service):
    """
    Directive 5: Post-June 1st Release 2-Year Dead Cap Split.
    Year 1: Absorbs only 1 year of proration ($2M), saving base ($6M) -> +$4M cap.
    Year 2: Absorbs remaining unamortized bonus ($6M) -> -$6M cap.
    """
    txs = ledger_service.record_player_release(
        team_id=4,
        player_id=401,
        base_salary_saved=6_000_000,
        unamortized_bonus_total=8_000_000,
        post_june_1=True,
        annual_proration=2_000_000,
        league_year=BASE_LEAGUE_YEAR,
    )
    assert len(txs) == 2

    # Year 1 Check
    tx_y1 = txs[0]
    assert tx_y1.league_year == BASE_LEAGUE_YEAR
    assert tx_y1.net_cap_delta == 4_000_000  # $6M saved - $2M dead = +$4M

    # Year 2 Check
    tx_y2 = txs[1]
    assert tx_y2.league_year == BASE_LEAGUE_YEAR + 1
    assert tx_y2.net_cap_delta == -6_000_000 # Remaining $6M hits next year

    # Validate Year 1 Statement
    stmt_y1 = ledger_service.get_team_statement(team_id=4, league_year=BASE_LEAGUE_YEAR)
    assert stmt_y1.is_balanced is True
    assert stmt_y1.dead_money_liability == 2_000_000

    # Validate Year 2 Statement
    stmt_y2 = ledger_service.get_team_statement(team_id=4, league_year=BASE_LEAGUE_YEAR + 1)
    assert stmt_y2.is_balanced is True
    assert stmt_y2.dead_money_liability == 6_000_000


def test_dry_run_simulation_isolation(ledger_service):
    """
    Directive 6: Dry-Run Simulation Isolation.
    Must verify proof of balance without committing state to accounts.
    """
    req = LedgerSimulateRequest(
        team_id=5,
        transaction_type=CapTransactionType.CONTRACT_SIGNING,
        annual_base_salary=12_000_000,
        signing_bonus_total=20_000_000,
        real_years=4,
        void_years=1,
    )
    res = ledger_service.simulate_proposal_isolated(req)
    assert res.is_compliant is True
    assert res.is_balanced is True
    assert res.proof_of_balance_delta == 0
    # Annual proration = $20M / 5 = $4M. Cap hit = $12M + $4M = $16M
    assert res.net_cap_delta == -16_000_000
    assert res.projected_cap_room == BASE_SALARY_CAP - 16_000_000

    # Ensure real account balance is completely untouched
    stmt = ledger_service.get_team_statement(team_id=5, league_year=BASE_LEAGUE_YEAR)
    assert stmt.available_cap_room == BASE_SALARY_CAP
    assert len(stmt.transactions) == 0


def test_insufficient_cap_rejection(ledger_service):
    """
    Directive 7: Cap Room Invariant Rejection.
    Attempting to sign a contract larger than available cap space MUST raise ValueError.
    """
    with pytest.raises(ValueError, match="Cap Invariant Rejection"):
        ledger_service.record_contract_signing(
            team_id=6,
            player_id=601,
            annual_base_salary=300_000_000,  # Far exceeds $255.4M cap!
            signing_bonus_total=0,
            real_years=1,
        )


def test_ledger_booking_latency_budget(ledger_service):
    """
    Directive 8: Operational Latency Budget.
    100 consecutive double-entry transactions MUST average < 1.0ms.
    """
    start_time = time.perf_counter()
    num_iterations = 100

    for i in range(num_iterations):
        entries = [
            (CapAccountType.ACTIVE_SALARY_LIABILITY, 100_000),
            (CapAccountType.CAP_ROOM, -100_000),
        ]
        ledger_service.book_transaction(
            team_id=7,
            transaction_type=CapTransactionType.INITIAL_ALLOCATION,
            league_year=BASE_LEAGUE_YEAR,
            description=f"Performance tick #{i}",
            entries=entries,
        )

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    avg_latency = elapsed_ms / num_iterations

    print(f"\nCap Ledger Latency Benchmark: {avg_latency:.4f}ms per transaction (Budget: <1.000ms)")
    assert avg_latency < 1.0, f"Latency {avg_latency:.4f}ms exceeded 1.0ms budget ceiling"
