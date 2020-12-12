"""empty message

Revision ID: 856ea492118d
Revises: b28cb548cb58
Create Date: 2020-12-12 19:07:30.999683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '856ea492118d'
down_revision = 'b28cb548cb58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders_meals', sa.Column('meal_num', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders_meals', 'meal_num')
    # ### end Alembic commands ###
