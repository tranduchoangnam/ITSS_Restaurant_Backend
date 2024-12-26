"""update_dish_table

Revision ID: 01ec83e7071f
Revises: adddddf7056e
Create Date: 2024-12-26 18:35:30.688347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01ec83e7071f'
down_revision: Union[str, None] = 'adddddf7056e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dishes', sa.Column('restaurant_name', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dishes', 'restaurant_name')
    # ### end Alembic commands ###
