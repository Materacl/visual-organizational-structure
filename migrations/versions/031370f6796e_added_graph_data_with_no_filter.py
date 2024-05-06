"""added graph data with no filter

Revision ID: 031370f6796e
Revises: 6eb59e118aed
Create Date: 2024-05-06 22:43:08.310069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '031370f6796e'
down_revision = '6eb59e118aed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dashboard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('graph_no_filter_data', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dashboard', schema=None) as batch_op:
        batch_op.drop_column('graph_no_filter_data')

    # ### end Alembic commands ###
