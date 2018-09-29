"""study

Revision ID: 6275db0e089a
Revises: abb8603105d8
Create Date: 2018-09-29 17:33:53.571106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6275db0e089a'
down_revision = 'abb8603105d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('study', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'study')
    # ### end Alembic commands ###
