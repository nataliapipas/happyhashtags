"""empty message

Revision ID: 728a7bf5a488
Revises: 
Create Date: 2020-08-22 23:29:12.767335

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '728a7bf5a488'
down_revision = None
branch_labels = None
depends_on = None

table_name = 'hourly_counts'


def upgrade():
    op.create_table(
        table_name,
        sa.Column('hashtag', sa.String(), nullable=False, primary_key=True),
        sa.Column('hour', sa.DateTime(), nullable=False, primary_key=True),
        sa.Column('count', sa.Integer(), nullable=False, primary_key=False)
    )


def downgrade():
    op.drop_table(table_name)
