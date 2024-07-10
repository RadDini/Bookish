"""empty message

Revision ID: dd6b7d62f309
Revises: 075e5edce945
Create Date: 2024-07-09 11:21:26.623188

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dd6b7d62f309'
down_revision = '075e5edce945'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'is_admin')
    # ### end Alembic commands ###
