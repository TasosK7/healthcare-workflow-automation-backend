"""Make email in Staff not nullable

Revision ID: 333090f891a6
Revises: a233052a27bd
Create Date: 2025-07-22 20:17:29.580027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '333090f891a6'
down_revision: Union[str, None] = 'a233052a27bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('staff', 'email', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    pass
