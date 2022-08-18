"""empty message

Revision ID: 73f693ccbe0a
Revises: 9b1e2863fdb4
Create Date: 2022-04-08 10:32:17.518190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "73f693ccbe0a"
down_revision = "9b1e2863fdb4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('ix_users_email', table_name='users')
    # op.drop_index('ix_users_username', table_name='users')
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_unique_constraint("pain", ["email"])
        batch_op.create_unique_constraint("usernameunconst", ["username"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
    op.create_index("ix_users_username", "users", ["username"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    # ### end Alembic commands ###
