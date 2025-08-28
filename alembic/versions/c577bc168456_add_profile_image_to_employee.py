"""add profile_image to employee

Revision ID: c577bc168456
Revises: 9f5e28f15dc4
Create Date: 2025-08-28 22:57:07.490148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c577bc168456'
down_revision: Union[str, Sequence[str], None] = '9f5e28f15dc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('employee', sa.Column('profile_image', sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('employee', 'profile_image')
