"""add ticket status and priority lookup tables

Revision ID: f8a2c1b90d3e
Revises: e46a988e8ad2
Create Date: 2026-05-25 19:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f8a2c1b90d3e"
down_revision: Union[str, Sequence[str], None] = "e46a988e8ad2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

STATUS_SEED = [
    {"id": 1, "label": "open"},
    {"id": 2, "label": "in_progress"},
    {"id": 3, "label": "resolved"},
    {"id": 4, "label": "closed"},
]

PRIORITY_SEED = [
    {"id": 1, "label": "low"},
    {"id": 2, "label": "medium"},
    {"id": 3, "label": "high"},
    {"id": 4, "label": "critical"},
]

STATUS_LABEL_TO_ID = {row["label"]: row["id"] for row in STATUS_SEED}
PRIORITY_LABEL_TO_ID = {row["label"]: row["id"] for row in PRIORITY_SEED}


def upgrade() -> None:
    op.create_table(
        "TicketStatus",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("label", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("label"),
    )
    op.create_index(op.f("ix_TicketStatus_label"), "TicketStatus", ["label"], unique=True)

    op.create_table(
        "TicketPriority",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("label", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("label"),
    )
    op.create_index(op.f("ix_TicketPriority_label"), "TicketPriority", ["label"], unique=True)

    status_table = sa.table(
        "TicketStatus",
        sa.column("id", sa.Integer()),
        sa.column("label", sa.String()),
    )
    priority_table = sa.table(
        "TicketPriority",
        sa.column("id", sa.Integer()),
        sa.column("label", sa.String()),
    )
    op.bulk_insert(status_table, STATUS_SEED)
    op.bulk_insert(priority_table, PRIORITY_SEED)

    op.add_column("Ticket", sa.Column("status_id", sa.Integer(), nullable=True))
    op.add_column("Ticket", sa.Column("priority_id", sa.Integer(), nullable=True))

    connection = op.get_bind()
    tickets = connection.execute(
        sa.text('SELECT id, status, priority FROM "Ticket"')
    ).fetchall()
    for ticket_id, status, priority in tickets:
        connection.execute(
            sa.text(
                'UPDATE "Ticket" SET status_id = :status_id, priority_id = :priority_id WHERE id = :id'
            ),
            {
                "id": ticket_id,
                "status_id": STATUS_LABEL_TO_ID.get(status, 1),
                "priority_id": PRIORITY_LABEL_TO_ID.get(priority, 2),
            },
        )

    op.alter_column("Ticket", "status_id", nullable=False)
    op.alter_column("Ticket", "priority_id", nullable=False)

    op.create_foreign_key(
        "fk_ticket_status_id",
        "Ticket",
        "TicketStatus",
        ["status_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_ticket_priority_id",
        "Ticket",
        "TicketPriority",
        ["priority_id"],
        ["id"],
    )
    op.create_index(op.f("ix_Ticket_status_id"), "Ticket", ["status_id"], unique=False)
    op.create_index(op.f("ix_Ticket_priority_id"), "Ticket", ["priority_id"], unique=False)

    op.drop_index(op.f("ix_Ticket_status"), table_name="Ticket")
    op.drop_index(op.f("ix_Ticket_priority"), table_name="Ticket")
    op.drop_column("Ticket", "status")
    op.drop_column("Ticket", "priority")


def downgrade() -> None:
    op.add_column("Ticket", sa.Column("status", sa.String(), nullable=True))
    op.add_column("Ticket", sa.Column("priority", sa.String(), nullable=True))

    id_to_status = {row["id"]: row["label"] for row in STATUS_SEED}
    id_to_priority = {row["id"]: row["label"] for row in PRIORITY_SEED}

    connection = op.get_bind()
    tickets = connection.execute(
        sa.text('SELECT id, status_id, priority_id FROM "Ticket"')
    ).fetchall()
    for ticket_id, status_id, priority_id in tickets:
        connection.execute(
            sa.text(
                'UPDATE "Ticket" SET status = :status, priority = :priority WHERE id = :id'
            ),
            {
                "id": ticket_id,
                "status": id_to_status.get(status_id, "open"),
                "priority": id_to_priority.get(priority_id, "medium"),
            },
        )

    op.alter_column("Ticket", "status", nullable=False)
    op.alter_column("Ticket", "priority", nullable=False)

    op.drop_constraint("fk_ticket_priority_id", "Ticket", type_="foreignkey")
    op.drop_constraint("fk_ticket_status_id", "Ticket", type_="foreignkey")
    op.drop_index(op.f("ix_Ticket_priority_id"), table_name="Ticket")
    op.drop_index(op.f("ix_Ticket_status_id"), table_name="Ticket")
    op.drop_column("Ticket", "priority_id")
    op.drop_column("Ticket", "status_id")

    op.create_index(op.f("ix_Ticket_priority"), "Ticket", ["priority"], unique=False)
    op.create_index(op.f("ix_Ticket_status"), "Ticket", ["status"], unique=False)

    op.drop_index(op.f("ix_TicketPriority_label"), table_name="TicketPriority")
    op.drop_table("TicketPriority")
    op.drop_index(op.f("ix_TicketStatus_label"), table_name="TicketStatus")
    op.drop_table("TicketStatus")
