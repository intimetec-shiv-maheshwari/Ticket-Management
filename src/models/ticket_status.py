from sqlalchemy import Column, Integer, String;
from sqlalchemy.orm import relationship;

from src.utils.db import Base;


class TicketStatus(Base):
    __tablename__ = "TicketStatus";
    id = Column(Integer, primary_key=True, autoincrement=False);
    label = Column(String, unique=True, nullable=False, index=True);

    tickets = relationship("Ticket", back_populates="status_ref");
