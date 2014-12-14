"""basic schema

Revision ID: 176bef6a90a3
Revises: 353dff346d3
Create Date: 2014-12-14 14:49:32.149387

"""

# revision identifiers, used by Alembic.
revision = '176bef6a90a3'
down_revision = '353dff346d3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.Unicode(), nullable=False),
        sa.Column('display_name', sa.Unicode(), nullable=True),
        sa.Column('password_hash', sa.Unicode(), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False),
        sa.Column('is_editor', sa.Boolean(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Unicode(), nullable=False),
        sa.Column('category', sa.Enum('Person', 'Company', 'Organization', 'Article'), nullable=False),
        sa.Column('text', sa.Unicode(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spider_tag',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('spider', sa.Unicode(), nullable=True),
        sa.Column('card_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reference',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('citation', sa.Unicode(), nullable=False),
        sa.Column('url', sa.Unicode(), nullable=False),
        sa.Column('source', sa.Unicode(), nullable=True),
        sa.Column('source_url', sa.Unicode(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('card_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('alias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(), nullable=True),
        sa.Column('card_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('link',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('offset', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected'), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('child_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['child_id'], ['card.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['card.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('link')
    op.drop_table('alias')
    op.drop_table('reference')
    op.drop_table('spider_tag')
    op.drop_table('card')
    op.drop_table('user')
