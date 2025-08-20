"""add birth_date, address, phone_number to employee"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "15c151897573"
down_revision = "c28159fdfb37"   # ← لازم تحط هون ID المايغريشن السابق عندك
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("employee", sa.Column("birth_date", sa.Date(), nullable=True))
    op.add_column("employee", sa.Column("address", sa.String(length=255), nullable=True))
    op.add_column("employee", sa.Column("phone_number", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("employee", "phone_number")
    op.drop_column("employee", "address")
    op.drop_column("employee", "birth_date")
