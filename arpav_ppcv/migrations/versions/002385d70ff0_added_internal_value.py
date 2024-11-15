"""added internal value

Revision ID: 002385d70ff0
Revises: 2c0e4144c2ec
Create Date: 2024-09-13 11:23:56.702504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '002385d70ff0'
down_revision: Union[str, None] = '2c0e4144c2ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configurationparametervalue', sa.Column('internal_value', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('configurationparametervalue', 'internal_value')
    # ### end Alembic commands ###
