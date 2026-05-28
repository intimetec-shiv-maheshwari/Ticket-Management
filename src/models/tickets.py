import secrets;

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text;
from sqlalchemy.orm import relationship;

from src.utils.db import Base;
from src.utils.helpers import utc_now;


def generate_ticket_id() -> str:
    return secrets.token_hex(8);


class Ticket(Base):
    __tablename__ = "Ticket";
    id = Column(String(16), primary_key=True, default=generate_ticket_id);
    user_id = Column(String(16), ForeignKey("User.id"), nullable=False, index=True);
    subject = Column(String, nullable=False, index=True);
    description = Column(Text, nullable=False);
    organization_id = Column(
        String(16),
        ForeignKey("Organization.id"),
        nullable=False,
        index=True,
    );
    status_id = Column(
        Integer,
        ForeignKey("TicketStatus.id"),
        nullable=False,
        default=1,
        index=True,
    );
    priority_id = Column(
        Integer,
        ForeignKey("TicketPriority.id"),
        nullable=False,
        default=2,
        index=True,
    );
    assigned_to_id = Column(String(16), ForeignKey("User.id"), nullable=True, index=True);
    category = Column(String, nullable=False, index=True);
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False);
    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    );

    status_ref = relationship("TicketStatus", back_populates="tickets");
    priority_ref = relationship("TicketPriority", back_populates="tickets");
    creator = relationship("Users", foreign_keys=[user_id], backref="created_tickets");
    assignee = relationship("Users", foreign_keys=[assigned_to_id], backref="assigned_tickets");
    organization = relationship("Organization", backref="tickets");

    @property
    def status(self) -> str:
        return self.status_ref.label;

    @property
    def priority(self) -> str:
        return self.priority_ref.label;
