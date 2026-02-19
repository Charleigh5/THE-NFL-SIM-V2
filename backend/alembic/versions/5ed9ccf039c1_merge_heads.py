"""Merge heads

Revision ID: 5ed9ccf039c1
Revises: 5b2c3d4e5f6a, d68652484c61
Create Date: 2025-12-03 20:39:48.194325

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '5ed9ccf039c1'
down_revision: str | Sequence[str] | None = ('5b2c3d4e5f6a', 'd68652484c61')
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
