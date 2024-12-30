"""update_review_table

Revision ID: 5c92eba3e206
Revises: 66e252e32b21
Create Date: 2024-12-30 16:16:03.926952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c92eba3e206'
down_revision: Union[str, None] = '66e252e32b21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('reviews_dish_id_fkey', 'reviews', type_='foreignkey')
    op.create_foreign_key(None, 'reviews', 'dishes', ['dish_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_foreign_key('reviews_dish_id_fkey', 'reviews', 'dishes', ['dish_id'], ['id'])
    # ### end Alembic commands ###
