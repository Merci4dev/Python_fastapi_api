"""create posts table

Revision ID: ca3ff50ffd3c
Revises: 
Create Date: 2022-12-03 05:31:46.627383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca3ff50ffd3c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,  primary_key=True), sa.Column('title', sa.String(), nullable=False))
    
    pass


def downgrade():
    op.drop_table('posts')
    pass
