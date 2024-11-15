"""added-municipality-centroid-coords

Revision ID: 2c0e4144c2ec
Revises: d445c73f5aef
Create Date: 2024-08-20 18:09:27.462147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '2c0e4144c2ec'
down_revision: Union[str, None] = 'd445c73f5aef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('municipality', sa.Column('centroid_epsg_4326_lon', sa.Float(), nullable=True))
    op.add_column('municipality', sa.Column('centroid_epsg_4326_lat', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('municipality', 'centroid_epsg_4326_lat')
    op.drop_column('municipality', 'centroid_epsg_4326_lon')
    # ### end Alembic commands ###
