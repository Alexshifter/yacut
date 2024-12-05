"""empty message.
Revision ID: 3257c36a79b7
Revises:
Create Date: 2024-12-05 15:44:11.918832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3257c36a79b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(length=128), nullable=False),
    sa.Column('short', sa.String(length=128), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_url_map_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_url_map_timestamp'))

    op.drop_table('url_map')
    # ### end Alembic commands ###