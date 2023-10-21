"""empty message

Revision ID: a03332164c25
Revises: c062311c1c52
Create Date: 2023-10-19 15:55:28.406309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a03332164c25'
down_revision = 'c062311c1c52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gsuser', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=7),
               type_=sa.String(length=14),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gsuser', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=14),
               type_=sa.VARCHAR(length=7),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###