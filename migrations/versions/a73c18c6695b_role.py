"""'Role'

Revision ID: a73c18c6695b
Revises: 1c42ba00cb4c
Create Date: 2020-05-27 02:17:23.602986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a73c18c6695b'
down_revision = '1c42ba00cb4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_index('ix_test_cloth', table_name='test')
    op.drop_index('ix_test_size', table_name='test')
    op.drop_index('ix_test_type', table_name='test')
    op.drop_table('test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('img_code', sa.VARCHAR(length=140), nullable=True),
    sa.Column('size', sa.VARCHAR(length=120), nullable=True),
    sa.Column('cloth', sa.VARCHAR(length=50), nullable=True),
    sa.Column('sex', sa.VARCHAR(length=10), nullable=True),
    sa.Column('type', sa.VARCHAR(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_test_type', 'test', ['type'], unique=False)
    op.create_index('ix_test_size', 'test', ['size'], unique=False)
    op.create_index('ix_test_cloth', 'test', ['cloth'], unique=False)
    op.drop_table('role_users')
    op.drop_table('role')
    # ### end Alembic commands ###
