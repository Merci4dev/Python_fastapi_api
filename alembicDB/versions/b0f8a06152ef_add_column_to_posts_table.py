"""add column to posts table

Revision ID: b0f8a06152ef
Revises: ca3ff50ffd3c
Create Date: 2022-12-03 05:48:00.686729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0f8a06152ef'
down_revision = 'ca3ff50ffd3c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
