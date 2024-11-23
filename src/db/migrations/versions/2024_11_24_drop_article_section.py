"""drop article section

Revision ID: e22ff06edc29
Revises: 60a91384626e
Create Date: 2024-11-24 00:07:25.084035

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e22ff06edc29"
down_revision: Union[str, None] = "60a91384626e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("article", sa.Column("section_id", sa.UUID(), nullable=False))
    op.create_foreign_key(
        None, "article", "section", ["section_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("article", "section")
    op.add_column("section", sa.Column("parent_section_id", sa.UUID(), nullable=True))
    op.drop_column("section", "created_at")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "section",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("section", "parent_section_id")
    op.add_column(
        "article",
        sa.Column("section", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "article", type_="foreignkey")
    op.drop_column("article", "section_id")
    # ### end Alembic commands ###