"""Make email in Patient not nullable

Revision ID: 15a2ba60f164
Revises: c546104b0530
Create Date: 2025-07-22 20:07:39.155465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15a2ba60f164'
down_revision: Union[str, None] = 'c546104b0530'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('patient', 'email', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    pass
