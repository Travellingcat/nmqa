"""empty message

Revision ID: 0cd476b5a6f3
Revises: 277bacdd977a
Create Date: 2021-12-02 11:03:24.121625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cd476b5a6f3'
down_revision = '277bacdd977a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'create_time')
    # ### end Alembic commands ###
