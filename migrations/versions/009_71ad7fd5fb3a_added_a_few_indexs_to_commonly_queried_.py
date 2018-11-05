"""Added a few indexs to commonly queried tables

Revision ID: 71ad7fd5fb3a
Revises: 5967a351c5f3
Create Date: 2018-11-05 15:37:32.047042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71ad7fd5fb3a'
down_revision = '5967a351c5f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('competition_event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_competition_event_competition_id'), ['competition_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_competition_event_event_id'), ['event_id'], unique=False)

    with op.batch_alter_table('user_event_results', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_event_results_comp_event_id'), ['comp_event_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_event_results', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_event_results_comp_event_id'))

    with op.batch_alter_table('competition_event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_competition_event_event_id'))
        batch_op.drop_index(batch_op.f('ix_competition_event_competition_id'))

    # ### end Alembic commands ###