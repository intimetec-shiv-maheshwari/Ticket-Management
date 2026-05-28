from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.tickets import (
    create_ticket,
    delete_ticket,
    get_all_tickets as repo_get_all_tickets,
    get_organization_by_id,
    get_ticket_by_id as repo_get_ticket_by_id,
    get_ticket_by_id_for_update,
    get_tickets_by_organization_id,
    get_tickets_by_user_id,
    get_user_by_id,
    update_ticket,
)
from src.dtos.tickets import TicketCreateDTO
from src.models.tickets import Ticket
from src.utils.constants import (
    ORGANIZATION_NOT_FOUND,
    TICKET_NOT_FOUND,
    TICKETS_NOT_FOUND_FOR_ORGANIZATION,
    TICKETS_NOT_FOUND_FOR_USER,
    USER_NOT_FOUND,
)
from src.utils.helpers import utc_now
from src.utils.ticket_lookups import resolve_priority_id, resolve_status_id


def _validate_ticket_references(
    user_id: str,
    organization_id: str,
    db: Session,
    assigned_to_id: str | None = None,
) -> None:
    if get_user_by_id(user_id, db) is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    if get_organization_by_id(organization_id, db) is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND)
    if assigned_to_id is not None and get_user_by_id(assigned_to_id, db) is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)


def _ticket_fields_from_dto(ticket: TicketCreateDTO, db: Session) -> dict:
    data = ticket.model_dump()
    data.pop("status")
    data.pop("priority")
    data["status_id"] = resolve_status_id(ticket.status, db)
    data["priority_id"] = resolve_priority_id(ticket.priority, db)
    return data


def get_all_tickets(db: Session):
    return repo_get_all_tickets(db)


def add_ticket(ticket: TicketCreateDTO, db: Session):
    _validate_ticket_references(
        ticket.user_id,
        ticket.organization_id,
        db,
        ticket.assigned_to_id,
    )
    now = utc_now()
    new_ticket = Ticket(
        **_ticket_fields_from_dto(ticket, db),
        created_at=now,
        updated_at=now,
    )
    return create_ticket(new_ticket, db)


def get_ticket_by_id(ticket_id: str, db: Session):
    ticket = repo_get_ticket_by_id(ticket_id, db)
    if ticket is None:
        raise HTTPException(status_code=404, detail=TICKET_NOT_FOUND)
    return ticket


def delete_ticket_by_id(ticket_id: str, db: Session):
    ticket = get_ticket_by_id_for_update(ticket_id, db)
    if ticket is None:
        raise HTTPException(status_code=404, detail=TICKET_NOT_FOUND)
    return delete_ticket(ticket, db)


def update_ticket_by_id(ticket_id: str, ticket: TicketCreateDTO, db: Session):
    existing_ticket = get_ticket_by_id_for_update(ticket_id, db)
    if existing_ticket is None:
        raise HTTPException(status_code=404, detail=TICKET_NOT_FOUND)
    _validate_ticket_references(
        ticket.user_id,
        ticket.organization_id,
        db,
        ticket.assigned_to_id,
    )
    fields = _ticket_fields_from_dto(ticket, db)
    existing_ticket.user_id = fields["user_id"]
    existing_ticket.subject = fields["subject"]
    existing_ticket.description = fields["description"]
    existing_ticket.organization_id = fields["organization_id"]
    existing_ticket.status_id = fields["status_id"]
    existing_ticket.priority_id = fields["priority_id"]
    existing_ticket.assigned_to_id = fields["assigned_to_id"]
    existing_ticket.category = fields["category"]
    existing_ticket.updated_at = utc_now()
    return update_ticket(existing_ticket, db)


def get_organization_tickets_by_organization_id(organization_id: str, db: Session):
    tickets = get_tickets_by_organization_id(organization_id, db)
    if not tickets:
        raise HTTPException(status_code=404, detail=TICKETS_NOT_FOUND_FOR_ORGANIZATION)
    return tickets


def get_user_tickets_by_user_id(user_id: str, db: Session):
    tickets = get_tickets_by_user_id(user_id, db)
    if not tickets:
        raise HTTPException(status_code=404, detail=TICKETS_NOT_FOUND_FOR_USER)
    return tickets
