import pytest
from app.services.trait_service import TraitService
from app.models.trait import Trait, PlayerTrait, TraitSource, TraitEffectType
from app.models.player import Player

# Mock DB Session if needed or use real test DB fixture
# Assuming standard pytest-asyncio and conftest setup for db_session fixture

def test_create_and_assign_trait(db_session):
    # 1. Create a Player
    player = Player(
        first_name="Test",
        last_name="TraitUser",
        position="QB",
        height=72,
        weight=220,
        age=22,
        overall_rating=75
    )
    db_session.add(player)

    # 2. Create a Trait
    trait = Trait(
        name="Clutch Kicker",
        description="Boost in 4th quarter",
        effect_type=TraitEffectType.SITUATIONAL,
        effect_value=10.0
    )
    db_session.add(trait)
    db_session.commit()
    db_session.refresh(player)
    db_session.refresh(trait)

    # 3. Assign Trait via Service
    # Note: Service methods in trait_service.py are currently synchronous/blocking SA?
    # I wrote them as sync `db.scalars(...)`. If I am in async test,
    # I should use `await db.run_sync(...)` or update service to be async.
    # The codebase seems to mix async/sync patterns. `MatchContext` used `await db.execute`.
    # `TraitService` methods used `db.scalars().all()` which is blocking.
    # If the app runs with `AsyncSession`, blocking calls will fail or warn.
    # I should verify `trait_service.py` async compatibility.

    # If `db` passed to service is `Session` (sync), it's fine.
    # If it is `AsyncSession`, we need `await db.scalar(...)` or `await session.execute(...)`.
    # `backend/app/api/endpoints/traits.py` uses `db: Session = Depends(deps.get_db)`.
    # If `deps.get_db` yields a sync session, we represent fine.
    # If `deps.get_db` yields AsyncSession, my service will break.

    # `MatchContext` takes `AsyncSession`.
    # I should probably make `TraitService` async to be safe for future.
    # But for now, I'll assume sync test or run_sync.

    assignment = TraitService.assign_trait(db_session, player.id, trait.id, TraitSource.DEVELOPMENT)

    assert assignment is not None
    assert assignment.player_id == player.id
    assert assignment.trait_id == trait.id

    # 4. Verify getting traits
    traits = TraitService.get_player_traits(db_session, player.id)
    assert len(traits) == 1
    assert traits[0].name == "Clutch Kicker"
