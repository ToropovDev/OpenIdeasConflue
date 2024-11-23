"""empty message

Revision ID: 60a91384626e
Revises: b29078d6b2c3, 5bb304a6a8d3
Create Date: 2024-11-23 23:59:54.243284

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "60a91384626e"
down_revision: Union[str, None] = ("b29078d6b2c3", "5bb304a6a8d3")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
