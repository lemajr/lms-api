"""message describing the change

Revision ID: 3a5a70a9399f
Revises: 080863fe0df1
Create Date: 2024-10-30 08:29:35.811561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a5a70a9399f'
down_revision: Union[str, None] = '080863fe0df1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
