"""new

Revision ID: b6d0aa245c60
Revises: b13b1e6ff73b
Create Date: 2024-10-10 23:04:01.806949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6d0aa245c60'
down_revision: Union[str, None] = 'b13b1e6ff73b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
