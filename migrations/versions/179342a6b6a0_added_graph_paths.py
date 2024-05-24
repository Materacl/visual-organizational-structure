"""added graph paths

Revision ID: 179342a6b6a0
Revises: 62e8918d56dd
Create Date: 2024-05-11 12:40:48.474748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '179342a6b6a0'
down_revision = '62e8918d56dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dashboard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('graph_paths', sa.Text(), nullable=True))
        batch_op.drop_column('graph_no_filter_data')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dashboard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('graph_no_filter_data', sa.TEXT(), nullable=True))
        batch_op.drop_column('graph_paths')

    # ### end Alembic commands ###
