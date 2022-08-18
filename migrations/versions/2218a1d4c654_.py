"""empty message

Revision ID: 2218a1d4c654
Revises: b43ee1cdb99b
Create Date: 2022-04-14 17:05:36.662443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2218a1d4c654"
down_revision = "b43ee1cdb99b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gsuser", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("selected_cgear_skin", sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column("selected_dex_skin", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("selected_musical", sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gsuser", schema=None) as batch_op:
        batch_op.drop_column("selected_musical")
        batch_op.drop_column("selected_dex_skin")
        batch_op.drop_column("selected_cgear_skin")

    # ### end Alembic commands ###
