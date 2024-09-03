"""added related time series cov conf

Revision ID: 2e38a7decfc3
Revises: 2c0e4144c2ec
Create Date: 2024-09-03 15:40:22.499783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '2e38a7decfc3'
down_revision: Union[str, None] = '2c0e4144c2ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coverageconfiguration', sa.Column('related_time_series_coverage_configuration_id', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'coverageconfiguration', 'coverageconfiguration', ['related_time_series_coverage_configuration_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'coverageconfiguration', type_='foreignkey')
    op.drop_column('coverageconfiguration', 'related_time_series_coverage_configuration_id')
    # ### end Alembic commands ###
