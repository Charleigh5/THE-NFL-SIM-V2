from typing import Type, TypeVar, Any, List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

T = TypeVar("T")

def get_object_or_404(db: Session, model: Type[T], object_id: Any, detail: str = None) -> T:
    """
    Get a record by ID or raise 404.
    """
    stmt = select(model).where(model.id == object_id)
    obj = db.execute(stmt).scalar_one_or_none()
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail=detail or f"{model.__name__} not found"
        )
    return obj


async def get_object_or_404_async(db: AsyncSession, model: Type[T], object_id: Any, detail: str = None) -> T:
    """
    Get a record by ID or raise 404 (Async).
    """
    stmt = select(model).where(model.id == object_id)
    result = await db.execute(stmt)
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail=detail or f"{model.__name__} not found"
        )
    return obj

def get_paginated_results(
    db: Session,
    stmt: Any,
    page: int,
    page_size: int
) -> Tuple[List[Any], int]:
    """
    Execute a select statement with pagination.
    Returns (items, total_count).

    Note: This executes two queries (count and data).
    """
    # Create count query from the original statement
    # We need to be careful with complex queries, but for simple selects this works
    # A safer way for complex queries might be needed, but for now:

    # This is a simplified approach. For complex queries with joins/groups,
    # we might need to pass a separate count_stmt or use subquery.
    # For now, let's assume the caller might pass the base query or we construct it.

    # Actually, to be generic and safe with SQLAlchemy 2.0:
    # It's often better to let the caller handle the query construction
    # and just handle the execution of pagination.

    # But to make it really helpful, let's try to count.
    # Using subquery for count is generally safe.

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar() or 0

    paginated_stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    items = db.execute(paginated_stmt).scalars().all()

    return list(items), total


async def get_paginated_results_async(
    db: AsyncSession,
    stmt: Any,
    page: int,
    page_size: int
) -> Tuple[List[Any], int]:
    """
    Execute a select statement with pagination (Async).
    Returns (items, total_count).
    """
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    paginated_stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    items_result = await db.execute(paginated_stmt)
    items = items_result.scalars().all()

    return list(items), total

def get_all_paginated(
    db: Session,
    model: Type[T],
    page: int,
    page_size: int,
    order_by: Any = None
) -> Tuple[List[T], int]:
    """
    Simple helper for "get all" on a model with pagination.
    """
    stmt = select(model)
    if order_by is not None:
        stmt = stmt.order_by(order_by)

    return get_paginated_results(db, stmt, page, page_size)


async def get_all_paginated_async(
    db: AsyncSession,
    model: Type[T],
    page: int,
    page_size: int,
    order_by: Any = None
) -> Tuple[List[T], int]:
    """
    Simple helper for "get all" on a model with pagination (Async).
    """
    stmt = select(model)
    if order_by is not None:
        stmt = stmt.order_by(order_by)

    return await get_paginated_results_async(db, stmt, page, page_size)
