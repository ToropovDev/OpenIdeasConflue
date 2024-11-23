"""create first tables

Revision ID: 2f2cc0b47a3b
Revises: 
Create Date: 2024-11-23 21:35:34.628794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f2cc0b47a3b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('text', sa.String(), server_default='', nullable=False),
    sa.Column('section', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=True),
    sa.Column('watching_count', sa.Integer(), server_default='0', nullable=False),
    sa.Column('is_draft', sa.Boolean(), server_default='true', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('text', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('file',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('s3_link', sa.String(length=512), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    op.drop_table('comment')
    op.drop_table('article')
    # ### end Alembic commands ###