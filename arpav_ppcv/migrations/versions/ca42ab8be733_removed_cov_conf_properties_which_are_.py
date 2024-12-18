"""removed cov conf properties which are now in climatic indicator

Revision ID: ca42ab8be733
Revises: 630cc1e4556d
Create Date: 2024-11-05 17:27:37.620072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ca42ab8be733'
down_revision: Union[str, None] = '630cc1e4556d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coverageconfiguration', 'display_name_english')
    op.drop_column('coverageconfiguration', 'display_name_italian')
    op.drop_column('coverageconfiguration', 'description_english')
    op.drop_column('coverageconfiguration', 'unit_italian')
    op.drop_column('coverageconfiguration', 'description_italian')
    op.drop_column('coverageconfiguration', 'color_scale_max')
    op.drop_column('coverageconfiguration', 'data_precision')
    op.drop_column('coverageconfiguration', 'color_scale_min')
    op.drop_column('coverageconfiguration', 'palette')
    op.drop_column('coverageconfiguration', 'unit_english')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coverageconfiguration', sa.Column('unit_english', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('coverageconfiguration', sa.Column('palette', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('coverageconfiguration', sa.Column('color_scale_min', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('coverageconfiguration', sa.Column('data_precision', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('coverageconfiguration', sa.Column('color_scale_max', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('coverageconfiguration', sa.Column('description_italian', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('coverageconfiguration', sa.Column('unit_italian', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('coverageconfiguration', sa.Column('description_english', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('coverageconfiguration', sa.Column('display_name_italian', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('coverageconfiguration', sa.Column('display_name_english', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###