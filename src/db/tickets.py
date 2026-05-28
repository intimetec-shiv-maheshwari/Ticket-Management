from sqlalchemy.orm import Session, joinedload

from src.models.organizations import Organization
from src.models.tickets import Ticket
from src.models.users import Users


def query_tickets(db: Session):
    return db.query(Ticket).options(
        joinedload(Ticket.status_ref),
        joinedload(Ticket.priority_ref),
    )


def get_user_by_id(user_id: str, db: Session):
    return db.query(Users).filter(Users.id == user_id).first()


def get_organization_by_id(organization_id: str, db: Session):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def get_all_tickets(db: Session):
    return query_tickets(db).all()


def get_ticket_by_id(ticket_id: str, db: Session):
    return query_tickets(db).filter(Ticket.id == ticket_id).first()


def get_ticket_by_id_for_update(ticket_id: str, db: Session):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def create_ticket(ticket: Ticket, db: Session):
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return query_tickets(db).filter(Ticket.id == ticket.id).one()


def update_ticket(existing_ticket: Ticket, db: Session):
    db.commit()
    return query_tickets(db).filter(Ticket.id == existing_ticket.id).one()


def delete_ticket(ticket: Ticket, db: Session):
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket deleted successfully"}


def get_tickets_by_organization_id(organization_id: str, db: Session):
    return query_tickets(db).filter(Ticket.organization_id == organization_id).all()


def get_tickets_by_user_id(user_id: str, db: Session):
    return query_tickets(db).filter(Ticket.user_id == user_id).all()
