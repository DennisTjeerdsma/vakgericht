"""update

Revision ID: 90c6f5db808f
Revises: a3cdeeda5d51
Create Date: 2018-08-16 11:53:03.033748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90c6f5db808f'
down_revision = 'a3cdeeda5d51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('location', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'location')
    # ### end Alembic commands ###