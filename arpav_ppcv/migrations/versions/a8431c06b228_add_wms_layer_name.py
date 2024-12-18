"""add-wms-layer-name

Revision ID: a8431c06b228
Revises: 9b9809ef3088
Create Date: 2024-06-13 14:57:05.789250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a8431c06b228'
down_revision: Union[str, None] = '9b9809ef3088'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coverageconfiguration', sa.Column('wms_main_layer_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coverageconfiguration', 'wms_main_layer_name')
    # ### end Alembic commands ###
