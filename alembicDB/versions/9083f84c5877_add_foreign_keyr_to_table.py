"""add foreign_key to table

Revision ID: 9083f84c5877
Revises: 38bfe91d0c5c
Create Date: 2022-12-03 05:57:17.949029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9083f84c5877'
down_revision = '38bfe91d0c5c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
