from fastapi import HTTPException;
from sqlalchemy.orm import Session;

from src.models.ticket_priority import TicketPriority;
from src.models.ticket_status import TicketStatus;
from src.utils.constants import INVALID_TICKET_PRIORITY, INVALID_TICKET_STATUS;

STATUS_LABEL_TO_ID = {
    "open": 1,
    "in_progress": 2,
    "resolved": 3,
    "closed": 4,
};

PRIORITY_LABEL_TO_ID = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
};


def resolve_status_id(label: str, db: Session) -> int:
    status_id = STATUS_LABEL_TO_ID.get(label);
    if status_id is not None:
        return status_id;
    row = db.query(TicketStatus).filter(TicketStatus.label == label).first();
    if row is None:
        raise HTTPException(status_code=400, detail=INVALID_TICKET_STATUS);
    return row.id;


def resolve_priority_id(label: str, db: Session) -> int:
    priority_id = PRIORITY_LABEL_TO_ID.get(label);
    if priority_id is not None:
        return priority_id;
    row = db.query(TicketPriority).filter(TicketPriority.label == label).first();
    if row is None:
        raise HTTPException(status_code=400, detail=INVALID_TICKET_PRIORITY);
    return row.id;
