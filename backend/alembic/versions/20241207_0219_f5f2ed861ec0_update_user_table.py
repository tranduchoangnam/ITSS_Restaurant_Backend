"""update_user_table

Revision ID: f5f2ed861ec0
Revises: 9c1ca82ebd8e
Create Date: 2024-12-07 02:19:15.035309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f5f2ed861ec0'
down_revision: Union[str, None] = '9c1ca82ebd8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('dark_mode', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('language', sa.String(length=10), nullable=True))
    op.add_column('users', sa.Column('font_size', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('notification', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('loved_flavor', sa.ARRAY(sa.String(length=255)), nullable=True))
    op.add_column('users', sa.Column('hated_flavor', sa.ARRAY(sa.String(length=255)), nullable=True))
    op.add_column('users', sa.Column('vegetarian', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('loved_distinct', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('loved_price', sa.Float(), nullable=True))
    op.drop_column('users', 'reset_password_token_expire_at')
    op.drop_column('users', 'reset_password_token')
    op.drop_column('users', 'new_email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('new_email', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('reset_password_token', sa.VARCHAR(length=2048), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('reset_password_token_expire_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('users', 'loved_price')
    op.drop_column('users', 'loved_distinct')
    op.drop_column('users', 'vegetarian')
    op.drop_column('users', 'hated_flavor')
    op.drop_column('users', 'loved_flavor')
    op.drop_column('users', 'notification')
    op.drop_column('users', 'font_size')
    op.drop_column('users', 'language')
    op.drop_column('users', 'dark_mode')
    # ### end Alembic commands ###
