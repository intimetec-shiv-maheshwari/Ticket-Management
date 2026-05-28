from fastapi import APIRouter, Depends;

from ..controllers.tickets import (
    add_ticket,
    delete_ticket_by_id,
    get_all_tickets,
    get_organization_tickets_by_organization_id,
    get_ticket_by_id,
    get_user_tickets_by_user_id,
    update_ticket_by_id,
);
from ..dtos.tickets import TicketCreateDTO, TicketDTO;
from ..utils.db import get_db;

router = APIRouter(prefix="/tickets", tags=["Tickets"]);


@router.get("/", response_model=list[TicketDTO])
def get_tickets(db=Depends(get_db)):
    return get_all_tickets(db);


@router.get("/{ticket_id}", response_model=TicketDTO)
def ticket_by_id(ticket_id: str, db=Depends(get_db)):
    return get_ticket_by_id(ticket_id, db);


@router.post("/", response_model=TicketDTO)
def create_ticket(data: TicketCreateDTO, db=Depends(get_db)):
    return add_ticket(data, db);


@router.put("/{ticket_id}", response_model=TicketDTO)
def update_ticket(ticket_id: str, data: TicketCreateDTO, db=Depends(get_db)):
    return update_ticket_by_id(ticket_id, data, db);


@router.delete("/{ticket_id}", response_model=dict)
def delete_ticket(ticket_id: str, db=Depends(get_db)):
    return delete_ticket_by_id(ticket_id, db);

@router.get("/organization/{organization_id}", response_model=list[TicketDTO])
def get_organization_tickets(organization_id: str, db=Depends(get_db)):
    return get_organization_tickets_by_organization_id(organization_id, db);

@router.get("/user/{user_id}", response_model=list[TicketDTO])
def get_user_tickets(user_id: str, db=Depends(get_db)):
    return get_user_tickets_by_user_id(user_id, db);