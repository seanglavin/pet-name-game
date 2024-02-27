"""add realtionship

Revision ID: e7b7bb63e12f
Revises: cbd7177e994d
Create Date: 2024-02-27 01:26:24.856796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e7b7bb63e12f'
down_revision: Union[str, None] = 'cbd7177e994d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game_boards', sa.Column('answer', sa.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game_boards', 'answer')
    # ### end Alembic commands ###