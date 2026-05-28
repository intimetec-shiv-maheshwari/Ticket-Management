from fastapi import HTTPException;
from sqlalchemy.orm import Session, joinedload;

from src.dtos.tickets import TicketCreateDTO;
from src.models.organizations import Organization;
from src.models.tickets import Ticket;
from src.models.users import Users;
from src.utils.constants import (
    ORGANIZATION_NOT_FOUND,
    TICKET_NOT_FOUND,
    TICKETS_NOT_FOUND_FOR_ORGANIZATION,
    TICKETS_NOT_FOUND_FOR_USER,
    USER_NOT_FOUND,
);
from src.utils.helpers import utc_now;
from src.utils.ticket_lookups import resolve_priority_id, resolve_status_id;


def _ticket_query(db: Session):
    return db.query(Ticket).options(
        joinedload(Ticket.status_ref),
        joinedload(Ticket.priority_ref),
    );


def _validate_ticket_references(
    user_id: str,
    organization_id: str,
    db: Session,
    assigned_to_id: str | None = None,
) -> None:
    if db.query(Users).filter(Users.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND);
    if db.query(Organization).filter(Organization.id == organization_id).first() is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND);
    if assigned_to_id is not None and db.query(Users).filter(Users.id == assigned_to_id).first() is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND);


def _ticket_fields_from_dto(ticket: TicketCreateDTO, db: Session) -> dict:
    data = ticket.model_dump();
    data.pop("status");
    data.pop("priority");
    data["status_id"] = resolve_status_id(ticket.status, db);
    data["priority_id"] = resolve_priority_id(ticket.priority, db);
    return data;


def get_all_tickets(db: Session):
    return _ticket_query(db).all();


def add_ticket(ticket: TicketCreateDTO, db: Session):
    _validate_ticket_references(
        ticket.user_id,
        ticket.organization_id,
        db,
        ticket.assigned_to_id,
    );
    now = utc_now();
    new_ticket = Ticket(
        **_ticket_fields_from_dto(ticket, db),
        created_at=now,
        updated_at=now,
    );
    db.add(new_ticket);
    db.commit();
    db.refresh(new_ticket);
    return _ticket_query(db).filter(Ticket.id == new_ticket.id).one();


def get_ticket_by_id(ticket_id: str, db: Session):
    ticket = _ticket_query(db).filter(Ticket.id == ticket_id).first();
    if ticket is None:
        raise HTTPException(status_code=404, detail=TICKET_NOT_FOUND);
    return ticket;


def delete_ticket_by_id(ticket_id: str, db: Session):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first();
    if ticket is None:
        raise HTTPException(status_code=404, detail=TICKET_NOT_FOUND);
    db.delete(ticket);
    db.commit();
    return {"message": "Ticket deleted successfully"};


def update_ticket_by_id(ticket_id: str, ticket: TicketCreateDTO, db: Session):
    existing_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first();
    if existing_ticket is None:
        raise HTTPException(status_code=404, detail=TICKET_NOT_FOUND);
    _validate_ticket_references(
        ticket.user_id,
        ticket.organization_id,
        db,
        ticket.assigned_to_id,
    );
    fields = _ticket_fields_from_dto(ticket, db);
    existing_ticket.user_id = fields["user_id"];
    existing_ticket.subject = fields["subject"];
    existing_ticket.description = fields["description"];
    existing_ticket.organization_id = fields["organization_id"];
    existing_ticket.status_id = fields["status_id"];
    existing_ticket.priority_id = fields["priority_id"];
    existing_ticket.assigned_to_id = fields["assigned_to_id"];
    existing_ticket.category = fields["category"];
    existing_ticket.updated_at = utc_now();
    db.commit();
    return _ticket_query(db).filter(Ticket.id == ticket_id).one();


def get_organization_tickets_by_organization_id(organization_id: str, db: Session):
    tickets = _ticket_query(db).filter(Ticket.organization_id == organization_id).all();
    if not tickets:
        raise HTTPException(status_code=404, detail=TICKETS_NOT_FOUND_FOR_ORGANIZATION);
    return tickets;


def get_user_tickets_by_user_id(user_id: str, db: Session):
    tickets = _ticket_query(db).filter(Ticket.user_id == user_id).all();
    if not tickets:
        raise HTTPException(status_code=404, detail=TICKETS_NOT_FOUND_FOR_USER);
    return tickets;
