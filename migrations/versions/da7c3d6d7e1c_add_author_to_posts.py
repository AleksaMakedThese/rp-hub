"""Add author to posts

Revision ID: da7c3d6d7e1c
Revises: 3c33bd005cbb
Create Date: 2026-07-15 09:53:36.510564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da7c3d6d7e1c'
down_revision = '3c33bd005cbb'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "posts",
        schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_posts_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )


def downgrade():
    with op.batch_alter_table(
        "posts",
        schema=None
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_posts_user_id_users",
            type_="foreignkey"
        )

        batch_op.drop_column("user_id")
