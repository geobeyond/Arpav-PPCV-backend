"""add tables for seasonal and yearly measurements

Revision ID: 7a6e61611951
Revises: b02523194bd6
Create Date: 2024-05-10 09:22:39.732156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7a6e61611951'
down_revision: Union[str, None] = 'b02523194bd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seasonalmeasurement',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('station_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('variable_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('season', sa.Enum('WINTER', 'SPRING', 'SUMMER', 'AUTUMN', name='season'), nullable=False),
    sa.ForeignKeyConstraint(['station_id'], ['station.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['variable_id'], ['variable.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('yearlymeasurement',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('station_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('variable_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['station_id'], ['station.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['variable_id'], ['variable.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('yearlymeasurement')
    op.drop_table('seasonalmeasurement')
    # ### end Alembic commands ###
