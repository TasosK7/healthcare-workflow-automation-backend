"""Make staff_id in Lab Test not nullable

Revision ID: ea1925676a28
Revises: 804f02bc5a7e
Create Date: 2025-07-23 12:49:23.891735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea1925676a28'
down_revision: Union[str, None] = '804f02bc5a7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('labtest', 'staff_id', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    pass
