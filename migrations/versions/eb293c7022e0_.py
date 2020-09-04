"""empty message

Revision ID: eb293c7022e0
Revises: 1556e9f35fd6
Create Date: 2020-09-04 16:49:51.273058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb293c7022e0'
down_revision = '1556e9f35fd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoked_tokens')
    # ### end Alembic commands ###
