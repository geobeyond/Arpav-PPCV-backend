"""add-related-cov-confs

Revision ID: 74ee5bc68b7e
Revises: e8bc68ec327b
Create Date: 2024-05-21 16:29:25.257549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '74ee5bc68b7e'
down_revision: Union[str, None] = 'e8bc68ec327b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('relatedcoverageconfiguration',
    sa.Column('main_coverage_configuration_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('secondary_coverage_configuration_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['main_coverage_configuration_id'], ['coverageconfiguration.id'], ),
    sa.ForeignKeyConstraint(['secondary_coverage_configuration_id'], ['coverageconfiguration.id'], ),
    sa.PrimaryKeyConstraint('main_coverage_configuration_id', 'secondary_coverage_configuration_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('relatedcoverageconfiguration')
    # ### end Alembic commands ###