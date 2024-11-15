"""remove optional in netcdf dataset name

Revision ID: 9f2dedc5396e
Revises: e3296ad62c68
Create Date: 2024-05-13 10:39:39.838577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9f2dedc5396e'
down_revision: Union[str, None] = 'e3296ad62c68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('coverageconfiguration', 'netcdf_main_dataset_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('coverageconfiguration', 'netcdf_main_dataset_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
