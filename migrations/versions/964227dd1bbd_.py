"""empty message

Revision ID: 964227dd1bbd
Revises: bbc525d6d902
Create Date: 2024-07-08 13:14:22.703914

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '964227dd1bbd'
down_revision = 'bbc525d6d902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('Name', sa.String(length=80), nullable=False),
                    sa.Column('Password', sa.String(length=80), nullable=False),
                    sa.Column('Email', sa.String(length=80), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('Email')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Users')
    # ### end Alembic commands ###
