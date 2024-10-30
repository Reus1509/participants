"""Add distance to User

Revision ID: e6ffea1b174c
Revises: c6b23cd26d3a
Create Date: 2024-10-30 16:55:29.473704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6ffea1b174c'
down_revision: Union[str, None] = 'c6b23cd26d3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('distance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'distance')
    # ### end Alembic commands ###