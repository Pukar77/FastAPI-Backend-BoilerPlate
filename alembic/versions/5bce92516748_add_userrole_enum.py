"""add userrole enum

Revision ID: 5bce92516748
Revises: 315326544c92
Create Date: 2026-07-15 20:10:04.630034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5bce92516748'
down_revision: Union[str, Sequence[str], None] = '315326544c92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE userrole AS ENUM ('user', 'admin', 'superadmin')")
    op.execute("UPDATE \"User\" SET role = 'user' WHERE role IS NULL")
    op.alter_column('User', 'role',
               existing_type=sa.VARCHAR(),
               type_=postgresql.ENUM('user', 'admin', 'superadmin', name='userrole', create_type=False),
               postgresql_using='role::userrole',
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('User', 'role',
               existing_type=postgresql.ENUM('user', 'admin', 'superadmin', name='userrole', create_type=False),
               type_=sa.VARCHAR(),
               nullable=True)
    op.execute("DROP TYPE userrole")
