"""baseline schema

Revision ID: 94fde2d87abd
Revises:
Create Date: 2026-05-22 14:47:08.961505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "94fde2d87abd"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def upgrade() -> None:
    if not _table_exists("Organization"):
        op.create_table(
            "Organization",
            sa.Column("id", sa.String(length=16), nullable=False),
            sa.Column("name", sa.String(), nullable=True),
            sa.Column("description", sa.String(), nullable=True),
            sa.Column("country", sa.String(), nullable=True),
            sa.Column("active", sa.Boolean(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_Organization_country"), "Organization", ["country"], unique=False)
        op.create_index(op.f("ix_Organization_name"), "Organization", ["name"], unique=False)

    if not _table_exists("Role"):
        op.create_table(
            "Role",
            sa.Column("id", sa.String(length=16), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("description", sa.String(), nullable=True),
            sa.Column("organization_id", sa.String(length=16), nullable=False),
            sa.Column("active", sa.Boolean(), nullable=True),
            sa.ForeignKeyConstraint(["organization_id"], ["Organization.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_Role_name"), "Role", ["name"], unique=False)

    if not _table_exists("User"):
        op.create_table(
            "User",
            sa.Column("id", sa.String(length=16), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("password", sa.String(), nullable=False),
            sa.Column("organization_id", sa.String(length=16), nullable=False),
            sa.Column("active", sa.Boolean(), nullable=True),
            sa.Column("role_id", sa.String(length=16), nullable=False),
            sa.ForeignKeyConstraint(["organization_id"], ["Organization.id"]),
            sa.ForeignKeyConstraint(["role_id"], ["Role.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_User_email"), "User", ["email"], unique=True)
        op.create_index(op.f("ix_User_name"), "User", ["name"], unique=False)
        op.create_index(op.f("ix_User_organization_id"), "User", ["organization_id"], unique=False)
        op.create_index(op.f("ix_User_role_id"), "User", ["role_id"], unique=False)

    # Legacy table from early create_all (plural name); app uses "Organization"
    if _table_exists("Organizations"):
        op.drop_index(op.f("ix_Organizations_country"), table_name="Organizations")
        op.drop_index(op.f("ix_Organizations_description"), table_name="Organizations")
        op.drop_index(op.f("ix_Organizations_name"), table_name="Organizations")
        op.drop_table("Organizations")

    if _table_exists("Role"):
        op.alter_column(
            "Role",
            "organization_id",
            existing_type=sa.String(length=16),
            nullable=False,
        )


def downgrade() -> None:
    if _table_exists("Role"):
        op.alter_column(
            "Role",
            "organization_id",
            existing_type=sa.String(length=16),
            nullable=True,
        )

    op.create_table(
        "Organizations",
        sa.Column("id", sa.String(length=16), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Organizations_name"), "Organizations", ["name"], unique=False)
    op.create_index(op.f("ix_Organizations_description"), "Organizations", ["description"], unique=False)
    op.create_index(op.f("ix_Organizations_country"), "Organizations", ["country"], unique=False)

    if _table_exists("User"):
        op.drop_index(op.f("ix_User_role_id"), table_name="User")
        op.drop_index(op.f("ix_User_organization_id"), table_name="User")
        op.drop_index(op.f("ix_User_name"), table_name="User")
        op.drop_index(op.f("ix_User_email"), table_name="User")
        op.drop_table("User")

    if _table_exists("Role"):
        op.drop_index(op.f("ix_Role_name"), table_name="Role")
        op.drop_table("Role")

    if _table_exists("Organization"):
        op.drop_index(op.f("ix_Organization_name"), table_name="Organization")
        op.drop_index(op.f("ix_Organization_country"), table_name="Organization")
        op.drop_table("Organization")
