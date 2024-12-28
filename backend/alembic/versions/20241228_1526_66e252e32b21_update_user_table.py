"""update_user_table

Revision ID: 66e252e32b21
Revises: 01ec83e7071f
Create Date: 2024-12-28 15:26:53.106964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66e252e32b21'
down_revision: Union[str, None] = '01ec83e7071f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('loved_dish', sa.ARRAY(sa.String(length=255)), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'loved_dish')
    # ### end Alembic commands ###
