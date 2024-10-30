"""message describing the change

Revision ID: 080863fe0df1
Revises: 322b2cebc281
Create Date: 2024-10-30 08:25:38.858541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '080863fe0df1'
down_revision: Union[str, None] = '322b2cebc281'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
