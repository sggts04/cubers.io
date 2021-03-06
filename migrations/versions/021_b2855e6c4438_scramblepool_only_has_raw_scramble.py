"""ScramblePool only has raw scramble

Revision ID: b2855e6c4438
Revises: c92b137ff8be
Create Date: 2019-02-20 14:45:45.565155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2855e6c4438'
down_revision = 'c92b137ff8be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scramble_pool', schema=None) as batch_op:
        batch_op.add_column(sa.Column('scramble', sa.Text(), nullable=True))
        batch_op.drop_column('scramble_app')
        batch_op.drop_column('scramble_reddit')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scramble_pool', schema=None) as batch_op:
        batch_op.add_column(sa.Column('scramble_reddit', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('scramble_app', sa.TEXT(), nullable=True))
        batch_op.drop_column('scramble')

    # ### end Alembic commands ###
