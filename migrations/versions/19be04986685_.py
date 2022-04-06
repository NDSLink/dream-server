"""The Poke Flattening

Revision ID: 19be04986685
Revises: a24ed513d3b0
Create Date: 2022-04-06 13:06:41.937710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19be04986685'
down_revision = None
branch_labels = None
depends_on = None

# Mass merge of every past migration
def upgrade():
    op.create_table(
        "gsuser",
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pokemon",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("dexno", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("exp", sa.Integer(), nullable=True),
        sa.Column("iv_hp", sa.Integer(), nullable=True),
        sa.Column("iv_atk", sa.Integer(), nullable=True),
        sa.Column("iv_def", sa.Integer(), nullable=True),
        sa.Column("iv_spatk", sa.Integer(), nullable=True),
        sa.Column("iv_spdef", sa.Integer(), nullable=True),
        sa.Column("iv_speed", sa.Integer(), nullable=True),
        sa.Column("ev_hp", sa.Integer(), nullable=True),
        sa.Column("ev_atk", sa.Integer(), nullable=True),
        sa.Column("ev_def", sa.Integer(), nullable=True),
        sa.Column("ev_spatk", sa.Integer(), nullable=True),
        sa.Column("ev_spdef", sa.Integer(), nullable=True),
        sa.Column("ev_speed", sa.Integer(), nullable=True),
        sa.Column("nature", sa.String(), nullable=True),
        sa.Column("ability", sa.String(), nullable=True),
        sa.Column("item", sa.String(), nullable=True),
        sa.Column("move1", sa.String(), nullable=True),
        sa.Column("move2", sa.String(), nullable=True),
        sa.Column("move3", sa.String(), nullable=True),
        sa.Column("move4", sa.String(), nullable=True),
        sa.Column("gsuser_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["gsuser_id"],
            ["gsuser.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("gsuser", sa.Column("name", sa.String(length=7), nullable=True))
    op.add_column("gsuser", sa.Column("poke_is_sleeping", sa.Boolean(), nullable=True))
    op.add_column("gsuser", sa.Column("tid", sa.Integer(), nullable=True))
    op.add_column('gsuser', sa.Column('gender', sa.Integer(), nullable=True))
    op.add_column('gsuser', sa.Column('gamever', sa.Integer(), nullable=True))
    op.add_column('gsuser', sa.Column('gsid', sa.INTEGER(), nullable=True))


def downgrade():
    op.drop_table("pokemon")
    op.drop_table("gsuser")
    op.drop_constraint(None, "gsuser", type_="unique")
    op.drop_column("gsuser", "tid")
    op.drop_column("gsuser", "poke_is_sleeping")
    op.drop_column("gsuser", "name")
    op.drop_column("gsuser", "gsid")
    op.drop_constraint(None, 'gsuser', type_='unique')
    op.drop_column('gsuser', 'gamever')
    op.drop_column('gsuser', 'gender')
